# LMS Telegram Bot Implementation Plan

## Overview

This document describes the implementation approach for the LMS Telegram bot across all four tasks: scaffold (Task 1), backend integration (Task 2), intent routing with LLM (Task 3), and Docker deployment (Task 4).

## Task 1: Scaffold

The foundation establishes a clean architecture separating handler logic from the Telegram transport layer. Handlers are pure functions that take a command string and return response text. This separation enables three critical capabilities:

1. **Test mode**: The `--test` flag in `bot.py` allows running handlers directly without Telegram infrastructure, enabling rapid local development and debugging.
2. **Unit testing**: Handlers can be tested in isolation using pytest, ensuring correctness before integration.
3. **Transport independence**: The same handler works whether called from `--test` mode, unit tests, or the actual Telegram bot.

The directory structure follows Python conventions with `handlers/` for command logic, `services/` for external API clients, and `config.py` for environment-based configuration.

## Task 2: Backend Integration

This task connects the bot to the LMS backend API. An API client service handles HTTP requests with Bearer token authentication. The key architectural decision is reading `LMS_API_BASE_URL` and `LMS_API_KEY` from environment variables rather than hardcoding them. This pattern ensures secrets never appear in version control and allows different configurations for development, testing, and production deployments.

Handlers will call the API client to fetch real data for `/health`, `/labs`, and `/scores` commands. Error handling is critical: when the backend is unavailable or returns errors, the bot should provide informative messages rather than crashing.

## Task 3: Intent Routing with LLM

This task adds natural language understanding. Instead of requiring exact slash commands, users can ask questions in plain text. The LLM receives tool descriptions and decides which handler to invoke. The key insight is that description quality matters more than prompt engineering: clear, specific tool descriptions enable the LLM to route intents correctly.

The architecture adds an `IntentRouter` service that constructs prompts with tool descriptions and parses LLM responses to determine which handler to call. This maintains the separation of concerns: handlers remain pure functions, now called via LLM routing instead of direct command matching.

## Task 4: Docker Deployment

Deployment requires understanding Docker networking. Containers communicate via service names (e.g., `backend`, `postgres`) rather than `localhost`. The bot container needs environment variables for the bot token, LLM credentials, and backend URL (using the Docker service name).

The Dockerfile uses multi-stage builds: a builder stage syncs dependencies with `uv`, and a runtime stage copies only the necessary artifacts. This produces smaller, more secure images. The `.env.bot.secret` file provides runtime configuration without baking secrets into the image.

## Testing Strategy

Each task includes verification steps:
- Task 1: `--test` mode for all handlers
- Task 2: Integration tests against the running backend
- Task 3: Manual testing of natural language queries
- Task 4: End-to-end testing in the Docker environment

## Summary

This plan builds a maintainable, testable bot through incremental steps. Each task adds capability while preserving the clean architecture established in Task 1.
