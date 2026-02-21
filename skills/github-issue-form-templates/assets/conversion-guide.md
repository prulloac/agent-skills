# Converting Markdown to YAML Issue Templates

This document shows a side-by-side comparison of converting a markdown issue template to a YAML issue form.

## Before: Markdown Template

```markdown
---
name: Bug Report
about: File a bug/issue
title: "[BUG] "
labels: bug, needs-triage
assignees: ''

---

<!-- Note: Please search to see if an issue already exists for the bug you encountered. -->

### Environment
- OS:
- Version:
- Browser (if applicable):

### Describe the bug
A clear and concise description of what the bug is.

### Steps To Reproduce
1. Go to...
2. Click on...
3. Enter...
4. Observe...

### Expected behavior
A clear and concise description of what you expected to happen.

### Actual behavior
A clear and concise description of what actually happens.

### Screenshots
If applicable, add screenshots to help explain your problem.

### Logs
Please copy and paste any relevant error logs.

```

## After: YAML Issue Form

```yaml
name: Bug Report
description: File a bug/issue
title: "[BUG] "
labels: ["bug", "needs-triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
        Please search existing issues before submitting.

  - type: input
    id: os
    attributes:
      label: Operating System
      placeholder: "e.g., Windows 10, macOS 12.0, Ubuntu 22.04"
    validations:
      required: false

  - type: input
    id: version
    attributes:
      label: Software Version
      placeholder: "e.g., 1.2.3"
    validations:
      required: true
      regex: ^\d+\.\d+\.\d+$

  - type: input
    id: browser
    attributes:
      label: Browser (if applicable)
      placeholder: "Chrome, Firefox, Safari, Edge"
    validations:
      required: false

  - type: textarea
    id: bug-description
    attributes:
      label: Describe the bug
      description: A clear and concise description
      placeholder: "I was trying to... and it..."
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps To Reproduce
      description: Clear steps to reproduce the bug
      placeholder: |
        1. Go to...
        2. Click on...
        3. Enter...
        4. Observe...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen
      placeholder: "I expected to see..."
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
      placeholder: "Instead, I saw..."
    validations:
      required: true

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots
      placeholder: "Drag and drop images here"
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Any relevant error logs
      render: shell
    validations:
      required: false
```

## Key Conversions

| Markdown | YAML Equivalent |
|----------|-----------------|
| `name:` | `name:` (unchanged) |
| `about:` | `description:` |
| `title:` | `title:` (unchanged) |
| `labels:` | `labels:` (now array format) |
| `assignees:` | `assignees:` (now array format) |
| HTML comments `<!-- -->` | `type: markdown` intro |
| Section headers `### Header` | `label:` in field |
| Section descriptions | `description:` in field |
| Placeholder text in comments | `placeholder:` in field |
| Text input areas | `type: input` or `type: textarea` |

## Step-by-Step Conversion Process

### Step 1: Set Up Header
```yaml
name: Bug Report
description: File a bug report
title: "[BUG] "
labels: ["bug", "needs-triage"]
body:
```

### Step 2: Add Introduction
If your markdown had an intro comment, convert to markdown field:
```yaml
- type: markdown
  attributes:
    value: |
      Thanks for reporting this bug!
      Please search existing issues first.
```

### Step 3: Convert Environment Section
Markdown environment section:
```markdown
### Environment
- OS:
- Version:
- Browser:
```

Becomes individual input fields:
```yaml
- type: input
  id: os
  attributes:
    label: Operating System
  validations:
    required: false

- type: input
  id: version
  attributes:
    label: Version
  validations:
    required: true
```

### Step 4: Convert Description Sections
Markdown section with instructions:
```markdown
### Steps To Reproduce
1. Go to...
2. Click...
```

Becomes textarea with placeholder:
```yaml
- type: textarea
  id: steps
  attributes:
    label: Steps To Reproduce
    placeholder: |
      1. Go to...
      2. Click...
  validations:
    required: true
```

### Step 5: Convert Special Sections

**For log/code output** - Use `render: shell` or `render: markdown`:
```yaml
- type: textarea
  id: logs
  attributes:
    label: Error Output
    render: shell
```

**For screenshots** - Keep as textarea with helpful placeholder:
```yaml
- type: textarea
  id: screenshots
  attributes:
    label: Screenshots
    placeholder: Drag and drop images here
```

### Step 6: Add Validations
Mark required fields and add patterns where helpful:
```yaml
- type: input
  id: version
  attributes:
    label: Version
  validations:
    required: true
    regex: ^\d+\.\d+\.\d+$
```

### Step 7: Test and Deploy
1. Create `.github/ISSUE_TEMPLATE/bug-report.yml`
2. Commit and push
3. Go to Issues → New Issue → select template
4. Test that form works correctly
5. Delete old markdown template once verified

## Benefits of Converting to YAML

| Benefit | Example |
|---------|---------|
| **Structured data** | Machine can parse responses consistently |
| **Required fields** | Prevent incomplete reports |
| **Validation** | Ensure version format correct |
| **Auto-assignment** | Automatically assign to maintainers |
| **Auto-labels** | Consistent labeling |
| **Better UX** | Guided form instead of free-text |
| **Consistency** | All reports have same structure |

## Common Conversion Tips

1. **Progressive disclosure**: Put essential fields first, optional later
2. **Use textareas wisely**: Multi-line text that needs more than one line
3. **Add regex validation**: Enforce format (versions, emails, etc.)
4. **Provide placeholders**: Help users understand what to enter
5. **Use markdown rendering**: For logs and code snippets (`render: shell`)
6. **Keep it short**: Aim for 7-10 fields maximum
7. **Test before deploying**: Push and verify form renders correctly

## Migration Checklist

- [ ] Create new `.yml` file with YAML form
- [ ] Copy metadata (name, description, title, labels)
- [ ] Convert each markdown section to appropriate field type
- [ ] Add helpful `placeholder` and `description` text
- [ ] Add validation rules (required, regex patterns)
- [ ] Test form in GitHub (Issues → New Issue)
- [ ] Verify all fields work correctly
- [ ] Delete old markdown template (don't forget!)
- [ ] Update contributing docs to reference new form

