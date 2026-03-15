#!/usr/bin/env python3
"""
Unified Skill Validator

Comprehensive validator that runs multiple checks on a skill:
1. Structure validation (quick_validate.py patterns)
2. Security validation (security_audit.py patterns)
3. Eval loop validation (run_skill_evals.py patterns)

Aggregates results into a single comprehensive report.

Usage:
    python validator.py /path/to/skill [--output report.json] [--verbose]
"""

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ValidationType(Enum):
    """Types of validation checks."""

    STRUCTURE = "structure"
    SECURITY = "security"
    EVALS = "evals"


@dataclass
class ValidationCheck:
    """Result of a single validation check."""

    type: str
    name: str
    passed: bool
    details: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class SkillValidator:
    """Unified skill validator orchestrator."""

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.checks: List[ValidationCheck] = []
        self.script_dir = Path(__file__).parent

    def validate_all(
        self, run_evals: bool = True, verbose: bool = False
    ) -> Dict[str, Any]:
        """Run all validation checks."""
        skill_name = self._get_skill_name()

        print(f"🔍 Validating skill: {skill_name}")
        print(f"📁 Path: {self.skill_path}\n")

        # Run structure validation
        print("1️⃣  Running structure validation...")
        structure_result = self._validate_structure()
        self.checks.append(structure_result)
        self._print_check_summary(structure_result)

        # Run security validation
        print("\n2️⃣  Running security validation...")
        security_result = self._validate_security(verbose)
        self.checks.append(security_result)
        self._print_check_summary(security_result)

        # Run eval validation (optional)
        evals_result = None
        if run_evals:
            print("\n3️⃣  Running eval validation...")
            evals_result = self._validate_evals(verbose)
            if evals_result:
                self.checks.append(evals_result)
                self._print_check_summary(evals_result)
            else:
                print("⏭️  Skipping eval validation (no evals file found)")

        # Aggregate results
        return self._aggregate_results(skill_name, evals_result is not None)

    def _get_skill_name(self) -> str:
        """Extract skill name from SKILL.md."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return "unknown"

        content = skill_md.read_text()
        lines = content.split("\n")

        for line in lines:
            if line.startswith("name:"):
                return line[len("name:") :].strip().strip('"').strip("'")

        return "unknown"

    def _validate_structure(self) -> ValidationCheck:
        """Run structure validation using quick_validate.py."""
        quick_validate = self.script_dir / "quick_validate.py"

        if not quick_validate.exists():
            return ValidationCheck(
                type=ValidationType.STRUCTURE.value,
                name="Structure Validation",
                passed=False,
                details={},
                errors=["quick_validate.py not found"],
                warnings=[],
            )

        try:
            result = subprocess.run(
                [sys.executable, str(quick_validate), str(self.skill_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # quick_validate prints "Skill is valid!" on success
            passed = result.returncode == 0 and "valid" in result.stdout.lower()

            return ValidationCheck(
                type=ValidationType.STRUCTURE.value,
                name="Structure Validation",
                passed=passed,
                details={
                    "output": result.stdout.strip(),
                    "skill_path": str(self.skill_path),
                },
                errors=[]
                if passed
                else [result.stderr or result.stdout or "Validation failed"],
                warnings=[],
            )

        except subprocess.TimeoutExpired:
            return ValidationCheck(
                type=ValidationType.STRUCTURE.value,
                name="Structure Validation",
                passed=False,
                details={},
                errors=["Structure validation timed out"],
                warnings=[],
            )
        except Exception as e:
            return ValidationCheck(
                type=ValidationType.STRUCTURE.value,
                name="Structure Validation",
                passed=False,
                details={},
                errors=[str(e)],
                warnings=[],
            )

    def _validate_security(self, verbose: bool = False) -> ValidationCheck:
        """Run security validation using run_security_checks.py."""
        security_checks = self.script_dir / "run_security_checks.py"

        if not security_checks.exists():
            return ValidationCheck(
                type=ValidationType.SECURITY.value,
                name="Security Validation",
                passed=False,
                details={},
                errors=["run_security_checks.py not found"],
                warnings=[],
            )

        try:
            cmd = [sys.executable, str(security_checks), str(self.skill_path)]
            if verbose:
                cmd.append("--verbose")
            cmd.extend(["--output", "/tmp/security_result.json"])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            try:
                with open("/tmp/security_result.json", "r") as f:
                    data = json.load(f)

                passed = data.get("passed", False)

                return ValidationCheck(
                    type=ValidationType.SECURITY.value,
                    name="Security Validation",
                    passed=passed,
                    details=data,
                    errors=[]
                    if passed
                    else [
                        f"Found {data.get('summary', {}).get('critical', 0)} critical issues"
                    ],
                    warnings=[],
                )
            except (FileNotFoundError, json.JSONDecodeError):
                return ValidationCheck(
                    type=ValidationType.SECURITY.value,
                    name="Security Validation",
                    passed=False,
                    details={},
                    errors=["Failed to parse security results"],
                    warnings=[],
                )

        except subprocess.TimeoutExpired:
            return ValidationCheck(
                type=ValidationType.SECURITY.value,
                name="Security Validation",
                passed=False,
                details={},
                errors=["Security validation timed out"],
                warnings=[],
            )
        except Exception as e:
            return ValidationCheck(
                type=ValidationType.SECURITY.value,
                name="Security Validation",
                passed=False,
                details={},
                errors=[str(e)],
                warnings=[],
            )

    def _validate_evals(self, verbose: bool = False) -> Optional[ValidationCheck]:
        """Run eval validation using run_skill_evals.py."""
        evals_runner = self.script_dir / "run_skill_evals.py"

        if not evals_runner.exists():
            return None

        # Check if evals file exists
        evals_file = self.skill_path / "evals" / "evals.json"
        if not evals_file.exists():
            return None

        try:
            cmd = [sys.executable, str(evals_runner), str(self.skill_path)]
            cmd.extend(["--output", "/tmp/evals_result.json"])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            try:
                with open("/tmp/evals_result.json", "r") as f:
                    data = json.load(f)

                passed = data.get("passed", False)
                trigger_rate = data.get("trigger_rate", 0)

                return ValidationCheck(
                    type=ValidationType.EVALS.value,
                    name="Eval Validation",
                    passed=passed,
                    details=data,
                    errors=[]
                    if passed
                    else [f"Trigger rate {trigger_rate} below threshold"],
                    warnings=[],
                )
            except (FileNotFoundError, json.JSONDecodeError):
                return None

        except subprocess.TimeoutExpired:
            return ValidationCheck(
                type=ValidationType.EVALS.value,
                name="Eval Validation",
                passed=False,
                details={},
                errors=["Eval validation timed out"],
                warnings=[],
            )
        except Exception:
            return None

    def _print_check_summary(self, check: ValidationCheck) -> None:
        """Print summary of a validation check."""
        status = "✅" if check.passed else "❌"
        print(f"{status} {check.name}: {'PASSED' if check.passed else 'FAILED'}")

        if check.errors:
            for error in check.errors:
                print(f"   ❌ {error}")

        if check.warnings:
            for warning in check.warnings:
                print(f"   ⚠️  {warning}")

    def _aggregate_results(
        self, skill_name: str, include_evals: bool
    ) -> Dict[str, Any]:
        """Aggregate all validation results."""
        overall_passed = all(check.passed for check in self.checks)

        summary = {
            "skill_name": skill_name,
            "skill_path": str(self.skill_path),
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "overall_passed": overall_passed,
            "checks_run": len(self.checks),
            "checks_passed": sum(1 for c in self.checks if c.passed),
            "checks_failed": sum(1 for c in self.checks if not c.passed),
            "validation_types": {
                "structure": any(
                    c.type == ValidationType.STRUCTURE.value for c in self.checks
                ),
                "security": any(
                    c.type == ValidationType.SECURITY.value for c in self.checks
                ),
                "evals": any(c.type == ValidationType.EVALS.value for c in self.checks),
            },
        }

        # Organize checks by type
        checks_by_type = {}
        for check in self.checks:
            if check.type not in checks_by_type:
                checks_by_type[check.type] = []

            check_dict = {
                "name": check.name,
                "passed": check.passed,
                "details": check.details,
                "errors": check.errors,
                "warnings": check.warnings,
            }
            checks_by_type[check.type].append(check_dict)

        return {
            "summary": summary,
            "checks": checks_by_type,
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Comprehensive skill validator")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSON file for detailed results",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print detailed validation information"
    )
    parser.add_argument(
        "--skip-evals", action="store_true", help="Skip eval validation"
    )

    args = parser.parse_args()
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"❌ Skill path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = SkillValidator(skill_path)
    results = validator.validate_all(
        run_evals=not args.skip_evals, verbose=args.verbose
    )

    # Print summary
    summary = results["summary"]
    print(f"\n{'='*70}")
    print(f"Validation Summary")
    print(f"{'='*70}")
    print(f"Skill: {summary['skill_name']}")
    print(f"Status: {'✅ ALL PASSED' if summary['overall_passed'] else '❌ SOME FAILED'}")
    print(f"Checks: {summary['checks_passed']}/{summary['checks_run']} passed")
    print(f"{'='*70}\n")

    # Save detailed results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"💾 Detailed results saved to {args.output}\n")

    sys.exit(0 if summary["overall_passed"] else 1)


if __name__ == "__main__":
    main()
