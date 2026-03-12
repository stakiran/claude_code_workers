---
name: api-debugger
description: Debug API issues by analyzing responses and logs. Use when API calls fail or return unexpected results.
allowed-tools: Read, Bash, Grep
user-invocable: true
argument-hint: [endpoint-url]
---

# API Debugging Skill

When debugging API issues:

1. Check recent API responses in logs
2. Analyze error messages for patterns
3. Verify request/response formats
4. Suggest fixes with before/after examples

Target endpoint: `$ARGUMENTS[0]`

## Steps
- Use `Grep` to search for error patterns in log files
- Use `Read` to examine relevant source files
- Use `Bash` to run `curl` commands for testing the endpoint
