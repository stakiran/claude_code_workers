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

## ライフサイクル

### いつ呼び出されるか

| 機能 | トリガー |
|------|---------|
| **Skill (inline)** | ユーザーが `/skill名` で手動実行、またはdescription一致でClaude自動判断 |
| **Skill (fork)** | 同上（`context: fork` 設定時） |
| **MCP Server** | セッション開始時 or 初回ツール呼び出し時に遅延起動 |
| **Custom Agent** | descriptionとタスクの一致でClaude自動判断、またはユーザー指示 |
| **Hooks** | イベント発火時（PreToolUse, PostToolUse, SessionStart 等） |

### 呼び出された後、いつまで常駐するか

| 機能 | 寿命 | ブロッキング |
|------|------|-------------|
| **Skill (inline)** | **ワンショット**。プロンプトとして会話に注入され、応答が終われば終了 | Yes（会話ターンを占有） |
| **Skill (fork)** | **ワンショット**。サブエージェントとして生成→完了→破棄 | foreground: Yes / background: No |
| **MCP Server** | **セッション全体に常駐**。セッション終了まで生き続ける唯一の永続プロセス | No（非同期） |
| **Custom Agent** | **ワンショット**。タスク完了 or maxTurns到達で終了。resumeで再開は可能だが自動常駐はしない | foreground: Yes / background: No |
| **Hooks** | **ワンショット**。イベント発火→シェルコマンド実行→即終了 | sync(デフォルト): Yes / async: No |

### ポイント

- **常駐するのはMCP Serverだけ**。他は全てワンショット（呼ばれて、完了したら消える）
- Skill(inline)は独立プロセスですらなく、プロンプトテキストの注入にすぎない
- Custom Agentはトランスクリプトが保存されるため明示的にresumeできるが、自動で常駐はしない
- Hooksは `async: true` にすればバックグラウンド実行可能だが、それでも実行完了後は消える

## MCP Serverの補足

### なぜSkill/Agentとは別にMCP Serverが必要なのか

Skill・Agentは「Claudeにプロンプトを渡して、Claudeが持っているツール（Bash, Read, Edit等）で作業する」だけで、Claude Codeの中で完結している。MCP Serverは**Claude Codeの外の世界とつなぐ**ためにある。

具体的には、以下のような**外部サービスとの接続状態を保持する必要がある**場面：

- PostgreSQLに常時接続してクエリを投げたい
- GitHubのAPIにOAuth認証済みセッションで繋ぎたい
- Slackのリアルタイム接続を維持したい
- ローカルのLanguage Serverと通信したい

```
# Bashでもできるが毎回接続→切断が発生する
Bash("psql -c 'SELECT * FROM users'")

# MCP Serverなら常時接続で即応答
mcp__postgres__query("SELECT * FROM users")
```

Skill/Agentは「Claudeの頭の使い方」のカスタマイズ、MCP Serverは「外部との接続方法」のカスタマイズ。

### MCP Serverの「常駐」とは

自律的に動くエージェントではなく、WebサーバーやDBと同じ**待機プロセス**。起動したらリクエストが来るまでただ待っている。

1. セッション開始時（or初回呼び出し時）にプロセスが**起動**
2. 何もしない。**ただ待つ**
3. Claudeが該当ツールを呼ぶ → リクエストを受けて処理 → 結果を返す
4. また**ただ待つ**
5. セッション終了時にプロセス**終了**

### MCP Serverのツールはいつ呼ばれるか

Claudeが他のツール（Bash, Read等）と全く同じ基準で、タスクに必要だと判断したら自動的に呼ぶ。特別な呼び出しルールはない。

```
Claudeが使えるツール一覧:
- Bash
- Read
- Edit
- Grep
- ...
- mcp__postgres__query      ← MCP由来
- mcp__github__create_pr    ← MCP由来
```

「遅延起動」はMCP Serverプロセスの起動タイミングの話で、「ツールとしていつ使われるか」とは別。
