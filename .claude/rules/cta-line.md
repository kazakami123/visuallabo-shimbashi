---
description: VISUAL LABO 新橋店のCTA・予約導線の正典。LINEリンクやボタンに触れるファイルを編集する時に読み込む。
paths:
  - "**/*.html"
  - "**/*.md"
  - "assets/*.js"
---

# CTA・予約導線（正典）

2026-09-12 オーナー確認。

## 公式LINEのURL

```
https://lin.ee/VAjIUgc
```

**予約・相談のCTAは、すべてこのURLに繋ぐ。** 新しくCTAを作るときも、
既存のCTAを直すときも、必ずこれを使う。

### 書き方

```html
<a class="btn btn-gold" href="https://lin.ee/VAjIUgc"
   target="_blank" rel="noopener" data-cta="任意のID">初回体験 60分 ¥2,980</a>
```

- `target="_blank"` と `rel="noopener"` を必ず付ける
- `data-cta` はGAのCTA計測に使っている。**どのボタンから押されたかを区別**
  するため、ページ・位置ごとに固有の値を付ける
  （例：`hero_reserve` / `final_line` / `bbar_line_contact` / `lp_hero_reserve`）

### 使ってはいけない旧URL

```
https://visuallabo-line.visuallabo.workers.dev/auth/line?
```

2026-09-12 に全47ファイル・169箇所から撤去済み。**復活させないこと。**
（Cloudflare Workers の中継URL。役割が残っている場合は
  オーナーに確認してから扱う）

## ホットペッパービューティーのURL

```
http://b.hpr.jp/kr/hp/H000797603
```

2026-09-17 オーナー確認。**LINEに次ぐ第2の予約導線。**

パソコンでLINEを使っていない人、LINEの友だち追加に抵抗がある人が
そのまま予約できるように置いている。LINEの代わりではなく、並べて出す。

### 書き方

```html
<a class="btn btn-out" href="http://b.hpr.jp/kr/hp/H000797603"
   target="_blank" rel="noopener" data-cta="任意のID">ホットペッパーで予約する</a>
```

- LINEより控えめな見た目にする（アウトライン系）。主導線はあくまでLINE
- 追従バーでは `.bh` クラスを使う

## CTAの構成

- 各ページ末尾に `<section class="sec cta">` を置く
- 画面下の追従バー `<div class="bbar b3">` に3本
  （LINE相談 `.bl` ／ ホットペッパー `.bh` ／ 初回体験予約 `.br`）
  - `b3` はモバイルで3本が収まるように文字を詰めるクラス。付け忘れると溢れる
  - chapter1_viewer は社内資料のため対象外。vip / shindan は現状なし
  - corporate.html は法人向けで予約導線ではないため、ホットペッパーは置かない
  - price.html はモバイルだけ `.bl` `.bh` を隠し、予約1本に絞っている
- フッターの連絡先行にも、電話番号と並べてホットペッパーのリンクを置く（全ページ）

## 価格の表記

CTAに金額を書くときは `.claude/rules/pricing.md` を必ず確認する。
現行は初回体験 60分 ¥2,980（通常 ¥9,800）。
