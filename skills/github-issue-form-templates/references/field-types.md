# Field Types Reference

Complete guide to all GitHub issue form field types with syntax and examples.

## Table of Contents
1. [Markdown](#markdown)
2. [Input](#input)
3. [Textarea](#textarea)
4. [Dropdown](#dropdown)
5. [Checkboxes](#checkboxes)
6. [Hidden](#hidden)

---

## Markdown

Display-only content. No user input. Commonly used for instructions, section headers, or formatted text.

### Syntax
```yaml
- type: markdown
  attributes:
    value: |
      Your markdown content here
```

### Attributes
- `value` (required, string): Markdown content to display

### Use Cases
- Welcome messages
- Instructions before form fields
- Section dividers
- Links to documentation
- Community guidelines

### Example
```yaml
- type: markdown
  attributes:
    value: |
      ## Before You Report
      
      Please check:
      1. Search [existing issues](https://github.com/org/repo/issues)
      2. Review [documentation](https://docs.example.com)
      3. Check [FAQ](https://example.com/faq)
      
      > Duplicates will be closed without response.
```

---

## Input

Single-line text field for short responses (email, version, URL, etc.).

### Syntax
```yaml
- type: input
  id: unique-id
  attributes:
    label: Field Label
    description: Help text
    placeholder: Example text
  validations:
    required: false
```

### Attributes
- `label` (required, string): Field label shown to user
- `description` (optional, string): Help text below label
- `placeholder` (optional, string): Placeholder text in empty field
- `value` (optional, string): Pre-filled value

### Validations
- `required` (boolean): Make field required
- `regex` (string): Validate against regex pattern
- `regex_error` (string): Custom error message for regex

### Examples

**Email input with regex validation:**
```yaml
- type: input
  id: email
  attributes:
    label: Email Address
    description: Where can we reach you?
    placeholder: you@example.com
  validations:
    required: true
    regex: ^[^\s@]+@[^\s@]+\.[^\s@]+$
    regex_error: "Please enter a valid email address"
```

**Version input:**
```yaml
- type: input
  id: version
  attributes:
    label: Software Version
    placeholder: e.g., 1.2.3
  validations:
    required: true
    regex: ^\d+\.\d+\.\d+$
    regex_error: "Version must be in format X.Y.Z"
```

**URL input:**
```yaml
- type: input
  id: reproduction-url
  attributes:
    label: URL (if applicable)
    description: Link where the issue is reproducible
    placeholder: https://example.com/page
  validations:
    regex: ^https?://.*
    regex_error: "URL must start with http:// or https://"
```

---

## Textarea

Multi-line text field for longer responses (descriptions, error logs, step-by-step instructions).

### Syntax
```yaml
- type: textarea
  id: unique-id
  attributes:
    label: Field Label
    description: Help text
    placeholder: Example text
    render: markdown
    value: Pre-filled content
  validations:
    required: false
```

### Attributes
- `label` (required, string): Field label
- `description` (optional, string): Help text
- `placeholder` (optional, string): Placeholder text
- `value` (optional, string): Pre-filled content
- `render` (optional, string): Format for display (`markdown`, `shell`, or `python`)

### Validations
- `required` (boolean): Make field required
- `regex` (string): Validate against regex pattern

### Render Options

**`render: markdown`**
```yaml
- type: textarea
  attributes:
    label: Details
    render: markdown
```
Treats content as markdown (bullet lists, bold, links, etc.).

**`render: shell`**
```yaml
- type: textarea
  attributes:
    label: Terminal Output
    render: shell
```
Formats as shell script block with syntax highlighting.

**`render: python`**
```yaml
- type: textarea
  attributes:
    label: Python Code
    render: python
```
Formats as Python code block with syntax highlighting.

### Examples

**Bug description:**
```yaml
- type: textarea
  id: what-happened
  attributes:
    label: What happened?
    description: Describe the bug clearly
    placeholder: |
      I was trying to...
      I expected...
      Instead, I got...
  validations:
    required: true
```

**Error log with shell rendering:**
```yaml
- type: textarea
  id: error-log
  attributes:
    label: Error Output
    description: Copy any relevant error messages
    placeholder: "Paste error output here"
    render: shell
  validations:
    required: false
```

**Steps to reproduce:**
```yaml
- type: textarea
  id: steps
  attributes:
    label: Steps to Reproduce
    description: "Use clear, numbered steps"
    placeholder: |
      1. Go to...
      2. Click on...
      3. Enter...
      4. Observe...
    render: markdown
  validations:
    required: true
```

---

## Dropdown

Single or multi-select dropdown menu.

### Syntax
```yaml
- type: dropdown
  id: unique-id
  attributes:
    label: Field Label
    description: Help text
    options:
      - Option 1
      - Option 2
      - Option 3
    multiple: false
    default: 0
  validations:
    required: false
```

### Attributes
- `label` (required, string): Field label
- `description` (optional, string): Help text
- `options` (required, array): List of options to choose from
- `multiple` (optional, boolean): Allow multiple selections (default: false)
- `default` (optional, integer): Index of default selected option (0-based)

### Notes
- `default` is the index position (0 = first option)
- When `multiple: true`, appears as checkboxes in the form
- Options cannot be conditional; all appear regardless

### Examples

**Browser selection (single):**
```yaml
- type: dropdown
  id: browser
  attributes:
    label: Browser
    options:
      - Chrome
      - Firefox
      - Safari
      - Edge
  validations:
    required: true
```

**Severity level with default:**
```yaml
- type: dropdown
  id: severity
  attributes:
    label: Severity
    description: How critical is this issue?
    options:
      - Critical
      - High
      - Medium
      - Low
    default: 2
  validations:
    required: true
```

**Multi-select platforms:**
```yaml
- type: dropdown
  id: platforms
  attributes:
    label: Affected Platforms
    description: Select all that apply
    multiple: true
    options:
      - Windows
      - macOS
      - Linux
      - iOS
      - Android
```

---

## Checkboxes

Multiple independent checkboxes. Can require one or more to be checked.

### Syntax
```yaml
- type: checkboxes
  id: unique-id
  attributes:
    label: Field Label
    description: Help text
    options:
      - label: Option 1
        required: false
      - label: Option 2
        required: true
```

### Attributes
- `label` (required, string): Field label
- `description` (optional, string): Help text
- `options` (required, array): List of checkbox options

### Option Attributes
- `label` (required, string): Checkbox label text
- `required` (optional, boolean): Require this specific checkbox to be checked

### Use Cases
- Pre-submission checklist
- Agreement confirmations
- "I have read the guidelines" type checks
- Multiple selection scenarios

### Examples

**Pre-submission checklist:**
```yaml
- type: checkboxes
  id: prechecks
  attributes:
    label: Before Submitting
    description: Please confirm
    options:
      - label: I have searched existing issues
        required: true
      - label: I am using the latest version
        required: true
      - label: I have read the documentation
        required: true
```

**Feature agreement:**
```yaml
- type: checkboxes
  id: agreement
  attributes:
    label: Agreement
    options:
      - label: I agree to the Code of Conduct
        required: true
      - label: I consent to this issue being made public
        required: false
      - label: I want to be notified of similar reports
        required: false
```

**Component selection (no required):**
```yaml
- type: checkboxes
  id: components
  attributes:
    label: Affected Components
    options:
      - label: Frontend
      - label: Backend
      - label: Database
      - label: Infrastructure
      - label: Documentation
```

---

## Hidden

Metadata fields not displayed to users. Useful for automation.

### Syntax
```yaml
- type: hidden
  id: unique-id
  attributes:
    label: Internal field
    value: fixed-value
```

### Attributes
- `label` (string): Metadata identifier (not shown to users)
- `value` (string): Fixed value for this field

### Use Cases
- Tracking template version
- Automation markers
- Form type identification
- Environment tracking

### Examples

**Template version tracking:**
```yaml
- type: hidden
  id: template-version
  attributes:
    label: version
    value: "1.2"
```

**Automation marker:**
```yaml
- type: hidden
  id: form-type
  attributes:
    label: form-type
    value: "bug-report"
```

---

## Field Attributes Reference

### Common to All Field Types
- `id` (required on non-markdown fields): Unique identifier for field
- `attributes` (required): Object containing field configuration
- `validations` (optional): Validation rules

### Available in Input/Textarea
- `label`: Field name shown to user
- `description`: Help text
- `placeholder`: Hint text in empty field
- `value`: Pre-filled content
- `render`: Display format (textarea only)

### Available in Dropdown
- `options`: Array of choices
- `multiple`: Enable multi-select
- `default`: Default selected index (0-based)

### Available in Checkboxes
- `options`: Array with `label` and `required`

