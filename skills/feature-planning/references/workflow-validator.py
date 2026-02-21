#!/usr/bin/env python3
"""
Workflow Validation: Test format contracts between skills.

This script validates that the complete workflow (breakdown → planning → execution)
maintains proper format contracts and produces valid outputs.

Run this after creating documents in each skill.
"""

import os
import re
import sys
from pathlib import Path


class WorkflowValidator:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.feature_dir = Path(f"docs/features/{feature_name}")
        self.errors = []
        self.warnings = []
        self.successes = []

    def validate_breakdown(self):
        """Validate feature breakdown document format."""
        print("\n" + "="*60)
        print("PHASE 1: Validating Feature Breakdown")
        print("="*60)
        
        breakdown_file = self.feature_dir / "breakdown.md"
        
        if not breakdown_file.exists():
            self.errors.append(f"❌ Breakdown file not found: {breakdown_file}")
            return False
        
        with open(breakdown_file) as f:
            content = f.read()
        
        # Check required sections
        required_sections = [
            "# Feature Breakdown:",
            "## Feature Overview",
            "## Tasks",
            "## Task Dependencies",
            "## Implementation Approach",
            "## Testing Strategy",
        ]
        
        for section in required_sections:
            if section not in content:
                self.warnings.append(f"⚠️  Missing section: {section}")
        
        # Count tasks
        task_pattern = r"### Task \d+:"
        tasks = re.findall(task_pattern, content)
        
        if len(tasks) < 3:
            self.warnings.append(f"⚠️  Breakdown has only {len(tasks)} tasks (expect 3+)")
        else:
            self.successes.append(f"✅ Breakdown has {len(tasks)} tasks")
        
        # Check each task has acceptance criteria
        task_sections = re.split(r"### Task \d+:", content)[1:]
        for i, task in enumerate(task_sections, 1):
            if "**Acceptance Criteria**" not in task and "**Acceptance criteria**" not in task.lower():
                self.errors.append(f"❌ Task {i} missing acceptance criteria")
            
            if "**Dependencies**" not in task and not ("None" in task or "no dependencies" in task.lower()):
                self.warnings.append(f"⚠️  Task {i} dependencies unclear")
        
        print(f"✅ Breakdown file found: {breakdown_file}")
        print(f"✅ Found {len(tasks)} tasks in breakdown")
        return True

    def validate_execution_sequence(self):
        """Validate execution sequence document format."""
        print("\n" + "="*60)
        print("PHASE 2: Validating Execution Sequence")
        print("="*60)
        
        sequence_file = self.feature_dir / "implementation-sequence.md"
        
        if not sequence_file.exists():
            self.errors.append(f"❌ Sequence file not found: {sequence_file}")
            print(f"❌ CRITICAL: Run feature-planning skill to generate {sequence_file}")
            return False
        
        with open(sequence_file) as f:
            content = f.read()
        
        # Check that sequence has batches
        batch_pattern = r"## Batch \d+:"
        batches = re.findall(batch_pattern, content)
        
        if len(batches) == 0:
            self.errors.append(f"❌ Execution sequence has no batches")
            return False
        
        self.successes.append(f"✅ Execution sequence has {len(batches)} batches")
        
        # Check each batch has tasks with dependencies
        batch_sections = re.split(r"## Batch \d+:", content)[1:]
        
        task_count = 0
        for batch_num, batch in enumerate(batch_sections, 1):
            batch_tasks = re.findall(r"### Task \d+:", batch)
            task_count += len(batch_tasks)
            
            if len(batch_tasks) == 0:
                self.errors.append(f"❌ Batch {batch_num} has no tasks")
            
            # Check dependencies marked
            for task in batch_tasks:
                if "Depends On:" not in batch and "Parallel With:" not in batch:
                    self.warnings.append(f"⚠️  Batch {batch_num} task dependencies not marked")
        
        if task_count < 3:
            self.warnings.append(f"⚠️  Sequence has only {task_count} tasks (expect 3+)")
        else:
            self.successes.append(f"✅ Sequence has {task_count} tasks organized in {len(batches)} batches")
        
        # Check for dependency graph
        if "Dependency Graph" in content or "dependency" in content.lower():
            self.successes.append(f"✅ Sequence includes dependency information")
        else:
            self.warnings.append(f"⚠️  Sequence should include dependency graph/analysis")
        
        # Check for parallelization notes
        if "Parallel" in content or "parallel" in content.lower():
            self.successes.append(f"✅ Sequence identifies parallelization opportunities")
        else:
            self.warnings.append(f"⚠️  Sequence should note which tasks can run in parallel")
        
        print(f"✅ Sequence file found: {sequence_file}")
        return True

    def validate_execution_progress(self):
        """Validate execution progress document."""
        print("\n" + "="*60)
        print("PHASE 3: Validating Execution Progress")
        print("="*60)
        
        progress_file = self.feature_dir / "implementation-progress.md"
        
        if not progress_file.exists():
            self.warnings.append(f"⚠️  Progress file not found: {progress_file} (created during execution)")
            print(f"ℹ️  Progress file created during first agent session")
            return True
        
        with open(progress_file) as f:
            content = f.read()
        
        # Check required sections
        required_patterns = [
            (r"Overall Progress", "Overall Progress % indicator"),
            (r"✅", "Completion status markers"),
            (r"Completed Batches", "Completed batches section"),
            (r"Current Batch|In Progress", "Current batch tracking"),
        ]
        
        for pattern, description in required_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.successes.append(f"✅ Has {description}")
            else:
                self.warnings.append(f"⚠️  Missing {description}")
        
        print(f"✅ Progress file found: {progress_file}")
        return True

    def validate_blockers(self):
        """Validate blockers log file."""
        print("\n" + "="*60)
        print("CHECKING: Blockers Log")
        print("="*60)
        
        blockers_file = self.feature_dir / "blockers.md"
        
        if not blockers_file.exists():
            self.warnings.append(f"⚠️  Blockers file not found: {blockers_file} (created when blockers occur)")
            print(f"ℹ️  Blockers file created when issues arise during execution")
            return True
        
        with open(blockers_file) as f:
            content = f.read()
        
        # Check for blocker tracking structure
        if "Blocker" in content or "blocker" in content.lower():
            self.successes.append(f"✅ Blockers file has blocker entries")
            
            # Check for blocker classifications
            blocker_types = ["Technical", "Integration", "Design", "External"]
            found_types = [t for t in blocker_types if t in content]
            if found_types:
                self.successes.append(f"✅ Blockers classified: {', '.join(found_types)}")
        
        print(f"✅ Blockers file found: {blockers_file}")
        return True

    def validate_format_contracts(self):
        """Validate that format contracts between skills are maintained."""
        print("\n" + "="*60)
        print("PHASE 4: Validating Format Contracts")
        print("="*60)
        
        # Check breakdown → planning contract
        breakdown_file = self.feature_dir / "breakdown.md"
        sequence_file = self.feature_dir / "implementation-sequence.md"
        
        if breakdown_file.exists() and sequence_file.exists():
            with open(breakdown_file) as f:
                breakdown = f.read()
            with open(sequence_file) as f:
                sequence = f.read()
            
            # Count tasks match (approximately)
            breakdown_tasks = len(re.findall(r"### Task \d+:", breakdown))
            sequence_tasks = len(re.findall(r"### Task \d+:", sequence))
            
            if breakdown_tasks == sequence_tasks:
                self.successes.append(f"✅ Task count matches: Breakdown ({breakdown_tasks}) → Sequence ({sequence_tasks})")
            elif abs(breakdown_tasks - sequence_tasks) <= 2:
                self.warnings.append(f"⚠️  Task count differs: Breakdown ({breakdown_tasks}) vs Sequence ({sequence_tasks})")
            else:
                self.errors.append(f"❌ Task count mismatch: Breakdown ({breakdown_tasks}) vs Sequence ({sequence_tasks})")
            
            # Check acceptance criteria transferred
            if "Acceptance Criteria" in breakdown and "Acceptance Criteria" in sequence:
                self.successes.append(f"✅ Acceptance criteria transferred from breakdown to sequence")
            else:
                self.warnings.append(f"⚠️  Check that acceptance criteria transferred properly")
        
        print(f"✅ Format contracts validated")
        return True

    def validate_workflow(self):
        """Run complete workflow validation."""
        print(f"\n🔍 Validating complete workflow for feature: {self.feature_name}")
        
        # Phase 1: Breakdown
        if not self.validate_breakdown():
            print("\n❌ WORKFLOW BLOCKED: Breakdown document invalid")
            return False
        
        # Phase 2: Execution Sequence
        if not self.validate_execution_sequence():
            print("\n❌ WORKFLOW BLOCKED: Execution sequence invalid")
            return False
        
        # Phase 3: Execution Progress
        self.validate_execution_progress()
        
        # Phase 4: Blockers
        self.validate_blockers()
        
        # Phase 5: Format Contracts
        self.validate_format_contracts()
        
        return True

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        if self.successes:
            print(f"\n✅ Successes ({len(self.successes)}):")
            for success in self.successes:
                print(f"   {success}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
        
        print("\n" + "="*60)
        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} error(s)")
            print("\nNext steps:")
            print("1. Fix errors above")
            print("2. Run skill that produced invalid document")
            print("3. Re-run validation")
            return False
        elif self.warnings:
            print(f"⚠️  VALIDATION PASSED (with {len(self.warnings)} warning(s))")
            print("\nNext steps:")
            print("1. Review warnings above")
            print("2. Improve documents if needed")
            print("3. Proceed with execution or re-run skills")
            return True
        else:
            print(f"✅ VALIDATION PASSED: All checks successful!")
            print("\nNext steps:")
            print("1. ✅ Breakdown document is valid")
            print("2. ✅ Execution sequence is valid")
            print("3. ✅ Format contracts maintained")
            print("4. Ready for agent execution!")
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 workflow-validator.py <feature-name>")
        print("\nExample: python3 workflow-validator.py user-authentication")
        print("\nThis script validates the complete workflow:")
        print("  1. Feature breakdown is properly formatted")
        print("  2. Execution sequence is derived from breakdown")
        print("  3. Tasks and dependencies are consistent")
        print("  4. Format contracts between skills are maintained")
        sys.exit(1)
    
    feature_name = sys.argv[1]
    
    # Ensure docs directory exists
    docs_dir = Path("docs/features")
    if not docs_dir.exists():
        print(f"Error: {docs_dir} directory not found")
        print("Please run this from the project root")
        sys.exit(1)
    
    validator = WorkflowValidator(feature_name)
    success = validator.validate_workflow()
    validator.print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
