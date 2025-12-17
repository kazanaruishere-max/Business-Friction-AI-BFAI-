<div align="center">

# 🔍 Business Friction AI (BFAI)

### *Intelligent Process Mining & Friction Detection Engine*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![CLI](https://img.shields.io/badge/Interface-CLI-black?style=for-the-badge&logo=windowsterminal)](https://github.com/kazanaruishere-max/Business-Friction-AI-BFAI-)

**Detect inefficiencies. Understand bottlenecks. Optimize workflows.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Author](#-author)

---

</div>

## 🎯 What is BFAI?

**Business Friction AI** is a CLI-first automation engine that analyzes operational workflow logs to detect process inefficiencies, bottlenecks, and friction points. It provides actionable insights without requiring expensive enterprise tools.

### The Problem
- ❌ Manual process analysis is time-consuming
- ❌ Hidden delays cost businesses millions
- ❌ Traditional tools require complex setup

### The Solution
- ✅ **Automated friction detection** from CSV logs
- ✅ **Deterministic analysis** with reproducible results
- ✅ **Zero configuration** - works offline, no API keys needed

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🕐 **Time Gap Detection** | Identifies unusual delays between process steps using statistical analysis |
| 🔄 **Loop Detection** | Finds repetitive cycles indicating rework or process failures |
| 👤 **Human Dependency Analysis** | Measures over-reliance on manual intervention vs automation |
| 📊 **Rich CLI Output** | Beautiful terminal visualizations with tables and panels |
| 📝 **Report Generation** | Export findings to Markdown for documentation |

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip or Poetry

### Quick Install
```bash
# Clone the repository
git clone https://github.com/kazanaruishere-max/Business-Friction-AI-BFAI-.git
cd Business-Friction-AI-BFAI-

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m bfai --help
```

### Using Poetry (Recommended)
```bash
poetry install
poetry run bfai --help
```

### Using Docker
```bash
docker build -t bfai:latest .
docker run bfai:latest --help
```

---

## 💻 Usage

### 1. Analyze Workflow Logs
Run full analysis on your CSV log file:
```bash
python -m bfai analyze your_logs.csv --verbose
```

**Output:** JSON with detected friction points and AI recommendations.

### 2. Explain Specific Case
Deep-dive into a single case with timeline visualization:
```bash
python -m bfai explain your_logs.csv --case-id ORDER-001
```

**Output:** Rich terminal table + friction breakdown.

### 3. Generate Report
Create a comprehensive Markdown report:
```bash
python -m bfai report your_logs.csv --output report.md
```

**Output:** Professional report ready for stakeholders.

---

## 📁 Input Format

BFAI accepts CSV files with workflow event logs:

```csv
case_id,activity,timestamp,resource,actor_type
ord-001,Order Placed,2024-01-01 10:00:00,System,system
ord-001,Payment Check,2024-01-01 10:00:05,System,system
ord-001,Packing,2024-01-01 10:30:00,Bob,human
ord-001,Shipping,2024-01-01 14:00:00,Carrier,system
```

**Required columns:** `case_id`, `activity`, `timestamp`  
**Optional columns:** `resource`, `actor_type`, `status`

---

## 🏗️ Architecture

```
bfai/
├── cli/           # Typer CLI commands
│   ├── commands/  # analyze, explain, report
│   └── main.py    # Entry point
├── core/          # Detection engine
│   ├── detectors/ # TimeGap, Loop, HumanDependency
│   ├── friction.py
│   └── reasoning.py
├── ingestion/     # CSV loading & normalization
├── llm/           # LLM interface (Mock provider)
├── models/        # Pydantic data models
└── utils/         # Output formatting
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Friction Logic](bfai/docs/friction_logic.md) | Detection algorithms explained |
| [Demo vs Production](docs/demo_vs_production.md) | Feature comparison |
| [Contributing](CONTRIBUTING.md) | How to contribute |

---

## 🛠️ Tech Stack

- **Python 3.11+** - Core language
- **Typer** - CLI framework
- **Rich** - Terminal formatting
- **Pydantic** - Data validation
- **Pandas** - Data processing
- **NumPy** - Statistical analysis

---

## 📈 Roadmap

- [x] Core friction detection (v0.1.0)
- [x] CLI interface
- [x] Mock LLM provider
- [ ] Real LLM integration (Gemini/OpenAI)
- [ ] Web dashboard
- [ ] Database persistence
- [ ] Multi-language support

---

## 👤 Author

<div align="center">

**Created by Kazanaru**

[![GitHub](https://img.shields.io/badge/GitHub-kazanaruishere--max-181717?style=for-the-badge&logo=github)](https://github.com/kazanaruishere-max)

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

*Built with ❤️ for the process mining community*

</div>
