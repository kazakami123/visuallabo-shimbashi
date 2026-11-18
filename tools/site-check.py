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
# いまキャンペーンを出しているか。2026-11-10 にオーナー確定で終了し、帯は全ページから撤去した。
# 次のキャンペーンを出すときは True にして CAMP_END / CAMP_REVERT を入れ直す。
CAMP_RUNNING = True
CAMP_END = datetime.date(2026, 11, 30)      # 11月の90分セットキャンペーンの最終日
CAMP_REVERT = '2026-12-01T00:00:00+09:00'   # 自動復帰の日付
OCT_END = datetime.date(2026, 10, 31)       # 10月キャンペーン（紹介特典・サウナ¥500）
OCT_REVERT = '2026-11-01T00:00:00+09:00'
CAMP_MARK = ('campBand', '.bbar .br', 'pt-camp')
OCT_MARK = ('flow-oct', 'oct-campaign')
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

# 2) キャンペーンの日付ゆれ
want_seg = '%d/%d（%s）まで 初回体験が90分セットに' % (
    CAMP_END.month, CAMP_END.day, '月火水木金土日'[CAMP_END.weekday()])
band = [p for p in pages if 'id="campBand"' in read(p)]
if CAMP_RUNNING:
    for p in band:
        s = read(p)
        if want_seg not in s:
            errs.append('%s キャンペーン帯の日付が「%s」になっていません' % (p, want_seg))
elif band:
    errs.append('キャンペーンは出していないのに、帯が%dページに残っています（%s）'
                % (len(band), '・'.join(band[:5])))

# 3) 自動復帰の日付が、¥980側と10月側で入れ替わっていないか
for p in pages:
    s = read(p)
    for m in re.finditer(r'2026-\d\d-\d\dT00:00:00\+09:00', s):
        ctx = s[max(0, m.start() - 420):m.end() + 420]
        side = ('camp' if any(k in ctx for k in CAMP_MARK)
                else 'oct' if any(k in ctx for k in OCT_MARK) else None)
        if side == 'camp' and m.group(0) != CAMP_REVERT:
            errs.append('%s ¥980キャンペーンの自動復帰日が %s（正しくは %s）'
                        % (p, m.group(0)[:10], CAMP_REVERT[:10]))
        if side == 'oct' and m.group(0) != OCT_REVERT:
            errs.append('%s 10月キャンペーンの自動復帰日が %s（正しくは %s）'
                        % (p, m.group(0)[:10], OCT_REVERT[:10]))
        if side is None:
            warns.append('%s 用途が判別できない自動復帰スクリプトがあります' % p)

# 4) 期限切れの残骸
if CAMP_RUNNING and TODAY > CAMP_END:
    left = [p for p in pages if 'id="campBand"' in read(p)]
    if left:
        errs.append('¥980キャンペーンは%sで終了しています。帯が%dページに残っています'
                    % (CAMP_END, len(left)))
left = [p for p in pages if 'id="oct-campaign"' in read(p) or 'id="flow-oct"' in read(p)]
if left:
    errs.append('終了した10月キャンペーンが%sに残っています' % '・'.join(left))

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
#    corporate.html の「1回あたり ¥4,980」だけは別物。法人福利厚生プラン
#    （ライト ¥49,800 ÷ 10回）の単価で、旧い初回体験価格とは関係がない。
#    この書き方のときだけ見逃す。ほかの場所の ¥4,980 はこれまでどおりNG。
DEAD_OK = {'corporate.html': ['1回あたり ¥4,980']}
for p in pages:
    s = read(p)
    for ok in DEAD_OK.get(p, []):
        s = s.replace(ok, '')
    for d in DEAD:
        if d in s:
            errs.append('%s 旧表記「%s」が残っています' % (p, d))

# 6) 本文に¥980（帯・CTA以外）が出ていないか
#    女性の初回体験¥980は 2026-11-18 に廃止した。ladies.html と
#    learn-ladies-* のページ単位の除外も、あわせて外してある。
#    残っていてよいのは「終了しました／取りやめました」と書いている履歴だけ。
for p in pages:
    s = read(p)
    for m in re.finditer(r'(?<![0-9,])¥980', s):
        ctx = s[max(0, m.start() - 320):m.end() + 200]
        if not any(k in ctx for k in ('camp-', 'bbar_', 'br-full', 'br-mini',
                                      'setAttribute', 'campBand', 'pt-camp',
                                      # 履歴として残している記述
                                      '終了しました', '終了いたしました',
                                      '取りやめ', '廃止', '承っていないこと',
                                      'ございません')):
            errs.append('%s 本文に¥980があります（女性の初回体験は廃止しました）' % p)

# 7) 廃止した営業区分の名前が残っていないか（2026-11-18 オーナー確定）
#    正典は .claude/rules/operating-days.md
#    LADIES DAY・UNISEX DAY・MEN'S DAY はすべて廃止した。
#    残っていてよいのは「廃止しました／取りやめました」と説明している文だけ。
DEAD_DAYS = ("MEN'S DAY", 'MEN&#39;S DAY', 'MEN’S DAY', 'LADIES DAY', 'UNISEX DAY',
             '男性専用DAY', '女性専用DAY', '男女共通DAY')
DEAD_DAY_OK = ('廃止', '取りやめ', 'ございません', '承っていないこと', '区分は')
for p in pages:
    s = read(p)
    for d in DEAD_DAYS:
        for m in re.finditer(re.escape(d), s):
            ctx = s[max(0, m.start() - 320):m.end() + 200]
            if not any(k in ctx for k in DEAD_DAY_OK):
                errs.append('%s 廃止した区分名「%s」が残っています' % (p, d))
                break
    for d in ('完全男性専用', '男性以外利用不可', '毎週日曜日営業',
              '女性のお客様と一緒になることはありません',
              '女性のお客様のご利用はお受けしていません。</p>'):
        if d in s:
            errs.append('%s 営業体制と矛盾する「%s」があります' % (p, d))

# 7b) お連れ様同伴の旧料金（¥29,800）が残っていないか
#     ¥29,800 は VIP単発の料金でもあるので、同伴の文脈だけを見る
for p in pages:
    s = read(p)
    for m in re.finditer(r'同伴', s):
        ctx = s[m.start():m.start() + 220]
        if '29,800' in ctx:
            errs.append('%s 同伴の旧料金¥29,800が残っています（＋¥10,000が正）' % p)
            break

# 8) 要のページに、お連れ様同伴の案内があるか
for p, mark in (('index.html', 'news-days'), ('flow.html', 'flow-days')):
    if os.path.exists(p) and mark not in read(p):
        errs.append('%s ご利用いただける方の案内（#%s）がありません' % (p, mark))
for p in ('faq.html', 'llms.txt', 'terms.html', 'guide.html', 'ladies.html'):
    if os.path.exists(p) and '同伴' not in read(p):
        errs.append('%s お連れ様同伴の記載がありません' % p)

# 8b) お連れ様向けページのLINEが、男性用アカウントに繋がっていないか
#     男性 https://lin.ee/VAjIUgc ／ 女性 https://lin.ee/8YFMCSD
#     正典は .claude/rules/cta-line.md
LINE_MEN = 'lin.ee/VAjIUgc'
LINE_LADIES = 'lin.ee/8YFMCSD'
for p in pages:
    if p != 'ladies.html' and not p.startswith('learn-ladies-'):
        continue
    s = read(p)
    n = s.count(LINE_MEN)
    if n:
        errs.append('%s お連れ様向けページに男性用LINEが%d件あります' % (p, n))
    if LINE_LADIES not in s:
        errs.append('%s 女性用LINEの導線がありません' % p)

# 9) 「痩身」を書いている場所に、個人差の注記が添えてあるか
for p in pages:
    s = read(p)
    if '痩身体験' in s and '個人差' not in s:
        errs.append('%s 痩身体験の近くに個人差の注記がありません' % p)

for w in sorted(set(warns)):
    print('WARN  ' + w)
for e in sorted(set(errs)):
    print('NG    ' + e)
print('\n%s 時点：%dページを確認。NG %d件／WARN %d件'
      % (TODAY, len(pages), len(set(errs)), len(set(warns))))
sys.exit(1 if errs else 0)
