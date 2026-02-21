# Dev Container Properties Reference

This reference covers all available `devcontainer.json` properties based on the official specification.

## General Properties

### Basic Configuration

- **name** (string): Display name for the dev container in the UI
- **forwardPorts** (array): Port numbers or "host:port" values to forward from container to local machine
  - Example: `[3000, "db:5432"]`
- **portsAttributes** (object): Maps ports to options like label, protocol, onAutoForward
- **otherPortsAttributes** (object): Default options for unconfigured ports

### Environment Variables

- **containerEnv** (object): Environment variables set on the Docker container itself
  - Static for container lifetime - requires rebuild to update
  - Available to all processes in the container
  - Example: `{"MY_VAR": "${localEnv:MY_VAR}"}`
- **remoteEnv** (object): Environment variables for dev tools/terminals but not the whole container
  - Can be updated without rebuilding
  - Client-specific

### User Configuration

- **remoteUser** (string): User for dev tools/terminals (not the whole container)
  - Defaults to containerUser or root
- **containerUser** (string): User for all container operations
  - Defaults to root or last USER in Dockerfile
- **updateRemoteUserUID** (boolean): On Linux, updates UID/GID to match local user (default: true)
- **userEnvProbe** (enum): Shell type for probing environment variables
  - Options: `none`, `interactiveShell`, `loginShell`, `loginInteractiveShell` (default)

### Container Behavior

- **overrideCommand** (boolean): Run sleep loop instead of default command (default: true for image/Dockerfile, false for Compose)
- **shutdownAction** (enum): What to do when tool closes
  - Options: `none`, `stopContainer` (default for image/Dockerfile), `stopCompose` (default for Compose)
- **init** (boolean): Use tini init process for zombie process handling (default: false)
- **privileged** (boolean): Run container in privileged mode (default: false)
- **capAdd** (array): Add capabilities (e.g., `["SYS_PTRACE"]` for debugging)
- **securityOpt** (array): Container security options (e.g., `["seccomp=unconfined"]`)
- **mounts** (array): Additional mounts using Docker CLI --mount syntax

### Features and Customizations

- **features** (object): Dev Container Features to install with their options
  - Example: `{"ghcr.io/devcontainers/features/github-cli": {}}`
- **overrideFeatureInstallOrder** (array): Override automatic Feature install ordering
- **customizations** (object): Product-specific properties (e.g., VS Code extensions)

## Image/Dockerfile Properties

### Using an Image

- **image** (string): Container image name from registry (DockerHub, GHCR, ACR)
  - Required when using an image

### Using a Dockerfile

- **build.dockerfile** (string): Path to Dockerfile relative to devcontainer.json
  - Required when using a Dockerfile
- **build.context** (string): Docker build context path (default: ".")
- **build.args** (object): Docker build arguments
  - Example: `{"MYARG": "MYVALUE", "FROM_ENV": "${localEnv:VAR}"}`
- **build.options** (array): Docker build CLI options
  - Example: `["--add-host=host.docker.internal:host-gateway"]`
- **build.target** (string): Docker build target stage
- **build.cacheFrom** (string/array): Images to use as build cache

### Workspace Configuration

- **workspaceMount** (string): Override workspace mount using Docker --mount syntax
  - Requires workspaceFolder to be set
- **workspaceFolder** (string): Path where tools should open in container
- **runArgs** (array): Docker CLI arguments for container runtime
  - Example: `["--cap-add=SYS_PTRACE", "--security-opt", "seccomp=unconfined"]`
- **appPort** (integer/string/array): Ports to publish (legacy - prefer forwardPorts)

## Docker Compose Properties

- **dockerComposeFile** (string/array): Path(s) to Docker Compose files
  - Required when using Docker Compose
- **service** (string): Service name to connect to
  - Required when using Docker Compose
- **runServices** (array): Services to start (defaults to all)
- **workspaceFolder** (string): Path to workspace in container (default: "/")

## Lifecycle Scripts

Executed in order during container setup:

1. **initializeCommand** (string/array/object): Runs on host during initialization
   - May run multiple times per session
   - Cloud: runs in cloud where source is located
2. **onCreateCommand** (string/array/object): First command inside container after creation
   - Cloud: used for caching/prebuilding, no user-scoped secrets
3. **updateContentCommand** (string/array/object): Runs when new content available
   - Cloud: periodically executed to refresh containers
4. **postCreateCommand** (string/array/object): Final setup command
   - Cloud: has access to user secrets
5. **postStartCommand** (string/array/object): Runs each time container starts
6. **postAttachCommand** (string/array/object): Runs each time tool attaches

### waitFor

- **waitFor** (enum): Command to wait for before connecting
  - Options: `onCreateCommand`, `updateContentCommand` (default), `postCreateCommand`, etc.

## Host Requirements

- **hostRequirements.cpus** (integer): Minimum CPUs/cores required
- **hostRequirements.memory** (string): Minimum memory (e.g., "4gb")
- **hostRequirements.storage** (string): Minimum storage (e.g., "32gb")
- **hostRequirements.gpu** (boolean/string/object): GPU requirements
  - boolean: GPU required or not
  - "optional": Use when available
  - object: `{"cores": 1000, "memory": "32gb"}`

## Port Attributes

Available in portsAttributes and otherPortsAttributes:

- **label**: Display name for the port
- **protocol**: `http` or `https` for web URL forwarding
- **onAutoForward**: Action when auto-forwarded
  - Options: `notify` (default), `openBrowser`, `openBrowserOnce`, `openPreview`, `silent`, `ignore`
- **requireLocalPort** (boolean): Require same port locally (default: false)
- **elevateIfNeeded** (boolean): Auto-elevate for privileged ports (default: false)

## Variables

Available in string values:

- **${localEnv:VAR_NAME}**: Environment variable from host
  - Default: `${localEnv:VAR:default_value}`
- **${containerEnv:VAR_NAME}**: Environment variable from running container
  - Default: `${containerEnv:VAR:default_value}`
- **${localWorkspaceFolder}**: Local path to workspace
- **${containerWorkspaceFolder}**: Container path to workspace
- **${localWorkspaceFolderBasename}**: Local workspace folder name
- **${containerWorkspaceFolderBasename}**: Container workspace folder name
- **${devcontainerId}**: Unique, stable identifier for the dev container

## Command Formats

### String Format
Goes through a shell, supports && and other shell syntax:
```json
"postCreateCommand": "npm install && npm run build"
```

### Array Format
Direct execution without shell:
```json
"postCreateCommand": ["npm", "install"]
```

### Object Format
Parallel execution of multiple commands:
```json
"postCreateCommand": {
  "server": "npm start",
  "db": ["mysql", "-u", "root", "-p", "mydb"]
}
```
