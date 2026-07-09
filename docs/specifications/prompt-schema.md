# Prompt Schema

This document defines the documentation-level structure for prompt assets in AI World OS.

## Purpose

Prompt assets capture reusable instructions, templates, policies, and example structures for future AI-driven workflows.

## Recommended Prompt Areas

- `templates/` - reusable prompt templates
- `system/` - system-level instructions
- `task/` - task-specific prompt variants
- `examples/` - prompt examples and demonstrations
- `policies/` - writing or behavior constraints

## Prompt Asset Principles

- Keep prompts modular and composable.
- Separate instructions from examples where practical.
- Prefer short, explicit sections.
- Document intended use clearly.
- Avoid coupling prompts to one specific workflow too early.

## Writing Guidance

- Use direct language.
- Keep variable placeholders obvious and consistent.
- Minimize hidden assumptions.
- Make prompt purpose, scope, and constraints easy to scan.

## Extensibility

Future prompt systems may introduce versioning, annotations, or evaluation metadata. This specification only defines the documentation-first foundation.
