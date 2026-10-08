#!/usr/bin/env python3
"""Builds index.html from chNN.py chapter files + intro.json. Run: python3 build.py (needs old_index.html as shell)."""
import json, html, importlib
e = html.escape
shell = open('index.html').read()  # the previous build is the page shell (head, css, footer)
pre = shell[:shell.index('<main')]; post = shell[shell.index('</main>'):]
import re; pre = re.sub(r'\n\.out\{.*?</style>', '</style>', pre, flags=re.S)
extra = """
.out{direction:ltr;text-align:left;background:#0b0c0f;border:1px solid #2f6f4a;border-radius:10px;padding:12px;overflow-x:auto;font-size:.82rem;line-height:1.5;white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,Menlo,Consolas,monospace;margin:6px 0 14px;color:#c9f0d8}
.olbl,.clbl{font-size:.78rem;color:#9aa0a8;margin:12px 0 3px;direction:ltr;text-align:left}.olbl{color:#5fbf8a}
.ex{border-right:4px solid #F7931A;background:#F7931A0d;border-radius:8px;padding:10px 14px;margin:10px 0;line-height:1.7}
.nt{border-right:4px solid #4a90d9;background:#4a90d90d;border-radius:8px;padding:10px 14px;margin:12px 0;font-size:.92rem;line-height:1.7;color:#cdd3da}
.ver{background:#5fbf8a14;border:1px solid #2f6f4a;border-radius:10px;padding:10px 14px;margin:8px 0 14px;font-size:.9rem;line-height:1.65}
.tb{overflow-x:auto}.tb table{border-collapse:collapse;width:100%;font-size:.9rem}.tb th,.tb td{border:1px solid #24282f;padding:8px 10px;text-align:right;vertical-align:top}.tb th{background:#111317}
.sm{color:#9aa0a8;font-size:.85rem}
.card p{line-height:1.75}
@media(max-width:700px){.tb table{min-width:0}.tb table,.tb tbody,.tb tr,.tb td{display:block;width:100%}.tb tr:first-child{display:none}.tb tr{border:1px solid #24282f;border-radius:12px;margin:10px 0;padding:6px 10px}.tb td{border:0;padding:6px 0}.tb td:before{content:attr(data-l) ": ";color:#F7931A;font-weight:600}}.ch details summary{cursor:pointer;color:#9aa0a8;font-size:.9rem;margin-top:14px}
"""
pre = pre.replace('</style>', extra + '</style>')
_C = json.load(open('content.json'))
I = _C['intro']
chs = _C['chapters']

def block(b):
    k, t = b['k'], b['t']
    if k == 'h': return f'<h4>{e(t)}</h4>'
    if k == 'p': return f'<p>{e(t)}</p>'
    if k == 'code':
        lab = f'<div class="clbl">{e(b["n"])}</div>' if b.get('n') else ''
        return f'{lab}<pre class="code"><code>{e(t)}</code></pre>'
    if k == 'out': return f'<div class="olbl">פלט (מהרצה אמיתית, כמוצג)</div><pre class="out">{e(t)}</pre>'
    if k == 'ex': return f'<div class="ex"><strong>תרגיל</strong> {e(t.split(":",1)[1].strip() if ":" in t[:12] else t)}</div>'
    if k == 'ul': return '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in t) + '</ul>'
    if k == 'tbl':
        h = ''.join(f'<th>{e(c)}</th>' for c in t[0])
        r = ''.join('<tr>' + ''.join(f'<td data-l="{e(t[0][i])}">{e(c)}</td>' for i, c in enumerate(row)) + '</tr>' for row in t[1:])
        return f'<div class="tb"><table><tr>{h}</tr>{r}</table></div>'
    if k == 'note': return f'<div class="nt">{e(t)}</div>'
    raise ValueError(k)

def chapter(c):
    p = c['proj']
    src = ''.join(f'<li><a class="src" href="{e(u)}" rel="noopener" target="_blank">{e(t)}</a></li>' for t, u in c['src'])
    return f'''<article class="card ch" id="c{c['id']}"><h3>פרק {c['id']}: {e(c['title'])}</h3><p class="hrs">{e(c['hours'])}</p>
<div class="ver"><strong>מה נבדק בפועל:</strong> {e(c['verified'])}</div>
{''.join(block(b) for b in c['blocks'])}
<div class="proj"><p class="lbl">פרויקט הפרק: {e(p['name'])}</p><p><span class="lbl">נתונים אמיתיים:</span> {e(p['data'])}</p><p><span class="lbl">הוכחה שזה עובד:</span> {e(p['proof'])}</p></div>
<details><summary>מקורות לציטוט (לא קריאת חובה, כל החומר כבר בפרק)</summary><ul class="res">{src}</ul></details></article>'''

WT = {1:"שבוע 1: יסודות וחיפוש סמנטי",2:"שבוע 2: RAG, סוכנים ו-MCP",3:"שבוע 3: פרודקשן, הערכה ועלויות",4:"שבוע 4: פרויקט גמר ולמידה מתמשכת"}
SCHED = ["בכל שבוע: חמישה מפגשים של שעה בימי חול ומפגש אחד של כ-5 שעות בסוף שבוע. כל שעה כוללת קריאה של חלק בפרק, הרצה של הקוד והתחלה של התרגיל.","הפרקים נכתבו כך שאפשר לעבוד איתם בלי לצאת מהדף. הקוד מועתק כמו שהוא, והפלט שמופיע אחריו הוא מה שאמור להתקבל."]
body = []; toc = []
for w in (1,2,3,4):
    toc.append(f'<a href="#w{w}">{e(WT[w])}</a>')
    body.append(f'<section class="section" id="w{w}"><div class="wrap"><h2 class="weekt">{e(WT[w])}</h2>' + ''.join(chapter(c) for c in chs if c['week']==w) + '</div></section>')
setup = ''.join(f'<li>{e(s)}</li>' for s in I['setup'])
sched = ''.join(f'<li>{e(s)}</li>' for s in SCHED)
ctoc = ''.join(f'<li><a class="src" href="#c{c["id"]}">פרק {c["id"]}: {e(c["title"])}</a> <span class="sm"> · {e(c["hours"])}</span></li>' for c in chs)
mid = f'''<main id="main"><div class="hero"><div class="wrap"><div class="eyebrow">AI ENGINEERING ROADMAP 2026 · מדריך עצמאי של 4 שבועות</div><h1>תכנית חודש ל-AI Engineering</h1>
<p class="lead">תשעה פרקים, ארבעה שבועות. כל הלימוד בתוך הדף: הסבר, מקרה שימוש, קוד להעתקה, פלט צפוי ותרגיל. הנתונים בפרויקטים נמשכים מהרשת, אבל אין שום חומר קריאה חיצוני.</p>
<div class="box"><p><strong>הנחות:</strong> {e(I['assume'])}</p></div>
<div class="box"><p><strong>הכנה (חצי שעה, לפני מפגש 1):</strong></p><ul>{setup}</ul></div>
<div class="box"><p><strong>איך הכול מתחבר:</strong> {e(I['chain'])}</p></div>
<div class="box"><p><strong>איך עובדים עם המדריך:</strong></p><ul>{sched}</ul></div>
<div class="box"><p><strong>תוכן הפרקים:</strong></p><ul>{ctoc}</ul></div>
<p class="note">בכל פרק מסומן מה הורץ ונבדק בפועל בעת הכתיבה (8.10.2026) ומה לא הורץ. קטעים שלא הורצו מסומנים כך במפורש. תיעוד משתנה, ולכן אם פקודה לא עובדת, גרסת התיעוד הנוכחית קובעת.</p>
<div class="toc">{''.join(toc)}</div></div></div>
{''.join(body)}'''
open('index.html','w').write(pre + mid + post)
print('built', len(chs), 'chapters', len(pre+mid+post), 'bytes')
