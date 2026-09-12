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

## CTAの構成

- 各ページ末尾に `<section class="sec cta">` を置く
- 画面下の追従バー `<div class="bbar">` に、LINE相談と初回体験予約の2本
  （chapter1_viewer は社内資料のため対象外。vip / shindan は現状なし）

## 価格の表記

CTAに金額を書くときは `.claude/rules/pricing.md` を必ず確認する。
現行は初回体験 60分 ¥2,980（通常 ¥9,800）。
