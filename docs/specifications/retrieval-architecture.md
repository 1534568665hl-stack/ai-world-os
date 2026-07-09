# Retrieval Architecture

This document defines the retrieval architecture for AI World OS.

It is documentation only and does not define backend logic, vector search implementation, or application code.

## Purpose

The retrieval system is responsible for finding relevant world data and memory so future prompts can be assembled with the right context.

## Complete Retrieval Pipeline

```text
User Input
 ->
Intent Analysis
 ->
Keyword Extraction
 ->
Structured Query
 ->
Vector Retrieval
 ->
Memory Retrieval
 ->
Context Ranking
 ->
Prompt Builder
 ->
LLM
 ->
Response
```

## Stage Responsibilities

### User Input

The original request, message, or command provided by the user.

### Intent Analysis

Determines the likely goal, topic, and scope of the request.

### Keyword Extraction

Identifies names, entities, terms, and other retrieval hints from the input.

### Structured Query

Converts the interpreted request into a normalized search intent for downstream systems.

### Vector Retrieval

Represents the future semantic lookup stage for locating conceptually related data.

### Memory Retrieval

Collects relevant short-term, long-term, and entity-specific memory items.

### Context Ranking

Orders the retrieved information by relevance, importance, and freshness.

### Prompt Builder

Organizes the selected context into a future prompt-ready structure.

### LLM

Consumes the assembled context and produces a response.

### Response

The final output returned to the user.

## Data Sources

The retrieval architecture should support the following sources:

- World Data
- NPC Data
- Player Memory
- NPC Memory
- Relationship Memory
- World Rules
- Items
- Events

### Source Roles

- World Data: general world facts and entity records
- NPC Data: character-specific information and descriptions
- Player Memory: durable user preferences and continuity signals
- NPC Memory: character-specific memory and state
- Relationship Memory: relationship state between entities
- World Rules: constraints, policies, and governing logic descriptions
- Items: object definitions and item-specific context
- Events: historical or current world events

## Retrieval Priority

Retrieval should favor information in the following order of immediate usefulness:

1. Session-relevant and context-specific information
2. Directly referenced entities
3. Player and NPC memory tied to the current request
4. Relationship memory that affects the interaction
5. World rules that constrain the response
6. Items or events explicitly mentioned or strongly implied
7. Broader world data that adds supporting context

### Priority Rationale

- Immediate context should be first because it best preserves continuity.
- Explicit entity references should outrank broad background information.
- Memory should support continuity, but should not override direct world facts when those facts are relevant.
- Rules matter when the response must remain consistent with the world model.

## Retrieval Limits

The architecture should define practical limits so future systems remain focused and efficient.

Recommended limit categories:

- Maximum retrieved entities
- Maximum retrieved memories
- Maximum context size
- Maximum source diversity

### Guidance

- Prefer a bounded number of high-value results over large unfiltered context sets.
- Cap retrieved items so the final context remains readable and stable.
- Allow limits to vary by task type, but keep the architecture explicit about their existence.

## Future Support for Semantic Vector Retrieval

Vector retrieval is expected to support semantic matching in future versions of the system.

This should be treated as a conceptual capability only.

### Intended Role

- Find related concepts when exact keywords are insufficient
- Surface nearby meaning rather than only literal matches
- Complement structured and memory-based lookup

### Architectural Notes

- Semantic retrieval should be one input to ranking, not the only signal.
- It should work alongside direct entity matches, memory matches, and rule-based context.
- The document intentionally does not define embedding models, indexes, similarity scoring, or storage details.

## Implementation Boundaries

This document deliberately excludes:

- backend code
- vector search implementation
- API design
- prompt construction code
- LLM integration code

The architecture should remain implementation-independent so it can evolve without locking the project into a specific technical design too early.
