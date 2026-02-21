#!/usr/bin/env python3
"""
GitHub Issue Creator

Creates GitHub issues with intelligent tool selection (MCP Server → gh CLI → REST API)
and optional template matching from .github/ISSUE_TEMPLATE directory.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Import template matcher from same directory
sys.path.insert(0, str(Path(__file__).parent))
from template_matcher import TemplateMatcher


class ToolAvailability(Enum):
    """Available tools for issue creation."""
    MCP_SERVER = "mcp"      # GitHub MCP Server (requires MCP context)
    GH_CLI = "gh"           # GitHub CLI (gh command)
    REST_API = "api"        # GitHub REST API (requires auth token)


@dataclass
class IssueData:
    """Data for creating a GitHub issue."""
    title: str
    body: str
    labels: Optional[List[str]] = None
    assignees: Optional[List[str]] = None
    milestone: Optional[str] = None
    project: Optional[str] = None
    template_file: Optional[str] = None


class GitHubIssueCreator:
    """Create GitHub issues using best available tool."""
    
    def __init__(self, repo_path: Optional[str] = None):
        """Initialize issue creator.
        
        Args:
            repo_path: Path to repository root. Defaults to current directory.
        """
        self.repo_path = Path(repo_path or ".")
        self.repo_owner = None
        self.repo_name = None
        self._detect_repository()
    
    def _detect_repository(self) -> None:
        """Detect repository owner and name from git config."""
        try:
            # Get remote URL
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            remote_url = result.stdout.strip()
            
            if not remote_url:
                return
            
            # Parse owner/repo from URL (handles both https and ssh)
            # https://github.com/owner/repo.git or git@github.com:owner/repo.git
            if "github.com" in remote_url:
                parts = remote_url.split("github.com")[1].replace(".git", "").strip("/:").split("/")
                if len(parts) >= 2:
                    self.repo_owner = parts[0]
                    self.repo_name = parts[1]
        except Exception:
            pass
    
    def detect_available_tools(self) -> List[ToolAvailability]:
        """Detect which tools are available for issue creation.
        
        Returns:
            List of available tools in order of precedence.
        """
        available = []
        
        # Check for MCP Server (would need to be checked in context, for now assume available if we're in an MCP context)
        # This would be detected by Claude when using the skill
        
        # Check for gh CLI
        try:
            result = subprocess.run(["gh", "--version"], capture_output=True, timeout=2)
            if result.returncode == 0:
                available.append(ToolAvailability.GH_CLI)
        except Exception:
            pass
        
        # Check for REST API authentication
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if token:
            available.append(ToolAvailability.REST_API)
        
        return available
    
    def create_issue_with_gh_cli(self, issue: IssueData) -> Dict:
        """Create issue using GitHub CLI (gh).
        
        Args:
            issue: IssueData object with issue information
            
        Returns:
            Dict with status and result or error info
        """
        try:
            cmd = ["gh", "issue", "create"]
            cmd.extend(["--title", issue.title])
            cmd.extend(["--body", issue.body])
            
            if issue.labels:
                cmd.extend(["--label", ",".join(issue.labels)])
            
            if issue.assignees:
                cmd.extend(["--assignee", ",".join(issue.assignees)])
            
            if issue.milestone:
                cmd.extend(["--milestone", issue.milestone])
            
            # Note: --project requires additional setup, so we'll skip it for CLI
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse issue URL from output
                output = result.stdout.strip()
                return {"success": True, "output": output, "tool": "gh"}
            else:
                return {"success": False, "error": result.stderr, "tool": "gh"}
        
        except Exception as e:
            return {"success": False, "error": str(e), "tool": "gh"}
    
    def create_issue_with_rest_api(self, issue: IssueData) -> Dict:
        """Create issue using GitHub REST API.
        
        Args:
            issue: IssueData object with issue information
            
        Returns:
            Dict with status and result or error info
        """
        try:
            import requests
        except ImportError:
            return {"success": False, "error": "requests library not installed", "tool": "api"}
        
        if not self.repo_owner or not self.repo_name:
            return {"success": False, "error": "Could not determine repository", "tool": "api"}
        
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if not token:
            return {"success": False, "error": "GITHUB_TOKEN not set", "tool": "api"}
        
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            payload: Dict = {
                "title": issue.title,
                "body": issue.body
            }
            
            if issue.labels:
                payload["labels"] = issue.labels  # type: ignore
            
            if issue.assignees:
                payload["assignees"] = issue.assignees  # type: ignore
            
            if issue.milestone:
                payload["milestone"] = issue.milestone
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in (200, 201):
                data = response.json()
                return {"success": True, "output": data.get("html_url"), "tool": "api"}
            else:
                return {"success": False, "error": response.text, "tool": "api"}
        
        except Exception as e:
            return {"success": False, "error": str(e), "tool": "api"}
    
    def create_issue(self, issue: IssueData, preferred_tool: Optional[str] = None) -> Dict:
        """Create a GitHub issue using best available tool.
        
        Args:
            issue: IssueData object with issue information
            preferred_tool: Optionally force a specific tool ("gh" or "api")
            
        Returns:
            Dict with status, output, and tool used
        """
        available = self.detect_available_tools()
        
        if preferred_tool:
            if preferred_tool == "gh" and ToolAvailability.GH_CLI in available:
                return self.create_issue_with_gh_cli(issue)
            elif preferred_tool == "api" and ToolAvailability.REST_API in available:
                return self.create_issue_with_rest_api(issue)
        
        # Try tools in order of precedence
        for tool in available:
            if tool == ToolAvailability.GH_CLI:
                result = self.create_issue_with_gh_cli(issue)
                if result["success"]:
                    return result
            elif tool == ToolAvailability.REST_API:
                result = self.create_issue_with_rest_api(issue)
                if result["success"]:
                    return result
        
        return {"success": False, "error": "No tools available for issue creation"}
    
    def load_template_content(self, template_path: str) -> str:
        """Load content from a template file.
        
        Args:
            template_path: Path to template file
            
        Returns:
            Template content as string
        """
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            return f"Error loading template: {e}"


def main():
    """CLI interface for issue creation."""
    if len(sys.argv) < 3:
        print("Usage: issue_creator.py <title> <body> [--labels LABELS] [--assignees ASSIGNEES] [--milestone MILESTONE]")
        sys.exit(1)
    
    title = sys.argv[1]
    body = sys.argv[2]
    
    # Parse optional arguments
    labels = None
    assignees = None
    milestone = None
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--labels" and i + 1 < len(sys.argv):
            labels = sys.argv[i + 1].split(",")
            i += 2
        elif sys.argv[i] == "--assignees" and i + 1 < len(sys.argv):
            assignees = sys.argv[i + 1].split(",")
            i += 2
        elif sys.argv[i] == "--milestone" and i + 1 < len(sys.argv):
            milestone = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    creator = GitHubIssueCreator()
    issue = IssueData(title=title, body=body, labels=labels, assignees=assignees, milestone=milestone)
    
    result = creator.create_issue(issue)
    # Output as simple text format
    if result["success"]:
        print(f"SUCCESS: Issue created")
        print(f"Output: {result.get('output', 'N/A')}")
        print(f"Tool: {result.get('tool', 'N/A')}")
    else:
        print(f"FAILED: {result.get('error', 'Unknown error')}")
        print(f"Tool: {result.get('tool', 'N/A')}")


if __name__ == "__main__":
    main()
