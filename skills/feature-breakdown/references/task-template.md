# Feature Breakdown Task Template

Use this template as a reference for creating clear, well-defined implementation tasks.

## Task Structure Template

```markdown
## Task [N]: [Brief Task Title]

**Component**: [Which component(s) this affects - e.g., Backend API, Database, Frontend UI]

**Description**: [1-2 sentences describing what needs to be implemented]

**Dependencies**: [List prerequisite tasks by number, or "None"]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Implementation Notes**: [Technical considerations, architectural patterns, security concerns, or references to relevant patterns]

**Estimated Effort**: [Small/Medium/Large]
```

## Writing Good Task Descriptions

### What Goes In Description

✅ **GOOD**: "Create a REST API endpoint that accepts user registration data (email, password), validates input, hashes the password using bcrypt, and stores the user in the database, returning appropriate error codes for validation failures."

❌ **BAD**: "Implement user registration"

✅ **GOOD**: "Build a React component that displays a list of products with pagination, filtering by category, and sorting options. Load data from API endpoint with loading and error states."

❌ **BAD**: "Make product list component"

### Description Elements

1. **Action**: What will be created/modified (endpoint, component, table, etc.)
2. **Input**: What data/input involved
3. **Processing**: What validation/transformation happens
4. **Output**: What gets returned/persisted
5. **Edge cases**: Brief mention of error handling

## Writing Good Acceptance Criteria

### Criteria Must Be

- **Specific**: No vague language like "nice", "good", "works"
- **Testable**: Someone can check if it's done without ambiguity
- **Independent**: Each criterion can be verified separately
- **Behavior-focused**: Describe WHAT not HOW

### Criteria Should NOT Include

- Implementation language or framework
- Architecture decisions
- File names or structure
- Performance implementation details ("use caching", "optimize with indexes")

### Good Examples

✅ `[ ] Password field accepts minimum 8 characters with uppercase, lowercase, and number`
✅ `[ ] API returns 409 status when email already exists in database`
✅ `[ ] Component displays loading spinner during data fetch`
✅ `[ ] Form validation displays error message below password field when password too weak`
✅ `[ ] Email sent within 30 seconds of password reset request`

### Bad Examples

❌ `[ ] Add password validation` (not specific enough)
❌ `[ ] Make it performant` (not testable)
❌ `[ ] Implement with Redux` (implementation detail)
❌ `[ ] Database query optimized` (how do we test this?)
❌ `[ ] Nice error messages` (subjective)

## Task Sizing Guide

### Small Tasks (1-2 days)

Characteristics:
- Single component or small module
- Straightforward requirements
- Limited or no external integrations
- Easy to test in isolation

Example:
```
Task: Create password reset confirmation endpoint
- Single endpoint, two inputs (token, new_password)
- Straightforward validation logic
- No external dependencies
- Easy to unit and integration test
```

### Medium Tasks (2-3 days)

Characteristics:
- Multiple components or moderate complexity
- Some integration between systems
- Multiple validation paths or edge cases
- Requires coordination with other tasks

Example:
```
Task: Implement user authentication API
- Multiple endpoints (register, login, logout, session)
- Integration with database and email service
- Multiple validation and error paths
- Requires session management setup
```

### Large Tasks (3+ days - usually should be split)

Characteristics:
- Multiple major components
- Complex business logic
- Heavy external integrations
- Usually should be broken down further

Example:
```
Task: Build complete admin dashboard
  → This should be broken into:
    - Task A: Admin user backend API
    - Task B: Dashboard layout component
    - Task C: Data visualization components
    - Task D: Admin authentication/authorization
```

**When to split**: If a task takes >3 days, break it into smaller tasks

## Dependency Management

### Dependency Types

**Sequential** (must complete first):
```
Task 1: Create database schema
Task 2: Implement API endpoint
↑ Task 2 depends on Task 1
```

**Parallel** (can start simultaneously):
```
Task A: Build login form component
Task B: Build password reset form component
→ Can work on both at once
```

**Critical Path** (affects timeline):
```
Task 1 → Task 2 → Task 3 → Task 4
These tasks block everything else
```

### Documenting Dependencies

```markdown
**Dependencies**: Task 1 (database schema), Task 2 (email service)
```

NOT:
```markdown
**Dependencies**: None - we can start right away!
```

## Common Task Categories

### Database/Data Model Tasks

```markdown
## Task N: [Create/Modify] [Entity] Table/Schema

**Component**: Database

**Description**: Define database schema for [entity] with [key fields]

**Acceptance Criteria**:
- [ ] Table/collection created with required fields
- [ ] Appropriate indexes created
- [ ] Data types correct (string length, numeric range, etc.)
- [ ] Relationships/foreign keys configured
- [ ] Constraints applied (unique, not null, etc.)
```

### API/Backend Tasks

```markdown
## Task N: Implement [HTTP Method] [Endpoint Name]

**Component**: Backend API

**Description**: Create API endpoint that [action] accepting [inputs] and [validation]

**Acceptance Criteria**:
- [ ] Endpoint accepts correct request format
- [ ] Input validation works (returns 400 for invalid data)
- [ ] Success case returns 200/201 with [expected response]
- [ ] Error cases return appropriate status codes
- [ ] Response time < [X]ms
```

### Frontend/UI Tasks

```markdown
## Task N: Build [Component Name]

**Component**: Frontend UI

**Description**: Create [component type] displaying [content] with [interactions]

**Acceptance Criteria**:
- [ ] Component renders correctly
- [ ] [Interaction] works as expected
- [ ] Form validation shows errors
- [ ] Loading state displayed during requests
- [ ] Responsive on mobile (< 600px) and desktop (> 1024px)
```

### Testing Tasks

```markdown
## Task N: Write [Test Type] Tests for [Module]

**Component**: Testing

**Description**: Create [unit/integration/e2e] tests covering [scenarios]

**Acceptance Criteria**:
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Test coverage > [%]
- [ ] All tests passing
```

### Integration Tasks

```markdown
## Task N: Integrate [Service Name]

**Component**: Backend Integration

**Description**: Configure and integrate [external service] for [purpose]

**Acceptance Criteria**:
- [ ] Service credentials securely stored
- [ ] Connection tested successfully
- [ ] Error handling for failures implemented
- [ ] Retry logic implemented
- [ ] Logging configured
```

## Example: Well-Defined Task

```markdown
## Task 7: Implement User Profile Update Endpoint

**Component**: Backend API

**Description**: Create PUT /api/users/:userId endpoint that accepts updated user profile data (name, email, phone, avatar URL), validates inputs, updates user record in database, and returns updated user data with 200 status or appropriate error status.

**Dependencies**: Task 2 (User schema), Task 4 (Authentication middleware)

**Acceptance Criteria**:
- [ ] Endpoint validates email format and uniqueness (not used by another user)
- [ ] Endpoint validates name is 1-100 characters
- [ ] Endpoint validates avatar URL is valid URL format
- [ ] Endpoint returns 401 if user not authenticated
- [ ] Endpoint returns 403 if trying to update another user's profile
- [ ] Endpoint returns 400 with field-specific error messages for validation failures
- [ ] Endpoint returns 200 with updated user object (excluding password)
- [ ] Update is atomic (either all fields update or none)
- [ ] Email change triggers re-verification flow
- [ ] Previous sessions remain valid after profile update
- [ ] Response time < 300ms under normal load

**Implementation Notes**: 
- Use transactions to ensure atomicity
- Email change should trigger re-verification for security
- Don't allow password change via this endpoint (separate endpoint)
- Log all profile updates for audit trail

**Estimated Effort**: Medium
```

## Checklist for Task Quality

Before finalizing each task, verify:

- [ ] Task title is specific (not just "Implement X")
- [ ] Component clearly identified
- [ ] Description includes what, input, processing, output
- [ ] Dependencies are explicit
- [ ] 2-5 acceptance criteria, all testable
- [ ] No implementation details in criteria
- [ ] No circular dependencies
- [ ] Effort estimated realistically
- [ ] Task is not too large (max 3 days)
- [ ] Task is not trivial (min 2-4 hours)
- [ ] Team member can understand without asking

---

## See Also

- `example-feature-breakdown.md` - Full example with real tasks
- `validation-checklist.md` - How to validate your task definitions
