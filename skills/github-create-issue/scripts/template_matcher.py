#!/usr/bin/env python3
"""
Template Matcher for GitHub Issues

Intelligently detects and matches issue templates from .github/ISSUE_TEMPLATE directory.
Supports .md and .yml/.yaml formats with fuzzy matching on template names and content.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple

try:
    import yaml
except ImportError:
    yaml = None


class TemplateMatcher:
    """Detect and match GitHub issue templates intelligently."""
    
    TEMPLATE_DIR = ".github/ISSUE_TEMPLATE"
    SUPPORTED_EXTENSIONS = {".md", ".yml", ".yaml"}
    
    def __init__(self, repo_root: Optional[str] = None):
        """Initialize template matcher in a repository.
        
        Args:
            repo_root: Path to repository root. Defaults to current directory.
        """
        self.repo_root = Path(repo_root or ".")
        self.template_dir = self.repo_root / self.TEMPLATE_DIR
    
    def find_templates(self) -> List[Dict[str, str]]:
        """Find all available issue templates.
        
        Returns:
            List of template dicts with keys: name, path, ext, content
        """
        templates = []
        
        if not self.template_dir.exists():
            return templates
        
        for template_file in sorted(self.template_dir.iterdir()):
            if template_file.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    content = template_file.read_text(encoding="utf-8")
                    templates.append({
                        "name": template_file.stem,
                        "path": str(template_file),
                        "ext": template_file.suffix.lower(),
                        "content": content
                    })
                except (IOError, UnicodeDecodeError):
                    pass
        
        return templates
    
    def extract_title(self, template: Dict[str, str]) -> Optional[str]:
        """Extract display title from template.
        
        For YAML templates, looks for 'name' field.
        For Markdown, extracts first heading or uses filename.
        
        Args:
            template: Template dictionary with content
            
        Returns:
            Display title or None
        """
        content = template["content"]
        
        if template["ext"] in {".yml", ".yaml"}:
            try:
                if yaml:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict) and "name" in data:
                        return data["name"]
            except:
                pass
        
        # Try to find first markdown heading
        match = re.search(r"^#+\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Fall back to filename
        return template["name"].replace("-", " ").replace("_", " ").title()
    
    def extract_keywords(self, template: Dict[str, str]) -> List[str]:
        """Extract keywords from template name and metadata.
        
        Extracts meaningful words from template filename and YAML metadata
        that describe what this template is for.
        
        Args:
            template: Template dictionary with content
            
        Returns:
            List of lowercase keywords found in template
        """
        keywords = []
        content = template["content"].lower()
        filename = template["name"].lower()
        
        # Extract words from filename (split on -, _, spaces)
        # Remove common words that don't add meaning
        filename_words = re.split(r'[-_\s]+', filename)
        common_words = {"form", "template", "issue", "report", "request", "new"}
        
        for word in filename_words:
            if word and len(word) > 1 and word not in common_words:
                keywords.append(word)
        
        # Extract metadata from YAML if present
        try:
            if template["ext"] in {".yml", ".yaml"} and yaml:
                data = yaml.safe_load(content)
                if isinstance(data, dict):
                    # Get name field
                    if "name" in data:
                        name_words = re.split(r'[-_\s]+', str(data["name"]).lower())
                        for word in name_words:
                            if word and len(word) > 1 and word not in common_words and word not in keywords:
                                keywords.append(word)
                    
                    # Get description field and extract key terms
                    if "description" in data:
                        desc = str(data["description"]).lower()
                        desc_words = re.split(r'[-_\s]+', desc)
                        for word in desc_words:
                            if word and len(word) > 1 and word not in common_words and word not in keywords:
                                keywords.append(word)
        except Exception:
            pass
        
        # Also extract from first heading in markdown
        if template["ext"] == ".md":
            match = re.search(r"^#+\s+(.+)$", content, re.MULTILINE)
            if match:
                heading = match.group(1).lower()
                heading_words = re.split(r'[-_\s]+', heading)
                for word in heading_words:
                    if word and len(word) > 1 and word not in common_words and word not in keywords:
                        keywords.append(word)
        
        return list(set(keywords))
    
    def match_templates(self, issue_description: str) -> Tuple[List[Dict], Dict]:
        """Match templates to a user's issue description based on template metadata.
        
        Scores templates by matching their keywords and names against the user's
        issue description. This allows matching any template type, not just
        predefined issue categories.
        
        Args:
            issue_description: User's issue title or description
            
        Returns:
            Tuple of (ranked_templates, match_details)
            - ranked_templates: List sorted by match score (highest first)
            - match_details: Dict with scoring info for debugging
        """
        templates = self.find_templates()
        if not templates:
            return [], {"error": "No templates found"}
        
        issue_words = set(issue_description.lower().split())
        scored_matches = []
        
        for template in templates:
            keywords = self.extract_keywords(template)
            title = self.extract_title(template)
            
            # Calculate match score based on keyword overlap
            # Keywords come from template metadata/name, not from hardcoded categories
            score = 0
            matched_keywords = []
            
            # Score template keywords that appear in issue description
            for keyword in keywords:
                keyword_words = set(keyword.split())
                if keyword_words & issue_words:
                    score += 5
                    matched_keywords.append(keyword)
            
            # Bonus if template name/title matches closely
            template_name_words = set(template["name"].lower().split("-"))
            if template_name_words & issue_words:
                score += 3
            
            # If title is extracted from metadata, give it some weight too
            if title:
                title_words = set(title.lower().split())
                if title_words & issue_words:
                    score += 2
            
            scored_matches.append({
                "score": score,
                "template": template,
                "title": title,
                "keywords": keywords,
                "matched_keywords": matched_keywords
            })
        
        # Sort by score (highest first), then by filename
        ranked = sorted(scored_matches, key=lambda x: (-x["score"], x["template"]["name"]))
        
        # If no matches found (all scores are 0), return all templates sorted by name
        # User should choose manually
        matched_count = len([r for r in ranked if r["score"] > 0])
        
        return ranked, {"total_templates": len(templates), "matched": matched_count}
    
    def format_template_options(self, ranked_templates: List[Dict]) -> str:
        """Format templates for user selection.
        
        Args:
            ranked_templates: Output from match_templates()
            
        Returns:
            Formatted string for displaying options to user
        """
        options = []
        for i, match in enumerate(ranked_templates, 1):
            template = match["template"]
            title = match["title"] or template["name"]
            score_indicator = "★" if match["score"] > 0 else "•"
            options.append(f"{i}. {score_indicator} {title}")
        
        return "\n".join(options)


def main():
    """CLI interface for template matching."""
    if len(sys.argv) < 2:
        print("Usage: template_matcher.py <issue_description> [repo_root]")
        sys.exit(1)
    
    issue_desc = sys.argv[1]
    repo_root = sys.argv[2] if len(sys.argv) > 2 else "."
    
    matcher = TemplateMatcher(repo_root)
    ranked, details = matcher.match_templates(issue_desc)
    
    if not ranked:
        # Output error as simple text
        print("ERROR: No templates found")
        print(f"Details: {details}")
        sys.exit(0)
    
    # Output as simple text format (no json required)
    print("TEMPLATES_FOUND")
    print(f"Total: {details['total_templates']}")
    print(f"Matched: {details['matched']}")
    print("")
    
    for i, m in enumerate(ranked, 1):
        print(f"Template {i}: {m['template']['name']}")
        print(f"  Title: {m['title']}")
        print(f"  Score: {m['score']}")
        print(f"  Keywords: {', '.join(m['keywords'])}")
        print(f"  Matched: {', '.join(m['matched_keywords'])}")
        print("")


if __name__ == "__main__":
    main()
