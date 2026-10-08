#!/usr/bin/env python3
"""Reads plan.json and writes index.html (static, Hebrew RTL). Run: python3 build.py"""
import json, html
e = html.escape
css = open('base.css').read() + """
.card{background:var(--card,#111317);border:1px solid #24282f;border-radius:16px;padding:20px;margin:16px 0}
.card h3{margin:0 0 6px;font-size:1.2rem}.hrs{color:#F7931A;font-weight:600;font-size:.9rem;margin:0 0 10px}
.card h4{margin:16px 0 6px;font-size:1rem;color:#fff}.card ol,.card ul{padding-right:20px}.card li{margin:7px 0;line-height:1.65}
.proj{border:1px solid #F7931A55;border-radius:12px;padding:14px;margin-top:14px;background:#F7931A0d}
.proj p{margin:6px 0}.lbl{color:#F7931A;font-weight:600}
.res a,.src{color:#F7931A;text-decoration:none;word-break:break-word}.res li{direction:rtl}
.note{color:#9aa0a8;font-size:.9rem}.weekt{margin-top:40px}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.toc a{border:1px solid #24282f;border-radius:999px;padding:6px 14px;font-size:.85rem;color:#9aa0a8;text-decoration:none}
.box{background:#111317;border:1px solid #24282f;border-radius:14px;padding:16px;margin:14px 0}
"""
P = json.load(open('plan.json'))
I = P['intro']; T = P['topics']
def res(rs): return '<ul class="res">' + ''.join(f'<li><a href="{e(r["u"])}" rel="noopener" target="_blank">{e(r["t"])}</a></li>' for r in rs) + '</ul>'
def topic(t):
    p = t['proj']
    days = ''.join(f'<li>{e(d)}</li>' for d in t['days'])
    return f'''<article class="card" id="t{t['id']}"><h3>נושא {t['id']}: {e(t['title'])}</h3><p class="hrs">{e(t['hours'])}</p>
<p>{e(t['learn'])}</p><h4>מה עושים, מפגש אחר מפגש</h4><ul>{days}</ul>
<h4>מקורות חינמיים</h4>{res(t['res'])}
<div class="proj"><p class="lbl">פרויקט: {e(p['name'])}</p><p><span class="lbl">נתונים אמיתיים:</span> {e(p['data'])}</p><p><span class="lbl">מה בונים:</span> {e(p['build'])}</p><p><span class="lbl">מה מתקבל:</span> {e(p['out'])}</p><p><span class="lbl">איך זה מוכיח את היכולת:</span> {e(p['proof'])}</p></div></article>'''
WT = {1:"שבוע 1: יסודות וחיפוש סמנטי",2:"שבוע 2: RAG וסוכנים",3:"שבוע 3: פרודקשן, הערכה והסקה",4:"שבוע 4: פרויקט מסכם ולמידה מתמשכת"}
body = []; toc = []
for w in (1,2,3,4):
    toc.append(f'<a href="#w{w}">{e(WT[w])}</a>')
    body.append(f'<section class="section" id="w{w}"><div class="wrap"><h2 class="weekt">{e(WT[w])}</h2>' + ''.join(topic(t) for t in T if t['week']==w) + '</div></section>')
setup = ''.join(f'<li>{e(s)}</li>' for s in I['setup'])
page = f'''<!DOCTYPE html>
<html dir="rtl" lang="he"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/><meta content="#030304" name="theme-color"/><meta content="תכנית עבודה לחודש: תשעת נושאי מפת הדרכים של AI Engineering 2026, עם פרויקט על נתוני אמת לכל נושא" name="description"/><title>תכנית חודש ל-AI Engineering 2026 | DATA&amp;AI</title><link href="https://fonts.googleapis.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet"/><style>{css}</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="https://rkinstinct.github.io/data-ai-hub/">DATA<span style="color:#F7931A">&amp;</span>AI <b>/ תכנית חודש</b></a></div></header>
<main id="main"><div class="hero"><div class="wrap"><div class="eyebrow">AI ENGINEERING ROADMAP 2026 · תכנית של 4 שבועות</div><h1>תכנית חודש ל-AI Engineering</h1>
<p class="lead">תשעה נושאים, ארבעה שבועות, ופרויקט אחד על נתוני אמת לכל נושא. הפרויקטים נשרשרים למאגר מסכם אחד.</p>
<div class="box"><p><strong>הנחות:</strong> {e(I['assume'])}</p></div>
<div class="box"><p><strong>הכנה (חצי שעה, לפני מפגש 1):</strong></p><ul>{setup}</ul></div>
<div class="box"><p><strong>איך הכול מתחבר:</strong> {e(I['chain'])}</p></div>
<p class="note">{e(I['resources_src'])}</p>
<div class="toc">{''.join(toc)}</div></div></div>
{''.join(body)}</main>
<footer><div class="wrap"><span>מבוסס על מפת הדרכים AI Engineering Roadmap 2026. כל המקורות ציבוריים וחינמיים.</span></div><p class="rights-line" style="text-align:center;margin:18px auto 0;padding:0 16px;font-size:.92em;opacity:.9;width:100%">© כל הזכויות שמורות לראובן קזורר</p></footer></body></html>'''
open('index.html','w').write(page)
print('built', len(T), 'topics', len(page), 'bytes')
