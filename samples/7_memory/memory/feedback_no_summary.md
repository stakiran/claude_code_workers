<!-- 配置先: ~/.claude/projects/<project-hash>/memory/feedback_no_summary.md -->
---
name: feedback_no_summary
description: User prefers terse responses without trailing summaries
type: feedback
---

Don't summarize what was just done at the end of every response.

**Why:** User can read the diff themselves and finds summaries redundant.
**How to apply:** Skip "Here's what I did" or "In summary" sections. Just do the work and stop.
