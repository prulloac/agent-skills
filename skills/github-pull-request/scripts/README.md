# Sanitizer Scripts

This directory contains three production-ready implementations of the git data sanitizer to protect the github-pull-request skill against prompt injection attacks.

## Available Scripts

### git_sanitizer.py
**Language:** Python 3
**Status:** Production-ready ✅
**Dependencies:** Standard library only

Main class: `GitDataSanitizer`

Usage:
```python
from git_sanitizer import GitDataSanitizer

sanitizer = GitDataSanitizer()
result = sanitizer.sanitize_commit_message("Your message here")
print(result['content'])
print(result['is_suspicious'])
```

Features:
- Sanitize commit messages
- Extract safe diff statistics
- Get commit summaries
- Detect comprehensive red flags
- Format safety reports

See: `../references/SANITIZER_USAGE.md` for complete API

---

### git_sanitizer.sh
**Language:** Bash
**Status:** Production-ready ✅
**Dependencies:** bash, git, jq

Main functions:
- `sanitize_commit_message`
- `extract_safe_diff_stats`
- `get_commit_summary`
- `detect_red_flags`
- `format_safety_report`
- `run_security_check`

Usage:
```bash
source git_sanitizer.sh

# Sanitize a message
result=$(sanitize_commit_message "Your message")

# Extract diff stats
stats=$(extract_safe_diff_stats main feature-branch)

# Run complete check
./git_sanitizer.sh main feature-branch
```

Features:
- JSON output for easy parsing
- Verbose mode support (`VERBOSE=1`)
- All functions exported for sourcing
- Self-contained, no dependencies beyond bash

See: `../references/SANITIZER_USAGE.md` for complete API

---

### git_sanitizer.js
**Language:** JavaScript (Node.js)
**Status:** Production-ready ✅
**Dependencies:** Node.js built-ins only

Main class: `GitDataSanitizer`

Usage:
```javascript
const { GitDataSanitizer } = require('./git_sanitizer.js');

const sanitizer = new GitDataSanitizer({ verbose: true });
const result = sanitizer.sanitizeCommitMessage("Your message");
console.log(JSON.stringify(result, null, 2));
```

Features:
- Comprehensive pattern detection
- Modular class design
- Logging support
- Error handling with timeouts
- JSON output

See: `../references/SANITIZER_USAGE.md` for complete API

---

## Quick Start

### Python
```bash
cd /path/to/script
python3 git_sanitizer.py
# Or import as module
python3 -c "
from git_sanitizer import GitDataSanitizer
s = GitDataSanitizer()
print(s.sanitize_commit_message('Fix: [SYSTEM: test] msg'))
"
```

### Bash
```bash
cd /path/to/script
source git_sanitizer.sh
sanitize_commit_message "Your message"
# Or run standalone
./git_sanitizer.sh main feature-branch
```

### Node.js
```bash
cd /path/to/script
node git_sanitizer.js main feature-branch
# Or use as module
node -e "
const { GitDataSanitizer } = require('./git_sanitizer.js');
const s = new GitDataSanitizer();
console.log(s.sanitizeCommitMessage('Your message'));
"
```

---

## Pattern Detection

All three sanitizers detect the same 8 injection patterns:

1. **system_instruction** - `[SYSTEM: ...]` directives
2. **ignore_directive** - `[IGNORE]` instructions
3. **override_directive** - `[BYPASS]`, `[OVERRIDE]` attempts
4. **html_comment_injection** - `<!-- SYSTEM: ... -->`
5. **yaml_injection** - YAML-format instructions
6. **markdown_comment** - Markdown comment injection
7. **template_literal** - `{{ ... }}` template injection
8. **jinja_injection** - `{% ... %}` template injection

Plus detection of 12+ suspicious keywords like:
- AUTO-APPROVE
- SKIP VALIDATION
- NEVER REVIEW
- FORCE MERGE
- etc.

---

## Output Format

All scripts output JSON for easy parsing:

### Python (dict-like)
```python
{
    'content': 'Sanitized message',
    'is_suspicious': True,
    'red_flags': ['system_instruction'],
    'original_length': 50,
    'sanitized_length': 30
}
```

### Bash (JSON)
```json
{
  "content": "Sanitized message",
  "is_suspicious": true,
  "red_flags": ["system_instruction"],
  "original_length": 50,
  "sanitized_length": 30
}
```

### Node.js (object)
```javascript
{
  content: 'Sanitized message',
  isSuspicious: true,
  redFlags: ['systemInstruction'],
  originalLength: 50,
  sanitizedLength: 30
}
```

---

## Configuration

### Python
```python
sanitizer = GitDataSanitizer(
    max_commit_length=300,      # Max length before truncation
    max_diff_lines=5000         # Max lines from diffs
)
```

### Bash
Edit at top of script:
```bash
MAX_COMMIT_LENGTH=300
MAX_DIFF_LINES=5000
VERBOSE=0  # Set to 1 for verbose logging
```

### Node.js
```javascript
const sanitizer = new GitDataSanitizer({
    maxCommitLength: 300,
    maxDiffLines: 5000,
    verbose: false
});
```

---

## Testing

Each script can be run directly to see example output:

```bash
# Python
python3 git_sanitizer.py

# Bash
./git_sanitizer.sh main HEAD

# Node.js
./git_sanitizer.js main HEAD
```

---

## Integration

### For Python Agents
```python
import sys
sys.path.insert(0, '/path/to/scripts')
from git_sanitizer import GitDataSanitizer

sanitizer = GitDataSanitizer()
# Use in your workflow...
```

### For Bash Scripts
```bash
source /path/to/scripts/git_sanitizer.sh

# Use functions:
result=$(sanitize_commit_message "$msg")
```

### For Node.js
```javascript
const { GitDataSanitizer } = require('/path/to/scripts/git_sanitizer.js');

const sanitizer = new GitDataSanitizer();
// Use in your workflow...
```

---

## Performance

Typical execution times:

| Operation | Time |
|-----------|------|
| Sanitize message | < 1ms |
| Extract diff stats (10 files) | 5-10ms |
| Get commit summary (10 commits) | 20-50ms |
| Full security check | 50-100ms |

All operations include timeouts to prevent hanging on large repositories.

---

## Error Handling

### Python
All methods return structured results even on error:
```python
result = sanitizer.extract_safe_diff_stats('main', 'bad-branch')
if 'error' in result:
    print(f"Error: {result['error']}")
```

### Bash
Errors are logged and safe defaults returned:
```bash
result=$(extract_safe_diff_stats 'main' 'bad-branch')
# Will return valid JSON with error field if command fails
```

### Node.js
Built-in error handling with try-catch and timeouts:
```javascript
try {
    const result = sanitizer.extractSafeDiffStats('main', 'HEAD');
} catch (error) {
    console.error(`Error: ${error.message}`);
}
```

---

## Maintenance

### Adding New Patterns

**Python:** Update `INJECTION_PATTERNS` dict in `GitDataSanitizer` class

**Bash:** Update `INJECTION_MARKERS` array at top of script

**Node.js:** Update `injectionPatterns` object in `GitDataSanitizer` class

### Adding New Keywords

**Python:** Update `SUSPICIOUS_KEYWORDS` list in `GitDataSanitizer` class

**Bash:** Update `SUSPICIOUS_KEYWORDS` array in script

**Node.js:** Update `suspiciousKeywords` array in `GitDataSanitizer` class

---

## Related Documentation

- `../references/SANITIZER_USAGE.md` - Complete API documentation
- `../references/SANITIZATION_GUIDE.md` - Implementation patterns
- `../references/SECURITY_REMEDIATION_SUMMARY.md` - Overview of fix
- `../references/INTEGRATION_EXAMPLE.py` - Full workflow example

---

## License

These scripts are part of the agent-skills repository and follow the same license.
