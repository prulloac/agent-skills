#!/usr/bin/env python3
"""
Skill Eval Loop Runner

Run trigger evaluation evals for a skill using OpenCode CLI.
Tests whether a skill is properly triggered by sample queries.

Usage:
    python run_skill_evals.py /path/to/skill [--eval-set evals.json] [--model provider/model]
"""

import argparse
import json
import shutil
import subprocess
import sys
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Optional


def parse_skill_md(skill_path: Path) -> tuple[str, str]:
    """Parse SKILL.md and return (name, description)."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter opening")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter closing")

    name = ""
    description = ""

    for line in lines[1:end_idx]:
        if line.startswith("name:"):
            name = line[len("name:") :].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:") :].strip()
            if value.startswith(">") or value.startswith("|"):
                # Multi-line description
                continuation = []
                idx = lines.index(line) + 1
                while idx < len(lines):
                    if lines[idx].startswith(("  ", "\t")):
                        continuation.append(lines[idx].strip())
                        idx += 1
                    else:
                        break
                description = " ".join(continuation)
            else:
                description = value.strip('"').strip("'")

    return name, description


def find_project_root() -> Path:
    """Find project root by locating .git, .agents, .opencode, or .claude."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if any(
            (parent / marker).exists()
            for marker in (".git", ".agents", ".opencode", ".claude")
        ):
            return parent
    return current


def extract_json_events(stdout_text: str) -> list[dict]:
    """Parse OpenCode json/ndjson output into events."""
    events = []
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                events.append(obj)
        except json.JSONDecodeError:
            continue
    return events


def was_skill_triggered(events: list[dict], skill_name: str) -> bool:
    """Infer whether skill was triggered by scanning event payloads."""
    needle = skill_name.lower()

    def iter_strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for k, v in value.items():
                if isinstance(k, str):
                    yield k
                yield from iter_strings(v)
        elif isinstance(value, list):
            for item in value:
                yield from iter_strings(item)

    for event in events:
        for text in iter_strings(event):
            if needle in text.lower():
                return True
    return False


def run_single_eval(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: Optional[str] = None,
) -> bool:
    """Run one eval query and return whether skill triggered."""
    root = Path(project_root)
    unique_id = uuid.uuid4().hex[:8]
    temp_skill_name = f"{skill_name}-eval-{unique_id}"[:64]
    temp_skill_dir = root / ".agents" / "skills" / temp_skill_name

    try:
        temp_skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = temp_skill_dir / "SKILL.md"
        skill_md.write_text(
            "\n".join(
                [
                    "---",
                    f"name: {temp_skill_name}",
                    f"description: {skill_description}",
                    "---",
                    "",
                    f"# {temp_skill_name}",
                    "",
                    "Temporary trigger-eval skill.",
                ]
            )
        )

        cmd = ["opencode", "run", "--format", "json"]
        if model:
            cmd.extend(["--model", model])
        cmd.append(query)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=root,
            timeout=timeout,
        )

        if result.returncode != 0:
            return False

        events = extract_json_events(result.stdout)
        if not events:
            return temp_skill_name in result.stdout

        return was_skill_triggered(events, temp_skill_name)

    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"Error running eval: {e}", file=sys.stderr)
        return False
    finally:
        if temp_skill_dir.exists():
            shutil.rmtree(temp_skill_dir, ignore_errors=True)


def load_evals(eval_file: Path) -> list[dict]:
    """Load eval set from JSON file."""
    if not eval_file.exists():
        raise FileNotFoundError(f"Eval file not found: {eval_file}")

    with open(eval_file, "r") as f:
        data = json.load(f)

    # Support both direct list and nested "evals" key
    return data.get("evals", data) if isinstance(data, dict) else data


def run_evals(
    skill_path: Path,
    eval_set: list[dict],
    num_workers: int = 4,
    timeout: int = 30,
    project_root: Optional[Path] = None,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: Optional[str] = None,
) -> dict:
    """Run eval set and return aggregate results."""
    if project_root is None:
        project_root = find_project_root()

    skill_name, description = parse_skill_md(skill_path)

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_query = {}
        for item in eval_set:
            query = item.get("prompt") or item.get("query")
            if not query:
                continue

            for run in range(runs_per_query):
                future = executor.submit(
                    run_single_eval,
                    query,
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_query[future] = (item, run)

        query_results: dict[str, dict] = {}

        for future in as_completed(future_to_query):
            item, run = future_to_query[future]
            query = item.get("prompt") or item.get("query")

            if query not in query_results:
                query_results[query] = {
                    "item": item,
                    "runs": [],
                    "triggered": 0,
                    "total": 0,
                }

            try:
                triggered = future.result()
                query_results[query]["runs"].append(triggered)
                query_results[query]["total"] += 1
                if triggered:
                    query_results[query]["triggered"] += 1
            except Exception as e:
                print(f"Error in eval: {e}", file=sys.stderr)
                query_results[query]["total"] += 1

    # Calculate statistics
    total_queries = len(query_results)
    total_runs = sum(r["total"] for r in query_results.values())
    successful_triggers = sum(r["triggered"] for r in query_results.values())
    trigger_rate = successful_triggers / total_runs if total_runs > 0 else 0

    # Check trigger threshold
    passed = trigger_rate >= trigger_threshold

    return {
        "skill_name": skill_name,
        "skill_description": description,
        "passed": passed,
        "trigger_threshold": trigger_threshold,
        "trigger_rate": round(trigger_rate, 2),
        "successful_triggers": successful_triggers,
        "total_runs": total_runs,
        "total_queries": total_queries,
        "results": [
            {
                "id": r["item"].get("id", "unknown"),
                "name": r["item"].get("name", "Unknown"),
                "query": q,
                "trigger_rate": round(r["triggered"] / r["total"], 2)
                if r["total"] > 0
                else 0,
                "runs": r["total"],
                "triggered": r["triggered"],
            }
            for q, r in query_results.items()
        ],
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation evals for a skill"
    )
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument(
        "--eval-set",
        type=Path,
        default=None,
        help="Path to evals JSON file (default: evals/evals.json in skill)",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout per eval in seconds (default: 30)",
    )
    parser.add_argument(
        "--runs-per-query",
        type=int,
        default=1,
        help="Number of runs per query (default: 1)",
    )
    parser.add_argument(
        "--trigger-threshold",
        type=float,
        default=0.5,
        help="Minimum trigger rate to pass (default: 0.5)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="LLM model to use (e.g., claude-opus/claude-3-5-sonnet)",
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="Output JSON file for results"
    )

    args = parser.parse_args()
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"❌ Skill path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Determine eval file
    eval_file = args.eval_set
    if eval_file is None:
        eval_file = skill_path / "evals" / "evals.json"

    if not eval_file.exists():
        print(f"⚠️  No evals file found at {eval_file}", file=sys.stderr)
        print("Skipping eval loop", file=sys.stderr)
        sys.exit(0)

    # Load evals
    try:
        evals = load_evals(eval_file)
    except Exception as e:
        print(f"❌ Failed to load evals: {e}", file=sys.stderr)
        sys.exit(1)

    # Run evals
    print(f"🧪 Running skill evals from {eval_file}")
    print(f"📊 {len(evals)} eval queries")

    results = run_evals(
        skill_path,
        evals,
        num_workers=args.num_workers,
        timeout=args.timeout,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    # Print summary
    print(f"\n{'='*70}")
    print(f"Skill: {results['skill_name']}")
    print(
        f"Trigger Rate: {results['trigger_rate']*100:.1f}% ({results['successful_triggers']}/{results['total_runs']} runs)"
    )
    print(f"Status: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
    print(f"Threshold: {results['trigger_threshold']*100:.1f}%")
    print(f"{'='*70}\n")

    # Print per-query results
    for r in results["results"]:
        status = "✅" if r["trigger_rate"] >= results["trigger_threshold"] else "❌"
        print(f"{status} {r['name']}")
        print(f"   Query: {r['query'][:60]}...")
        print(
            f"   Trigger Rate: {r['trigger_rate']*100:.1f}% ({r['triggered']}/{r['runs']})"
        )

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
