#!/usr/bin/env python
"""
クリップボード監視スクリプト
- クリップボードを1秒間隔でポーリング
- 3行以上のテキストを検知したら claude CLI で一言要約
- work/yyyymmdd_hhmmss.md として保存
"""

import os
import subprocess
import sys
import time
from datetime import datetime

import pyperclip

POLL_INTERVAL = 1  # 秒
MIN_LINES = 3
WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")


def get_clipboard():
    try:
        return pyperclip.paste()
    except Exception:
        return ""


def summarize_with_claude(text):
    """claude CLI に要約させて結果を返す"""
    prompt = f"以下のテキストを一言（1行）で要約してください。要約文だけを出力し、それ以外は何も出力しないでください。\n\n{text}"
    result = subprocess.run(
        ["claude", "-p", prompt, "--model", "haiku"],
        capture_output=True,
        encoding="utf-8",
        timeout=30,
    )
    if result.returncode != 0:
        print(f"[ERROR] claude CLI failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout.strip()


def save(summary, original_text):
    """work/yyyymmdd_hhmmss.md に保存"""
    os.makedirs(WORK_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(WORK_DIR, f"{ts}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {summary}\n\n")
        f.write("## 元テキスト\n\n")
        f.write(f"```\n{original_text}\n```\n")
    return filepath


def main():
    print(f"クリップボード監視を開始します（{MIN_LINES}行以上で要約）")
    print(f"保存先: {WORK_DIR}")
    print("終了: Ctrl+C")
    print()

    prev = get_clipboard()

    while True:
        time.sleep(POLL_INTERVAL)
        current = get_clipboard()

        if current == prev or not current.strip():
            continue

        prev = current
        lines = current.strip().splitlines()

        if len(lines) < MIN_LINES:
            print(f"[SKIP] {len(lines)}行（{MIN_LINES}行未満）")
            continue

        print(f"[DETECT] {len(lines)}行のテキストを検知。要約中...")
        summary = summarize_with_claude(current)

        if summary is None:
            continue

        filepath = save(summary, current)
        print(f"[SAVED] {summary}")
        print(f"        -> {filepath}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n終了しました。")
