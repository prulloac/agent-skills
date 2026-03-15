#!/usr/bin/env python3
"""
Security Checks Runner

Run security validation on a skill using the SecurityAuditor.
Detects prompt injection risks, unsafe operations, and other security issues.

Usage:
    python run_security_checks.py /path/to/skill [--output results.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from security_audit import SecurityAuditor, Severity


def parse_skill_md(skill_path: Path) -> tuple[str, str]:
    """Parse SKILL.md and return (name, content)."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Extract name from frontmatter
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
    for line in lines[1:end_idx]:
        if line.startswith("name:"):
            name = line[len("name:") :].strip().strip('"').strip("'")
            break

    return name, content


def collect_skill_scripts(skill_path: Path) -> List[tuple[str, str]]:
    """Collect all Python scripts in the skill for security analysis."""
    scripts = []
    scripts_dir = skill_path / "scripts"

    if scripts_dir.exists():
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                scripts.append((py_file.name, content))
            except Exception as e:
                print(f"⚠️  Failed to read script {py_file.name}: {e}", file=sys.stderr)

    return scripts


def audit_skill(skill_path: Path, auditor: SecurityAuditor) -> Dict[str, Any]:
    """Run security audit on skill and collect results."""
    name, skill_md_content = parse_skill_md(skill_path)

    # Audit SKILL.md
    md_result = auditor.audit(skill_md_content, str(skill_path / "SKILL.md"))

    # Audit all scripts
    script_results = {}
    scripts = collect_skill_scripts(skill_path)

    for script_name, script_content in scripts:
        script_result = auditor.audit(
            script_content, str(skill_path / "scripts" / script_name)
        )
        script_results[script_name] = script_result

    return {
        "skill_name": name,
        "skill_path": str(skill_path),
        "md_audit": md_result,
        "script_audits": script_results,
        "scripts": [name for name, _ in scripts],
    }


def format_security_issue(issue) -> Dict[str, Any]:
    """Convert SecurityIssue to dict for JSON serialization."""
    return {
        "rule": issue.rule,
        "severity": issue.severity.name,
        "severity_emoji": issue.severity.value,
        "title": issue.title,
        "description": issue.description,
        "location": issue.location,
        "line_number": issue.line_number,
        "remediation": issue.remediation,
        "example": issue.example,
    }


def format_audit_result(result) -> Dict[str, Any]:
    """Convert SecurityAuditResult to dict for JSON serialization."""
    return {
        "skill_path": result.skill_path,
        "passed": result.passed,
        "critical_count": result.critical_count(),
        "high_count": result.high_count(),
        "medium_count": result.medium_count(),
        "total_issues": len(result.issues),
        "issues": [format_security_issue(issue) for issue in result.issues],
    }


def aggregate_results(audit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate security results from SKILL.md and scripts."""
    md_passed = audit_data["md_audit"].passed
    scripts_passed = all(
        result.passed for result in audit_data["script_audits"].values()
    )

    all_passed = md_passed and scripts_passed

    # Collect all issues
    all_issues = []
    all_issues.extend(audit_data["md_audit"].issues)
    for script_result in audit_data["script_audits"].values():
        all_issues.extend(script_result.issues)

    # Count by severity
    critical_count = sum(1 for i in all_issues if i.severity == Severity.CRITICAL)
    high_count = sum(1 for i in all_issues if i.severity == Severity.HIGH)
    medium_count = sum(1 for i in all_issues if i.severity == Severity.MEDIUM)
    low_count = sum(1 for i in all_issues if i.severity == Severity.LOW)

    return {
        "skill_name": audit_data["skill_name"],
        "skill_path": audit_data["skill_path"],
        "passed": all_passed,
        "scripts_scanned": len(audit_data["scripts"]),
        "script_names": audit_data["scripts"],
        "md_audit": format_audit_result(audit_data["md_audit"]),
        "script_audits": {
            name: format_audit_result(result)
            for name, result in audit_data["script_audits"].items()
        },
        "summary": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "total": len(all_issues),
        },
    }


def print_results(results: Dict[str, Any], verbose: bool = False) -> None:
    """Print security check results to stdout."""
    summary = results["summary"]
    status = "✅ PASSED" if results["passed"] else "❌ FAILED"

    print(f"\n{'='*70}")
    print(f"Security Audit: {results['skill_name']}")
    print(f"Status: {status}")
    print(f"Scripts Scanned: {results['scripts_scanned']}")
    print(f"{'='*70}")

    print(f"\n📊 Summary:")
    print(f"  🚨 Critical: {summary['critical']}")
    print(f"  ⚠️  High: {summary['high']}")
    print(f"  ℹ️  Medium: {summary['medium']}")
    print(f"  💡 Low: {summary['low']}")
    print(f"  Total: {summary['total']}")

    if not verbose or summary["total"] == 0:
        return

    # Print SKILL.md audit
    md_audit = results["md_audit"]
    if md_audit["total_issues"] > 0:
        print(f"\n📄 SKILL.md Issues ({md_audit['total_issues']}):")
        for issue in md_audit["issues"]:
            print(f"  {issue['severity_emoji']} [{issue['severity']}] {issue['title']}")
            print(f"      {issue['description']}")
            if issue["remediation"]:
                print(f"      ✏️  {issue['remediation']}")

    # Print script audits
    for script_name, script_audit in results["script_audits"].items():
        if script_audit["total_issues"] > 0:
            print(f"\n🐍 {script_name} Issues ({script_audit['total_issues']}):")
            for issue in script_audit["issues"]:
                print(
                    f"  {issue['severity_emoji']} [{issue['severity']}] {issue['title']}"
                )
                print(f"      {issue['description']}")
                if issue["remediation"]:
                    print(f"      ✏️  {issue['remediation']}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run security checks on a skill")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument(
        "--output", type=Path, default=None, help="Output JSON file for results"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print detailed issue information"
    )

    args = parser.parse_args()
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"❌ Skill path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Run security audit
    print(f"🔒 Running security checks on {skill_path.name}...")
    auditor = SecurityAuditor()

    try:
        audit_data = audit_skill(skill_path, auditor)
        results = aggregate_results(audit_data)
    except Exception as e:
        print(f"❌ Failed to run security checks: {e}", file=sys.stderr)
        sys.exit(1)

    # Print results
    print_results(results, verbose=args.verbose)

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
