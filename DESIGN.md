# DESIGN.md — VISUAL LABO 新橋店

> AIコーディングエージェント（Claude/Cursor等）がこのプロジェクトのUIを生成・編集する際に読むデザインシステム定義。
> 参考フォーマット: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
> 正典は `CLAUDE.md`（作業ルール）。本ファイルはそれをAIが解析しやすい形に構造化したもの。

## 1. Visual Theme & Atmosphere

VISUAL LABO 新橋店（会員制体型管理サロン、2026年8月中旬OPEN）のTOPページは「エディトリアル×ラグジュアリー」。
夜のラウンジのようなダーク基調に、控えめなゴールドの光が差す。過剰な装飾はなく、余白と細い罫線（hairline）で高級感を出す。
明るいセクション（`.lt`クラス）は紙色ベースの落ち着いたパートで、写真点数の多い実績・BA紹介などに使う。
下層ページ（learn/care系）はTOPより機能寄りだが、ゴールドstrokeのSVGラインアイコンと罫線グリッドで世界観を継続する。
絵文字は全ページ禁止。装飾は必ずSVGラインアイコン（ゴールドstroke）。

## 2. Color Palette & Roles

TOP（index.html、ダークテーマ）:

| Token | Hex/Value | Role |
|---|---|---|
| `--bg` | #0e0c0a | ベース背景（ほぼ黒） |
| `--bg2` | #14110e | セクション背景（カード等） |
| `--bg3` | #1a1613 | ホバー時の背景 |
| `--ink` | #f0eae0 | 主要テキスト（オフホワイト） |
| `--ink-soft` | #cfc7b9 | 本文テキスト |
| `--mute` | #96897a | 補助・注記テキスト |
| `--gold` | #c9a768 | アクセント（見出し強調・CTA・罫線） |
| `--gold-l` | #e0c48d | ゴールドのホバー明色 |
| `--gold-d` | #a98c50 | ゴールドの濃色（プログレスバー等） |
| `--paper` | #f4efe6 | 明るいセクション内の紙色背景・価格カード |
| `--paper-ink` | #211d18 | 紙色背景の上のテキスト |
| `--line` / `--line-2` | rgba(240,234,224,.13/.07) | 罫線・グリッド境界（極細） |
| LINE公式カラー | #06C755 | LINE CTAボタン専用（ブランドカラーとは別枠） |

下層ページ（style.css、ライトテーマ）:

| Token | Hex | Role |
|---|---|---|
| `--paper` | #ffffff | ベース背景 |
| `--paper-2` | #F6F3ED | セクション背景 |
| `--gold` | #b89b5e | アクセント |
| `--ink` | #1a1a1a | 本文テキスト |

ルール: ゴールドは「アクセント」専用。地の色として大面積に使わない。ロゴは常に白（LABOだけゴールドにしない）。

## 3. Typography Rules

| 用途 | フォントスタック | 備考 |
|---|---|---|
| 和文見出し（TOP） | `"Shippori Mincho B1","Hiragino Mincho ProN",serif` (`--serif`) | h1/h2/lead、字間 letter-spacing:.06em |
| 英字（TOP） | `"Cormorant Garamond",Georgia,serif` (`--eng`) italic | kicker・番号・キャプション |
| ゴシック体（全体統一） | `"Futura","Century Gothic","Outfit","Noto Sans JP",sans-serif` (`--sans`/`--ui`) | 本文・UI・ボタン |

階層（TOP, `clamp()`でレスポンシブ）:
- Hero h1: `clamp(24px,6.4vw,60px)` / weight 500 / line-height 1.55
- lead (`.lead`): `clamp(26px,5.2vw,44px)` / weight 500 / line-height 1.65
- 本文 (`.body-txt`): 15px / weight 300 / line-height 2.3
- kicker（英字ラベル）: `clamp(14px,1.8vw,17px)` italic / letter-spacing .14em

改行ルール: 日本語見出しは `word-break:keep-all` + サイズ調整で意図した `<br>` 位置に折る。狭いカード内の本文には keep-all を使わない（不自然な改行になるため）。

## 4. Component Stylings

**ボタン (`.btn`)**: `padding:18px 34px`, `letter-spacing:.1em`, transition .35s。
- `.btn-gold`: 背景ゴールド／文字 #171310、hoverで `--gold-l` に明るくなり letter-spacing 拡張
- `.btn-line`: 背景 #06C755（LINE専用、ブランドゴールドと混同しない）
- `.btn-out`: 透明背景＋ゴールド枠線、hoverで薄いゴールド背景

**カードグリッド (`.vm-grid`, `.learn-grid`, `.bl-grid` 等)**: 1pxの `--line-2` をgapに使い擬似的な罫線グリッドを作る（`background:var(--line-2)` の上にカードを並べる手法）。カード背景は `--bg2`、hoverで `--bg3` ＋ `translateY(-4px)`。

**価格カード (`.price-card`)**: 紙色 (`--paper`) の実体カード。四隅にゴールドのコーナー装飾（`::before`/`::after` で26px角の2pxボーダー）。ダーク背景の中に「紙が置かれている」ような浮遊感を出す演出。

**FAQ (`.fq`)**: 連番は `counter()` + 英字イタリックのゴールド番号。開閉は `max-height` transition、`::after` の「＋」が45度回転して「×」に。

**枠付きボックス (`.mw-note`, `.pos-box`)**: 外枠 `1px solid rgba(201,167,104,.4)` の内側に `inset:6-7px` でもう一段薄い枠（`rgba(201,167,104,.15)`）を重ねる二重罫線が定番装飾。

## 5. Layout Principles

- 最大幅: `.wrap` 1160px（`.narrow` 780px）、左右 padding 24px
- セクション余白: `.sec{padding:clamp(80px,13vw,160px) 0}` — 上下に大きく取る
- 中央ぞろえの単調レイアウトは禁止。ファーストビューだけ豪華で下が弱い状態も禁止（全セクションで作り込みの密度を揃える）
- カードグリッドは1pxの罫線color(`--line-2`)を背景にした擬似グリッド線で区切る（marginではなくgapでの罫線表現）
- セクション間の区切りに `.hairline`（縦1px・ゴールドグラデーション・高さ`clamp(50px,7vw,90px)`）を使う

## 6. Depth & Elevation

- 基本はフラット（ダーク背景に溶け込むカード、box-shadowはほぼ使わない）
- 例外: `.frame`（明るい画像フレーム）と `.price-card` は `box-shadow:0 30-40px 70-90px rgba(0,0,0,.45-.5)` の大きく柔らかい影で「浮いている」印象を出す
- ヘッダーは固定＋スクロールで `backdrop-filter:blur(16px)` の半透明→ソリッド化（`.solid`クラス）

## 7. Do's and Don'ts

**Do**:
- ゴールドはアクセントとして最小限、罫線・番号・CTA・強調語のみに使う
- SVGラインアイコン（ゴールドstroke）でVITAキャラ以外の装飾を統一
- 効果表現には必ず近接して「※効果・感じ方には個人差があります」を置く
- 修正のたびにモバイル幅（375〜430px）で表示確認する

**Don't**:
- 絵文字を使わない（全ページ禁止）
- 中央ぞろえだけの単調レイアウトにしない
- ファーストビューだけ作り込んで下のセクションを手薄にしない
- 狭いカード内本文に `word-break:keep-all` を使わない（不自然な改行になる）
- VITAキャラをTOP・menu.htmlの2択カード・machine.htmlキービジュアルに置かない
- 旧価格・旧メニュー名（¥3,980系3コース、STANDARD/PREMIUM等）を復活させない（詳細は `CLAUDE.md` 参照）
- インディバとの比較で「同じ」「より上」という断定表現を使わない

## 8. Responsive Behavior

- ブレークポイントの主軸は900px・760-780px・480px
- `.vm-grid`: 4列 → 900px以下で2列 → 480px以下で1列
- `.hero-facts` 等の横並び要素は `flex-wrap:wrap` で自然に折り返す
- モバイルはPCフローティングCTA（`.fcta`）を非表示にし、代わりに下部固定バー（`.mbar`、LINE＋ホットペッパーの2ボタン）を表示
- タッチ操作前提でボタンのpaddingは大きめ（14px以上）を確保

## 9. Agent Prompt Guide

クイックカラー参照:
- ダーク背景 `#0e0c0a` / ゴールド `#c9a768` / オフホワイト文字 `#f0eae0` / 紙色 `#f4efe6`
- 明朝見出し: Shippori Mincho B1 / 英字イタリック: Cormorant Garamond / ゴシック統一: Futuraスタック

このプロジェクトで新しいセクション・ページを作る際のプロンプト例:
「VISUAL LABOのTOPと同じダーク×ゴールドのエディトリアルトーンで、罫線グリッドのカードセクションを作って。見出しはShippori Mincho、英字ラベルはCormorant Garamondイタリック、絵文字なし、ゴールドはアクセントのみ」

新規ページ作成後は必ずローカルサーバー＋スクリーンショットで表示確認すること（特にモバイル375〜430px、詳細は `CLAUDE.md`）。

## Exports — VIP page (2026-09-10)

VIPページ専用の追加定義。既存ページの色・書体・共通ナビ・フッターは変更しません。
構成は Split Studio（個室紹介 → 120分の施術 → 月額・単発 → デポジット → VIP体験 → FAQ）。
料金・契約条件は既存内容を維持し、お一人専用・同伴不可に統一。2ベッドの室内画像は掲載せず、既存の待合ラウンジ・入口画像を正確なキャプション付きで使用します。
ブラウザで320 / 375 / 414 / 768 / 1024 / 1280 / 1920pxの横はみ出しがないことを確認済み。本文103要素のコントラストは最低4.86:1。リンクとネイティブdetails以外の非同期操作はありません。

### CSS (source of truth: tokens.css)

```css
/* VIP page tokens. Existing pages keep their shared style.css palette. */
html.vip-page {
  --color-paper: #ffffff;
  --color-paper-2: #f6f3ed;
  --color-ink: #1a1a1a;
  --color-ink-2: #333333;
  --color-muted: #595959;
  --color-rule: #e4e2dd;
  --color-accent: #806731;
  --color-accent-light: #c9a768;
  --color-accent-ink: #ffffff;
  --color-focus: #806731;
  --color-dark: #211d18;
  --color-on-dark: #f4efe6;
  --color-on-dark-muted: #cfc7b9;
  --color-dark-rule: #595149;
  --font-display: 'Futura', 'Century Gothic', 'Outfit', 'Noto Sans JP', sans-serif;
  --font-body: 'Futura', 'Century Gothic', 'Outfit', 'Noto Sans JP', sans-serif;
  --font-outlier: 'Outfit', 'Futura', sans-serif;
  --text-xs: .75rem;
  --text-sm: .875rem;
  --text-md: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: clamp(1.75rem, 2.7vw, 2.5rem);
  --text-display: clamp(2.75rem, 4.6vw, 4.5rem);
  --space-3xs: .25rem;
  --space-2xs: .5rem;
  --space-xs: .75rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  --space-2xl: 4rem;
  --space-3xl: 6rem;
  --space-section: clamp(3.5rem, 7vw, 6rem);
  --rule-fine: 1px;
  --radius-card: 0;
  --vp-gutter: clamp(1.25rem, 4vw, 3rem);
  --vp-sticky-height: 5rem;
}
```

### Tailwind v4 (portable core mapping; not loaded by this static site)

```css
@theme {
  --color-paper: #ffffff;
  --color-paper-2: #f6f3ed;
  --color-ink: #1a1a1a;
  --color-muted: #595959;
  --color-rule: #e4e2dd;
  --color-accent: #806731;
  --font-display: 'Futura', 'Century Gothic', 'Outfit', 'Noto Sans JP', sans-serif;
  --font-body: 'Futura', 'Century Gothic', 'Outfit', 'Noto Sans JP', sans-serif;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --radius-card: 0;
}
```

### DTCG (portable core mapping)

```json
{
  "color": {
    "paper": { "$type": "color", "$value": "#ffffff" },
    "paper-2": { "$type": "color", "$value": "#f6f3ed" },
    "ink": { "$type": "color", "$value": "#1a1a1a" },
    "muted": { "$type": "color", "$value": "#595959" },
    "rule": { "$type": "color", "$value": "#e4e2dd" },
    "accent": { "$type": "color", "$value": "#806731" }
  },
  "font": {
    "body": { "$type": "fontFamily", "$value": ["Futura", "Century Gothic", "Outfit", "Noto Sans JP", "sans-serif"] }
  },
  "space": {
    "sm": { "$type": "dimension", "$value": { "value": 1, "unit": "rem" } },
    "md": { "$type": "dimension", "$value": { "value": 1.5, "unit": "rem" } },
    "lg": { "$type": "dimension", "$value": { "value": 2, "unit": "rem" } }
  }
}
```

### shadcn/ui (OKLCH triples; use with oklch(var(--token)))

```css
:root {
  --background: 100% 0 0;
  --foreground: 21.779% 0 0;
  --card: 96.481% 0.00860 84.573;
  --card-foreground: 21.779% 0 0;
  --primary: 52.673% 0.07881 84.598;
  --primary-foreground: 100% 0 0;
  --muted: 96.481% 0.00860 84.573;
  --muted-foreground: 46.400% 0 0;
  --border: 91.295% 0.00707 88.646;
  --ring: 52.673% 0.07881 84.598;
  --radius: 0;
}
```
