#!/usr/bin/env bash
# 独自ドメインへの一括切り替え
#   使い方: bash scripts/set-domain.sh visuallabo.jp
# サイト内の全URL（canonical / OGP / sitemap / 構造化データ）を書き換え、CNAMEを作ります。
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "使い方: bash scripts/set-domain.sh <ドメイン名>   例) bash scripts/set-domain.sh visuallabo.com"; exit 1
fi

DOMAIN="$1"
OLD="https://kazakami123.github.io/visuallabo-shimbashi/"
NEW="https://${DOMAIN}/"

echo "旧: $OLD"
echo "新: $NEW"

# 1) 全HTML/XML/JSONのURLを置換
grep -rl "$OLD" --include="*.html" --include="*.xml" --include="*.json" --include="*.md" . 2>/dev/null \
  | while read -r f; do
      python3 - "$f" "$OLD" "$NEW" <<'PY'
import io,sys
p,old,new=sys.argv[1],sys.argv[2],sys.argv[3]
s=io.open(p,encoding='utf-8').read()
io.open(p,'w',encoding='utf-8').write(s.replace(old,new))
PY
      echo "  更新: $f"
    done

# 2) ルート相対リンク（404ページなど）の調整
python3 - "$DOMAIN" <<'PY'
import io,glob,sys
for f in glob.glob('*.html'):
    s=io.open(f,encoding='utf-8').read(); o=s
    s=s.replace('href="/visuallabo-shimbashi/','href="/')
    if s!=o: io.open(f,'w',encoding='utf-8').write(s); print('  ルート相対リンク更新:',f)
PY

# 3) CNAME
echo "$DOMAIN" > CNAME
echo "  CNAME を作成: $DOMAIN"

echo
echo "完了。このあと:"
echo "  1) git add -A && git commit -m \"独自ドメイン ${DOMAIN} へ切り替え\" && git push"
echo "  2) ドメイン管理画面で Aレコード4件（185.199.108-111.153）と CNAME(www→kazakami123.github.io) を設定"
echo "  3) GitHub → Settings → Pages → Custom domain に ${DOMAIN} を入力し、Enforce HTTPS にチェック"
echo "  4) Search Console にドメインプロパティを追加し、sitemap.xml を送信"
