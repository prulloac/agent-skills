# Feature Documentation Skills Ecosystem

This document shows how feature-summary fits into the feature documentation workflow.

## The Four Skills

```
┌──────────────────────────────────────────────────────────────┐
│         FEATURE DOCUMENTATION SKILL ECOSYSTEM               │
└──────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────┐
 │ 1. feature-breakdown                                       │
 │    Question: "What needs to be built and how do we         │
 │              validate it's complete?"                      │
 │    Input:    Feature specification or idea                │
 │    Output:   docs/features/[name]/breakdown.md             │
 │    Audience: Implementation team                           │
 └─────────────────────────────────────────────────────────────┘
                            ↓
 ┌─────────────────────────────────────────────────────────────┐
  │ 2. feature-summary                                         │
  │    Question: "How do we document and communicate this      │
  │              feature to users?"                            │
  │    Input:    Implemented feature + breakdown (optional)   │
  │    Output:   docs/features/[name]/summary.md              │
  │    Audience: End users, stakeholders, developers           │
  └─────────────────────────────────────────────────────────────┘
                      ↙              ↘
 ┌──────────────────────┐    ┌──────────────────────┐
 │ 3. feature-planning  │    │ 4. execution-tracking│
 │                      │    │                      │
 │ Question: "In what   │    │ Question: "Are we on │
 │ order should tasks   │    │ schedule? What's     │
 │ be executed?"        │    │ blocking us?"        │
 │                      │    │                      │
 │ Input: breakdown.md  │    │ Input:               │
 │ Output:              │    │ impl.-sequence.md    │
 │ impl.-sequence.md    │    │ Output:              │
 │                      │    │ impl.-progress.md    │
 └──────────────────────┘    └──────────────────────┘
```

## Documentation Hierarchy

### Feature Documentation (Unified Structure)
```
docs/features/
├── git-blame-overlay/
│   ├── breakdown.md ◄── created by feature-breakdown
│   ├── summary.md ◄── created by feature-summary
│   ├── configuration.md ◄── optional, created by feature-summary
│   ├── reference.md ◄── optional, created by feature-summary
│   ├── implementation-sequence.md ◄── created by feature-planning
│   └── implementation-progress.md ◄── created by execution-tracking
├── customizable-formatting/
│   └── [similar structure]
└── [other-features]/
    └── [similar structure]
```

## When to Use Each Skill

| Skill | When | What you need | What you get |
|-------|------|---------------|--------------|
| **feature-breakdown** | Planning a new feature | Spec or detailed idea | Task decomposition + acceptance criteria |
| **feature-summary** | Documenting existing feature | Implemented feature | User-facing documentation + roadmap |
| **feature-planning** | Scheduling work | breakdown.md | Execution sequence + timeline |
| **execution-tracking** | Monitoring progress | implementation-sequence.md | Progress reports + blocker tracking |

## Information Flow

```
Feature Specification
    ↓
feature-breakdown creates tasks
    ├→ docs/features/[name]/breakdown.md (internal: what to build)
    ├→ Also used by: feature-planning and feature-summary
    ↓
feature-summary creates user docs
    ├→ docs/features/[name]/summary.md (external: what users need to know)
    ├→ Can reference: feature-planning roadmap info
    ↓
feature-planning sequences tasks
    ├→ docs/features/[name]/implementation-sequence.md (internal: when to build)
    ↓
Team implements + feature-summary updates docs
    ├→ Update "Current Status" with progress
    ├→ Move items from "Future" when completed
    ↓
execution-tracking monitors
    ├→ docs/features/[name]/implementation-progress.md (internal: tracking progress)
```

## Feature-Summary's Role

The **feature-summary** skill transforms internal planning into user-facing documentation:

| Source | From | Use For |
|--------|------|---------|
| Feature spec | Input | Overview, use cases |
| breakdown.md | Optional input | Completeness check, architecture context |
| Actual implementation | Input | Technical accuracy, current status |
| feature-planning docs | Optional input | Future enhancements, roadmap |

**Result**: Comprehensive documentation that serves users, developers, and stakeholders

## Directory Organization Rules

**MANDATORY structure:**

```
✅ docs/features/[feature-name]/summary.md          (user documentation)
✅ docs/features/[feature-name]/breakdown.md        (internal planning)
✅ docs/features/[feature-name]/configuration.md    (optional, detailed config)
✅ docs/features/[feature-name]/reference.md        (optional, technical details)
✅ Feature names in kebab-case

❌ docs/my-feature.md                (wrong - flat structure)
❌ docs/my-feature/README.md         (wrong - old structure)
❌ docs/features/my-feature/feature-summary.md (wrong - redundant naming)
```

## Recommended Execution Order

1. **Create feature-breakdown** (1-2 hrs)
   - Understand scope completely
   - Document all tasks and acceptance criteria

2. **Create feature-summary** (1-2 hrs)
   - Document for users
   - Classify feature type
   - Plan future enhancements

3. **Create feature-planning** (1-2 hrs)
   - Sequence tasks for team
   - Identify dependencies
   - Create timeline

4. **Team implementation** (varies)
   - Follow the plan
   - Implement features

5. **execution-tracking** (ongoing)
   - Monitor progress
   - Adjust as needed
   - Track blockers

## See Also

- `SKILL.md` - Complete feature-summary workflow
- `workflow-integration-guide.md` - Detailed integration examples
- `assets/documentation-template.md` - Blank template to use
- `feature-type-reference.md` - Feature classification guide
- `../examples/` - Real-world feature documentation examples
