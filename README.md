# Business Friction AI (BFAI)

**Business Friction AI** is a CLI-first AI Automation Engine that analyzes operational workflow data to verify, detect, and explain process inefficiencies.

## Project Philosophy
- **Engine-first, interface-last**: Deterministic core logic independent of the UI.
- **Stateless & Reproducible**: Inputs always produce the same outputs.
- **Demo-safe**: Runs offline without external API keys.

## Architecture
BFAI follows a clean layered architecture:
- **CLI Layer**: `bfai/cli` (Typer + Rich)
- **Service Layer**: `bfai/core` (Orchestration)
- **Domain Layer**: `bfai/models` (Pydantic) & `bfai/detectors` (Logic)
- **Infra Layer**: `bfai/ingestion` & `bfai/llm` (Adapters)

## Getting Started

### Prerequisites
- Python 3.11+
- Poetry

### Installation
```powershell
git clone <repo-url>
cd bfai
poetry install
```

### Running the Demo
We provide a "One Click" demo script for Windows (PowerShell):
```powershell
./scripts/run_demo.ps1
```

### Manual Usage

**1. Analyze a log file (JSON output)**
```powershell
poetry run bfai analyze bfai/examples/sample_logs.csv --verbose
```

**2. Explain a specific case (Rich visualization)**
```powershell
poetry run bfai explain bfai/examples/sample_logs.csv --case-id ord-002
```

**3. Generate a PDF-ready Report (Markdown)**
```powershell
poetry run bfai report bfai/examples/sample_logs.csv -o report.md
```

## Documentation
- [System Design](system_design.md) (Artifact)
- [Friction Logic](bfai/docs/friction_logic.md)
- [Demo vs Production](docs/demo_vs_production.md)
