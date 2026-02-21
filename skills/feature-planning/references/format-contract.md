# Format Contract: Feature Breakdown → Feature Planning

This document defines the interface contract between the `feature-breakdown` and `feature-planning` skills. It ensures safe, predictable handoff of data from breakdown to planning.

## Purpose

The format contract ensures that:
1. `feature-breakdown` produces output that `feature-planning` can reliably consume
2. `feature-planning` knows exactly what to expect and how to parse it
3. If either skill changes format, both must be updated in lockstep
4. Tools can validate format compliance before planning starts

---

## Input Format: Breakdown Document Structure

**File Location**: `docs/features/[feature-name]-breakdown.md`

**Format**: Markdown document with exactly 8 sections (in order):

### 1. Executive Summary
```markdown
## Executive Summary

Feature name and clear overview of what's being built.
Success criteria and expected impact.
```
**Required fields**:
- Feature name
- Clear objective statement
- 2-5 success criteria
- Expected impact/benefits

### 2. Component Architecture
```markdown
## Component Architecture

[Optional ASCII diagram]

### Components

- **Component Name**: Description, responsibilities, scope
- **Component Name**: Description, responsibilities, scope
```
**Required fields**:
- At least 1 component definition
- Each component has: name, description, responsibilities
- Integration points between components documented
- External dependencies listed (if any)

### 3. Implementation Tasks
```markdown
## Implementation Tasks

### Task 1: [Clear title]
- **Component**: [Which component(s)]
- **Description**: [What needs to be done]
- **Dependencies**: [Task 1, Task 3] or "None"
- **Effort**: Small/Medium/Large
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Criterion 3
```
**Required fields per task**:
- Task ID (sequential)
- Clear, action-oriented title
- Component mapping (which component(s) this affects)
- Description of work
- Dependencies list (task IDs or "None")
- Effort estimate (Small/Medium/Large only)
- 2-5 acceptance criteria (checklist format)

**Validation rules**:
- Minimum 5 tasks, maximum 50 tasks
- All tasks must have acceptance criteria
- All task dependencies must reference other tasks or be "None"
- No circular dependencies allowed
- Effort must be one of: Small, Medium, Large

### 4. Acceptance Criteria Reference
```markdown
## Acceptance Criteria Reference

| Task | Acceptance Criteria |
|------|-------------------|
| Task 1 | AC1, AC2, AC3 |
| Task 2 | AC1, AC2 |
```
**Required fields**:
- Reference table mapping each task to its acceptance criteria
- One row per task
- Criteria listed as comma-separated items

### 5. Validation Plan
```markdown
## Validation Plan

### Specification Requirements Coverage

| Requirement | Validated By | Method |
|-------------|-------------|--------|
| Requirement 1 | Task 1, Task 2 | Unit tests, manual testing |
```
**Required fields**:
- Coverage matrix showing which tasks validate which requirements
- Validation method documented for each requirement
- Testing strategy section (unit, integration, E2E, security)

### 6. Completion Criteria
```markdown
## Completion Criteria

### Implementation Complete
- [ ] All tasks complete
- [ ] Code merged to main

### Quality Assurance
- [ ] All unit tests passing
- [ ] Code review approved

### Documentation
- [ ] API documentation updated
- [ ] Architecture documented
```
**Required fields**:
- Comprehensive checklist with 15-30 items
- Organized into logical categories (Implementation, QA, Documentation, etc.)
- All items are verifiable/testable

### 7. Risk & Mitigation
```markdown
## Risk & Mitigation

### High Priority Risks

| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|-----------|-------|
| Risk 1 | High | Medium | Strategy 1 | Person |
```
**Required fields**:
- At least 1 risk identified
- Maximum 10 risks per breakdown
- Each risk has: description, impact level (High/Medium/Low), probability, mitigation strategy
- Owner assigned for tracking

**Risk format**:
```
- **[Risk Title]**: [Description]
  - Impact: High/Medium/Low
  - Probability: High/Medium/Low
  - Mitigation: [Strategy]
  - Owner: [Name/Role]
```

### 8. Next Steps
```markdown
## Next Steps

1. Use feature-planning skill to create timeline and resource plan
2. Follow the sequenced task list during implementation
3. Update progress in tracking system
```
**Required fields**:
- Instructions for next phase (planning)
- How to use breakdown during implementation
- How to report issues or changes

---

## Validation Checklist for Planning Skill

Before proceeding with feature-planning, verify:

- [ ] File exists at `docs/features/[feature-name]-breakdown.md`
- [ ] All 8 sections present in correct order
- [ ] Section 1 (Executive Summary): Has feature name and success criteria
- [ ] Section 2 (Architecture): At least 1 component defined
- [ ] Section 3 (Tasks): 5-50 tasks with all required fields
- [ ] Section 4 (Acceptance Criteria): Reference table maps all tasks
- [ ] Section 5 (Validation): Coverage matrix present
- [ ] Section 6 (Completion): 15-30 checklist items
- [ ] Section 7 (Risks): 1-10 risks with proper format
- [ ] Section 8 (Next Steps): Instructions present
- [ ] No circular dependencies in task list
- [ ] All task dependencies reference valid task IDs
- [ ] All effort estimates are Small/Medium/Large
- [ ] All risks have Impact and Probability (High/Medium/Low)

### Validation Script

```python
def validate_breakdown_format(file_path):
    """Validate that breakdown.md meets format contract"""
    
    required_sections = [
        "Executive Summary",
        "Component Architecture",
        "Implementation Tasks",
        "Acceptance Criteria Reference",
        "Validation Plan",
        "Completion Criteria",
        "Risk & Mitigation",
        "Next Steps"
    ]
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check all sections present
    for section in required_sections:
        if f"## {section}" not in content:
            raise ValueError(f"Missing required section: {section}")
    
    # Check section order
    section_positions = {
        section: content.find(f"## {section}") 
        for section in required_sections
    }
    
    for i in range(len(required_sections) - 1):
        current = section_positions[required_sections[i]]
        next_section = section_positions[required_sections[i + 1]]
        if current >= next_section:
            raise ValueError(f"Section {required_sections[i]} appears after {required_sections[i+1]}")
    
    # Parse and validate tasks
    import re
    task_pattern = r"### Task \d+:"
    tasks = re.findall(task_pattern, content)
    if len(tasks) < 5 or len(tasks) > 50:
        raise ValueError(f"Expected 5-50 tasks, found {len(tasks)}")
    
    print("✅ Breakdown format validated successfully")
    return True
```

---

## Breaking Changes Policy

If either skill needs to change the format:

1. **feature-breakdown changes output**: Update this contract first, then update feature-planning
2. **feature-planning needs different input**: Update this contract first, then feature-breakdown
3. **Major version change**: Update version number in both skills
4. **Minor addition**: Document new optional fields clearly

### Version History

| Date | Change | Breaking | Skills Updated |
|------|--------|----------|-----------------|
| 2026-02-19 | Initial contract definition | No | Both |

---

## Examples

See `example-format-contract-valid.md` for a complete valid breakdown document that meets all contract requirements.

See `example-format-contract-invalid.md` for examples of invalid formats and what makes them non-compliant.

---

## For Skill Developers

**When updating feature-breakdown**:
1. Check this contract before changing output format
2. If output needs to change, update contract FIRST
3. Add version number update to SKILL.md frontmatter
4. Notify feature-planning maintainer of breaking changes

**When updating feature-planning**:
1. Check this contract for input requirements
2. If input expectations change, update contract FIRST
3. Add validation check to skill startup to catch format violations
4. Notify feature-breakdown maintainer of new input requirements

---

## Questions & Clarifications

**Q: What if my breakdown doesn't have 8 sections?**
A: feature-planning cannot proceed. Load feature-breakdown skill and regenerate breakdown until all 8 sections exist.

**Q: Can I skip sections?**
A: No. All 8 sections are required. They may be brief, but must exist.

**Q: What if I have more than 50 tasks?**
A: Consider breaking the feature into smaller features. 50+ tasks should be multiple smaller breakdown documents.

**Q: Can tasks have fewer than 2 acceptance criteria?**
A: No. Each task must have 2-5 acceptance criteria to be testable. If you can't write 2 criteria, the task may be too vague.
