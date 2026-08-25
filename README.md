# ai-cockpit-test-framework

AI-powered intelligent cockpit automated testing framework for zero-hardware IVI simulation, CAN signal validation, Robot Framework acceptance tests, and AI/RAG-assisted test case generation.

## Project Positioning

The framework provides layered testing for intelligent cockpit features. It supports fast local testing with a simulator and Mock mode, while leaving extension points for CANoe, UDS, real IVI APIs, LLM providers, and vector retrieval.

## Capabilities

- IVI simulator: volume control, music playback state, reset, and simulated bus messages.
- CAN adapter: connection lifecycle, signal transmission, message history, and big-endian response parsing.
- AI pipeline: requirement parsing, test-point extraction, text test-case generation, and RAG document lookup.
- Acceptance testing: Robot Framework multimedia volume scenarios covering boundaries, increments, invalid values, and mute state.
- Reporting: pytest logs and HTML output can be stored under `results/`.

## Quick Start

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
python -m robot --outputdir results tests/acceptance/
```

See [docs/deployment.md](docs/deployment.md) for setup and [docs/testing.md](docs/testing.md) for the complete test inventory.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `src/ai/` | Requirement parsing, test generation, and RAG pipeline |
| `src/cockpit/` | IVI simulator and CAN bus adapter |
| `src/utils/` | Environment and logging utilities |
| `tests/unit/` | IVI simulator unit tests |
| `tests/integration/` | AI/RAG pipeline integration tests |
| `tests/acceptance/` | Robot Framework suites and resources |
| `data/raw/` | Input requirements |
| `data/rag_knowledge/` | RAG knowledge documents |
| `results/` | Test reports and execution artifacts |
| `docs/` | Project, architecture, API, deployment, and test documentation |

## Documentation

- [Deployment Guide](docs/deployment.md)
- [Test Execution Guide](docs/testing.md)
- [Architecture](docs/architecture.md)
- [Cockpit API](docs/api_docs/cockpit_api.md)
- [MIT License](LICENSE)

## Runtime Mode

The default `RUN_MODE` is `mock`, so tests run without physical cockpit hardware or external LLM credentials. Real integrations require project-specific adapters and credentials.
