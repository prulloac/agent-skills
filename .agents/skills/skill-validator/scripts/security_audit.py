#!/usr/bin/env python3
"""
Security Audit Module for Skill Validator

Validates security properties of agent skills by checking for:
1. Untrusted data sources (git, subprocess, files, APIs, user input)
2. Sanitization of untrusted data
3. High-privilege operations (file operations, git operations, shell execution)
4. Injection vulnerabilities (prompt, shell, SQL, code)
5. Error handling completeness
6. Secrets/credentials protection

Usage:
    from security_audit import SecurityAuditor
    auditor = SecurityAuditor()
    results = auditor.audit("path/to/skill")
"""

import re
from typing import Dict, List, Tuple, Any
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "🚨"
    HIGH = "⚠️"
    MEDIUM = "ℹ️"
    LOW = "💡"
    INFO = "ℹ️"


class SecurityIssue:
    """Represents a single security issue found"""
    def __init__(self, rule, severity, title, description, location="", line_number=0, remediation="", example=""):
        self.rule = rule
        self.severity = severity
        self.title = title
        self.description = description
        self.location = location
        self.line_number = line_number
        self.remediation = remediation
        self.example = example


class SecurityAuditResult:
    """Complete security audit result"""
    def __init__(self, skill_path, passed=False):
        self.skill_path = skill_path
        self.passed = passed
        self.issues = []
        self.findings = {}
    
    def critical_count(self):
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
    
    def high_count(self):
        return sum(1 for i in self.issues if i.severity == Severity.HIGH)
    
    def medium_count(self):
        return sum(1 for i in self.issues if i.severity == Severity.MEDIUM)


class SecurityAuditor:
    """Main security audit engine"""
    
    def __init__(self):
        """Initialize security patterns and detection rules"""
        self.untrusted_data_patterns = {
            'subprocess': {
                'patterns': [
                    r'subprocess\.',
                    r'spawnSync',
                    r'execSync',
                    r'Popen',
                    r'os\.system',
                    r'os\.popen',
                ],
                'severity': Severity.CRITICAL,
                'description': 'Subprocess execution detected - verify input sanitization'
            },
            'file_read': {
                'patterns': [
                    r'open\(',
                    r'readFile',
                    r'read_file',
                    r'fs\.read',
                    r'pathlib\.Path\(.*\)\.read',
                ],
                'severity': Severity.HIGH,
                'description': 'File read operation detected - verify content validation'
            },
            'api_call': {
                'patterns': [
                    r'requests\.',
                    r'fetch\(',
                    r'curl',
                    r'axios',
                    r'urllib\.request',
                ],
                'severity': Severity.HIGH,
                'description': 'API call detected - verify response validation'
            },
            'git_data': {
                'patterns': [
                    r'git\s+log',
                    r'git\s+diff',
                    r'git\s+show',
                    r'git\s+blame',
                    r'subprocess.*git',
                ],
                'severity': Severity.CRITICAL,
                'description': 'Git data extraction detected - HIGH RISK for prompt injection'
            },
            'user_input': {
                'patterns': [
                    r'\buser\b.*input',
                    r'argument',
                    r'parameter',
                    r'sys\.argv',
                    r'argparse',
                ],
                'severity': Severity.HIGH,
                'description': 'User input detected - verify validation'
            }
        }
        
        self.sanitization_keywords = [
            'sanitize',
            'escape',
            'validate',
            'filter',
            'clean',
            'strip',
            'trim',
            'escape_html',
            'escape_bash',
            'quote',
            'shlex.quote',
            'html.escape',
            'json.dumps',
        ]
        
        self.high_privilege_ops = {
            'file_delete': {
                'patterns': [r'rm\s', r'unlink', r'delete.*file', r'removeSync', r'truncate'],
                'severity': Severity.CRITICAL,
                'description': 'File deletion detected - requires user confirmation'
            },
            'file_modify': {
                'patterns': [r'chmod', r'chown', r'truncate', r'rename'],
                'severity': Severity.HIGH,
                'description': 'File modification detected - requires validation'
            },
            'git_push': {
                'patterns': [r'git\s+push', r'gh\s+pr\s+create', r'git\s+merge'],
                'severity': Severity.CRITICAL,
                'description': 'Git push/PR creation detected - requires human approval'
            },
            'git_force': {
                'patterns': [r'git\s+push.*--force', r'git\s+reset.*--hard'],
                'severity': Severity.CRITICAL,
                'description': 'Force git operation detected - EXTREMELY high risk'
            },
            'shell_exec': {
                'patterns': [r'system\(', r'exec\(', r'shell\s*=\s*True'],
                'severity': Severity.CRITICAL,
                'description': 'Shell execution detected - use subprocess with list args'
            },
            'file_write': {
                'patterns': [r'open\(.*["\']w["\']', r'writeFile\('],
                'severity': Severity.HIGH,
                'description': 'File write operation detected - verify content validation'
            }
        }
        
        self.injection_patterns = {
            'prompt_injection': {
                'patterns': [
                    r'(prompt|system_message|instructions|message)\s*=\s*[f"\'].*[\${]',
                    r'(LLM|llm|chat).*f["\'].*[\${]',
                    r'\.format\(.*user|\.format\(.*input',
                ],
                'keywords': ['[SYSTEM:', '[IGNORE]', '[BYPASS]', '[OVERRIDE]', 'SKIP VALIDATION'],
                'risk': 'HIGH',
                'description': 'Untrusted data used in LLM prompts - prompt injection risk'
            },
            'shell_injection': {
                'patterns': [
                    r'(subprocess|system|shell)\s*[\(\[].*[f"\'].*[\${]',
                    r'os\.system\(.*[f"\']',
                    r'shell\s*=\s*True.*[\${]',
                ],
                'risk': 'CRITICAL',
                'description': 'Untrusted data in shell command - shell injection risk'
            },
            'sql_injection': {
                'patterns': [
                    r'(query|execute|sql)\s*[\(\[].*[f"\'].*[\${]',
                    r'(SELECT|INSERT|UPDATE|DELETE).*[f"\']',
                ],
                'risk': 'CRITICAL',
                'description': 'Untrusted data in SQL query - SQL injection risk'
            },
            'code_injection': {
                'patterns': [
                    r'eval\s*\(',
                    r'exec\s*\(',
                    r'__import__',
                ],
                'risk': 'CRITICAL',
                'description': 'Code injection detected - eval/exec of untrusted data'
            }
        }
        
        self.suspicious_keywords = {
            'AUTO-APPROVE': Severity.CRITICAL,
            'SKIP VALIDATION': Severity.CRITICAL,
            'SKIP CHECKS': Severity.CRITICAL,
            'DISABLE SECURITY': Severity.CRITICAL,
            'OVERRIDE RULES': Severity.CRITICAL,
            'IGNORE POLICY': Severity.CRITICAL,
            'FORCE MERGE': Severity.HIGH,
            'IMMEDIATE ACTION': Severity.HIGH,
            'URGENT - BYPASS': Severity.CRITICAL,
            'CRITICAL - SKIP': Severity.CRITICAL,
            'SYSTEM:': Severity.CRITICAL,
            'BYPASS': Severity.HIGH,
        }
        
        self.error_handling_keywords = [
            'try',
            'except',
            'catch',
            'error',
            'Exception',
            'fail',
            'handle',
        ]
        
        self.secrets_keywords = [
            'token',
            'api_key',
            'password',
            'secret',
            'credential',
            'auth',
            '.env',
            'os.environ',
            'process.env',
        ]
    
    def audit(self, skill_content: str, skill_path: str = "unknown") -> SecurityAuditResult:
        """
        Run complete security audit on skill content
        
        Args:
            skill_content: Full content of SKILL.md file
            skill_path: Path to skill for reference
            
        Returns:
            SecurityAuditResult with findings and issues
        """
        result = SecurityAuditResult(skill_path=skill_path)
        
        # Run all security checks
        self._check_untrusted_data(skill_content, result)
        self._check_sanitization(skill_content, result)
        self._check_high_privilege_ops(skill_content, result)
        self._check_injection_risks(skill_content, result)
        self._check_error_handling(skill_content, result)
        self._check_secrets_protection(skill_content, result)
        self._check_suspicious_keywords(skill_content, result)
        
        # Determine pass/fail
        result.passed = result.critical_count() == 0
        
        return result
    
    def _check_untrusted_data(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 1: Detect untrusted data sources"""
        found_sources = {}
        
        for source_type, config in self.untrusted_data_patterns.items():
            found = False
            for pattern in config['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    found = True
                    break
            
            if found:
                found_sources[source_type] = True
                result.findings.setdefault('untrusted_data_sources', {})[source_type] = True
        
        if found_sources:
            description = "Found untrusted data sources: " + ", ".join(found_sources.keys())
            result.issues.append(SecurityIssue(
                rule="Rule 1: Untrusted Data Detection",
                severity=Severity.HIGH,
                title="Untrusted Data Sources Detected",
                description=description,
                remediation="Verify all untrusted data is sanitized before use",
            ))
    
    def _check_sanitization(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 2: Verify sanitization of untrusted data"""
        has_sanitization = False
        
        for keyword in self.sanitization_keywords:
            if keyword in content.lower():
                has_sanitization = True
                break
        
        untrusted_found = result.findings.get('untrusted_data_sources', {})
        
        if untrusted_found and not has_sanitization:
            result.issues.append(SecurityIssue(
                rule="Rule 2: Sanitization Requirement",
                severity=Severity.CRITICAL,
                title="Untrusted Data Without Sanitization",
                description="Untrusted data sources found but no sanitization functions detected",
                remediation="Add sanitization functions to validate/escape all untrusted data before use",
                example="Use sanitize_commit_message() or equivalent for git data"
            ))
        elif untrusted_found and has_sanitization:
            result.findings['sanitization_found'] = True
    
    def _check_high_privilege_ops(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 3: Detect high-privilege operations"""
        found_ops = {}
        
        for op_type, config in self.high_privilege_ops.items():
            for pattern in config['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    found_ops[op_type] = config
                    break
        
        for op_type, config in found_ops.items():
            # Check if operation requires human confirmation
            has_confirmation = any(word in content.lower() 
                                  for word in ['confirm', 'approve', 'user', 'check'])
            
            severity = config['severity'] if not has_confirmation else Severity.HIGH
            
            result.issues.append(SecurityIssue(
                rule="Rule 3: High-Privilege Operations",
                severity=severity,
                title=f"High-Privilege Operation: {op_type}",
                description=config['description'],
                remediation="Ensure human confirmation before executing this operation"
            ))
    
    def _check_injection_risks(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 4: Detect injection vulnerabilities"""
        for injection_type, config in self.injection_patterns.items():
            found = False
            for pattern in config['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    found = True
                    break
            
            if found:
                result.issues.append(SecurityIssue(
                    rule="Rule 4: Injection Risk Analysis",
                    severity=Severity.CRITICAL,
                    title=f"{injection_type.replace('_', ' ').title()} Detected",
                    description=config['description'],
                    remediation=f"Review {injection_type} patterns and apply appropriate escaping/validation"
                ))
            
            # Check for suspicious injection keywords
            for keyword in config.get('keywords', []):
                if keyword in content:
                    result.issues.append(SecurityIssue(
                        rule="Rule 4: Injection Risk Analysis",
                        severity=Severity.CRITICAL,
                        title=f"Suspicious Injection Keyword: {keyword}",
                        description=f"Found suspicious keyword '{keyword}' which may indicate prompt injection attack",
                        remediation="Remove or sanitize this keyword from the skill"
                    ))
    
    def _check_error_handling(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 5: Verify error handling completeness"""
        # Check for error handling
        has_try_except = 'try' in content and 'except' in content
        has_timeout = 'timeout' in content.lower()
        
        # Check for sensitive data in errors
        sensitive_error_pattern = r'error.*(?:token|key|password|secret)'
        has_sensitive_errors = re.search(sensitive_error_pattern, content, re.IGNORECASE)
        
        if not has_try_except:
            result.issues.append(SecurityIssue(
                rule="Rule 5: Error Handling Completeness",
                severity=Severity.HIGH,
                title="Missing Error Handling",
                description="No try/except blocks found for external operations",
                remediation="Add try/except blocks around subprocess, file, and API operations"
            ))
        
        if not has_timeout:
            result.issues.append(SecurityIssue(
                rule="Rule 5: Error Handling Completeness",
                severity=Severity.MEDIUM,
                title="No Timeout Protection",
                description="Long-running operations may not have timeout protection",
                remediation="Add timeout parameters to subprocess and API calls"
            ))
        
        if has_sensitive_errors:
            result.issues.append(SecurityIssue(
                rule="Rule 5: Error Handling Completeness",
                severity=Severity.CRITICAL,
                title="Sensitive Data in Error Messages",
                description="Found potential sensitive data (tokens, keys) in error handling",
                remediation="Remove sensitive data from error messages; log securely instead"
            ))
    
    def _check_secrets_protection(self, content: str, result: SecurityAuditResult) -> None:
        """Rule 6: Verify secrets/credentials are protected"""
        # Check for hardcoded credentials
        hardcoded_patterns = [
            r'token\s*=\s*["\'](?!YOUR_|EXAMPLE_|PLACEHOLDER)["\']',
            r'api[_.]?key\s*=\s*["\'](?!YOUR_|EXAMPLE_|PLACEHOLDER)["\']',
            r'password\s*=\s*["\'](?!YOUR_|EXAMPLE_|PLACEHOLDER)["\']',
            r'secret\s*=\s*["\'](?!YOUR_|EXAMPLE_|PLACEHOLDER)["\']',
        ]
        
        has_hardcoded = False
        for pattern in hardcoded_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                has_hardcoded = True
                result.issues.append(SecurityIssue(
                    rule="Rule 6: Secrets Protection",
                    severity=Severity.CRITICAL,
                    title="Hardcoded Credentials Detected",
                    description="Found potential hardcoded credentials in skill content",
                    remediation="Use environment variables or placeholder values (YOUR_TOKEN, EXAMPLE_KEY)"
                ))
        
        # Check for environment variable references
        has_env_reference = any(keyword in content for keyword in ['.env', 'environ', 'getenv', 'process.env'])
        
        has_secrets_mention = any(keyword in content.lower() 
                                 for keyword in ['token', 'api_key', 'password', 'secret', 'credential'])
        
        if has_secrets_mention and not has_env_reference and not has_hardcoded:
            result.findings['secrets_mentioned'] = True
            result.issues.append(SecurityIssue(
                rule="Rule 6: Secrets Protection",
                severity=Severity.MEDIUM,
                title="Secrets Mentioned But .env Not Documented",
                description="Skill mentions credentials/secrets but doesn't reference .env or secrets manager",
                remediation="Add documentation for how secrets should be configured (.env, environment variables, etc.)"
            ))
    
    def _check_suspicious_keywords(self, content: str, result: SecurityAuditResult) -> None:
        """Check for suspicious keywords that indicate attack attempts"""
        for keyword, severity in self.suspicious_keywords.items():
            if keyword in content:
                result.issues.append(SecurityIssue(
                    rule="Security Check: Suspicious Keywords",
                    severity=severity,
                    title=f"Suspicious Keyword Found: {keyword}",
                    description=f"Found suspicious keyword '{keyword}' which may indicate prompt injection or policy bypass",
                    remediation="Review context; sanitize or remove this keyword"
                ))


def format_audit_report(result: SecurityAuditResult) -> str:
    """
    Format security audit result as a readable report
    
    Args:
        result: SecurityAuditResult to format
        
    Returns:
        Formatted report string
    """
    lines = []
    lines.append("═" * 60)
    lines.append("SECURITY AUDIT REPORT")
    lines.append("═" * 60)
    lines.append("")
    lines.append(f"Skill: {result.skill_path}")
    lines.append(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
    lines.append("")
    lines.append("─" * 60)
    lines.append("SUMMARY")
    lines.append("─" * 60)
    lines.append(f"🚨 Critical Issues: {result.critical_count()}")
    lines.append(f"⚠️  High Priority: {result.high_count()}")
    lines.append(f"ℹ️  Medium Priority: {result.medium_count()}")
    lines.append(f"Total Issues: {len(result.issues)}")
    lines.append("")
    
    if result.issues:
        lines.append("─" * 60)
        lines.append("ISSUES DETECTED")
        lines.append("─" * 60)
        
        for issue in result.issues:
            lines.append(f"{issue.severity.value} {issue.title}")
            lines.append(f"   Rule: {issue.rule}")
            lines.append(f"   Description: {issue.description}")
            if issue.remediation:
                lines.append(f"   Remediation: {issue.remediation}")
            if issue.example:
                lines.append(f"   Example: {issue.example}")
            lines.append("")
    else:
        lines.append("✅ No security issues detected!")
        lines.append("")
    
    lines.append("═" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        skill_path = sys.argv[1]
        try:
            with open(skill_path, 'r') as f:
                content = f.read()
            
            auditor = SecurityAuditor()
            result = auditor.audit(content, skill_path)
            report = format_audit_report(result)
            print(report)
            
            sys.exit(0 if result.passed else 1)
        except Exception as e:
            print(f"Error auditing skill: {e}")
            sys.exit(1)
    else:
        print("Usage: python security_audit.py <path_to_skill_md>")
