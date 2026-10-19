#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sitemap.xml に、まだ載っていない learn-*.html を追記する。
既存の行は触らない。lastmod はファイルの最終コミット日（なければ今日）。
"""
import io, os, re, glob, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://visuallabo.com/'
SM = os.path.join(ROOT, 'sitemap.xml')


def lastmod(name):
    try:
        d = subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', name],
                                    cwd=ROOT, text=True).strip()
        if d:
            return d
    except Exception:
        pass
    return datetime.date.today().isoformat()


def main():
    s = io.open(SM, encoding='utf-8').read()
    have = set(re.findall(r'<loc>(.*?)</loc>', s))
    added = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'learn-*.html'))):
        name = os.path.basename(p)
        url = SITE + name
        if url in have:
            continue
        entry = ('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n'
                 '    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
                 % (url, lastmod(name)))
        s = s.replace('</urlset>', entry + '</urlset>')
        added.append(name)
    if added:
        io.open(SM, 'w', encoding='utf-8').write(s)
    print('sitemap: %d件追加 %s' % (len(added), ' '.join(added) if added else ''))


if __name__ == '__main__':
    main()
