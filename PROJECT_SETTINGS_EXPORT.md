# 🎯 Archon Project Settings Export

This guide contains all the key configuration settings, tools, and development environment setups from the Archon project that can be exported and reused in other projects.

## 📋 Table of Contents

- [Python Development Setup](#python-development-setup)
- [TypeScript/React Configuration](#typescriptreact-configuration)
- [Linting & Code Quality](#linting--code-quality)
- [Testing Configuration](#testing-configuration)
- [Docker Configuration](#docker-configuration)
- [IDE Settings](#ide-settings)
- [CI/CD Templates](#cicd-templates)

---

## Python Development Setup

### 📦 pyproject.toml Template

```toml
[project]
name = "your-project"
version = "0.1.0"
description = "Your project description"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

# PyTorch CPU-only for development
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = [{ index = "pytorch-cpu" }]

[dependency-groups]
dev = [
    "mypy>=1.17.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.12.0",
    "pytest-timeout>=2.3.0",
    "pytest-cov>=6.2.1",
    "ruff>=0.12.5",
    "requests>=2.31.0",
    "factory-boy>=3.3.0",
]

server = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "python-multipart>=0.0.20",
    "supabase>=2.15.1",
    "asyncpg>=0.29.0",
    "openai>=1.71.0",
    "httpx>=0.24.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "logfire>=0.30.0",
]

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "B", "C4", "UP",
]
ignore = [
    "E501", "B008", "C901", "W191",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_any_unimported = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
check_untyped_defs = true
ignore_missing_imports = true
```

### 🐳 Python Dockerfiles

**Server Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml .
RUN uv pip install --system --group server

COPY src/ src/
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Development with hot reload:**
```dockerfile
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## TypeScript/React Configuration

### ⚙️ tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src", "tests"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 🎨 Tailwind Configuration

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // Add your custom colors
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
```

### 📦 package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "type-check": "tsc --noEmit"
  }
}
```

---

## Linting & Code Quality

### 🔍 Biome Configuration

```json
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/2.2.2/schema.json",
  "files": {
    "includes": ["src/**/*"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 120,
    "bracketSpacing": true,
    "attributePosition": "auto"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSameLine": false
    }
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "assist": {
    "enabled": true,
    "actions": {
      "source": {
        "organizeImports": {
          "level": "on"
        }
      }
    }
  }
}
```

### 🐍 Ruff Configuration (Already in pyproject.toml)

The Ruff configuration is included in the pyproject.toml template above.

---

## Testing Configuration

### 🧪 Vitest Configuration

```typescript
// vitest.config.ts
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        'src/test-utils.tsx',
      ],
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})
```

### 🐍 Pytest Configuration

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --disable-warnings
    --asyncio-mode=auto
    -v
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
asyncio_mode = auto
```

---

## Docker Configuration

### 🐳 docker-compose.yml Template

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    volumes:
      - .:/app
    command: npm run dev

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

### 🏗️ Multi-stage Dockerfile

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## IDE Settings

### 🎯 Cursor/VS Code Settings

**Global Settings:**
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "ms-python.black-formatter",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "javascript.preferences.importModuleSpecifier": "relative"
}
```

**Project-specific settings (.vscode/settings.json):**
```json
{
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  }
}
```

### 🚀 Cursor MCP Configuration

```json
// .cursor/settings.json
{
  "mcpServers": {
    "archon": {
      "uri": "http://localhost:8051/sse"
    }
  }
}
```

---

## CI/CD Templates

### 🔄 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Type check
      run: npm run type-check

    - name: Lint
      run: npm run lint

    - name: Test
      run: npm run test:coverage

    - name: Build
      run: npm run build

  python-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install uv
      run: pip install uv

    - name: Install dependencies
      run: uv sync --group all

    - name: Run tests
      run: uv run pytest

    - name: Run linting
      run: uv run ruff check
```

### 🐳 Docker Build Workflow

```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: yourusername/yourapp:latest
```

---

## Quick Setup Scripts

### 🐧 Linux/Mac Setup Script

```bash
#!/bin/bash
# setup.sh

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install uv
uv sync --group all

# Setup pre-commit hooks
pip install pre-commit
pre-commit install

# Copy environment file
cp .env.example .env

echo "Setup complete! Edit .env file with your configuration."
```

### 🪟 Windows Setup Script

```powershell
# setup.ps1

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install uv
uv sync --group all

# Setup pre-commit hooks
pip install pre-commit
pre-commit install

# Copy environment file
Copy-Item .env.example .env

Write-Host "Setup complete! Edit .env file with your configuration."
```

---

## 📝 Usage Instructions

1. **Copy the configurations** you need from this export
2. **Adapt them** to your project structure
3. **Install dependencies** using the provided commands
4. **Configure your IDE** with the recommended settings
5. **Set up CI/CD** using the workflow templates

This export contains all the production-ready configurations from the Archon project that have been battle-tested and optimized for modern development workflows.

**🎯 Start with the basics**: Copy the linting/formatting configs, then add testing, then CI/CD as your project grows.**
