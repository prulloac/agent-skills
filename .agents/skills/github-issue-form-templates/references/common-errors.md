# Common Validation Errors

Troubleshooting guide for GitHub issue form validation errors.

## Table of Contents
1. [Syntax Errors](#syntax-errors)
2. [Field Type Errors](#field-type-errors)
3. [Attribute Errors](#attribute-errors)
4. [Validation Errors](#validation-errors)
5. [Troubleshooting Checklist](#troubleshooting-checklist)

---

## Syntax Errors

### Invalid YAML Syntax

**Error**: `YAML parsing error` or `Unexpected character`

**Common causes:**
- Incorrect indentation (YAML requires consistent spacing)
- Missing colons after keys
- Improper list formatting
- Unmatched quotes or pipes

**Example - Incorrect indentation:**
```yaml
# ✗ Wrong: Mixed indentation
- type: input
  id: email
    label: Email
    description: Your email
```

**Fix:**
```yaml
# ✓ Correct: Consistent indentation
- type: input
  id: email
  attributes:
    label: Email
    description: Your email
```

**Example - Missing colon:**
```yaml
# ✗ Wrong
- type: input
  attributes
    label: Email
```

**Fix:**
```yaml
# ✓ Correct
- type: input
  attributes:
    label: Email
```

---

## Field Type Errors

### Unknown Field Type

**Error**: `Invalid field type: 'text'` or similar

**Cause**: Using a field type that doesn't exist

**Valid field types:**
- `markdown`
- `input`
- `textarea`
- `dropdown`
- `checkboxes`
- `hidden`

**Example - Invalid type:**
```yaml
# ✗ Wrong: 'text' is not a valid type
- type: text
  attributes:
    label: Email
```

**Fix:**
```yaml
# ✓ Use 'input' instead
- type: input
  attributes:
    label: Email
```

### Missing Required Field Type

**Error**: `Field must have a 'type'` or similar

**Cause**: Forgot to specify the field type

**Example - Missing type:**
```yaml
# ✗ Wrong
- id: email
  attributes:
    label: Email
```

**Fix:**
```yaml
# ✓ Correct: Include type
- type: input
  id: email
  attributes:
    label: Email
```

---

## Attribute Errors

### Missing Required Attributes

**Error**: `Missing required attribute: 'label'` or similar

**Cause**: Field type requires certain attributes that are missing

**Required attributes by field type:**
- `markdown`: `value`
- `input`: `label`
- `textarea`: `label`
- `dropdown`: `label`, `options`
- `checkboxes`: `label`, `options`
- `hidden`: `label`, `value`

**Example - Missing label:**
```yaml
# ✗ Wrong
- type: input
  id: email
  attributes:
    placeholder: "you@example.com"
```

**Fix:**
```yaml
# ✓ Correct: Include label
- type: input
  id: email
  attributes:
    label: Email Address
    placeholder: "you@example.com"
```

### Invalid Attribute Value

**Error**: `Invalid value for attribute 'options'` or similar

**Cause**: Attribute value has wrong format

**Common attribute issues:**

**Dropdown options must be array:**
```yaml
# ✗ Wrong: Options as string
- type: dropdown
  attributes:
    options: "Option 1, Option 2"

# ✓ Correct: Options as array
- type: dropdown
  attributes:
    options:
      - Option 1
      - Option 2
```

**Checkbox options must have label:**
```yaml
# ✗ Wrong: Options as strings
- type: checkboxes
  attributes:
    options:
      - I agree
      - I consent

# ✓ Correct: Options with label key
- type: checkboxes
  attributes:
    options:
      - label: I agree
      - label: I consent
```

**Multiple should be boolean:**
```yaml
# ✗ Wrong: String value
- type: dropdown
  attributes:
    multiple: "true"

# ✓ Correct: Boolean value
- type: dropdown
  attributes:
    multiple: true
```

---

## Validation Errors

### Invalid Regex Pattern

**Error**: `Invalid regular expression` or pattern doesn't match

**Cause**: Regex pattern syntax error

**Example - Unescaped special characters:**
```yaml
# ✗ Wrong: Special char not escaped
validations:
  regex: ^user(name)@example.com$

# ✓ Correct: Escape or properly group
validations:
  regex: ^user\(name\)@example\.com$
```

**Example - Missing anchors:**
```yaml
# ✗ Works but incomplete
validations:
  regex: \d+\.\d+\.\d+

# ✓ Better: Use anchors for full match
validations:
  regex: ^\d+\.\d+\.\d+$
```

### Invalid Default Index

**Error**: `Invalid default index` or field shows no default

**Cause**: Default index is out of range

**Example - Index too high:**
```yaml
# ✗ Wrong: Only 3 options (indices 0-2), default is 5
- type: dropdown
  attributes:
    options:
      - Option 1
      - Option 2
      - Option 3
    default: 5

# ✓ Correct: Default within range (0-2)
- type: dropdown
  attributes:
    options:
      - Option 1
      - Option 2
      - Option 3
    default: 1
```

---

## ID and Naming Errors

### Duplicate IDs

**Error**: `Duplicate field ID` or `ID must be unique`

**Cause**: Two fields have the same `id`

**Example - Duplicate IDs:**
```yaml
# ✗ Wrong: Both have id: email
- type: input
  id: email
  attributes:
    label: Primary Email

- type: input
  id: email
  attributes:
    label: Secondary Email
```

**Fix:**
```yaml
# ✓ Correct: Different IDs
- type: input
  id: primary-email
  attributes:
    label: Primary Email

- type: input
  id: secondary-email
  attributes:
    label: Secondary Email
```

### Invalid ID Format

**Error**: `ID must be lowercase` or similar

**Cause**: ID contains uppercase, spaces, or special characters

**ID rules:**
- Lowercase letters only
- Hyphens allowed (not underscores)
- No spaces
- No special characters

**Example - Invalid ID:**
```yaml
# ✗ Wrong: Uppercase and spaces
- type: input
  id: Contact Email
```

**Fix:**
```yaml
# ✓ Correct: Lowercase with hyphens
- type: input
  id: contact-email
```

---

## Render Attribute Errors

### Invalid Render Type

**Error**: `Invalid render type` or rendering doesn't work

**Cause**: Invalid value for `render` attribute

**Valid render values:**
- `markdown` (for formatted text)
- `shell` (for terminal output)
- `python` (for Python code)
- No value (for plain text)

**Example - Invalid render:**
```yaml
# ✗ Wrong: 'html' is not valid
- type: textarea
  attributes:
    render: html
```

**Fix:**
```yaml
# ✓ Correct: Use valid render type
- type: textarea
  attributes:
    render: markdown
```

---

## Body and Top-Level Errors

### Missing Body

**Error**: `Field 'body' is required` or form won't save

**Cause**: No `body` key at top level or it's empty

**Example - Missing body:**
```yaml
# ✗ Wrong: No body section
name: Bug Report
description: Report a bug
```

**Fix:**
```yaml
# ✓ Correct: Include body
name: Bug Report
description: Report a bug
body:
  - type: markdown
    attributes:
      value: "Thanks for reporting!"
```

### Missing Name or Description

**Error**: `Field 'name' is required` or similar

**Cause**: Missing top-level `name` or `description`

**Required top-level fields:**
- `name` - Template display name
- `description` - Template description
- `body` - Form fields

**Example - Missing fields:**
```yaml
# ✗ Wrong: Missing description
name: Bug Report
body:
  - type: input
```

**Fix:**
```yaml
# ✓ Correct: All required fields
name: Bug Report
description: File a bug report
body:
  - type: input
```

---

## Project and Assignee Errors

### Invalid Project Format

**Error**: `Invalid project reference` or projects not assigned

**Cause**: Project format incorrect

**Project format:**
- `org-name/project-number`
- Example: `my-org/1`

**Example - Invalid format:**
```yaml
# ✗ Wrong formats
projects: ["my-org/my-project"]
projects: ["project-1"]
projects: ["1"]
```

**Fix:**
```yaml
# ✓ Correct format
projects:
  - my-org/1
  - my-org/44
```

**Note**: Project assignment requires write permissions. If it fails, check:
1. Project ID is correct (number, not name)
2. User has write access
3. Consider using project's auto-add workflow instead

### Invalid Assignee

**Error**: `User not found` or assignee isn't applied

**Cause**: Username doesn't exist or isn't accessible

**Example - Invalid username:**
```yaml
# ✗ Wrong: Username doesn't exist
assignees:
  - nonexistent-user
```

**Fix:**
```yaml
# ✓ Correct: Real username
assignees:
  - octocat
  - github-user
```

---

## Troubleshooting Checklist

When your form has validation errors:

- [ ] **YAML syntax**: Check indentation (2 spaces per level)
- [ ] **Required fields**: Has `name`, `description`, `body`?
- [ ] **Field types**: Using valid type (`input`, `textarea`, `dropdown`, `checkboxes`, `markdown`, `hidden`)?
- [ ] **Required attributes**: All required attributes present for field type?
- [ ] **Attribute types**: Array vs string vs boolean correct?
- [ ] **Unique IDs**: All field IDs different?
- [ ] **ID format**: IDs lowercase, hyphens only, no spaces?
- [ ] **Default index**: Default within range of options?
- [ ] **Regex pattern**: Pattern valid and properly escaped?
- [ ] **Render values**: Using `markdown`, `shell`, or `python`?
- [ ] **Project format**: Using `org/number` format?
- [ ] **Usernames**: Assignees and code owners exist?

## Test Your Form

1. Push form file to `.github/ISSUE_TEMPLATE/`
2. Go to repository Issues tab
3. Click "New Issue"
4. Check if template appears in menu
5. Try creating an issue to test validations
6. Check console for detailed errors

## Getting Help

- Check [Field Types Reference](field-types.md)
- Review [Validation Patterns](validations.md)
- See GitHub's form schema docs: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema

