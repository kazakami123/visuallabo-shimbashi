#!/bin/bash
# VISUAL LABO ホームページ更新用 push スクリプト
# 使い方: このファイルをダブルクリック、またはターミナルで ./push.command
# → 変更を全部コミットして GitHub Pages に反映します

cd "$(dirname "$0")" || exit 1

echo "=== VISUAL LABO サイト更新 ==="
git status --short

if [ -z "$(git status --porcelain)" ]; then
  echo "変更はありません。push するものがないため終了します。"
  read -p "Enterで閉じる" _; exit 0
fi

MSG="update: $(date '+%Y-%m-%d %H:%M')"
git add -A
git commit -m "$MSG"
git push origin main

if [ $? -eq 0 ]; then
  echo ""
  echo "✔ push 完了。1〜2分でGitHub Pagesに反映されます。"
  echo "  確認URL: https://kazakami123.github.io/visuallabo-shimbashi/?v=$(date +%s)"
else
  echo ""
  echo "✖ push に失敗しました。ネット接続やGitHubログインを確認してください。"
fi
read -p "Enterで閉じる" _
