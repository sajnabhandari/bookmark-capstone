# Bookmark Manager — CLAUDE.md

## What this project is

This project is a Bookmark Manager web app that lets users save, tag, search, and filter bookmarks. Users can add URLs with optional titles and tags, browse their saved bookmarks, filter by tag, and search by keyword. The goal is a lightweight, functional tool built as a capstone to practice full-stack web development with Python and Flask.

## Tech stack

Python + Flask for the backend and routing, with Jinja2 HTML templates for the UI. Storage is intentionally kept in-memory (a plain Python list/dict) to avoid database complexity and keep the focus on application logic and UI. No frontend framework — plain HTML and minimal CSS only.

## Conventions

- Keep functions small and focused on a single responsibility
- Use type hints where possible (function signatures at minimum)
- No global mutable state outside of the initial app setup (e.g. the bookmarks store initialized once at startup)
- Prefer simple, readable logic over clever abstractions
- Route handlers should stay thin — delegate logic to helper functions

## Do not

- Add external dependencies (pip packages) without asking first
- Modify tests to make them pass — fix the code instead
- Over-engineer: no class hierarchies, no ORM, no JS frameworks unless explicitly requested
- Add logging, metrics, or observability scaffolding unprompted
