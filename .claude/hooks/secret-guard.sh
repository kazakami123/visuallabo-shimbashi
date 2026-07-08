#!/usr/bin/env bash
# PreToolUse hook (matcher: Write|Edit|Bash)
# APIキー・トークンらしき文字列の直書きを検出してブロックする。
set -euo pipefail

INPUT=$(cat)
CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // .tool_input.command // ""')
[ -n "$CONTENT" ] || exit 0

# 代表的なシークレットの形（環境変数参照 ${VAR} は許可）
if printf '%s' "$CONTENT" | grep -Eq '(sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,})'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "シークレットらしき文字列を検出。直書きせず環境変数（例: ${API_KEY}）を使ってください。"
    }
  }'
  exit 0
fi
exit 0
