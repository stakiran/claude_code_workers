#!/bin/bash
# Prevents edits to sensitive files

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED=(".env" "package-lock.json" ".git/" "node_modules")

for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: Cannot edit $pattern files" >&2
    exit 2  # Exit 2 = block the action
  fi
done

exit 0  # Exit 0 = allow the action
