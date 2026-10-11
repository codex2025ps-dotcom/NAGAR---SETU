# Nagar Setu

An AI-powered verified local digital ecosystem for Raghunathganj, West Bengal, India.

## Current scope

This repository contains a planning foundation and its validation tools. It does not yet contain a working API, database schema, web dashboard, mobile application, authentication service, or AI integration. Production readiness is a future acceptance gate, not a current claim.

## Start here

- [Architecture and proposed stack](docs/ARCHITECTURE.md)
- [Development phases and acceptance gates](docs/ROADMAP.md)
- [Authentication and security design](docs/SECURITY.md)
- [Coding standards](docs/CODING_STANDARDS.md)
- [Testing and release validation](docs/TESTING.md)
- [Hosting and cost controls](docs/OPERATIONS.md)
- [Instructions for coding agents](AGENTS.md)
- [Verified project state](PROJECT_STATE.md)
- [Task registry](TASK_REGISTRY.md)
- [Decisions and unresolved choices](DECISIONS.md)

## Validate the planning foundation

Requires Python 3.10+; no third-party packages, credentials, database, or network access are needed.

```sh
python3 tools/validate_planning.py
python3 -m unittest discover -s tools/tests -v
```

These checks validate planning consistency, local document links, and the validator's failure behavior. They do not prove application functionality or security. The GitHub workflow runs these checks on pushes and pull requests; remote execution must be checked separately.

## Contribution scope

Read AGENTS.md before changing files. Preserve existing work, use additive changes for this first task, and do not deploy to production. Future implementation should begin with NS-010 in TASK_REGISTRY.md after review of the proposal. No npm scripts or runnable monorepo applications exist yet.
