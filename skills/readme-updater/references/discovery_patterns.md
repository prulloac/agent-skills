# Project Discovery Patterns

This document defines common patterns for discovering project metadata (name, description, version, dependencies, entry points) across different languages and ecosystems.

## Node.js (JavaScript/TypeScript)

- **Metadata file**: `package.json`
- **Name**: `$.name`
- **Description**: `$.description`
- **Version**: `$.version`
- **Dependencies**: `$.dependencies`, `$.devDependencies`
- **Entry points**: `$.main`, `$.bin`, `$.module`, `$.exports`
- **Setup command**: `npm install`, `yarn`, `pnpm install`
- **Run/Test commands**: `npm run scripts`, `npm test`

## Python

- **Metadata files**: `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `poetry.lock`
- **Name/Version**: `[project] name` and `[project] version` in `pyproject.toml`
- **Description**: `[project] description` in `pyproject.toml` or `summary` in `setup.py`
- **Dependencies**: `[project] dependencies` (pyproject.toml), `install_requires` (setup.py), `requirements.txt`
- **Setup command**: `pip install -r requirements.txt`, `pip install .`, `poetry install`
- **Entry points**: `[project.scripts]` (pyproject.toml), `scripts` (setup.py)

## Rust

- **Metadata file**: `Cargo.toml`
- **Name**: `[package] name`
- **Version**: `[package] version`
- **Dependencies**: `[dependencies]`
- **Setup command**: `cargo build`
- **Entry point**: `src/main.rs`, `src/lib.rs`

## Go

- **Metadata file**: `go.mod`
- **Module name**: `module <MODULE_NAME>`
- **Dependencies**: `require (...)`
- **Setup command**: `go mod download`, `go build ./...`
- **Entry point**: `main.go`

## VS Code Extensions (General)

- **Metadata files**: `package.json`, `.vscode-test.js`
- **Identify by**: Presence of `engines: { vscode: "..." }` in `package.json`
- **Important sections**: `contributes`, `activationEvents`, `displayName`
- **Setup command**: `npm install`
- **Launch command**: Press F5 in VS Code
