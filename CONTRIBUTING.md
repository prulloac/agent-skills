# Contributing to Agent Skills

Thank you for your interest in contributing to the Agent Skills repository! This project aims to provide a collection of specialized skills for AI agents.

## How to Contribute

### Adding a New Skill

1.  **Create a Directory:** New skills should be added to the `skills/` directory at the repository root.
2.  **Follow Conventions:** Ensure your skill follows the established structure and naming conventions used by existing skills in `.agents/skills/`.
3.  **Documentation:** Include a `SKILL.md` or similar documentation file explaining the skill's purpose and usage.

### Improving Existing Skills

1.  Identify the skill in `skills/` or `.agents/skills/`.
2.  Make your improvements, ensuring they are backward compatible or clearly document breaking changes.
3.  Ensure the skill remains independent and doesn't introduce unnecessary dependencies.

## Guidelines

-   **Code Quality:** Follow the guidelines in `AGENTS.md` for code generation and review.
-   **Simplicity:** Prioritize simplicity and clarity.
-   **Security:** Never commit secrets or sensitive information.
-   **Testing:** Verify your changes thoroughly.

## Committing Changes

- **Message Style:** Use concise, descriptive commit messages (no longer than a Tweet, 280 characters). Follow conventional commits
- **Scope:** Focus each commit on a single logical change.
- **Secrets:** Double-check that no secrets (API keys, credentials) are included in your commits.
- **Verification:** Ensure that your changes pass all local checks (linting, tests) before committing.

## Pull Request Process

1.  Create a new branch for your changes.
2.  Commit your changes with clear, descriptive messages.
3.  Open a Pull Request (PR) against the `main` branch.
4.  Participate in the code review process and address any feedback.

We appreciate your contributions!
