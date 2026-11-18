# Codex に渡すプロンプト

以下をそのまま貼ってください。

---

VISUAL LABO 新橋店の公式サイト（静的HTML・GitHub Pages）に、営業日の変更を反映してください。

## リポジトリ

`kazakami123/visuallabo-shimbashi`。ビルドはありません。`main` にマージすると GitHub Pages が https://visuallabo.com に公開します。**`main` へ直接pushせず、ブランチを切ってPRを作ってください。**

## 先に読むファイル（ここが正典です）

- `CLAUDE.md` … 作業ルール全般
- `.claude/rules/operating-days.md` … 営業日と女性ゲスト利用条件の正典
- `.claude/rules/pricing.md` … 価格の正典
- `compliance.yaml` と `.claude/compliance/blocklist.txt` … 使ってはいけない語

**正典とサイトが食い違ったら、勝手に直さずに報告してください。**

## 反映する内容（2026-11-17 オーナー確定）

1. **2026年12月と2027年1月は、毎週日曜日に営業する。** 通常は定休日の第2・第4日曜日も営業する
2. **年末年始の休業は 2026年12月28日（月）〜2027年1月3日（日）。** 1月4日（月）から通常営業
3. **2027年2月からは、毎月第2・第4日曜日の定休に戻す**

日曜日の営業日は次のとおりです。

| 日付 | |
|---|---|
| 12/6・12/20 | 営業（通常の日曜） |
| 12/13・12/27 | 営業（通常は定休の第2・第4日曜） |
| 1/3 | **休業**（第1日曜だが年末年始にあたる） |
| 1/10・1/24 | 営業（通常は定休の第2・第4日曜） |
| 1/17・1/31 | 営業（通常の日曜） |

- **曜日による男女区分は設けない。** 女性はVIP月額会員の男性同伴・VIP ROOM限定です
- **営業時間は変えません。** 平日 12:00 — 21:00 ／ 土日祝 10:00 — 18:00
- **1月3日は日曜ですが休業です。** 「1月は毎週日曜日営業」とだけ書かないでください

## 直す場所

1. **全ページのFAQ定型文（15ファイル・33箇所）**
   「12月以降は毎週日曜日と祝日。第2・第4日曜の定休日を除く）」で検索。
   **画面テキストとFAQPage構造化データの2箇所に同じ文が入っています。必ず両方そろえてください。**
2. `index.html` … `#news-days` の曜日表の下にある注記
3. `news.html` … お知らせの記事。手順は `NEWS-HOWTO.md`
4. `llms.txt` … 営業区分の行と定休日の行
5. `.claude/rules/operating-days.md` … 正典
6. `drafts/area-ginza.md` … **`area-ginza.html` はこの原稿から生成されます。** HTMLだけ直すと、次に誰かが原稿を足したときに巻き戻ります

**フッターの「定休日：第2・第4日曜、年末年始、大型連休」は触らないでください。** 56ファイル115箇所にあり、これは通常の定めです。期間限定の例外をそこに書くと、2月に戻すときの作業が大きくなります。実際の営業日はホットペッパービューティーとGoogleマップに委ねる方針です。

## 守ること

- **絵文字を使わない**（全ページ禁止）
- **効果を言い切らない。** 「※効果・感じ方には個人差があります」を近くに置く
- 封印語を使わない（`.claude/compliance/blocklist.txt`）
- **容姿を評価する言い方をしない**
- 男性向けサロンであることを基本にし、女性について触れる場合は「VIP月額会員の男性本人が予約・来店・同伴し、同じVIP ROOMを120分利用する女性ゲスト1名のみ。＋¥10,000（税込）。女性単独不可」を明記する
- **モバイルでは共通の `<br>` が非表示**になります（`p br,li br,dd br,.fa br,.a br{display:none}`）。改行に頼った組版をしないでください
- `index.html` だけ `style.css` を読み込まず、CSSを全部インラインで持っています。CSSを変えるときは複数箇所
- 生成物である `learn-*.html` を直接編集しないでください。原稿は `drafts/*.md`、変換は `python3 tools/column.py`
- `tools/column-template.html` を手で編集しないでください

## 終わったら必ず通すもの

```
python3 tools/check-compliance.py --all
python3 tools/site-check.py
```

どちらも NG 0件にしてください（`404.html canonical` のWARNは既存で、直さなくて構いません）。

あわせて、次の2つも確認してください。

- **全ページの JSON-LD が構文エラーなしで読めること**
- **FAQの画面テキストと FAQPage 構造化データがずれていないこと**（タグを外して比較する）

確認用のスクリプト例です。

```python
import json, re, glob
def norm(t): return re.sub(r'\s+', '', re.sub('<[^>]+>', '', t))
bad = ng = 0
for f in sorted(glob.glob('*.html')):
    s = open(f, encoding='utf-8').read()
    sc = {}
    for a, b in re.findall(r'<button class="fq">(.*?)</button><div class="fa">(.*?)</div>', s, re.S):
        sc[norm(a)] = norm(b)
    for a, b in re.findall(r'<summary>(.*?)</summary>\s*<div class="a">(.*?)</div>', s, re.S):
        sc[norm(a)] = norm(b)
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            o = json.loads(m)
        except Exception as e:
            print('JSON NG', f, e); bad += 1; continue
        for x in (o if isinstance(o, list) else [o]):
            if x.get('@type') != 'FAQPage': continue
            for q in x['mainEntity']:
                n = norm(q['name'])
                if n in sc and sc[n] != norm(q['acceptedAnswer']['text']):
                    print('FAQずれ', f, q['name'][:30]); ng += 1
print('JSON-LD NG', bad, '/ FAQずれ', ng)
```

## 報告してほしいこと

- 直したファイルと箇所数
- 上の点検の結果
- 正典とサイトで食い違っていた点があれば、直さずにそのまま報告してください
