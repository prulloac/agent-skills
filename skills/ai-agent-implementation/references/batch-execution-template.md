# Batch Execution Template

Use this template to prepare each batch for agent execution.

**File Location**: Save in `docs/features/[feature-name]/` directory with descriptive name.  
**Example**: `docs/features/user-authentication/batch-1-backend.md`

## Before Agent Session

### Batch Context

Copy this template and fill in for the batch you're about to execute:

```markdown
# Batch Execution: [Feature Name] - Batch [N]: [Batch Name]

**Feature**: [Feature name]
**Batch Number**: [N]
**Batch Name**: [Descriptive name]
**Prepared**: [Date/Time]

---

## Batch Overview

**Purpose**: [What does this batch accomplish in the feature?]

**Expected Duration**: [Short estimate, e.g. "one agent session"]

**Dependencies**: 
- All met? ✅ or ⏭️ [Waiting for...]
- Previous batch status: [Complete/In Progress/Ready]

**Integration Points**: [What does this batch need from previous work? What will next batch need from this?]

---

## Tasks in This Batch

### Task [ID]: [Title]

**Description**: [What needs to be built?]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Integration**: [How does this connect with other tasks?]

**Known Complexity**: [Any technical challenges?]

**Reference**: [Link to breakdown doc where this was detailed]

---

### Task [ID]: [Title]

[Repeat for each task in batch]

---

## Agent Instructions

**Your mission for this batch**:
1. Execute the [N] tasks listed above
2. Verify each meets its acceptance criteria
3. Test integration with [previous batch / other components]
4. Document any issues or blockers
5. When done, provide a session summary

**Success looks like**:
- All [N] tasks complete and working
- All acceptance criteria met for each task
- Integration with [previous work] verified
- No critical blockers

**If you encounter blockers**:
- Document them clearly (what's blocking, why, impact)
- Suggest resolution path
- Note in session summary for next agent

**What we'll provide you**:
- Clear task descriptions above
- Acceptance criteria for each task
- Integration requirements
- Any context from previous batches

---

## Integration Checklist

Before marking batch complete:

- [ ] Does Task [ID] output match what Task [ID] expects?
- [ ] Do new components integrate with [previous batch]?
- [ ] Do tests pass for new code?
- [ ] Does [specific integration point] work end-to-end?

---

## Session Notes

[After agent completes: fill in what happened]

**Tasks Completed**: [✅/🔄 for each task]

**Issues Encountered**: [What went wrong or what was unclear?]

**Quality Assessment**: [Any concerns about implementation?]

**Integration Status**: [Does it work with rest of feature?]

**For Next Batch**: [What do they need to know?]
```

---

## How to Use This Template

### Step 1: Prepare Context
1. Select next batch from execution sequence
2. Verify all dependencies are complete
3. Extract all tasks in that batch with full descriptions
4. Copy template above and fill in blanks

### Step 2: Brief Agent
- Provide filled-in context to agent
- Include task descriptions and acceptance criteria
- Call out any integration requirements
- Highlight known complexity or risks

### Step 3: Monitor Execution
- Watch for blockers or issues
- Help agent if stuck (clarify requirements, debug)
- Verify test results as they come in

### Step 4: Verify Completion
- Check each task against acceptance criteria
- Verify integration with previous work
- Update implementation-progress.md
- Document session summary

### Step 5: Prepare Handoff
- What completed successfully
- Any issues discovered
- Integration status
- What next batch needs to know

---

## Batch Sizing Guide

### Good batch size: 1-3 related tasks

**Example Batch (Good)**:
- Task 1: Create database schema for user profiles
- Task 2: Add user profile API endpoints
- Task 3: Test user profile API with mock data

**Why this works**: Related tasks, can complete in one session, clear integration (schema → endpoints → tests).

### Batch too small: 1 task in isolation

**Example Batch (Too Small)**:
- Task 1: Create database schema for user profiles

**Problem**: Each task unnecessarily isolated. Combine with tasks that depend on it.

### Batch too large: 4+ unrelated tasks

**Example Batch (Too Large)**:
- Task 1: Create user profile schema
- Task 2: Build billing payment processor
- Task 3: Add email notification system
- Task 4: Create admin dashboard

**Problem**: Too much context. Agent can't focus. May not complete in one session.

---

## Integration Patterns

### Sequential Integration
Use when tasks must happen in strict order:

```
Task 1 (Build feature) → Task 2 (Add tests) → Task 3 (Integrate)
```

**Batch instructions**: "Do Task 1, then Task 2, then Task 3. Don't move to Task 2 until Task 1 is working."

### Parallel Integration
Use when tasks can happen simultaneously:

```
Task 1 (Frontend)  ┐
                   └→ Task 3 (Integration & E2E tests)
Task 2 (Backend)   ┘
```

**Batch instructions**: "Task 1 and Task 2 can happen in parallel. Don't start Task 3 until both are done and merged."

### Dependency Integration
Use when tasks depend on previous batch output:

```
Previous Batch: Build core feature
       ↓
This Batch: Task 1 (Use core feature to build next layer)
            Task 2 (Test against core feature)
```

**Batch instructions**: "These tasks build on [previous batch]. When you start, [previous batch output] will be available at [location]."

---

## Common Agent Questions

**Q: Can I parallelize Task 1 and Task 2?**  
A: Yes, if they don't depend on each other. But you'll need to integrate them before moving to Task 3.

**Q: What if Task 1 fails?**  
A: Document what failed and why. We may ask you to rework it, or we may adjust the approach. Don't move to Task 2 until Task 1 is solid.

**Q: How do I know if integration is working?**  
A: Check the acceptance criteria. If they all pass and the feature works end-to-end, integration is working.

**Q: What if I need clarification on a task?**  
A: Ask now. It's better to clarify before building than to discover issues later.

**Q: How long should this batch take?**  
A: If it takes much longer than expected, document blockers and we can pause, regroup, and adjust.

---

## Template Checklist

Before handing batch to agent, verify:

- [ ] All task descriptions filled in
- [ ] Acceptance criteria defined for each task
- [ ] Integration points documented
- [ ] Dependencies verified as complete
- [ ] Known complexity/risks called out
- [ ] Agent instructions clear
- [ ] Success criteria defined
- [ ] Blocker reporting process explained
