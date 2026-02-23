#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version

No external dependencies. Uses a simple frontmatter parser instead of PyYAML
since skill frontmatter only contains simple key: value pairs.
"""

import sys
import re
from pathlib import Path


def parse_frontmatter(text):
    """
    Parse simple YAML frontmatter (key: value pairs) without external dependencies.

    Handles:
    - Simple scalars: name: my-skill
    - Quoted strings: description: "my description"
    - Multi-line folded strings using trailing whitespace continuation
    - Blank/comment-only lines

    Does NOT handle nested objects, lists, anchors, or other advanced YAML.
    This is intentional -- skill frontmatter should only use simple key-value pairs.

    Returns:
        dict of parsed key-value pairs

    Raises:
        ValueError on parse errors
    """
    result = {}
    current_key = None
    current_value_lines = []

    def _flush():
        nonlocal current_key, current_value_lines
        if current_key is not None:
            raw = ' '.join(current_value_lines)
            # Strip matching quotes
            if len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
                raw = raw[1:-1]
            result[current_key] = raw
            current_key = None
            current_value_lines = []

    for line in text.splitlines():
        stripped = line.strip()
        # Skip blank lines and comments
        if not stripped or stripped.startswith('#'):
            continue

        # Continuation line (starts with whitespace and we have a current key)
        if line[0] in (' ', '\t') and current_key is not None:
            current_value_lines.append(stripped)
            continue

        # New key: value pair
        colon_pos = line.find(':')
        if colon_pos == -1:
            raise ValueError(f"Expected 'key: value' but got: {line}")

        _flush()
        current_key = line[:colon_pos].strip()
        value_part = line[colon_pos + 1:].strip()
        if value_part:
            current_value_lines.append(value_part)

    _flush()
    return result


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse frontmatter
    try:
        frontmatter = parse_frontmatter(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except ValueError as e:
        return False, f"Invalid frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)