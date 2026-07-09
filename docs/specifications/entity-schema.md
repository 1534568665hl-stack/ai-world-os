# Entity Schema

This document defines the universal structure for all world assets.

## Standard Directory Structure

Every world object should use a plural, snake_case directory at the top level.

```text
world/
  npcs/
    npc_0001_alice/
      info.json
      tags.json
      description.md

  locations/
    loc_0001_warm_corner/
      info.json
      tags.json
      description.md

  items/
  organizations/
  factions/
  rules/
  quests/
  events/
```

Each entity directory should contain:

- `info.json` for machine-readable metadata
- `tags.json` for retrieval and categorization signals
- `description.md` for human-readable context

## info.json

`info.json` stores the core metadata for an entity.

Recommended fields:

- `id` - globally unique entity identifier
- `name` - human-readable entity name
- `type` - entity type such as `npc`, `location`, or `item`
- `version` - entity definition version
- `created_at` - creation timestamp
- `updated_at` - last update timestamp
- `author` - creator or responsible source
- `status` - lifecycle state such as `draft`, `active`, or `archived`

Guidance:

- Keep `id` stable over time.
- Use `type` to support future validation and routing.
- Treat timestamps as optional but preferred for maintained assets.
- Keep the field set extensible for future project needs.

## tags.json

`tags.json` stores flexible indexing and retrieval hints.

Recommended concepts:

- `search tags` - direct labels useful for filtering and browsing
- `retrieval tags` - tags intended to improve downstream lookup
- `semantic keywords` - meaningful concepts and descriptors
- `category` - a primary grouping label
- `priority` - relative importance or retrieval preference

Guidance:

- Use concise, consistent tags.
- Separate structural categories from descriptive keywords when possible.
- Keep the format broad enough to support future ranking or retrieval strategies.

## description.md

`description.md` is the AI-readable and human-readable narrative file.

It should include:

- purpose - what the entity is for
- writing conventions - how the file should be maintained
- length recommendation - keep content concise but sufficient
- Markdown usage - headings, lists, and short sections are preferred
- LLM optimization guidelines - write clearly, avoid ambiguity, and front-load important context

Guidance:

- Write in natural language.
- Prefer short sections over dense prose.
- Avoid implementation details in this file.
- Keep the text stable and easy to reference.

## Extensibility

The schema is intentionally generic.

Future entity types may add new files or metadata fields, but the core contract should remain consistent across all world assets.
