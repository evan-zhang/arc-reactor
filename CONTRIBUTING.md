# Contributing to ARC Reactor

> [!IMPORTANT]
> This repository is managed under the **AODW (Agent-Oriented Development Workflow)** protocol. If you are an AI Agent (Codex, Claude Code, OpenClaw, etc.), you are **MANDATED** to follow these standards. failure to do so will result in PR rejection.

## 🏛️ The Constitution (Core Principles)

1. **Traceability First**: No code change without a Requirement Traceability (RT) entry.
2. **Atomic Main Commits**: We use a **Strict-Main (Trunk-Based)** protocol to ensure all Agents share the same global state. No feature branches are allowed for AI agents unless specifically requested.
3. **Commit Guard**: You **MUST** run `python3 skills/arc-reactor/scripts/governance-audit.py` before every commit. If it fails, do not commit.
4. **Tool Sovereignty**: Use `archive-manager.py` for all Wiki / Knowledge operations.

## 🛠️ Development Workflow

### 1. Preparation
Before starting a task:
- Check for existing issues: `gh issue list`
- Find or create a matching RT in `RT/index.yaml`.
- Create a spec file: `RT/RT-xxx-description.md`.

### 2. Implementation
- Use feature branches: `[agent]/[issue-number]-[desc]`
- Follow the architectural patterns established in `archive-manager.py`.
- Keep the `SKILL.md` updated with any new capabilities.

### 3. Submission
- Message format: `[Type]: [Description] (by [AgentName])`
- Ensure all tests pass: `bash verify-v42.sh` (if applicable).

## 🦾 Agent Collaboration Protocol

We welcome multiple agents working together. To prevent chaos:
- **Locking**: Respect the `closed_at` field in `RT/index.yaml`. Do not modify logic related to a closed RT without opening a new Enhancement RT.
- **Antigravity Control**: As the Senior Architect Agent, Antigravity's architectural decisions (documented in `RT-013`) are binding.

## 📁 Repository Structure

- `skills/`: Core logic and configurations.
- `RT/`: Requirement traceability and specifications (Source of Truth).
- `arc-reactor-doc/`: Knowledge base data (Protected Layer).
- `scripts/`: Operational tools.

---
*For human developers: Please observe the same rigour as our AI colleagues.*
