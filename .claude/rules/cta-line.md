---
description: VISUAL LABO 新橋店のCTA・予約導線の正典。LINEリンクやボタンに触れるファイルを編集する時に読み込む。
paths:
  - "**/*.html"
  - "**/*.md"
  - "assets/*.js"
---

# CTA・予約導線（正典）

2026-11-18 オーナー確認。

## 男性のお客様の予約

- 公式LINE：`https://lin.ee/VAjIUgc`
- ホットペッパービューティー：`http://b.hpr.jp/kr/hp/H000797603`
- 電話：`03-6205-4900`

各ページは、原則としてLINE・ホットペッパー・初回体験予約の3導線を維持する。
LINEを主導線、ホットペッパーを副導線とする。

## 女性ゲストの案内

- 女性本人が単独で予約する導線は設けない
- 女性用LINE `https://lin.ee/8YFMCSD` は、公式サイトの予約CTAには使用しない
- 女性をご招待できるのは VIP ROOMを120分ご利用になる男性のお客様
- VIP月額会員ご本人が、ご自身のVIP予約に「女性同伴オプション」を追加する
- 女性ゲスト1名＋¥10,000（税込・施術を含む）、同じVIP ROOMで120分
- VIP月額会員以外の方は、VIP 120分 単発 ¥29,800 とあわせて ¥39,800（税込）。通常の月額コースは消化しない
- 女性単独の予約・来店・入会は不可

`ladies.html` と `learn-ladies-*.html` は女性ゲスト向けの説明ページとして維持する。
CTAは女性本人の予約ではなく、VIP月額会員が同伴オプションを相談する男性用LINEへつなぐ。

## CTAの書き方

```html
<a class="btn btn-gold" href="https://lin.ee/VAjIUgc"
   target="_blank" rel="noopener" data-cta="任意のID">初回体験 60分 ¥2,980</a>
```

- `target="_blank"` と `rel="noopener"` を付ける
- `data-cta` はページ・位置ごとに固有の値を付ける
- 女性ゲスト向けのCTA文言は「VIP女性同伴オプションを相談する」とする
- 「女性の予約」「女性の初回体験」「女性専用LINE」と書かない

## 追従バー

- 通常ページは `.bbar.b3` にLINE相談・ホットペッパー・初回体験予約の3本
- `ladies.html` と `learn-ladies-*.html` も、VIP月額会員向けの相談導線として男性用LINEを使う
- corporate.html は法人向けのため、3本目は導入相談。ホットペッパーは置かない
- price.html はモバイルだけLINE・ホットペッパーを隠し、予約1本に絞る
- index.html と shindan.html は独自CSSのため、バーの見た目を変えるときは3箇所を確認する

## 使ってはいけない旧URL・旧導線

- `https://visuallabo-line.visuallabo.workers.dev/auth/line?`
- 女性単独予約用の `https://lin.ee/8YFMCSD`
- LADIES DAY／UNISEX DAYを前提とした予約ボタン

CTAに金額を書くときは `.claude/rules/pricing.md` を確認する。
