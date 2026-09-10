from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_marker = '/* record edit grip explicit pressed state */'
if css_marker not in s:
    s = s.replace('</style>', '''\n/* record edit grip explicit pressed state */\n#modal .tlsheet-grip.is-pressed{background:var(--accent);transform:scaleX(1.08);}\n</style>''', 1)

js_marker = '/* record edit grip explicit pointer feedback */'
if js_marker not in s:
    insert_before = '</script>'
    js = r'''\n/* record edit grip explicit pointer feedback */\n(function(){\n  const head=document.getElementById('modalSheetHead');\n  if(!head || head.dataset.gripFeedbackBound==='1') return;\n  const grip=head.querySelector('.tlsheet-grip');\n  if(!grip) return;\n  head.dataset.gripFeedbackBound='1';\n  const on=()=>grip.classList.add('is-pressed');\n  const off=()=>grip.classList.remove('is-pressed');\n  head.addEventListener('pointerdown',e=>{\n    if(e.target.closest('button')) return;\n    on();\n  });\n  head.addEventListener('pointerup',off);\n  head.addEventListener('pointercancel',off);\n  head.addEventListener('lostpointercapture',off);\n  window.addEventListener('pointerup',off);\n})();\n'''
    pos = s.rfind(insert_before)
    if pos == -1:
        raise SystemExit('script end not found')
    s = s[:pos] + js + s[pos:]

p.write_text(s, encoding='utf-8')
