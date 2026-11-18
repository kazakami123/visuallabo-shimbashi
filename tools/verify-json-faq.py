#!/usr/bin/env python3
"""Validate JSON-LD blocks and compare visible FAQ answers with FAQPage data."""
import glob
import html
import json
import re


def norm(text):
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', '', html.unescape(text))


json_errors = 0
faq_mismatches = 0
blocks = 0
for path in sorted(glob.glob('*.html')):
    source = open(path, encoding='utf-8').read()
    visible = {}
    for question, answer in re.findall(
            r'<button class="fq">(.*?)</button><div class="fa">(.*?)</div>',
            source, re.S):
        visible[norm(question)] = norm(answer)
    for question, answer in re.findall(
            r'<details[^>]*>.*?<summary>(.*?)</summary>(.*?)</details>',
            source, re.S):
        visible[norm(question)] = norm(answer)
    for raw in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        blocks += 1
        try:
            data = json.loads(raw)
        except Exception as exc:
            print('JSON NG', path, exc)
            json_errors += 1
            continue
        for item in data if isinstance(data, list) else [data]:
            if item.get('@type') != 'FAQPage':
                continue
            for entry in item.get('mainEntity', []):
                question = norm(entry.get('name', ''))
                answer = norm(entry.get('acceptedAnswer', {}).get('text', ''))
                if question not in visible:
                    print('FAQ visible missing', path, entry.get('name', ''))
                    faq_mismatches += 1
                elif visible[question] != answer:
                    print('FAQ mismatch', path, entry.get('name', ''))
                    faq_mismatches += 1

print('JSON-LD blocks', blocks, '/ JSON errors', json_errors,
      '/ FAQ mismatches', faq_mismatches)
raise SystemExit(1 if json_errors or faq_mismatches else 0)
