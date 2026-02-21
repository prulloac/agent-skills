# Integration Guide: Using feature-summary with Other Skills

This document explains how to integrate feature-summary with feature-breakdown, feature-planning, and execution-tracking.

## Quick Integration Matrix

| Integration | Use Case | How It Works |
|-------------|----------|-------------|
| breakdown → summary | Document planned feature | Use breakdown tasks to ensure docs are complete |
| summary → planning | Plan feature development | Reference future enhancements section |
| planning → summary | Update roadmap | Add timeline info to roadmap section |
| tracking → summary | Update during development | Update status section weekly |

---

## Workflow 1: Document an Existing Feature

**Duration**: 1-2 hours  
**Skills used**: feature-summary only

```
1. Gather materials
   ├─ Access to working feature
   ├─ Any existing docs
   └─ Source code to reference

2. Run feature-summary skill
   ├─ Analyze feature scope
   ├─ Classify feature type
   ├─ Write documentation
   └─ Output: docs/features/[name]/summary.md

3. Share with users
   └─ Documentation now available for feature discovery
```

**Example**: Document the "Git Blame Overlay" feature after implementation

---

## Workflow 2: Plan and Document a New Feature

**Duration**: 4-8 hours  
**Skills used**: feature-breakdown → feature-summary → feature-planning

### Step 1: Create Feature Breakdown

```
Input:  "Add SSH key management to authentication system"
Output: docs/features/ssh-keys/breakdown.md

Contains:
├─ 20+ implementation tasks
├─ Component dependencies
├─ Acceptance criteria
└─ Validation plan
```

### Step 2: Create Feature Summary (PARALLEL with planning)

```
Input:  breakdown.md + feature spec
Output: docs/features/ssh-keys/summary.md

Use breakdown to:
├─ Ensure documentation covers all components
├─ Reference architecture from breakdown
├─ Validate completeness
├─ Extract technical details

Result: Users and stakeholders understand the feature
```

### Step 3: Create Feature Planning

```
Input:  breakdown.md
Output: docs/features/ssh-keys/implementation-sequence.md

Now team knows:
├─ Task execution order
├─ Dependencies
├─ Parallelization opportunities
└─ Timeline for completion
```

### Step 4: Team Implementation

```
Based on: implementation-sequence.md

Team:
├─ Assigns tasks
├─ Tracks progress
├─ Resolves blockers
└─ Completes features
```

### Step 5: Track Execution Progress

```
Input:  implementation-sequence.md
Output: docs/features/ssh-keys/implementation-progress.md

Management:
├─ Monitors actual vs. planned progress
├─ Identifies delays
├─ Adjusts timeline
└─ Reports status
```

---

## Workflow 3: Maintain Documentation During Development

**Duration**: 15 minutes per week  
**Skills used**: feature-summary updates

### During Development

```
Weekly tasks:
├─ Update "Current Status" section
│  └─ List what's been completed
├─ Check "Future Enhancements" section
│  └─ Move completed items to current status
├─ Update version if applicable
└─ Review limitations section
   └─ Add new constraints discovered
```

### Before Release

```
Final review:
├─ Verify all sections are accurate
├─ Update version number
├─ Move all completed items from "Future"
├─ Mark status as "Current" or "Latest"
└─ Ready for release announcement
```

### After Release

```
Post-release:
├─ Create new feature summary for next version
├─ Archive old docs (if major version change)
├─ Link previous versions in "See Also"
└─ Update roadmap with next phase
```

---

## Integration: breakdown → summary

### What to Extract from breakdown.md

From breakdown document, feature-summary should identify:

```
From breakdown.md:         Use in summary as:
─────────────────────────────────────────────────
Executive summary      →   Overview section
Component architecture →   Technical implementation section
All requirements       →   Completeness check
Acceptance criteria    →   How to validate user satisfaction
Testing plan           →   Part of "How to test" in docs
```

### What NOT to Duplicate

```
❌ Don't copy task lists (that's breakdown's job)
❌ Don't copy acceptance criteria verbatim (paraphrase for users)
❌ Don't duplicate implementation plan details
✅ Do use breakdown to ensure you didn't miss anything
```

### Example: Git Blame Overlay

**From breakdown.md**:
```
Tasks:
  - Implement BlameProvider class
  - Create OverlayManager for decorations
  - Wire click event handlers
  - Add configuration support
  - Write performance caching

Acceptance Criteria:
  - Clicking a line shows blame overlay
  - Overlay contains hash, author, date, message
  - Format is configurable
  - Performance meets 30-second cache TTL
```

**Used in summary.md**:
```
## What It Does
When a user clicks a line, an overlay appears with:
- Commit hash (7-char)
- Author name and/or email
- Commit date
- Commit message

## Technical Implementation
Components:
- BlameProvider: Fetches git blame data
- OverlayManager: Creates and positions decorations
- Extension: Coordinates between components

## Configuration
Users can customize the output format...
```

---

## Integration: planning → summary

### What to Include in Future Enhancements

From feature-planning, copy planned items to "Future Enhancements":

```
From implementation-sequence.md:
├─ Planned features (Planned for v0.0.4)
├─ Dependency chains (affects roadmap order)
└─ Timeline (when features arrive)

To summary.md "Future Enhancements":
├─ What? (The feature)
├─ When? (Planned version)
└─ Why? (What problem it solves)
```

### Example

**From planning document**:
```
v0.0.3 (Feb 2025): Keyboard shortcuts
v0.0.4 (Mar 2025): Multiple overlays
v0.0.5 (Apr 2025): Blame history
```

**In summary.md**:
```
## Future Enhancements (Out of Scope - v0.0.2)

- [ ] Keyboard shortcut to show blame (planned v0.0.3)
- [ ] Multiple overlays support (planned v0.0.4)
- [ ] Blame history navigation (planned v0.0.5)

See [implementation-sequence.md](../features/git-blame-overlay/implementation-sequence.md) for details.
```

---

## Integration: tracking → summary

### Weekly Status Updates

Use execution-tracking to update feature docs:

```
From implementation-progress.md:        Update in summary.md:
──────────────────────────────────────────────────────────
Completed features              →   Move to "Current Status"
New blockers discovered         →   Add to "Known Limitations"
Timeline slippage               →   Note in roadmap section
Version bump                    →   Update version section
Bugs fixed                      →   Update "Current Status"
```

### Example Update Cycle

**Week 1 - docs/features/git-blame-overlay/implementation-progress.md**:
```
Completed:
- BlameProvider implementation ✅
- OverlayManager decorations ✅

In Progress:
- Event handler wiring
- Configuration support

Blockers:
- None currently
```

**Update summary doc**:
```
## Current Status

✅ Click-based blame display
✅ Git integration via native commands
🚧 Configurable output format (in progress)
```

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Copying Task Lists Verbatim

**Wrong**:
```markdown
## Implementation

1. Create BlameProvider class
2. Implement caching logic
3. Add configuration parsing
4. Create OverlayManager
...
```

**Right**:
```markdown
## Technical Implementation

The feature uses three main components:
- BlameProvider: Fetches and caches git blame data
- OverlayManager: Creates inline decorations
- Extension: Coordinates between components
```

### ❌ Pitfall 2: Not Updating When Status Changes

**Problem**: Documentation gets out of sync with actual feature status

**Solution**: Update docs weekly during development, at minimum before release

### ❌ Pitfall 3: Ignoring Breakdown's Acceptance Criteria

**Problem**: Summary docs miss important validation points

**Solution**: Review breakdown's acceptance criteria to ensure docs cover them

### ❌ Pitfall 4: Not Cross-Referencing Related Features

**Problem**: Users can't discover related features

**Solution**: Always add "Related Features" section with links

---

## File References

When working with multiple skills, reference files correctly:

```
From feature-summary docs to internal planning:
docs/features/git-blame-overlay/summary.md
  ↓ References ↓
docs/features/git-blame-overlay/breakdown.md
docs/features/git-blame-overlay/implementation-sequence.md

Example markdown:
[View implementation plan](./implementation-sequence.md)
```

---

## Integration with Other Documentation

Feature-summary docs can also reference:

```
├─ Project README.md
│  └─ Link: "See [features](docs/) for detailed documentation"
├─ CHANGELOG.md
│  └─ Link released features to their docs
├─ Contributing guide
│  └─ Link to breakdown for contributors
└─ API documentation
   └─ Link to technical implementation section
```

---

## Recommended Tools & Processes

### For Documentation Team

```
Week 1:  feature-breakdown (1-2 hrs)
         ↓
Week 2:  feature-summary (1-2 hrs)
         ↓
Share breakdown with team
         ↓
Week 3:  feature-planning (1-2 hrs)
```

### For Development Team

```
Review breakdown.md (understand scope)
         ↓
Review implementation-sequence.md (understand order)
         ↓
Begin implementation
         ↓
Weekly: Update feature-summary "Current Status"
         ↓
Weekly: Track progress in execution-tracking
```

### Automation Opportunities

```
├─ Auto-update version numbers from package.json
├─ Auto-generate cross-reference links
├─ Auto-create feature summary from template
└─ Auto-validate links between docs
```

---

## Quick Reference: When to Use Each Skill

### Use feature-summary when:
- ✅ Feature exists and works
- ✅ Need user-facing documentation
- ✅ Want to create feature catalog
- ✅ Need to classify feature type

### Use feature-breakdown when:
- ✅ Planning a new feature
- ✅ Need to decompose into tasks
- ✅ Want acceptance criteria
- ✅ Creating implementation plan

### Use feature-planning when:
- ✅ Have breakdown document
- ✅ Need execution sequence
- ✅ Want to identify dependencies
- ✅ Need timeline

### Use execution-tracking when:
- ✅ Team is actively building
- ✅ Have implementation-sequence.md
- ✅ Need progress updates
- ✅ Want blocker tracking

---

## See Also

- `ecosystem-diagram.md` - Visual overview of skill ecosystem
- `SKILL.md` - Complete feature-summary workflow
- `assets/documentation-template.md` - Blank template
- `feature-type-reference.md` - Feature classification
- `../examples/` - Real-world feature documentation examples
