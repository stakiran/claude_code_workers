# 9_clipboard_monitor

クリップボードを監視し、3行以上のテキストがコピーされたら `claude` CLI で一言要約して `work/yyyymmdd_hhmmss.md` に保存するスクリプト。

## なぜ Claude Code の Agent 機能だけではできないのか

「常駐してクリップボードを監視する」という要件は、Claude Code のどの拡張機能でも実現できない。

| 機能 | なぜダメか |
|------|-----------|
| **Custom Agent** | ワンショット。タスクを受けて完了したら消える。自発的に起動もしない |
| **MCP Server** | 唯一の常駐だが「呼ばれたら応答する」受動的なサーバー。能動的に何かを監視する仕組みではない |
| **Hooks** | イベント駆動のワンショット。「クリップボード変更」というイベントは存在しない |
| **Skill** | プロンプトの注入にすぎない。常駐の仕組みなし |

Claude Code は**「自発的に動き続ける常駐エージェント」の仕組み自体を持っていない**。すべて「何かをトリガーに呼ばれて、終わったら消える」設計。

## 採用したアプローチ

Python スクリプトでクリップボード監視ループを回し、要約だけ `claude` CLI に委譲する構成。

```
[Python: クリップボード監視ループ（1秒間隔）]
  ↓ 3行以上の変化を検知
  ↓
claude -p "一言で要約して: ..." --model haiku
  ↓
work/yyyymmdd_hhmmss.md に保存
```

- API キー不要（`claude` コマンドの認証をそのまま使う）
- Anthropic SDK 不要（依存は `pyperclip` のみ）
- モデルは Haiku でコスト最小

## 使い方

```bash
# 前提: pyperclip がインストール済みであること
pip install pyperclip

# 起動（Claude Code セッションの外で実行すること）
cd samples/9_clipboard_monitor
python clipboard_monitor.py
```

**注意**: Claude Code セッション内から `claude` CLI は呼べない（入れ子禁止）。必ず別のターミナルから起動する。

## 出力例

3行以上のテキストをコピーすると:

```
[DETECT] 5行のテキストを検知。要約中...
[SAVED] Pythonのリスト操作に関する基本的なコード例
        -> .../work/20260312_190523.md
```

保存されるファイル (`work/20260312_190523.md`):

```markdown
# Pythonのリスト操作に関する基本的なコード例

## 元テキスト

（コピーした原文）
```

## ファイル構成

```
9_clipboard_monitor/
  clipboard_monitor.py   # メインスクリプト
  README.md              # このファイル
  work/                  # 要約ファイルの保存先（自動作成）
```
