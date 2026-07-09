# Prompt Architecture

This document defines the prompt architecture for AI World OS.

It is documentation only and does not define backend logic, prompt assembly code, or LLM integration.

## Purpose

The prompt system should support modular composition so individual prompt parts can be added, removed, or replaced without redesigning the whole system.

## Overall Prompt Pipeline

```text
System Prompt
 ->
World Context
 ->
Retrieved Entities
 ->
Retrieved Memories
 ->
Conversation Context
 ->
User Input
 ->
LLM
 ->
Response
```

## Prompt Modules

### System Prompt

Defines the highest-level behavior, role, tone, and global constraints for the model.

### World Prompt

Provides broad world-setting context, canon, and background information relevant to the current environment.

### Character Prompt

Defines the behavior, voice, knowledge boundaries, and identity of a specific character or agent.

### Memory Prompt

Summarizes durable memory items that should influence the response, such as preferences, prior events, or long-lived context.

### Rule Prompt

Supplies governing rules, constraints, and policy-like conditions that must be respected during generation.

### Story Prompt

Provides narrative framing, scene context, or storytelling intent when the interaction is story-driven.

### User Prompt

Contains the latest user request and any directly supplied instructions for the current turn.

## Assembly Order

Prompt modules should be assembled from most stable to most immediate context.

Recommended order:

1. System Prompt
2. World Prompt
3. Character Prompt
4. Rule Prompt
5. Memory Prompt
6. Retrieved Entities
7. Retrieved Memories
8. Conversation Context
9. User Input

## Why Order Matters

- Higher-level instructions should appear before lower-level contextual details.
- Stable world and rule information should be established before conversational content.
- Memory and retrieval results should augment, not obscure, the core instructions.
- Recent user input should remain the most immediate task signal.

## Prompt Size Management

Prompt construction should remain aware of context-window limits and future token constraints.

### Context Window Limits

- Keep the assembled prompt within the available model window.
- Reserve space for the model response.
- Prefer concise context over exhaustive context.

### Memory Truncation

- Shorten low-value memory content before truncating high-value context.
- Preserve stable identifiers and key facts when compression is needed.
- Remove redundancy before removing meaningful distinctions.

### Retrieval Limits

- Limit the number of retrieved entities and memories included in the prompt.
- Prefer a smaller set of highly relevant items over a large noisy set.
- Align retrieval limits with the available prompt budget.

### Token Budgeting

- Allocate budget across modules before assembly.
- Reserve budget for user input and model output.
- Use module-level budgeting so a single module does not consume the entire prompt.

## Modularity

The prompt architecture should allow individual modules to be replaced or extended independently.

Examples of modular behavior:

- Add a new module without changing the entire prompt structure
- Remove a module that is not relevant to a given task
- Replace a module with a more specialized version for a specific character, world, or workflow
- Reorder subcomponents inside a module without changing the larger architecture

## Future Compatibility

The prompt architecture should remain compatible with different LLM providers, including OpenAI, Anthropic, Gemini, and local models.

### Compatibility Principles

- Keep the architecture provider-neutral.
- Avoid depending on provider-specific formatting in the architecture itself.
- Allow future adaptation to different context-window sizes and message styles.
- Separate conceptual prompt roles from provider-specific implementation details.

## Implementation Boundaries

This document intentionally excludes:

- backend code
- prompt assembly code
- LLM integration code
- provider-specific API design

The architecture should remain implementation-independent so the project can evolve across models and vendors without changing its core prompt design.
