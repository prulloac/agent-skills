# Agent Skills

A comprehensive collection of specialized skills for AI agents to enhance their capabilities in software engineering, documentation, feature planning, and workflow automation. This repository powers agents like OpenCode and GitHub Copilot with domain-specific expertise.

## Project Overview

Agent Skills provides a two-tier skill system:
- **Internal Agent Skills** (`.agents/skills/`): 19 specialized capabilities for agent-to-agent coordination and advanced workflows
- **User-Facing Skills** (`.skills/`): 20+ publicly available skills for extending agent capabilities

Each skill is a self-contained, well-documented module that agents can load to perform complex tasks with consistency and adherence to best practices. Skills cover areas including feature planning, GitHub automation, git workflows, validation, and code generation.

## Key Features

- **Feature Breakdown & Planning**: Decompose specifications into tasks and create optimal execution sequences
- **GitHub Automation**: Create issues, PRs, labels, and manage PR comments
- **Git Workflow Integration**: Commit management and isolated worktree creation
- **Code Generation Tools**: Custom agent creation, MCP server development
- **Documentation**: README synchronization, markdown validation, feature documentation
- **Development Environment**: DevContainer configuration and setup
- **Validation & Quality**: System prompts, cross-references, and skill validation

## Repository Structure

- `.agents/`: Internal agent infrastructure
  - `.agents/skills/`: 19 internal agent skills for complex workflows and automation
- `.github/`: GitHub-specific configuration, including PR templates
- `.opencode/`: Configuration and plugins for OpenCode integration
- `.devcontainer/`: Development container configuration for consistent environments
- `AGENTS.md`: General guidelines and mandates for agents interacting with this repository
- `CONTRIBUTING.md`: Guidelines for contributing and creating new skills
- `mcp.json`: Configuration for Model Context Protocol (MCP) servers
- `opencode.json`: OpenCode agent configuration
- `skills/`: 20+ user-facing skills for public use. Each skill has its own subdirectory with `SKILL.md` documentation and supporting resources

## Available Skills

### Feature Development
- **feature-breakdown**: Decompose feature specifications into components, tasks, and acceptance criteria
- **feature-planning**: Sequence tasks into optimal execution order with dependency analysis
- **feature-summary**: Create comprehensive feature documentation and roadmap
- **ai-agent-implementation**: Implement feature tasks using AI agents with progress tracking

### GitHub & Git Workflows
- **github-pull-request**: Create pull requests with repository standards and templates
- **github-create-issue**: Create GitHub issues with intelligent template matching
- **github-create-label**: Create and manage GitHub issue labels
- **github-issue-form-templates**: Design custom GitHub issue forms with YAML
- **github-pr-comments**: Analyze and manage pull request comments
- **git-commit-workflow**: Commit changes following repository guidelines
- **git-worktrees-usage**: Create isolated git worktrees for feature work

### Agent & Skill Development
- **custom-agent-creator**: Create custom agents for VS Code Copilot or OpenCode
- **skill-creator**: Guide for creating effective skills
- **mcp-builder**: Build high-quality MCP servers for external service integration
- **reusable-commands**: Create reusable commands for OpenCode or Copilot

### Documentation & Validation
- **readme-updater**: Synchronize README with current project metadata
- **markdown-crossref-validator**: Validate cross-references in markdown documents
- **system-prompt-validator**: Validate agent system prompts for quality and completeness

### Development Environment
- **devcontainer-config**: Create and manage DevContainer configurations
- **tmux-usage-guide**: Terminal multiplexer expertise for session, window, and pane management
- **vscode-extension-builder**: Guide for creating Visual Studio Code extensions and plugins

## Usage for Agents

Agents can discover and load skills from either directory:
- **Internal Skills** (`.agents/skills/`): Loaded automatically by agent infrastructure for coordination and advanced capabilities
- **User-Facing Skills** (`skills/`): Available for agents to use via the skill loading mechanism

Each skill contains a `SKILL.md` file which serves as the primary instruction set. Skills include examples, workflows, and resources to guide agents through complex tasks.

## Skill Categories

### By Purpose
| Category | Skills | Purpose |
|----------|--------|---------|
| **Planning** | feature-breakdown, feature-planning, ai-agent-implementation | Break down features and plan execution sequences |
| **GitHub & Git** | github-pull-request, github-create-issue, git-commit-workflow, git-worktrees-usage | Manage version control and GitHub workflows |
| **Development** | custom-agent-creator, skill-creator, mcp-builder, reusable-commands, vscode-extension-builder | Create and extend agent capabilities |
| **Documentation** | readme-updater, markdown-crossref-validator, feature-summary | Maintain and validate documentation |
| **Validation** | system-prompt-validator | Validate quality and consistency |
| **Infrastructure** | devcontainer-config, tmux-usage-guide | Manage development environments and tools |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to:
- Create new skills in the `skills/` directory (user-facing) or `.agents/skills/` (internal agent use)
- Improve existing skills with enhancements and bug fixes
- Ensure your changes meet the project's quality standards
- Follow the established structure and naming conventions

## Core Guidelines

Agents and contributors should follow the mandates outlined in [AGENTS.md](AGENTS.md):

- **Simplicity & Clarity**: Prioritize readable, maintainable code and clear instructions
- **Security**: Never commit secrets or sensitive information  
- **Verification**: Always verify changes through linting, testing, and manual review
- **Skill Independence**: Each skill should be self-contained without unnecessary dependencies
- **Documentation**: Include clear `SKILL.md` files with purpose, usage, and examples

## Resources

- **[AGENTS.md](AGENTS.md)**: Agent guidelines and best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **[mcp.json](mcp.json)**: MCP server configuration
- **[opencode.json](opencode.json)**: OpenCode agent configuration
