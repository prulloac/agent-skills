# Validation Patterns Reference

Guide to validation rules, patterns, and best practices for GitHub issue forms.

## Table of Contents
1. [Required Field Validation](#required-field-validation)
2. [Regex Patterns](#regex-patterns)
3. [Field-Specific Validations](#field-specific-validations)
4. [Validation Best Practices](#validation-best-practices)

---

## Required Field Validation

Mark fields as required to prevent issue creation without them.

### Syntax
```yaml
validations:
  required: true
```

### Which Field Types Support Required
- ✓ `input`
- ✓ `textarea`
- ✓ `dropdown`
- ✓ `checkboxes` (per checkbox)

### Which Field Types Don't Support Required
- ✗ `markdown` (no input)
- ✗ `hidden` (auto-filled)

### Example: Required Issue Title
```yaml
- type: input
  id: issue-title
  attributes:
    label: Issue Title
  validations:
    required: true
```

### Example: Optional Details
```yaml
- type: textarea
  id: additional-context
  attributes:
    label: Additional Context
    description: (Optional) Any other information?
  validations:
    required: false
```

### Best Practices for Required Fields
1. **Be selective**: Only require truly essential information
2. **Be clear**: Clearly mark required vs optional in labels
3. **Provide help**: Add descriptions for required fields
4. **Use wisely**: Too many required fields discourage submissions

---

## Regex Patterns

Validate input against regular expression patterns.

### Syntax
```yaml
validations:
  regex: ^pattern$
  regex_error: "Custom error message"
```

### Attributes
- `regex` (string): JavaScript regex pattern
- `regex_error` (optional, string): Custom error message shown when regex fails

**Important**: Wrap patterns with `^` and `$` anchors to match entire input.

### Common Regex Patterns

**Email address:**
```yaml
regex: ^[^\s@]+@[^\s@]+\.[^\s@]+$
regex_error: "Please enter a valid email address"
```

**Version number (X.Y.Z):**
```yaml
regex: ^\d+\.\d+\.\d+$
regex_error: "Version must be in format X.Y.Z"
```

**URL (http/https):**
```yaml
regex: ^https?:\/\/.+
regex_error: "URL must start with http:// or https://"
```

**GitHub username:**
```yaml
regex: ^@?[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,38}[a-zA-Z0-9])?$
regex_error: "Invalid GitHub username"
```

**Semantic version:**
```yaml
regex: ^v?\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?(\+[a-zA-Z0-9]+)?$
regex_error: "Version format should be v1.2.3 or 1.2.3"
```

**ISO date (YYYY-MM-DD):**
```yaml
regex: ^\d{4}-\d{2}-\d{2}$
regex_error: "Date format must be YYYY-MM-DD"
```

**US phone number:**
```yaml
regex: ^\d{3}-\d{3}-\d{4}$
regex_error: "Phone format should be XXX-XXX-XXXX"
```

**Environment (single word, lowercase, no spaces):**
```yaml
regex: ^[a-z]+$
regex_error: "Environment must be lowercase letters only"
```

---

## Field-Specific Validations

### Input Field

**With regex:**
```yaml
- type: input
  id: github-username
  attributes:
    label: GitHub Username
    placeholder: "octocat"
  validations:
    required: true
    regex: ^@?[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,38}[a-zA-Z0-9])?$
    regex_error: "Invalid GitHub username format"
```

**Required email:**
```yaml
- type: input
  id: contact-email
  attributes:
    label: Contact Email
    description: "We'll only use this to follow up"
  validations:
    required: true
    regex: ^[^\s@]+@[^\s@]+\.[^\s@]+$
```

**Optional with pattern:**
```yaml
- type: input
  id: issue-id
  attributes:
    label: Related Issue ID
    placeholder: "#123 or leave blank"
  validations:
    required: false
    regex: ^#?\d+$
```

### Textarea Field

**Required, no pattern:**
```yaml
- type: textarea
  id: description
  attributes:
    label: Problem Description
  validations:
    required: true
```

**With code rendering:**
```yaml
- type: textarea
  id: error-logs
  attributes:
    label: Error Logs
    render: shell
  validations:
    required: false
    regex: ^.+$
```

### Dropdown Field

**Required selection:**
```yaml
- type: dropdown
  id: severity
  attributes:
    label: Severity
    options:
      - Critical
      - High
      - Medium
  validations:
    required: true
```

**With default value:**
```yaml
- type: dropdown
  id: environment
  attributes:
    label: Environment
    options:
      - Production
      - Staging
      - Development
    default: 2
  validations:
    required: true
```

### Checkbox Field

**Required confirmation:**
```yaml
- type: checkboxes
  id: confirm
  attributes:
    label: Verification
    options:
      - label: I have read the contributing guidelines
        required: true
      - label: This is not a duplicate issue
        required: true
```

**Optional selections:**
```yaml
- type: checkboxes
  id: affected-systems
  attributes:
    label: Affected Systems (optional)
    options:
      - label: Frontend
      - label: Backend
      - label: Database
```

---

## Validation Best Practices

### 1. Use Required Selectively
```yaml
# ✓ Good: Only essential fields required
- type: input
  attributes:
    label: Bug Title
  validations:
    required: true

# ✗ Bad: Too many required fields
- type: input
  attributes:
    label: Optional Context
  validations:
    required: true
```

### 2. Provide Clear Error Messages
```yaml
# ✓ Good: Specific, helpful error
validations:
  regex: ^\d+\.\d+\.\d+$
  regex_error: "Version must be in format X.Y.Z (e.g., 1.2.3)"

# ✗ Bad: Generic error
validations:
  regex: ^\d+\.\d+\.\d+$
  regex_error: "Invalid input"
```

### 3. Help with Placeholders
```yaml
# ✓ Good: Clear example
- type: input
  attributes:
    placeholder: "1.2.3"
  validations:
    regex: ^\d+\.\d+\.\d+$

# ✗ Bad: Unclear
- type: input
  attributes:
    placeholder: "version"
```

### 4. Use Regex Carefully
```yaml
# ✓ Good: Specific, purposeful
regex: ^(dev|staging|prod)$
regex_error: "Must be dev, staging, or prod"

# ✗ Bad: Overly restrictive
regex: ^.+$
regex_error: "Must contain something"
```

### 5. Combine Validation with Description
```yaml
# ✓ Good: Clear guidance
- type: input
  id: version
  attributes:
    label: Affected Version
    description: "Exact version where bug was found (e.g., 2.1.0)"
  validations:
    required: true
    regex: ^\d+\.\d+\.\d+$
    regex_error: "Format: X.Y.Z"
```

### 6. Pre-fill Helpful Defaults
```yaml
# ✓ Good: Helps users
- type: dropdown
  attributes:
    label: Environment
    options:
      - Production
      - Staging
      - Development
    default: 0

# Less helpful: No guidance
- type: dropdown
  attributes:
    label: Environment
    options:
      - Production
      - Staging
      - Development
```

---

## Validation Workflow

### Step 1: Identify Essential Information
What MUST users provide?
- Issue title
- Problem description
- Steps to reproduce

### Step 2: Apply Required Validation
```yaml
- type: input
  id: title
  validations:
    required: true
```

### Step 3: Add Regex for Format Validation
If input must follow a pattern:
```yaml
- type: input
  id: version
  validations:
    required: true
    regex: ^\d+\.\d+\.\d+$
```

### Step 4: Provide Clear Error Messaging
```yaml
validations:
  required: true
  regex: ^\d+\.\d+\.\d+$
  regex_error: "Please use format X.Y.Z (e.g., 1.2.3)"
```

### Step 5: Add Helpful Context
```yaml
- type: input
  id: version
  attributes:
    label: Software Version
    description: "Find this in Settings > About"
    placeholder: "1.2.3"
  validations:
    required: true
    regex: ^\d+\.\d+\.\d+$
    regex_error: "Format: X.Y.Z"
```

