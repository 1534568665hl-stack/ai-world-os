# AI World OS

AI World OS is a modular foundation for building a scalable AI operating system for world models, memory, chat, prompts, embeddings, and related services.

This repository currently contains only the project scaffold. There is no application logic yet.

## Goals

- Keep the architecture modular and easy to extend
- Separate product areas by responsibility
- Reserve clear places for frontend, backend, data, memory, prompts, and world state
- Make room for future services without forcing early design decisions

## Repository Layout

- `docs/` - design notes, specifications, and architecture docs
- `frontend/` - user-facing applications and interfaces
- `backend/` - API services and server-side components
- `world/` - world models, simulation state, and related modules
- `memory/` - short-term and long-term memory components
- `prompt/` - prompt templates, policies, and prompt assets
- `database/` - schemas, migrations, and persistence helpers
- `config/` - environment and deployment configuration
- `assets/` - shared static assets
- `cache/` - generated cache data and transient artifacts
- `scripts/` - utility scripts and maintenance helpers
- `tests/` - automated tests
- `temp/` - temporary working files
- `embeddings/` - embedding indexes and related data
- `chat/` - chat flows, transcripts, and conversation artifacts

## Status

Initial scaffold only. The next implementation steps can add services, data models, and workflows without changing the overall structure.
