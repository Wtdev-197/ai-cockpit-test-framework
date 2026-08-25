# Architecture

## Overview

The framework is organized into four layers:

```text
Requirement files / RAG knowledge
		|
		v
	AI and RAG layer
		|
		v
  Test layers: pytest + Robot Framework
		|
		v
  IVI simulator / CAN adapter / real adapters
```

## Source Components

### `src/ai`

`CaseGenerator` loads Markdown knowledge and parses requirements. In the default Mock mode it recognizes volume requirements, extracts boundary and acoustic test points, and generates text or Robot Framework cases. `RAGPipeline` provides simple document lookup in Mock mode and is the extension point for ChromaDB and embeddings.

### `src/cockpit`

`IVISimulator` models IVI state without hardware. It validates volume values, records simulated CAN messages, tracks music playback, and resets state between tests. `CANBusAdapter` provides a small interface for connection, signal transmission, response parsing, and message history.

### `tests`

pytest covers simulator, CAN, and AI/RAG behavior. Robot Framework covers acceptance scenarios and shared vehicle-domain keywords/resources.

## Runtime Modes

`src/utils/config.py` reads `.env` values. The default mode is `RUN_MODE=mock`, which is deterministic and requires no hardware or external services. A future real mode can connect the AI layer to an LLM/vector store and the cockpit layer to CANoe or vehicle hardware.

## Data Flow

1. A requirement is read from `data/raw/`.
2. `CaseGenerator` parses the requirement and identifies test points.
3. `RAGPipeline` supplies relevant knowledge documents.
4. pytest or Robot Framework executes the generated or hand-authored scenarios.
5. Reports and logs are written under `results/` and `logs/`.

## Extension Points

- Replace Mock requirement parsing with an LLM provider.
- Replace text matching with ChromaDB and an embedding model.
- Replace simulator keywords with CANoe/UDS/IVI API adapters.
- Add environment-specific variables under `tests/acceptance/variables/`.
