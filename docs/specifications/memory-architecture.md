# Memory Architecture

This document defines the memory architecture for AI World OS.

It is documentation only and does not define backend code, API behavior, vector search, prompt building, or any retrieval implementation.

## Purpose

The memory system is designed to preserve useful context across time while keeping temporary interaction data separate from durable knowledge.

## Memory Hierarchy

### Context Memory

- Purpose: hold immediate conversational context and the most recent interaction state
- Lifetime: very short, usually only for the current exchange or session segment
- Storage location: `memory/context/`
- Update strategy: updated continuously as new user input arrives
- Retrieval priority: highest for immediate continuity

### Session Memory

- Purpose: preserve information relevant to the current session
- Lifetime: short, usually the active session only
- Storage location: `memory/session/`
- Update strategy: appended or refined during the session, then summarized or discarded later
- Retrieval priority: high within the active session

### Long-term Memory

- Purpose: store durable facts, preferences, summaries, and stable context
- Lifetime: long-lived
- Storage location: `memory/long_term/`
- Update strategy: only promoted from shorter-lived memory after evaluation
- Retrieval priority: medium to high depending on relevance

### NPC Memory

- Purpose: store memory specific to a non-player character
- Lifetime: long-lived, with optional pruning or versioning
- Storage location: `memory/npc/`
- Update strategy: updated when NPC knowledge, state, or relationship context changes
- Retrieval priority: high when the NPC is the subject of the interaction

### Player Memory

- Purpose: store durable user-related preferences, history, and stable context
- Lifetime: long-lived
- Storage location: `memory/player/`
- Update strategy: updated cautiously and only when information is stable or clearly useful
- Retrieval priority: high for personalization and continuity

### World Memory

- Purpose: store durable world facts, world events, and environment state
- Lifetime: long-lived
- Storage location: `memory/world/`
- Update strategy: updated when the world changes in a meaningful way
- Retrieval priority: high when reasoning about world state

## Directory Structure

Future memory assets should follow a clear, purpose-based layout.

```text
memory/
  context/
  session/
  player/
  npc/
  long_term/
  world/
  relationship/
  summary/
```

This structure is intentionally extensible. Additional folders may be introduced later if they follow the same naming and separation rules.

## JSON Templates

The following are template examples only. They describe the shape of future memory records without defining implementation behavior.

### player-memory.json

```json
{
  "id": "player_0001",
  "type": "player",
  "subject_id": "player_0001",
  "summary": "Player prefers concise responses and structured explanations.",
  "importance": "high",
  "created_at": "2026-07-09T00:00:00Z",
  "updated_at": "2026-07-09T00:00:00Z"
}
```

### npc-memory.json

```json
{
  "id": "npc_0001_alice_memory_0001",
  "type": "npc",
  "subject_id": "npc_0001_alice",
  "summary": "Alice remembers meeting the player before.",
  "importance": "medium",
  "created_at": "2026-07-09T00:00:00Z",
  "updated_at": "2026-07-09T00:00:00Z"
}
```

### relationship-memory.json

```json
{
  "id": "relationship_player_0001_npc_0001_alice",
  "type": "relationship",
  "source_id": "player_0001",
  "target_id": "npc_0001_alice",
  "summary": "The player and Alice have a familiar but neutral relationship.",
  "importance": "medium",
  "created_at": "2026-07-09T00:00:00Z",
  "updated_at": "2026-07-09T00:00:00Z"
}
```

### world-memory.json

```json
{
  "id": "world_event_0001",
  "type": "world",
  "scope": "global",
  "summary": "A major weather shift changed movement across the northern region.",
  "importance": "high",
  "created_at": "2026-07-09T00:00:00Z",
  "updated_at": "2026-07-09T00:00:00Z"
}
```

## Memory Lifecycle

Memory should evolve through a staged process rather than being stored directly as durable knowledge.

```text
User Input
 ->
Conversation
 ->
Memory Extraction
 ->
Importance Evaluation
 ->
Memory Storage
 ->
Future Retrieval
```

### Lifecycle Notes

- User Input: the original interaction content
- Conversation: the full conversational context
- Memory Extraction: identification of candidate memory items
- Importance Evaluation: assessment of how valuable the item is for future use
- Memory Storage: placement into the appropriate memory layer
- Future Retrieval: later access when the information becomes relevant again

## Importance Levels

Memory importance should be treated as a retention signal.

### Low

- Useful only in narrow or temporary situations
- May be retained briefly or omitted if not helpful

### Medium

- Potentially useful later
- Should be retained if it supports continuity or common workflows

### High

- Important for continuity, personalization, or world consistency
- Should be retained with stronger preference

### Critical

- Essential for correctness, continuity, or safety-sensitive context
- Should be retained with the highest priority and strongest protection from pruning

## Retention Guidance

- Higher importance should increase retention preference.
- Lower importance should be easier to discard or compress.
- Importance should not replace judgment; it is a guideline for future memory policy.
- Stable facts should be preferred over noisy or speculative content.

## Implementation Boundaries

This document intentionally avoids:

- backend code
- APIs
- vector search
- prompt implementation
- retrieval logic

The architecture should remain implementation-independent so it can support future system design without forcing early technical decisions.
