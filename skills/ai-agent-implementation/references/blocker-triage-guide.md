# Blocker Triage Guide

How to identify, classify, and resolve blockers in agent-based execution.

## Blocker Classification

When an agent reports they're stuck, determine the blocker type:

### Type 1: Technical Blocker 🔧

**What it is**: Feature design is broken, code won't work as intended, or implementation is infeasible.

**Signs**:
- "Task won't compile"
- "API design doesn't support what we need"
- "There's a fundamental conflict between Task 1 and Task 2"
- "Performance is unacceptable"
- "Framework limitation prevents this approach"

**Examples**:
- Agent implements API but discovers the approach violates REST principles
- Feature requires recursive data structure but framework doesn't support it efficiently
- Test suite reveals a flaw in the architecture

**Resolution Path**:
1. **Diagnose**: What specifically doesn't work?
2. **Options**:
   - Can agent fix it with code changes? → Have them rework it
   - Does it need design change? → Clarify with breakdo or adjust acceptance criteria
   - Is it a real blocker? → Document and decide: rework or workaround?
3. **Fix**: Agent re-executes task with new approach
4. **Verify**: New approach passes acceptance criteria
5. **Document**: What changed and why

**Timeline**: 1-3 hours (agent rework) to 1+ days (design change)

**Action in blocker log**:
```
**Severity**: High (blocks feature completion)
**Cause**: Technical - [specific issue]
**Resolution**: Rework task with [new approach]
**Owner**: Agent [Name]
```

---

### Type 2: Integration Blocker 🔗

**What it is**: Task works in isolation but breaks when connected to other work. Outputs don't match inputs expected by dependent tasks.

**Signs**:
- "Task 1 works, but Task 2 can't use its output"
- "Components compile separately but don't integrate"
- "API returns wrong format for frontend"
- "Database schema doesn't match ORM expectations"

**Examples**:
- Frontend expects user object with `id` field, backend returns `userId`
- API response includes extra fields that cause validation to fail
- Component exports interface but consumer expects different interface
- Data format mismatch between microservices

**Resolution Path**:
1. **Diagnose**: What specifically doesn't match?
   - Review Task 1 output vs. Task 2 input spec
   - Identify the mismatch
2. **Options**:
   - Rework Task 1 to produce correct format
   - Rework Task 2 to accept Task 1 format
   - Agree on new format both support
3. **Fix**: Agent updates one or both tasks
4. **Retest**: Full end-to-end integration passes
5. **Document**: What was mismatched and how it was fixed

**Timeline**: 30 minutes to 2 hours (usually straightforward to fix)

**Action in blocker log**:
```
**Severity**: High (blocks downstream work)
**Cause**: Integration - Task 1 output format ≠ Task 2 input spec
**Resolution**: Update [Task/Component] to use [agreed format]
**Owner**: Agent [Name]
```

---

### Type 3: Design Blocker 🎨

**What it is**: Requirements were unclear, contradictory, or wrong. Agent implemented correctly but delivered something other than what was actually needed.

**Signs**:
- "I built what you asked, but it doesn't make sense"
- "The acceptance criteria conflict with each other"
- "This design doesn't match the actual use case"
- "We need to rethink this feature"

**Examples**:
- Acceptance criteria asks for both real-time updates AND eventual consistency (contradictory)
- Feature spec says "all users see same data" but use case is per-user dashboards
- API design assumes single-user but needs multi-tenant support
- Component tree designed without considering data flow

**Resolution Path**:
1. **Diagnose**: What's the actual problem with the design?
2. **Clarify**: 
   - What was the intent?
   - What should it actually do?
   - What did we get wrong?
3. **Rework spec**:
   - Update acceptance criteria
   - Update task description
   - Document the fix
4. **Agent redoes**: Agent re-executes task with corrected requirements
5. **Verify**: New implementation matches fixed requirements

**Timeline**: 1-4 hours (requires thinking + rework)

**Action in blocker log**:
```
**Severity**: High (requires rework after design change)
**Cause**: Design - Requirements were [unclear/contradictory/wrong]
**Resolution**: Clarify [specific aspect], agent redoes task
**Owner**: You (requirements) + Agent (rework)
```

---

### Type 4: External Blocker 🚧

**What it is**: Task is blocked by something outside this feature. Usually a dependency, library issue, or infrastructure problem.

**Signs**:
- "Waiting for [library] to be updated"
- "[External service] is down"
- "Need [API key] from [external team]"
- "Blocked on [infrastructure change]"

**Examples**:
- Need new version of authentication library (waiting for release)
- API depends on feature flag from platform team (waiting for them to enable)
- Frontend needs backend API that's not deployed yet
- Build depends on Docker image that hasn't been pushed yet

**Resolution Path**:
1. **Diagnose**: What external thing are we waiting for?
2. **Options**:
   - **Wait**: External dependency will be ready by [date]. Work on other tasks meanwhile.
   - **Workaround**: Use mock/stub version to unblock. Plan real integration later.
   - **Change approach**: Don't depend on external thing. Different implementation.
3. **Action**:
   - Waiting: Document timeline, work on other batches
   - Workaround: Agent uses mock, document real integration task
   - Change: Agent pivots to alternative approach
4. **Unblock**: Once external blocker resolved, revisit task

**Timeline**: Varies (could be hours to days depending on external dependency)

**Action in blocker log**:
```
**Severity**: Medium/Low (external, can work around)
**Cause**: External - Waiting for [dependency]
**Resolution**: [Wait for date] / [Workaround: use mock] / [Change approach]
**Owner**: External [Service/Team], or Agent [if workaround]
```

---

## Triage Decision Tree

When agent reports blocker, follow this flow:

```
Blocker Reported
    ↓
What's preventing progress?
    ├─ Code doesn't compile / wrong approach / feature impossible
    │   └─ TECHNICAL BLOCKER → Rework task or adjust design
    │
    ├─ Works alone but doesn't integrate with other task
    │   └─ INTEGRATION BLOCKER → Fix format mismatch
    │
    ├─ Requirements were wrong / contradictory
    │   └─ DESIGN BLOCKER → Clarify requirements, rework task
    │
    └─ Waiting on something external to feature
        └─ EXTERNAL BLOCKER → Wait, workaround, or change approach
```

---

## Resolution Strategies by Blocker Type

### Technical Blockers: 3 Options

| Option | When | Process |
|--------|------|---------|
| **Rework** | Simple fix (code change) | Agent fixes code, re-tests, verifies |
| **Design Change** | Fundamental approach wrong | Clarify real requirement, agent rebuilds, re-tests |
| **Accept Limitation** | Can't fix (framework limit) | Document limitation, work within it, continue |

### Integration Blockers: 2 Options

| Option | When | Process |
|--------|------|---------|
| **Rework Task 1** | Task 1 output format wrong | Agent fixes Task 1 output, re-tests integration |
| **Rework Task 2** | Task 2 expectations wrong | Agent fixes Task 2 to accept Task 1 format, re-tests |

### Design Blockers: 1 Option

| Option | When | Process |
|--------|------|---------|
| **Clarify & Rework** | Always | Update spec/acceptance criteria, agent re-executes, re-tests |

### External Blockers: 3 Options

| Option | When | Process |
|--------|------|---------|
| **Wait** | External will be ready soon | Document date, work on other batches, revisit later |
| **Workaround** | Need unblocked, can use mock | Agent uses mock/stub, plan real integration later |
| **Change Approach** | External not needed | Agent implements differently, no dependency on external |

---

## Blocker Resolution Timeline

**Estimate how long resolution will take**:

### Fast (< 1 hour)
- Integration format mismatch (change field name, retype)
- Simple code fix (compilation error, syntax issue)
- Test failure with obvious cause

**Action**: Have agent fix immediately, verify, continue.

### Medium (1-4 hours)
- Technical blocker requiring code rework (better algorithm, error handling)
- Design blocker requiring clarification (spec change, rework task)
- Integration issue requiring coordination between multiple tasks

**Action**: Clarify if needed, agent reworks, re-tests, document what changed.

### Slow (> 4 hours or blocking)
- External dependency with no timeline
- Major design flaw requiring rethinking
- Complex integration issue across multiple components

**Action**: 
1. Pause this batch
2. Work on other batches in parallel
3. Revisit when blocker resolved
4. Document blocker as blocking other work

---

## Blocker Log Format

When documenting a blocker, fill in all sections:

```markdown
### Blocker: [Short Title]

**Type**: Technical / Integration / Design / External

**Severity**: Critical / High / Medium / Low
- Critical: Feature cannot ship without fixing
- High: Major work blocked
- Medium: Affects some tasks
- Low: Nice to fix but not urgent

**Affected Tasks**: Task [ID], Task [ID]

**Description**: [What's the problem?]

**Cause**: [Why is it happening?]
- For Technical: What specifically doesn't work?
- For Integration: What mismatch?
- For Design: What requirement was unclear?
- For External: What are we waiting for?

**Impact**: [If we don't fix this...]
- What feature doesn't work?
- What tasks stay blocked?
- How many other tasks are downstream?

**Resolution**: [How will we fix it?]
- Technical: Rework with [new approach]
- Integration: Fix [component] to match [spec]
- Design: Clarify [requirement], then rework
- External: Wait for [date] / Use mock / Change approach

**Owner**: [Who fixes it?]
- Agent [Name]
- You
- External team/service

**Estimated Time**: [How long to resolve?]
- < 1 hour / 1-4 hours / > 4 hours / Unknown

**Target Resolution**: [When should it be fixed?]
- Immediately (blocks other work)
- After current batch
- Later (can work around)

**Status**: Open / In Progress / Resolved

**Resolution Date**: [When it was fixed]

**Resolution Details**: [What we actually did]

**Lessons Learned**: [What did we learn from this blocker?]
```

---

## Blocker Communication

### Report from Agent
Agent reports: "I'm stuck on Task X. The API design doesn't support this."

**Your action**:
1. Classify: Is this Technical/Integration/Design/External?
2. Triage: Is this a real blocker or a misunderstanding?
3. Act:
   - If technical: Do we need to rework? Can agent fix it?
   - If integration: Can agent coordinate with other task owner?
   - If design: Do we need to clarify requirements?
   - If external: Do we wait, work around, or change approach?
4. Communicate back: Here's how we're unblocking this

**Example response**:
> This is a Design blocker - the API spec wasn't clear. Let me review what the feature actually needs. Once I clarify, can you rework the API design? I'll have clarification for you in [time].

### Update Blocker Log
```markdown
### Blocker: API design insufficient

**Type**: Design

**Severity**: High

**Description**: API design doesn't support multi-tenant access

**Agent Reported**: [Date/Time]

**Status**: In Progress - Clarifying requirements

**Next Step**: Return clarified spec by [Date]
```

### Resolution Communication
Once resolved:
> Blocker resolved! The API needs to support [specific requirement]. I've updated the acceptance criteria. Can you rework the API design with [new approach]?

---

## Preventing Blockers

### At Batch Preparation Time
1. **Review batch context** carefully - clear task descriptions prevent design blockers
2. **Verify dependencies** - ensure all inputs are ready (prevents integration blockers)
3. **Call out complexity** - tell agent about known technical challenges
4. **Confirm requirements** - get agreement on acceptance criteria before starting

### During Agent Execution
1. **Monitor progress** - ask for updates if taking longer than expected
2. **Escalate early** - don't wait for agent to finish if seeing issues
3. **Unblock fast** - if agent reports blocker, triage and resolve quickly
4. **Coordinate integration** - ensure tasks working together test early

### After Resolution
1. **Document** - why did blocker happen? How can we prevent next time?
2. **Update templates** - if unclear spec caused issue, improve task template
3. **Share learning** - tell next agent "we learned that [lesson]"

---

## Blocker Patterns

### Pattern: "I built it, but acceptance criteria conflict"

**Blocker Type**: Design

**Root Cause**: Requirements were contradictory or incomplete

**Resolution**: 
1. Clarify which criterion is actually important
2. Update acceptance criteria
3. Agent reworks feature to match clarified spec

**Prevention**: 
- During batch prep: Review acceptance criteria for conflicts
- Get confirmation from stakeholders before starting

### Pattern: "This works alone but breaks in integration"

**Blocker Type**: Integration

**Root Cause**: Task output format didn't match downstream task's expectations

**Resolution**:
1. Identify specific format mismatch
2. Decide: fix source (Task 1) or consumer (Task 2)?
3. Agent fixes whichever needs changing
4. Test end-to-end integration

**Prevention**:
- During batch prep: Document integration contracts explicitly
- During execution: Test integration early, don't wait until batch done

### Pattern: "Framework doesn't support this"

**Blocker Type**: Technical

**Root Cause**: Feature requires capability framework doesn't have

**Resolution**:
1. Can we work around it? (use different approach)
2. Can we upgrade framework? (external dependency)
3. Can we accept limitation? (document, document, use differently)
4. Agent implements with chosen approach

**Prevention**:
- During spec phase: Research framework capabilities
- During batch prep: Highlight known framework limitations
- Call out if approaching framework limits

### Pattern: "API from [other team] isn't ready"

**Blocker Type**: External

**Root Cause**: Dependency on work outside this feature

**Resolution**:
1. What's the timeline for their delivery?
2. Can we use mock API? (unblock us, plan real integration later)
3. Can we build without it? (different approach)
4. Must we wait? (schedule other work, revisit later)

**Prevention**:
- During planning: Identify external dependencies
- During batch prep: Confirm external dependencies are ready
- Have mock APIs available for common dependencies

---

## Blocker Dashboard (Live Tracking)

Maintain this summary as blockers come and go:

```markdown
# Blocker Status: [Feature]

**Total Blockers**: [N] (Critical: X, High: Y, Medium: Z, Low: W)

**Blocking Feature Completion**: X blockers

**Timeline Impact**: [On track / At risk / Delayed by N days]

---

## Critical Blockers (Blocking entire feature)

### Blocker 1: [Title]
- **Status**: Open
- **Days Open**: N
- **Target Fix**: [Date]
- **Owner**: [You/Agent/External]

---

## High Blockers (Blocking some tasks)

### Blocker: [Title]
- **Status**: [Open/In Progress]
- **Affected**: [Task X, Task Y]

---

## Medium Blockers (Slow progress on specific tasks)

### Blocker: [Title]
- **Status**: [Open/In Progress]

---

## Recent Resolutions ✅

### Resolved: [Title] - [Date]
- Took: N hours
- Cost: [What did fix require?]
```

---

## See Also

- `SKILL.md`: Core workflow for tracking blockers
- `example-ai-execution.md`: Real example with blocker scenarios
- Feature-planning `implementation-sequence.md`: Task dependencies that inform blocker analysis
