# Contributing to BFAI

Thank you for your interest in contributing to **Business Friction AI**! 🎉

## How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/bfai.git
cd bfai
```

### 2. Setup Development Environment
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
pip install -e .
```

### 3. Run Tests
```bash
pytest bfai/tests/
```

### 4. Code Style
We use **Ruff** for linting and formatting:
```bash
ruff check bfai/
ruff format bfai/
```

### 5. Submit a Pull Request
1. Create a new branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests and linting
4. Commit with clear message: `git commit -m "feat: add new detector"`
5. Push and create PR

## Project Structure
```
bfai/
├── cli/          # Typer CLI commands
├── core/         # Friction detection engine
├── ingestion/    # CSV loading & normalization
├── llm/          # LLM interface & mock provider
├── models/       # Pydantic data models
├── tests/        # Unit tests
└── utils/        # Output utilities
```

## Code Guidelines
- Use **type hints** for all functions
- Follow **Pydantic** for data models
- Keep CLI **thin** (no business logic)
- Write **unit tests** for new features

## Questions?
Open an issue on GitHub!
