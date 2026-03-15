#!/usr/bin/env python3
"""
Comprehensive Skill Validator Documentation Generator

Generates documentation for the unified skill validator system.
"""

# This is metadata for the validator documentation

VALIDATOR_DOCUMENTATION = """

# Skill Validator - Complete Implementation Guide

## Overview

The Skill Validator is a comprehensive validation system that ensures OpenCode agent skills meet quality, security, and correctness standards. It integrates three complementary validation approaches:

1. **Structure Validation** - SKILL.md format, file organization, frontmatter compliance
1. **Security Validation** - Detects vulnerabilities, unsafe operations, prompt injection risks
1. **Eval Loop Validation** - Tests skill triggering using sample queries

## Quick Start

### Running the Unified Validator

```bash
cd /workspaces/vibe-coding-template/.agents/skills/skill-validator/scripts

# Basic validation (structure + security)
python validator.py /path/to/skill

# Include eval testing (requires evals/evals.json)
python validator.py /path/to/skill --no-skip-evals

# Verbose output with detailed results
python validator.py /path/to/skill --verbose

# Save comprehensive report
python validator.py /path/to/skill --output validation_report.json
```

### Running Individual Validators

```bash
# Structure validation only
python quick_validate.py /path/to/skill

# Security validation with details
python run_security_checks.py /path/to/skill --verbose --output security_report.json

# Eval validation (requires evals.json)
python run_skill_evals.py /path/to/skill --output eval_results.json --trigger-threshold 0.7
```

## Validation System Components

### 1. Structure Validator (`quick_validate.py`)

**Purpose**: Ensures skill folder organization and SKILL.md compliance

**Checks**:

- SKILL.md file exists
- YAML frontmatter is valid with required fields:
  - `name`: Short identifier (alphanumeric-dash)
  - `description`: Clear usage guidance
- Required directories exist
- No circular references between skills

**Example Output**:

```
Skill is valid!
```

**When it fails**:

```
ERROR: Missing SKILL.md file
ERROR: Missing required field 'name' in frontmatter
ERROR: Invalid YAML frontmatter
```

### 2. Security Validator (`run_security_checks.py`)

**Purpose**: Detects security vulnerabilities and unsafe patterns

**Security Checks**:

#### Rule 1: Untrusted Data Detection

Identifies potential sources of untrusted data:

- Subprocess execution patterns
- File read/write operations
- API calls and network requests
- Git data extraction
- User input handling

**Example Issue**:

```
⚠️ [HIGH] Untrusted Data Sources Detected
   Found untrusted data sources: subprocess, file_read
   Remediation: Verify all untrusted data is sanitized before use
```

#### Rule 2: Sanitization Verification

Checks if untrusted data is properly validated/escaped:

- Searches for sanitization functions
- Verifies input validation patterns
- Detects missing protections

**Example Issue**:

```
🚨 [CRITICAL] Untrusted Data Without Sanitization
   Untrusted data sources found but no sanitization functions detected
   Remediation: Add sanitization functions to validate/escape all untrusted data before use
```

#### Rule 3: High-Privilege Operations

Detects operations requiring special care:

- File deletion/modification
- Shell command execution
- Git repository operations
- Process management

**Example Issue**:

```
⚠️ [HIGH] High-Privilege Operation: file_removal
   File removal operation detected - requires user confirmation
   Remediation: Ensure human confirmation before executing this operation
```

#### Rule 4: Injection Vulnerabilities

Detects injection attack risks:

- **Prompt Injection**: Skill description suggests prompt concatenation without escaping
- **Shell Injection**: Subprocess execution with unsanitized input
- **SQL Injection**: Database queries with untrusted input
- **Code Injection**: eval/exec with user input

**Example Issue**:

```
🚨 [CRITICAL] Prompt Injection Vulnerability
   Skill description mentions unsafe prompt concatenation
   Remediation: Always escape user input before including in prompts
```

#### Rule 5: Error Handling

Checks for comprehensive error handling:

- try/except blocks around dangerous operations
- Proper exception logging
- No sensitive data exposure in errors

**Example Issue**:

```
⚠️ [HIGH] Missing Error Handling
   No try/except blocks found for external operations
   Remediation: Add try/except blocks around subprocess, file, and API operations
```

#### Rule 6: Secrets Protection

Verifies credentials aren't hardcoded:

- API keys, tokens, passwords
- Database connection strings
- Private URLs

**Example Issue**:

```
🚨 [CRITICAL] Hardcoded Secrets Found
   Found hardcoded API key or password
   Remediation: Use environment variables or secure vaults instead
```

**Running Security Validation**:

```bash
python run_security_checks.py /path/to/skill

# With detailed output
python run_security_checks.py /path/to/skill --verbose

# Save report
python run_security_checks.py /path/to/skill --output report.json
```

**Report Format**:

```json
{
  "skill_name": "brainstorming-partner",
  "passed": false,
  "critical": 1,
  "high": 8,
  "medium": 3,
  "low": 0,
  "total": 12,
  "md_audit": {...},
  "script_audits": {...}
}
```

### 3. Eval Loop Validator (`run_skill_evals.py`)

**Purpose**: Tests skill triggering effectiveness with sample queries

**How It Works**:

1. Reads test queries from `evals/evals.json`
1. Creates temporary skill copies for testing
1. Runs OpenCode CLI with each query
1. Detects skill triggering in response
1. Calculates trigger rate statistics

**Query Format** (`evals/evals.json`):

```json
{
  "evals": [
    {
      "id": "eval-1",
      "name": "Feature Brainstorm",
      "prompt": "Brainstorm innovative features for a mobile app",
      "category": "feature_ideation"
    }
  ]
}
```

**Running Eval Tests**:

```bash
# Basic eval run
python run_skill_evals.py /path/to/skill

# With custom model
python run_skill_evals.py /path/to/skill --model claude-opus/claude-3-5-sonnet

# Multiple runs per query for reliability
python run_skill_evals.py /path/to/skill --runs-per-query 3

# Adjust trigger threshold
python run_skill_evals.py /path/to/skill --trigger-threshold 0.8

# Save results
python run_skill_evals.py /path/to/skill --output eval_results.json
```

**Report Format**:

```json
{
  "skill_name": "brainstorming-partner",
  "passed": true,
  "trigger_threshold": 0.5,
  "trigger_rate": 0.85,
  "successful_triggers": 17,
  "total_runs": 20,
  "total_queries": 10,
  "results": [
    {
      "id": "eval-1",
      "name": "Feature Brainstorm",
      "query": "Brainstorm innovative features...",
      "trigger_rate": 1.0,
      "runs": 2,
      "triggered": 2
    }
  ]
}
```

### 4. Unified Validator (`validator.py`)

**Purpose**: Orchestrates all validation checks and aggregates results

**Features**:

- Runs structure, security, and eval checks in sequence
- Aggregates results into comprehensive report
- Provides clear pass/fail status
- Generates JSON export for CI/CD integration

**Running Unified Validation**:

```bash
# Full validation (structure + security + evals)
python validator.py /path/to/skill

# Skip evals (faster for development)
python validator.py /path/to/skill --skip-evals

# Verbose output
python validator.py /path/to/skill --verbose

# Export detailed report
python validator.py /path/to/skill --output validation_report.json
```

**Report Structure**:

```json
{
  "summary": {
    "skill_name": "brainstorming-partner",
    "overall_passed": false,
    "checks_run": 3,
    "checks_passed": 1,
    "checks_failed": 2,
    "validation_types": {
      "structure": true,
      "security": true,
      "evals": true
    }
  },
  "checks": {
    "structure": [
      {
        "name": "Structure Validation",
        "passed": true,
        "details": {...}
      }
    ],
    "security": [
      {
        "name": "Security Validation",
        "passed": false,
        "details": {
          "critical": 1,
          "high": 8,
          "medium": 3
        }
      }
    ],
    "evals": [...]
  }
}
```

## Testing with Brainstorming-Partner

### Example: Running Full Validation

```bash
cd /workspaces/vibe-coding-template/.agents/skills/skill-validator/scripts

# Full validation with output
python validator.py \
  /workspaces/vibe-coding-template/.agents/skills/brainstorming-partner \
  --output /tmp/brainstorm_validation.json \
  --verbose
```

### Example Results

```
🔍 Validating skill: brainstorming-partner
📁 Path: /workspaces/vibe-coding-template/.agents/skills/brainstorming-partner

1️⃣  Running structure validation...
✅ Structure Validation: PASSED

2️⃣  Running security validation...
❌ Security Validation: FAILED
   ❌ Found 1 critical issues

3️⃣  Running eval validation...
⏭️  Skipping eval validation (no evals file found)

======================================================================
Validation Summary
======================================================================
Skill: brainstorming-partner
Status: ❌ SOME FAILED
Checks: 1/2 passed
======================================================================

💾 Detailed results saved to /tmp/brainstorm_validation.json
```

## Security Test Cases

The validator includes comprehensive security test cases in `tests/security_test_cases.json`:

1. **Secure Skill** - No security concerns
1. **Unsafe Subprocess** - Shell injection vulnerability
1. **Unsafe File Read** - Path traversal risk
1. **Unsafe API** - Hardcoded credentials
1. **Unsafe Git** - Unsanitized git data in commands
1. **Missing Error Handling** - Multiple unhandled exceptions
1. **Prompt Injection** - Vulnerable to prompt injection
1. **Partial Sanitization** - Incomplete input validation
1. **Safe with Warnings** - Generally safe implementation
1. **Unsafe os.system** - Direct command execution
1. **Unsafe eval()** - Arbitrary code execution

Each test case includes:

- `id`: Unique identifier
- `name`: Human-readable name
- `skill_content`: Sample skill SKILL.md content
- `expected_passed`: Whether it should pass validation
- `expected_issues`: Number of issues expected
- `expected_severity`: Severity level if it fails
- `description`: What the test demonstrates

### Running Security Tests

```bash
# Test a specific security case
python -c "
from security_audit import SecurityAuditor
import json

with open('tests/security_test_cases.json') as f:
    cases = json.load(f)['security_test_cases']

auditor = SecurityAuditor()
for case in cases[:2]:  # Test first 2 cases
    result = auditor.audit(case['skill_content'])
    print(f'{case[\"name\"]}: {result.passed}')
"
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Validate skills
        run: |
          cd .agents/skills/skill-validator/scripts
          python validator.py ../../skill-name --output report.json

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: report.json
```

### Script Example

```bash
#!/bin/bash
# Validate all skills

VALIDATOR_DIR=".agents/skills/skill-validator/scripts"
SKILLS_DIR=".agents/skills"

for skill_dir in $SKILLS_DIR/*; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        echo "Validating: $skill_name"

        python "$VALIDATOR_DIR/validator.py" "$skill_dir" \
            --output "reports/$skill_name-validation.json" \
            --skip-evals

        if [ $? -ne 0 ]; then
            echo "❌ $skill_name failed validation"
            exit 1
        fi
    fi
done

echo "✅ All skills validated successfully"
```

## Troubleshooting

### Structure Validation Issues

**Error**: "Missing SKILL.md file"

- **Solution**: Create a SKILL.md file with proper frontmatter

**Error**: "Missing required field 'name'"

- **Solution**: Add `name: your-skill-name` to frontmatter

### Security Validation Issues

**Critical Issue**: "Untrusted Data Without Sanitization"

- **Problem**: Using subprocess/files/API without input validation
- **Solution**: Add sanitization functions and validate all user input

**Critical Issue**: "Hardcoded Secrets Found"

- **Problem**: API keys, passwords in code
- **Solution**: Use environment variables or secret management

**High Issue**: "Missing Error Handling"

- **Problem**: No try/except blocks around dangerous operations
- **Solution**: Add comprehensive error handling

### Eval Validation Issues

**Error**: "No evals file found"

- **Solution**: Create `evals/evals.json` with test queries

**Warning**: "Trigger rate below threshold"

- **Problem**: Skill not being triggered for test queries
- **Solution**: Improve skill description to better match test queries

**Error**: "OpenCode command failed"

- **Solution**: Ensure OpenCode CLI is installed and in PATH

## Performance Notes

- **Structure validation**: \< 1 second
- **Security validation**: 5-10 seconds (depends on code size)
- **Eval validation**: 30-300 seconds (depends on queries and timeout)
- **Full validation**: 40-320 seconds

Use `--skip-evals` for faster feedback during development.

## File Structure

```
.agents/skills/skill-validator/
├── SKILL.md                          # Main skill documentation
├── scripts/
│   ├── validator.py                  # Unified validator orchestrator
│   ├── quick_validate.py             # Structure validator
│   ├── run_security_checks.py        # Security validator
│   ├── run_skill_evals.py           # Eval loop validator
│   ├── security_audit.py             # Security detection engine
│   └── SECURITY_AUDIT_GUIDE.md       # Security audit documentation
└── tests/
    └── security_test_cases.json      # Comprehensive test cases
```

## Contributing

To extend the validator:

1. **Add new security checks**: Modify `security_audit.py` to add new detection patterns
1. **Add new structure checks**: Extend `quick_validate.py` with additional validations
1. **Add eval templates**: Create example evals JSON files in skill directories
1. **Test thoroughly**: Use `tests/security_test_cases.json` as reference

## References

- [Security Audit Guide](scripts/SECURITY_AUDIT_GUIDE.md)
- [Brainstorming Partner Skill](../brainstorming-partner/SKILL.md)
- [OpenCode CLI Documentation](https://opencode.ai/docs)
  """

if __name__ == "__main__":
print(VALIDATOR_DOCUMENTATION)
