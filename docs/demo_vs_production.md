# Demo vs Production

BFAI is designed for scalability, but the demo version runs in a constrained "local" mode for ease of evaluation.

## Feature Comparison

| Feature | Demo Mode (Current) | Production (Target) |
| :--- | :--- | :--- |
| **Ingestion** | CSV Files (Local) | Event Bus / Database |
| **State** | Stateless (In-Memory) | Database Persistence (PostgreSQL) |
| **LLM Provider** | Mock / Deterministic | Gemini / OpenAI via API |
| **Scaling** | Single Threaded | Horizontal Scaling (Workers) |
| **Caching** | None | Redis Caching for embeddings |

## Mock Data

The demo uses `bfai/examples/sample_logs.csv` which contains synthetic data simulating an E-Commerce order flow.
- **Case `ord-001`**: Happy path.
- **Case `ord-002`**: Contains loops (payment retry) and time gaps.

## Mock Intelligence

To avoid API keys requirement during evaluation, the `ReasoningEngine` uses a `MockLLMProvider`.
- It detects friction types reliably.
- It returns hardcoded "best practice" recommendations based on the friction type.
- In production, this would be replaced by a generative model that reads the specific context of the logs.
