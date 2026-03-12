# claude_code_workers
skill とか agent とかその辺

## Samples

| # | ディレクトリ | 内容 | 配置先（実運用時） |
|---|-------------|------|-------------------|
| 1 | `1_custom_skills/` | `/api-debugger` スキル（SKILL.md） | `.claude/skills/` or `~/.claude/skills/` |
| 2 | `2_mcp_servers/` | GitHub・PostgreSQL・ファイルシステム連携 | プロジェクトルート `.mcp.json` or `~/.claude.json` |
| 3 | `3_custom_agents/` | コードレビュー専門エージェント（AGENT.md） | `.claude/agents/` or `~/.claude/agents/` |
| 4 | `4_hooks/` | ファイル保護フック + 編集ログ記録 | `.claude/settings.json` + `.claude/hooks/` |
| 5 | `5_keybindings/` | キーバインド設定 | `~/.claude/keybindings.json` |
| 6 | `6_permissions/` | ツール許可/拒否ルール | `.claude/settings.json` |
| 7 | `7_memory/` | メモリ（user/feedback/project/reference各タイプ） | `~/.claude/projects/<project-hash>/memory/` |
| 8 | `8_claude_md/` | プロジェクト指示 + パス別ルール | プロジェクトルート `CLAUDE.md` + `.claude/rules/` |
