# AgentPlatform 🧠🤖

> A production-ready AI agent platform built with **Hexagonal Architecture**, where the domain is completely decoupled from LLMs, databases, and external tools.

**Read this in:** [English](README.md) | [Español](README.es.md)

## 🎯 The Problem

Building AI agents is easy. Building **maintainable, testable, and production-ready** AI agents is hard. When your business logic is tightly coupled to OpenAI, Redis, or a specific vector database, changing a single component becomes a nightmare.

**AgentPlatform** solves this by applying **Hexagonal Architecture (Ports & Adapters)** to the core of the agent, ensuring that:

- The domain logic (the `AgentLoop`) **never** imports a concrete LLM, database, or tool.
- You can swap Ollama for OpenAI, or Redis for PostgreSQL, by changing a single line of dependency injection.
- The core is **100% testable** without spinning up any external services.

## ✨ Key Features (Production-Ready)

This project goes beyond a simple script. It includes the infrastructure and patterns needed for real-world deployment:

| Feature | Description |
| :--- | :--- |
| **Hexagonal Architecture** | Pure domain (`domain/`), isolated ports (`ports/`), and interchangeable adapters (`adapters/`). |
| **Multi-Stage Docker Builds** | Optimized for size and security. Uses a `builder` stage for dependencies and a slim `runner` stage with a non-root user. |
| **Infrastructure as Code** | Terraform modules for provisioning a VPC, public/private subnets, security groups, RDS (PostgreSQL), and ElastiCache (Redis). |
| **Circuit Breaker** | `pybreaker` integration to fail-fast when the LLM API is down, preventing cascading failures. |
| **Rate Limiting** | `slowapi` protection to prevent abuse and ensure fair usage (HTTP 429). |
| **Shadow Mode (A/B Testing)** | Run a new prompt/model (v2) in the background while the user receives the response from the stable version (v1). Zero-risk experimentation. |
| **Pure Unit Tests** | `pytest` suite that runs in milliseconds with **zero external services** required. |

## 🏗️ Architecture at a Glance

```text
agentplatform/
├── domain/                  # 🔒 Pure business logic (zero external dependencies)
│   ├── ports/              # Abstract interfaces (LLM, Memory, Tools, Storage)
│   ├── models.py           # Dataclasses (AgentState, AgentStep, ToolCall)
│   └── agent_loop.py       # The core ReAct loop (only uses ports)
├── adapters/               # 🔌 Concrete implementations
│   ├── llm/                # OllamaAdapter, MockLLMAdapter
│   ├── memory/             # RedisAdapter, InMemoryAdapter
│   ├── storage/            # PostgreSQLAdapter, MockAdapter
│   └── tools/              # MCPAdapter, MockAdapter
├── api/                    # 🌐 FastAPI routes (composition root)
├── core/                   # 🛡️ Cross-cutting concerns (ShadowRunner)
├── infrastructure/         # ☁️ Terraform & Docker
└── tests/                  # ✅ Unit tests for the pure domain
