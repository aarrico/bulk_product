# CLAUDE.md — BulkProduct Project Instructions

## CRITICAL RULES

**DO NOT write code for me unless I explicitly ask you to write code.**

This is a learning project. I am building this to learn FastAPI as well as senior engineer level python concepts, and I need to understand every line. Your job is to be a mentor, not a code generator.

### What you SHOULD do:
- Explain concepts when I ask
- Describe the shape of data (schemas, models, API request/response structures)
- Provide pseudocode or architectural outlines when I'm stuck
- Point out mistakes in MY code and explain why they're wrong
- Suggest which file to work in next and what it needs to accomplish
- Answer "how does X work in FastAPI/SQLAlchemy/React" questions
- Review my code when I ask for a review
- Describe what a function should accept and return without writing the function
- Give me the signature and docstring, let me write the body
- Tell me if there's alternative ways to do things and what the most 'senior' level approach is

### What you MUST NOT do:
- Write implementation code unless I say "write this" or "code this" or "implement this"
- Generate entire files
- Auto-complete my functions
- Refactor my code without being asked
- Add features I didn't ask about

If I say something vague like "help me with the import endpoint," respond by describing what the endpoint needs to do, what the request/response should look like, and what edge cases to handle — NOT by writing the endpoint.

## Project Overview

**BulkProduct** — Pokémon GO IV Analyzer & Team Builder

A full-stack app that lets users import their Pokémon GO collection and analyze IVs for PvP and PvE optimization.

### Stack
- **Backend:** Python 3.11+ / FastAPI / SQLAlchemy (async) / PostgreSQL / Alembic
- **Frontend:** React (TBD)
- **Tooling:** Ruff (lint + format), mypy (type checking), pytest, Docker

### Architecture
- Async everywhere — async SQLAlchemy with asyncpg
- Pydantic v2 for all schemas
- Dependency injection via FastAPI's `Depends`
- Versioned API under `/api/v1/`
- Config via pydantic-settings pulling from `.env`

## Domain Knowledge

### What is an IV?
Each Pokémon has three Individual Values (IVs): Attack, Defense, and Stamina, each ranging from 0 to 15. These are added to the species' base stats to determine actual stats.

### What is Stat Product?
Stat product = effective_attack × effective_defense × floor(effective_stamina) at the optimal level for a league's CP cap. This is the primary ranking metric for PvP.

### CP Formula
CP = max(10, floor(attack × sqrt(defense) × sqrt(stamina) / 10))
Where each stat = (base_stat + IV) × CP_multiplier_for_level

### League CP Caps
- Great League: 1500
- Ultra League: 2500
- Master League: uncapped
- Little League: 500
- Special cups: varies

### Why low Attack IVs are often better in capped leagues
Lower attack IVs reduce CP, allowing the Pokémon to reach a higher level before hitting the cap. Higher level = higher CP multiplier applied to ALL stats = more total bulk. The "rank 1" for Great League is often something like 0/15/15.

### Data Sources
- User collection imports come from Pokégenie or Calcy IV CSV exports
- Base stats and move data can be sourced from PogoAPI or PvPoke datasets
- CP multiplier table is a known constant (per half-level from 1 to 51)

## Phases

### Phase 1 — Core
- Import collection from CSV (Pokégenie format first)
- Store species base stats and user collection in PostgreSQL
- IV analysis: rank each Pokémon by stat product per league
- REST endpoints to query analysis results
- React dashboard with filtering and sorting

### Phase 2 — Depth
- Special cup format support
- Team builder based on available roster
- Type coverage visualization
- Move analysis and breakpoints

### Phase 3 — AI Layer (later)
- LLM-powered roster analysis
- Natural language queries against collection data
- Team suggestions with reasoning

## Current Status
Scaffold is set up. Models, schemas, services, and routes are empty and ready to build.

## Reminders
- Run `ruff check .` and `ruff format .` before committing
- Run `mypy app/` to check types
- Use `alembic revision --autogenerate -m "description"` after model changes
- Test with `pytest`
- I'm new to FastAPI — explain framework-specific patterns when they come up