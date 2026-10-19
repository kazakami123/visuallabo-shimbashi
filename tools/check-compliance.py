#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""原稿の封印語チェック。1つでも当たったら exit 1。

    python3 tools/check-compliance.py drafts/foo.md
    python3 tools/check-compliance.py --all
正典は .claude/compliance/blocklist.txt（ここにハードコードしない）。
"""
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKLIST = os.path.join(ROOT, '.claude', 'compliance', 'blocklist.txt')
EMOJI = re.compile('[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF️❤]')
# 効果に触れたら近くに個人差の注記が要る、の検知用
EFFECT = ('痩せ', '細くな', '引き締ま', '落ち', 'サイズダウン', '燃焼', '変化')


def words():
    out = []
    for ln in io.open(BLOCKLIST, encoding='utf-8'):
        ln = ln.strip()
        if ln and not ln.startswith('#'):
            out.append(ln)
    return out


def check(path, banned):
    text = io.open(path, encoding='utf-8').read()
    lines = text.split('\n')
    errs, warns = [], []
    for i, ln in enumerate(lines, 1):
        for w in banned:
            if w in ln:
                errs.append('%s:%d 封印語「%s」: %s' % (path, i, w, ln.strip()[:60]))
        if EMOJI.search(ln):
            errs.append('%s:%d 絵文字は全ページ禁止: %s' % (path, i, ln.strip()[:60]))
    if any(w in text for w in EFFECT) and '個人差' not in text:
        warns.append('%s 効果に触れているのに「個人差」の注記がありません'
                     '（変換時に定型の免責は入りますが、本文でも触れてください）' % path)
    return errs, warns


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    files = sorted(glob.glob(os.path.join(ROOT, 'drafts', '*.md'))) if args[0] == '--all' else args
    banned = words()
    all_e, all_w = [], []
    for f in files:
        if args[0] == '--all' and os.path.basename(f).startswith('_'):
            continue
        e, w = check(f, banned)
        all_e += e
        all_w += w
    for w in all_w:
        print('WARN  ' + w)
    for e in all_e:
        print('NG    ' + e)
    if all_e:
        print('\n封印語・絵文字が %d 件あります。原稿を直してください。' % len(all_e))
        sys.exit(1)
    print('コンプラチェック OK（%d ファイル）' % len(files))


if __name__ == '__main__':
    main()
