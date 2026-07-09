# Project Conventions

This document defines project-wide documentation conventions for AI World OS.

## Naming Conventions

- Use plural directory names for collections of assets.
- Use snake_case for folders and file names.
- Use globally unique IDs for reusable entities.
- Keep machine-readable files separate from AI-readable files.

## Directory Style

Recommended pattern:

```text
world/
  npcs/
  locations/
  items/
  organizations/
  factions/
  rules/
  quests/
  events/
```

## File Separation

- Machine-readable files: `info.json`, `tags.json`, future schemas and indexes
- AI-readable files: `description.md`, future narrative or prompt-oriented documents

## Data Consistency

- Prefer stable identifiers over names as references.
- Keep field names consistent across entity types.
- Use concise, predictable terminology.
- Avoid introducing special cases unless they are clearly documented.

## Documentation Standards

- Keep documents concise and professional.
- Write for future maintainers and future automation.
- Document structure before behavior.
- Prefer explicit examples over ambiguous language.

## Extensibility

The conventions in this document are intended to remain stable as the project grows. New asset types should follow the same naming, separation, and documentation principles.
