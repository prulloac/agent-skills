# Skill Validator Scripts

This directory contains executable scripts that enhance the skill validation process.

## Available Scripts

### `security_audit.py`
Automated security vulnerability scanner for agent skills.

**Purpose:** Detect common security issues in skills before production deployment.

**Usage:**
```bash
python3 security_audit.py /path/to/SKILL.md
```

**Features:**
- Rule 1: Untrusted Data Detection
- Rule 2: Sanitization Requirement Verification
- Rule 3: High-Privilege Operation Detection
- Rule 4: Injection Risk Analysis
- Rule 5: Error Handling Completeness
- Rule 6: Secrets Protection Checking

**Output:**
- Formatted security report with categorized issues
- Exit code 0 if passed, 1 if failed

**Documentation:**
See `SECURITY_AUDIT_GUIDE.md` for comprehensive guide, examples, and troubleshooting.

## Integration

These scripts are automatically called during the skill validation process. They can also be run independently for quick security checks.

## Example Commands

```bash
# Audit a specific skill
python3 security_audit.py ../../.agents/skills/github-pull-request/SKILL.md

# Audit multiple skills
for skill in ../../.agents/skills/*/SKILL.md; do
    echo "Checking: $skill"
    python3 security_audit.py "$skill"
done

# Check exit code
python3 security_audit.py /path/to/SKILL.md
if [ $? -eq 0 ]; then
    echo "Security check passed!"
else
    echo "Security issues detected"
fi
```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Contributing

When adding new security rules:
1. Add detection logic to `SecurityAuditor` class
2. Document the rule in this README
3. Add tests for common patterns
4. Update `SECURITY_AUDIT_GUIDE.md` with examples
