# GitHub PR Comments Examples

This file contains examples of PR comment categorization, severity assignment, and output formatting for the github-pr-comments skill.

## Category Definitions

### Security
Comments related to security vulnerabilities, authentication issues, data exposure, or unsafe practices.

**Severity indicators:**
- **Critical**: Active vulnerabilities, credential exposure, severe security flaws
- **High**: Authentication weaknesses, input validation issues, potential data leaks
- **Medium**: Security best practices, minor vulnerabilities
- **Info**: Security suggestions, hardening recommendations

### Code Changes
Comments requesting modifications to code logic, structure, or implementation.

**Severity indicators:**
- **Critical**: Breaking bugs, logic errors causing data corruption
- **High**: Significant architectural issues, performance problems
- **Medium**: Code improvements, refactoring suggestions
- **Info**: Style preferences, minor optimizations

### Documentation
Comments about code documentation, comments, README files, or API docs.

**Severity indicators:**
- **Critical**: Missing critical documentation for production systems
- **High**: Incomplete API documentation, missing usage examples
- **Medium**: Unclear comments, outdated documentation
- **Info**: Typos, formatting suggestions

### Clarifications
Questions or requests for explanation about the code or approach.

**Severity indicators:**
- **Critical**: Fundamental misunderstandings of requirements
- **High**: Confusion about critical functionality
- **Medium**: Questions about implementation details
- **Info**: General curiosity, optional explanations

### Bugs & Code Smells
Comments identifying bugs, potential bugs, or code quality issues.

**Severity indicators:**
- **Critical**: Production-breaking bugs, data loss risks
- **High**: Functional bugs, race conditions, memory leaks
- **Medium**: Edge case bugs, code smells, anti-patterns
- **Info**: Minor issues, potential future problems

### Other
Comments that don't fit the above categories (praise, meta-discussion, etc.).

**Severity indicators:**
- **Critical**: Blocking issues (CI failures, merge conflicts)
- **High**: Process issues, missing requirements
- **Medium**: General feedback, suggestions
- **Info**: Acknowledgments, thank yous, minor notes

---

## Sample Comments with Categorization

### Example 1: Security - Critical
**Comment:**
> "The API key is hardcoded in line 47. This needs to be moved to environment variables immediately before merging."

**Category:** Security  
**Severity:** Critical  
**Reasoning:** Credential exposure in source code is a critical security vulnerability.

---

### Example 2: Security - High
**Comment:**
> "This endpoint doesn't validate user input before passing it to the SQL query. This could be vulnerable to SQL injection."

**Category:** Security  
**Severity:** High  
**Reasoning:** Input validation issue with potential for SQL injection.

---

### Example 3: Code Changes - Critical
**Comment:**
> "This function deletes all user data when userId is null. This will wipe the entire database if called incorrectly!"

**Category:** Code Changes  
**Severity:** Critical  
**Reasoning:** Logic error that could cause catastrophic data loss.

---

### Example 4: Code Changes - High
**Comment:**
> "This O(n²) nested loop will cause severe performance degradation with large datasets. Consider using a hash map instead."

**Category:** Code Changes  
**Severity:** High  
**Reasoning:** Significant performance issue affecting functionality.

---

### Example 5: Code Changes - Medium
**Comment:**
> "Consider extracting this repeated logic into a helper function to improve maintainability."

**Category:** Code Changes  
**Severity:** Medium  
**Reasoning:** Refactoring suggestion that improves code quality.

---

### Example 6: Code Changes - Info
**Comment:**
> "You could use the spread operator here instead of Object.assign for slightly cleaner syntax."

**Category:** Code Changes  
**Severity:** Info  
**Reasoning:** Minor style preference with no functional impact.

---

### Example 7: Documentation - High
**Comment:**
> "The new API endpoint is missing documentation. Please add JSDoc comments explaining parameters and return values."

**Category:** Documentation  
**Severity:** High  
**Reasoning:** Missing documentation for new public API.

---

### Example 8: Documentation - Info
**Comment:**
> "Typo in the README: 'recieve' should be 'receive'."

**Category:** Documentation  
**Severity:** Info  
**Reasoning:** Minor typo with no functional impact.

---

### Example 9: Clarifications - Medium
**Comment:**
> "Why did you choose to use polling instead of webhooks here? Could you explain the reasoning?"

**Category:** Clarifications  
**Severity:** Medium  
**Reasoning:** Question about implementation choice requiring explanation.

---

### Example 10: Bugs & Code Smells - Critical
**Comment:**
> "The mutex isn't being released in the error path. This will cause a deadlock!"

**Category:** Bugs & Code Smells  
**Severity:** Critical  
**Reasoning:** Bug causing production-breaking deadlock.

---

### Example 11: Bugs & Code Smells - High
**Comment:**
> "This race condition between lines 34-42 could cause incorrect totals in the checkout flow."

**Category:** Bugs & Code Smells  
**Severity:** High  
**Reasoning:** Race condition affecting critical business logic.

---

### Example 12: Bugs & Code Smells - Medium
**Comment:**
> "This error is being silently swallowed. Consider at least logging it for debugging."

**Category:** Bugs & Code Smells  
**Severity:** Medium  
**Reasoning:** Code smell that makes debugging difficult.

---

### Example 13: Other - Info
**Comment:**
> "Great refactoring! This is much more readable now. 👍"

**Category:** Other  
**Severity:** Info  
**Reasoning:** Positive feedback with no action required.

---

## Sample Summary Table Format

### Format 1: Severity Distribution Table

```
PR Comment Analysis Summary
═══════════════════════════════════════════════════════════════

| Category              | Critical | High | Medium | Info | Total |
|-----------------------|----------|------|--------|------|-------|
| Security              |    1     |  2   |   1    |  0   |   4   |
| Code Changes          |    0     |  1   |   3    |  2   |   6   |
| Documentation         |    0     |  1   |   2    |  1   |   4   |
| Clarifications        |    0     |  0   |   2    |  5   |   7   |
| Bugs & Code Smells    |    1     |  3   |   2    |  0   |   6   |
| Other                 |    0     |  0   |   0    |  3   |   3   |
|-----------------------|----------|------|--------|------|-------|
| TOTAL                 |    2     |  7   |  10    | 11   |  30   |
```

### Format 2: Detailed Comment List

```
🔴 CRITICAL (2 comments)
───────────────────────────────────────────────────────────────
1. [Security] API key hardcoded at line 47
   → Must move to environment variables
   
2. [Bugs] Mutex not released in error path (lines 89-95)
   → Will cause deadlock

🟠 HIGH (7 comments)
───────────────────────────────────────────────────────────────
3. [Security] SQL injection vulnerability in user endpoint
4. [Code Changes] O(n²) performance issue in data processing
5. [Documentation] Missing API docs for /users/create
...

🟡 MEDIUM (10 comments)
───────────────────────────────────────────────────────────────
10. [Code Changes] Extract repeated logic to helper function
11. [Documentation] Update outdated installation instructions
...

ℹ️  INFO (11 comments)
───────────────────────────────────────────────────────────────
21. [Code Changes] Consider using spread operator
22. [Documentation] Typo in README
...
```

### Format 3: Action Required Summary

```
Action Required
═══════════════════════════════════════════════════════════════

⚠️  Must Fix Before Merge (2 Critical):
  • [Security] Remove hardcoded API key
  • [Bugs] Fix mutex deadlock in error handler

🔧 Should Fix (7 High Priority):
  • [Security] Add SQL injection protection
  • [Code Changes] Optimize nested loop performance
  • [Documentation] Document new API endpoints
  • [Bugs] Fix race condition in checkout
  (+ 3 more)

📝 Consider Addressing (10 Medium):
  • Refactoring suggestions
  • Documentation updates
  • Code smell fixes

💬 Questions & Info (18):
  • 7 clarification questions
  • 11 informational comments
```

---

## User Interaction Examples

### Example Prompt Flow

**Agent presents summary, then asks:**

```
How would you like to proceed with these comments?

Please select what you'd like me to do:

1. 🤖 Auto-fix: Which comments should I attempt to fix automatically?
   Options: [List comment numbers or categories]

2. ✋ Won't Fix: Which comments should be marked as "won't fix"?
   Options: [List comment numbers]

3. 👤 Manual: Which comments will you handle manually?
   Options: [List comment numbers]

Please respond with your choices, or I can suggest a recommended approach.
```

**Example user response:**
```
Auto-fix: All security and bugs with critical/high severity
Won't fix: Comment #22 (style preference)
Manual: I'll handle the clarifications
```

---

## Agent Response Templates

### Auto-fix Acknowledgment (posted to GitHub)
```
🤖 Working on this comment, please be patient.

I'll address this issue and update the PR shortly.
```

### Completion Response (posted to GitHub)
```
✅ Fixed in commit abc1234

Changes made:
- [Brief description of fix]
- [Any relevant details]

Please review and let me know if this addresses your concern.
```

### Won't Fix Response (posted to GitHub)
```
Thanks for the feedback! After consideration, we've decided not to implement this change because [reason].

Feel free to discuss further if you have concerns.
```
