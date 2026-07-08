#!/usr/bin/env bash
# PreToolUse hook (matcher: Write|Edit)
# 書き込まれようとしている本文に Tier A（封印語）が含まれていたらブロックする。
# 封印語リスト: .claude/compliance/blocklist.txt（1行1語, # はコメント）
set -euo pipefail

INPUT=$(cat)
ROOT="${CLAUDE_PROJECT_DIR:-.}"
BLOCKLIST="$ROOT/.claude/compliance/blocklist.txt"

# Write は content、Edit は new_string に本文が入る
CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // ""')

[ -f "$BLOCKLIST" ] || exit 0
[ -n "$CONTENT" ] || exit 0

while IFS= read -r phrase; do
  [ -z "$phrase" ] && continue
  case "$phrase" in \#*) continue ;; esac
  if printf '%s' "$CONTENT" | grep -qF -- "$phrase"; then
    jq -n --arg p "$phrase" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("コンプラ違反: Tier A封印語「" + $p + "」が含まれています。公開物では使用禁止です。")
      }
    }'
    exit 0
  fi
done < "$BLOCKLIST"

exit 0
