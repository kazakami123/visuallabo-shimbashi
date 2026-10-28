#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""古くなった価格・キャンペーン・営業時間を機械で見つける。

    python3 tools/site-check.py

正典は .claude/rules/pricing.md。ここにハードコードした値と食い違ったら、
まずルールファイルを確認すること（価格を変えたらこのファイルも直す）。
"""
import io, os, re, sys, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today()

# ---- 正典（.claude/rules/pricing.md と必ずそろえる） ----
HOURS = '平日 12:00 — 21:00 ／ 土日祝 10:00 — 18:00'
NOV_END = datetime.date(2026, 11, 30)       # 11月限定・初回体験特典の最終日
NOV_REVERT = '2026-12-01T00:00:00+09:00'   # 自動非表示の日付
NOV_MARK = ('campBand', '.bbar .br', 'campaign-reset', 'pt-camp', 'flow-nov', 'nov-campaign')
# サイトに出ていてはいけない旧価格
DEAD = ['¥4,980', '¥9,980', '¥34,800', '¥3,980', 'STANDARD会員', 'デイ会員',
        'お連れ様同伴 ¥24,800', 'ご利用可能額 ¥315,000', '満足保証']

pages = [p for p in sorted(glob.glob('*.html')) if p != 'chapter1_viewer.html']
# コラム生成テンプレートも見る。ここが古いと、新しいコラムに古い日付が入る
TPL = 'tools/column-template.html'
if os.path.exists(TPL):
    pages.append(TPL)
errs, warns = [], []


def read(p):
    return io.open(p, encoding='utf-8').read()


# 1) 営業時間の表記ゆれ
for p in pages:
    s = read(p)
    if '12:00' in s and HOURS not in s and '12:00 — 21:00' in s:
        if '土日祝 10:00 — 18:00' not in s:
            errs.append('%s 営業時間が平日だけになっています' % p)

# 2) キャンペーン表記の統一
want_seg = '11月来店限定｜初回体験90分セット ¥2,980｜BODY 60分＋選べる30分（フェイシャル or 脚）'
band = [p for p in pages if 'camp-seg' in read(p)]
for p in band:
    s = read(p)
    if want_seg not in s:
        errs.append('%s 11月限定特典の帯が統一文言になっていません' % p)

# 3) 自動復帰の日付が、¥980側と10月側で入れ替わっていないか
for p in pages:
    s = read(p)
    for m in re.finditer(r'2026-\d\d-\d\dT00:00:00\+09:00', s):
        ctx = s[max(0, m.start() - 420):m.end() + 420]
        side = 'nov' if any(k in ctx for k in NOV_MARK) else None
        if side == 'nov' and m.group(0) != NOV_REVERT:
            errs.append('%s 11月限定特典の自動非表示日が %s（正しくは %s）'
                        % (p, m.group(0)[:10], NOV_REVERT[:10]))
        if side is None:
            warns.append('%s 用途が判別できない自動復帰スクリプトがあります' % p)

# 4) 期限切れの残骸
if TODAY > NOV_END:
    left = [p for p in pages if 'camp-seg' in read(p)]
    if left:
        errs.append('11月限定特典は%sで終了しています。帯が%dページに残っています'
                    % (NOV_END, len(left)))

# 4b) canonical が自分自身を指しているか（生成ページで事故が起きやすい）
CANON_OK = {'index.html': '', 'lp-ladies-hie.html': '', 'lp-ladies-kubire.html': '',
            'care-fukurahagi.html': 'care-ashi.html', 'care-hip.html': 'care-soriko.html',
            'care-kubire.html': 'care-onaka.html', 'care-maemomo.html': 'care-ashi.html',
            'care-ninoude.html': 'care-onaka.html', 'care-sotomomo.html': 'care-ashi.html',
            'care-uchimomo.html': 'care-ashi.html', 'care-uramomo.html': 'care-ashi.html',
            'kiyaku.html': 'terms.html',
            'learn-cold.html': 'learn-onkatsu.html',
            'learn-mukumi.html': 'learn-lymph.html',
            'learn-circulation.html': 'learn-lymph.html',
            'learn-posture.html': 'care-soriko.html'}
for p in pages:
    if not p.endswith('.html') or p.startswith('tools/'):
        continue
    m = re.search(r'<link rel="canonical" href="https://visuallabo\.com/([^"]*)"', read(p))
    if not m:
        warns.append('%s canonical がありません' % p)
        continue
    want = CANON_OK.get(p, p)
    if m.group(1) != want:
        errs.append('%s canonical が %s を指しています（正しくは %s）'
                    % (p, m.group(1) or 'ルート', want or 'ルート'))

# 5) 旧価格・旧表記
for p in pages:
    s = read(p)
    for d in DEAD:
        if d in s:
            errs.append('%s 旧表記「%s」が残っています' % (p, d))

# 6) 終了した¥980キャンペーンが残っていないか
for p in pages:
    s = read(p)
    for m in re.finditer(r'(?<![0-9,])¥980', s):
        ctx = s[max(0, m.start() - 260):m.end() + 160]
        errs.append('%s 終了した初回体験¥980の表記が残っています' % p)

for w in sorted(set(warns)):
    print('WARN  ' + w)
for e in sorted(set(errs)):
    print('NG    ' + e)
print('\n%s 時点：%dページを確認。NG %d件／WARN %d件'
      % (TODAY, len(pages), len(set(errs)), len(set(warns))))
sys.exit(1 if errs else 0)
