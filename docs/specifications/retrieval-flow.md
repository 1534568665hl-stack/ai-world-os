# Retrieval Flow

This document is a simplified overview only.

The authoritative retrieval specification is [retrieval-architecture.md](./retrieval-architecture.md).

## Conceptual Pipeline

```text
User Input
 ->
Intent Extraction
 ->
Vector Retrieval
 ->
Prompt Builder
 ->
LLM
 ->
Response
```

## Purpose

This overview exists to provide a compact summary of the future retrieval path.

For full stage responsibilities, data sources, priority rules, and limits, refer to [retrieval-architecture.md](./retrieval-architecture.md).

## Notes

- This document is conceptual only.
- It does not define storage engines, ranking logic, or retrieval code.
- It does not define AI integration details.
- It is intentionally shorter than the authoritative retrieval architecture document.
