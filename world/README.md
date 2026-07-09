# World Data Specification

This directory defines the canonical structure for world entities in AI World OS.

The goal is to keep world content human-readable, modular, and easy to extend without tying it to any runtime implementation.

## Standard Entity Layout

Every world entity should follow the same basic pattern:

```text
world/
  npcs/
    npc_0001_example/
      info.json
      tags.json
      description.md
```

## Entity Types

Planned entity types in this specification:

- `npcs/`
- `locations/`
- `items/`
- `organizations/`
- `factions/`
- `rules/`
- `quests/`
- `events/`

## File Roles

- `info.json` - structured metadata for the entity
- `tags.json` - flexible tag and categorization data
- `description.md` - long-form human-readable description

## Template Files

Template files for each entity type live beside this specification:

- `npcs/template_npc/`
- `locations/template_location/`
- `items/template_item/`
- `rules/template_rule/`

Each template folder uses the same file structure described above.

## Specification Documents

The related specification documents live in:

- `docs/specifications/entity-schema.md`
- `docs/specifications/memory-schema.md`
- `docs/specifications/prompt-schema.md`
- `docs/specifications/retrieval-flow.md`
- `docs/specifications/project-conventions.md`

These documents are intentionally broad so future projects can extend them without breaking the directory contract.
