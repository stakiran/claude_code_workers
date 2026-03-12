<!-- 配置先: ~/.claude/projects/<project-hash>/memory/feedback_testing.md -->
---
name: feedback_testing
description: Integration tests must use real database, not mocks
type: feedback
---

Integration tests must hit a real database, not mocks.

**Why:** Prior incident where mock/prod divergence masked a broken migration.
**How to apply:** When writing or modifying integration tests, always connect to a real test database instance.
