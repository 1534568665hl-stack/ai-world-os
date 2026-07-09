# Memory Schema

This document defines the documentation-level structure for memory assets in AI World OS.

## Purpose

Memory stores context that may be reused later by the system, including short-term session notes, durable world knowledge, and structured references.

## Recommended Memory Areas

- `context/` - immediate conversational context
- `session/` - temporary session-scoped context
- `player/` - durable player-related memory
- `npc/` - character-specific memory
- `relationship/` - relationship state and interaction history
- `world/` - persistent world facts and events
- `summary/` - condensed memory summaries
- `long_term/` - persistent remembered facts and summaries

## Common Memory Asset Pattern

Memory items should follow the same general separation principle as world entities:

- machine-readable metadata
- retrieval-oriented tags
- human-readable narrative or summary

## Design Principles

- Keep memory entries small and focused.
- Prefer stable identifiers for reusable memory objects.
- Separate factual memory from conversational output.
- Preserve provenance when possible.
- Avoid mixing temporary session context with long-lived memory.

## Extensibility

Future implementations may add schemas, indexes, or memory policies. This document only defines the conceptual structure and not any runtime behavior.
