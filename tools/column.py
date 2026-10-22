#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drafts/*.md を、既存コラムと同じ構造の learn-<slug>.html に変換する。

使い方:
    python3 tools/column.py drafts/foo.md          # 1本を変換
    python3 tools/column.py --all                  # drafts/ 配下すべて
書き方は COLUMN-HOWTO.md を参照。
"""
import io, os, re, sys, json, html, datetime, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, 'tools', 'column-template.html')
SITE = 'https://visuallabo.com/'
DISCLAIMER = ('※ VISUAL LABOは医療機関ではなく、施術は医療行為ではありません。'
              '効果・感じ方・変化には個人差があり、すべての方に同様の結果をお約束するものではありません。')


def esc(t):
    return html.escape(t, quote=True)


def inline(t):
    """段落内の記法。**太字** と [文字](url) だけ。"""
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)',
               r'<a href="\2" style="border-bottom:1px solid var(--gold-d)">\1</a>', t)
    return t


def parse_front(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not m:
        raise SystemExit('front matter（--- で囲んだ先頭ブロック）がありません')
    meta, body = {}, m.group(2)
    key = None
    for line in m.group(1).split('\n'):
        if not line.strip():
            continue
        if re.match(r'^\s+\S', line) and key:
            meta.setdefault(key + '_list', []).append(line.strip())
            continue
        k, _, v = line.partition(':')
        key = k.strip()
        meta[key] = v.strip()
    return meta, body


def split_panels(body):
    """@ラベル ごとにパネルへ分ける。"""
    parts = re.split(r'^@(.+)$', body, flags=re.M)
    if len(parts) < 3:
        raise SystemExit('本文に @ラベル が1つもありません')
    panels = []
    for i in range(1, len(parts), 2):
        panels.append((parts[i].strip(), parts[i + 1].strip()))
    return panels


def render_blocks(src, heads):
    """通常パネル。## を .blk + <h2> に、### を <h3> に。"""
    out, buf, cur = [], [], None

    def flush_para():
        if buf:
            out.append('<p>' + '<br>'.join(inline(x) for x in buf) + '</p>')
            del buf[:]

    def close():
        flush_para()
        if cur is not None:
            out.append('</div>')

    lines = src.split('\n')
    i = 0
    ul = False
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith('## '):
            if ul:
                out.append('</ul>'); ul = False
            close()
            t = ln[3:].strip()
            hid = 'h%d' % (len(heads) + 1)
            heads.append((hid, t))
            cur = hid
            out.append('<div class="blk" id="%s"><h2>%s</h2>' % (hid, esc(t)))
        elif ln.startswith('### '):
            if ul:
                out.append('</ul>'); ul = False
            flush_para()
            out.append('<h3>%s</h3>' % esc(ln[4:].strip()))
        elif ln.startswith('- '):
            flush_para()
            if not ul:
                out.append('<ul>'); ul = True
            out.append('<li>%s</li>' % inline(ln[2:].strip()))
        elif not ln:
            if ul:
                out.append('</ul>'); ul = False
            flush_para()
        else:
            if ul:
                out.append('</ul>'); ul = False
            buf.append(ln)
        i += 1
    if ul:
        out.append('</ul>')
    close()
    return '\n'.join(out)


def render_faq(src):
    items, q, a = [], None, []
    for ln in src.split('\n'):
        if ln.startswith('### '):
            if q:
                items.append((q, ' '.join(a).strip()))
            q, a = ln[4:].strip(), []
        elif ln.strip():
            a.append(ln.strip())
    if q:
        items.append((q, ' '.join(a).strip()))
    if not items:
        raise SystemExit('よくある質問パネルに ### 質問 がありません')
    cards = '\n'.join(
        '      <details><summary>%s</summary><div class="a">%s</div></details>'
        % (esc(q), inline(a)) for q, a in items)
    blk = ('<div class="blk" id="faq"><h2>よくあるご質問</h2><div class="faqd">\n'
           + cards + '\n</div></div>')
    return blk, items


def build(path):
    text = io.open(path, encoding='utf-8').read()
    meta, body = parse_front(text)
    need = ['slug', 'title', 'h1', 'description', 'published']
    miss = [k for k in need if not meta.get(k)]
    if miss:
        raise SystemExit('front matter に %s がありません' % '・'.join(miss))

    slug = meta['slug']
    out_name = meta.get('out') or ('learn-%s.html' % slug)
    heads = []
    panels = split_panels(body)

    tabs, body_parts, faq_items = [], [], []
    for n, (label, src) in enumerate(panels, 1):
        pid = 'page-%d' % n
        tabs.append('    <a class="choice-tab" data-tab href="#%s">%s</a>' % (pid, esc(label)))
        if 'よくある質問' in label:
            blk, faq_items = render_faq(src)
            body_parts.append('<div id="%s" data-tab-panel>\n%s\n</div>' % (pid, blk))
        else:
            body_parts.append('<div id="%s" data-tab-panel>\n%s\n</div>'
                              % (pid, render_blocks(src, heads)))

    # 目次を最初のパネルの末尾に差し込む
    if heads:
        toc = ('<nav class="toc"><div class="tt">CONTENTS</div><ol>'
               + ''.join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in heads)
               + '</ol></nav>')
        body_parts[0] = body_parts[0][:-len('\n</div>')] + '\n' + toc + '\n</div>'

    # 免責は必ず最後の本文パネルに入れる
    last = len(body_parts) - 1 if not faq_items else max(0, len(body_parts) - 2)
    body_parts[last] = (body_parts[last][:-len('\n</div>')]
                        + '\n<p style="font-size:12px;color:var(--ink-mute)">%s</p>\n</div>' % DISCLAIMER)

    rel = []
    for line in meta.get('related_list', []):
        f = [x.strip() for x in line.split('|')]
        if len(f) != 4:
            raise SystemExit('related の行は href|ラベル|見出し|説明 の4つに区切ってください: ' + line)
        rel.append('      <a class="rv" href="%s"><span class="nl">%s</span>'
                   '<span class="nt">%s →</span><span class="nd">%s</span></a>'
                   % (esc(f[0]), esc(f[1]), esc(f[2]), esc(f[3])))
    if len(rel) != 3:
        raise SystemExit('related は3本ちょうどにしてください（いまは%d本）' % len(rel))

    hero, hpos = (meta.get('hero') or 'images/menu-ems-photo.webp|center 35%').split('|')
    h1raw = meta['h1']
    h1 = ('<h1>%s<span class="jp">%s</span></h1>' % tuple(esc(x) for x in h1raw.split('|', 1))
          if '|' in h1raw else '<h1>%s</h1>' % esc(h1raw))
    h1 = h1[len('<h1>'):-len('</h1>')]

    plain_title = re.split(r'[｜|]', meta['title'])[0]
    ld_article = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": plain_title, "description": meta['description'],
        "image": SITE + (meta.get('og_image') or 'images/mysticore-salon.webp'),
        "author": {"@type": "Organization", "name": "VISUAL LABO 新橋店"},
        "publisher": {"@type": "Organization", "name": "VISUAL LABO 新橋店"},
        "datePublished": meta['published'],
        "dateModified": meta.get('modified') or meta['published'],
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + out_name},
    }, ensure_ascii=False, indent=1)
    ld_faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer",
                                           "text": re.sub(r'\*\*(.+?)\*\*', r'\1', a)}}
                       for q, a in faq_items],
    }, ensure_ascii=False, indent=1) if faq_items else ''
    ld_crumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": SITE},
            {"@type": "ListItem", "position": 2,
             "name": meta.get('crumb_name') or "学び（BODY LABO）",
             "item": SITE + (meta.get('crumb_url') or "learn.html")},
            {"@type": "ListItem", "position": 3, "name": plain_title, "item": SITE + out_name},
        ],
    }, ensure_ascii=False, indent=1)

    tpl = io.open(TEMPLATE, encoding='utf-8').read()
    vals = {
        'TITLE': esc(meta['title']),
        'DESCRIPTION': esc(meta['description']),
        'OG_TITLE': esc(meta.get('og_title') or meta['title']),
        'OG_DESCRIPTION': esc(meta.get('og_description') or meta['description']),
        'OG_IMAGE': esc(meta.get('og_image') or 'images/mysticore-salon.webp'),
        'URL': out_name,
        'HERO_IMG': esc(hero), 'HERO_POS': esc(hpos),
        'HERO_ALT': esc(meta.get('hero_alt') or (plain_title + '｜VISUAL LABO 新橋店')),
        'H1': h1, 'SUB': esc(meta.get('sub') or ''),
        'TAG': esc(meta.get('tag') or 'BODY LABO ／ 学び'),
        'BACK_HREF': esc(meta.get('back_href') or 'learn.html'),
        'BACK_LABEL': esc(meta.get('back_label') or '学びへ'),
        'TABS': '\n' + '\n'.join(tabs) + '\n  ',
        'BODY': '\n' + '\n'.join(body_parts) + '\n    ',
        'RELATED': '\n' + '\n'.join(rel),
        'JSONLD_ARTICLE': ld_article, 'JSONLD_FAQ': ld_faq, 'JSONLD_CRUMB': ld_crumb,
    }
    for k, v in vals.items():
        tpl = tpl.replace('{{%s}}' % k, v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', tpl)
    assert not left, '未置換のプレースホルダ: %s' % left
    if not faq_items:
        tpl = re.sub(r'<script type="application/ld\+json">\s*\n\s*\n\s*</script>\n?', '', tpl)
    io.open(os.path.join(ROOT, out_name), 'w', encoding='utf-8').write(tpl)
    return out_name


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    all_mode = args[0] == '--all'
    files = sorted(glob.glob(os.path.join(ROOT, 'drafts', '*.md'))) if all_mode else args
    made = []
    for f in files:
        # _ で始まるファイルは見本。--all のときだけ飛ばす
        if all_mode and os.path.basename(f).startswith('_'):
            continue
        made.append(build(f))
    print('\n'.join(made) if made else '変換対象がありません')


if __name__ == '__main__':
    main()
