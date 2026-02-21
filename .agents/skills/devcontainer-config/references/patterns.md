# Common Dev Container Patterns

This guide covers common configuration patterns and real-world examples.

## Language-Specific Configurations

### Node.js Development

```json
{
  "name": "Node.js",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  },
  "forwardPorts": [3000],
  "postCreateCommand": "npm install",
  "remoteUser": "node"
}
```

### Python Development

```json
{
  "name": "Python 3",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "remoteUser": "vscode"
}
```

## Multi-Service with Docker Compose

### Web App + Database

devcontainer.json:
```json
{
  "name": "Full Stack App",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint"
      ]
    }
  },
  "forwardPorts": [3000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "PostgreSQL"
    }
  },
  "postCreateCommand": "npm install"
}
```

docker-compose.yml:
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspaces:cached
    command: sleep infinity
    environment:
      DATABASE_URL: postgres://postgres:postgres@db:5432/myapp
  
  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

## Advanced Features

### Adding Multiple Features

```json
{
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true,
      "username": "vscode"
    }
  }
}
```

### Environment Variables

```json
{
  "containerEnv": {
    "NODE_ENV": "development",
    "API_URL": "http://localhost:3000",
    "PATH": "${containerEnv:PATH}:/custom/bin"
  },
  "remoteEnv": {
    "LOCAL_HOME": "${localEnv:HOME}"
  }
}
```

### Port Forwarding with Attributes

```json
{
  "forwardPorts": [3000, 8080, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser",
      "protocol": "https"
    },
    "8080": {
      "label": "API",
      "onAutoForward": "notify"
    },
    "5432": {
      "label": "Database",
      "onAutoForward": "silent"
    }
  },
  "otherPortsAttributes": {
    "onAutoForward": "ignore"
  }
}
```

## Lifecycle Script Patterns

### Sequential Commands (String)

```json
{
  "postCreateCommand": "npm install && npm run build && npm run db:migrate"
}
```

### Direct Execution (Array)

```json
{
  "postCreateCommand": ["npm", "install"]
}
```

### Parallel Execution (Object)

```json
{
  "postCreateCommand": {
    "install": "npm install",
    "prepare-db": "npm run db:setup",
    "seed": "npm run db:seed"
  }
}
```

### Complete Lifecycle

```json
{
  "initializeCommand": "echo 'Starting setup on host...'",
  "onCreateCommand": {
    "deps": "apt-get update && apt-get install -y curl",
    "node": "npm ci"
  },
  "updateContentCommand": "npm install",
  "postCreateCommand": "npm run build",
  "postStartCommand": "npm run dev",
  "postAttachCommand": "echo 'Welcome to the dev container!'"
}
```

## Security and Permissions

### Debugging Support (C++, Go, Rust)

```json
{
  "runArgs": [
    "--cap-add=SYS_PTRACE",
    "--security-opt",
    "seccomp=unconfined"
  ],
  "capAdd": ["SYS_PTRACE"],
  "securityOpt": ["seccomp=unconfined"]
}
```

### Docker-in-Docker

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "mounts": [
    {
      "source": "dind-var-lib-docker",
      "target": "/var/lib/docker",
      "type": "volume"
    }
  ]
}
```

### Custom Mounts

```json
{
  "mounts": [
    {
      "source": "${localEnv:HOME}/.ssh",
      "target": "/home/vscode/.ssh",
      "type": "bind",
      "consistency": "cached"
    },
    {
      "source": "project-cache",
      "target": "/workspace/.cache",
      "type": "volume"
    }
  ]
}
```

## Host Requirements

```json
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb",
    "gpu": {
      "cores": 1000,
      "memory": "4gb"
    }
  }
}
```

## Custom User Configuration

```json
{
  "containerUser": "vscode",
  "remoteUser": "vscode",
  "updateRemoteUserUID": true,
  "userEnvProbe": "loginInteractiveShell"
}
```

## Monorepo with Workspace Folder

```json
{
  "name": "Frontend App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "workspaceFolder": "/workspaces/my-monorepo/apps/frontend",
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/my-monorepo,type=bind,consistency=cached"
}
```
