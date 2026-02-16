# Agent Skills

A collection of specialized skills for AI agents to enhance their capabilities in software engineering, documentation, and workflow automation.

## Project Overview

This repository provides structured, domain-specific instructions (skills) that agents can load to perform complex tasks with consistency and adherence to best practices. Each skill is designed to be self-contained and easily integrated into agent workflows.

## Repository Structure

- `.devcontainer/`: Development container configuration for a consistent dev environment.
- `.github/`: GitHub-specific configuration, including PR templates.
- `.opencode/`: Configuration and plugins for the OpenCode agent.
- `AGENTS.md`: General guidelines and mandates for agents interacting with this repository.
- `CONTRIBUTING.md`: Guidelines for adding or improving skills.
- `mcp.json`: Configuration for the Model Context Protocol (MCP) servers.
- `skills/`: Contains the individual agent skills meant to be shared with agents. Each skill has its own subdirectory with documentation and resources.

## Usage for Agents

Agents can discover and load skills from the `skills/` directory. Each skill contains a `SKILL.md` file which serves as the primary instruction set for that specific domain.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to:
- Create new skills following the established directory structure.
- Improve existing skills.
- Ensure your changes meet the project's quality standards.

## Guidelines

Agents and contributors should follow the core mandates outlined in [AGENTS.md](AGENTS.md), focusing on:
- **Simplicity & Clarity**: Prioritize readable and maintainable code and instructions.
- **Security**: Never commit secrets or sensitive information.
- **Verification**: Always verify changes through linting, testing, and manual review.
