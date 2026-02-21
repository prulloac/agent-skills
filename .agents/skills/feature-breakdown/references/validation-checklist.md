# Feature Breakdown Validation Checklist Template

Use this template to validate that the generated implementation plan meets quality standards.

## Plan Quality Checklist

### Structure & Completeness
- [ ] All 8 major sections included (Executive Summary, Architecture, Tasks, Acceptance Criteria Reference, Validation Plan, Completion Criteria, Risk & Mitigation, Next Steps)
- [ ] Every functional requirement from spec mapped to one or more tasks
- [ ] Every task has clear acceptance criteria
- [ ] Every task has estimated effort (Small/Medium/Large)
- [ ] Dependencies clearly documented for all tasks

### Task Quality
- [ ] Each task has specific, actionable description (not vague)
- [ ] Each task assigned to a component
- [ ] Each task has 2-5 acceptance criteria
- [ ] Acceptance criteria are testable (not "works well" or "is optimized")
- [ ] No task is larger than 3 days work
- [ ] No task has circular dependencies
- [ ] Parallel work opportunities identified
- [ ] Critical path identified

### Acceptance Criteria
- [ ] Each criterion is objectively verifiable
- [ ] Each criterion focuses on behavior, not implementation
- [ ] Each criterion can be tested independently
- [ ] No implementation details in criteria (no "use React", "write SQL", etc.)
- [ ] Success metrics included where applicable

### Validation Coverage
- [ ] Requirement-to-task traceability complete
- [ ] Validation method specified for each requirement
- [ ] Testing strategy includes unit, integration, E2E, and security tests
- [ ] Validation checklist references actual task numbers

### Completion Criteria
- [ ] All items specific and measurable
- [ ] Clear pass/fail conditions for each item
- [ ] Covers implementation, testing, documentation, deployment
- [ ] Sign-off requirements clear

### Risk Management
- [ ] Potential technical risks identified
- [ ] Security risks addressed
- [ ] Mitigation strategies documented
- [ ] Fallback plans for critical items

### Traceability & Coverage
- [ ] Can trace from spec requirement → task → acceptance criteria → test
- [ ] No spec requirements missed
- [ ] No orphan tasks (every task supports a spec requirement)
- [ ] No ambiguous mappings

### Feasibility
- [ ] All tasks are technically feasible with existing tech stack
- [ ] All external dependencies identified
- [ ] No dependency chains longer than 4 tasks (else refactor)
- [ ] Estimated effort realistic for team skill level

---

## Usage

1. **After generating plan**: Complete this checklist
2. **Flag incomplete items**: Note specific issues with line numbers/sections
3. **Share with team**: Get team review of critical sections
4. **Update plan**: Revise any sections that don't pass validation
5. **Recheck**: Verify fixes before starting implementation

---

## Common Issues to Check For

### Red Flags

❌ Tasks that say "TBD" or "TK" - needs definition
❌ Acceptance criteria like "must be fast" or "should work well"
❌ 20+ page documents - likely over-detailed
❌ 50+ tasks - likely needs consolidation
❌ No testing tasks - where's validation?
❌ Circular dependencies - design issue
❌ Tasks estimated >3 days - should split
❌ No security task - required!

### Quality Indicators

✅ 10-40 tasks total (typical feature size)
✅ Each task 1-3 days work
✅ Clear dependency flow
✅ Testing + documentation included
✅ Risk assessment present
✅ All spec requirements covered
✅ Team can explain plan in 5 minutes

---

## Review Sign-Off

- [ ] Product Manager: Validates against requirements
- [ ] Tech Lead: Validates architecture and feasibility
- [ ] QA Lead: Validates testing approach
- [ ] Team: Understands and agrees with plan

**Date Validated**: _____________

**Reviewer Name**: _____________________________

**Approved By**: ________________________________
