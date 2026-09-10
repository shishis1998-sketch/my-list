from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# The record edit sheet previously only imitated the timeline header while still
# carrying .mhdr/.mtitle, so global modal styles continued to affect spacing and
# typography. Use the exact same header structure/classes as #tlSheet instead.
s = s.replace(
    '<div class="mhdr tlsheet-head" id="modalSheetHead">',
    '<div class="tlsheet-head" id="modalSheetHead">',
    1,
)
s = s.replace(
    '<div class="mtitle tlsheet-title" id="mtitle">添加记录</div>',
    '<div class="tlsheet-title" id="mtitle">添加记录</div>',
    1,
)

# Remove old modal-only header imitation blocks if present. The new rules below
# share one selector list with #tlSheet, so both sheets literally use one recipe.
start = s.find('/* 记录编辑顶部：直接照搬时间线章节抽屉的把手/标题栏 */')
if start != -1:
    end = s.find('</style>', start)
    if end == -1:
        raise SystemExit('style end not found after modal header block')
    s = s[:start] + s[end:]

# Replace the original #tlSheet-only visual rules with shared rules for #tlSheet
# and #modal. This avoids two almost-the-same CSS implementations drifting apart.
repls = {
'''#tlSheet .tlsheet-head{background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);}''':
'''#tlSheet .tlsheet-head,#modal .tlsheet-head{background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);}''',
'''#tlSheet .tlsheet-grip{width:36px;height:4px;margin:0 auto 8px;background:rgba(86,86,90,.34);\n  transition:background .14s ease,transform .14s ease;}''':
'''#tlSheet .tlsheet-grip,#modal .tlsheet-grip{width:36px;height:4px;margin:0 auto 8px;background:rgba(86,86,90,.34);\n  transition:background .14s ease,transform .14s ease;}''',
'''#tlSheet .tlsheet-head:active .tlsheet-grip,\n#tlSheet.dragging .tlsheet-grip{background:var(--accent);transform:scaleX(1.08);}''':
'''#tlSheet .tlsheet-head:active .tlsheet-grip,#modal .tlsheet-head:active .tlsheet-grip,\n#tlSheet.dragging .tlsheet-grip,#modal .mbox.dragging .tlsheet-grip{background:var(--accent);transform:scaleX(1.08);}''',
'''#tlSheet .tlsheet-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}''':
'''#tlSheet .tlsheet-headrow,#modal .tlsheet-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}''',
'''#tlSheet .tlsheet-title{min-width:0;text-align:center;color:var(--text-primary);}''':
'''#tlSheet .tlsheet-title,#modal .tlsheet-title{min-width:0;text-align:center;color:var(--text-primary);}'''
}
for old, new in repls.items():
    if old in s:
        s = s.replace(old, new, 1)
    elif new not in s:
        raise SystemExit('shared timeline rule not found: ' + old[:60])

# Record sheet keeps the same 70vh height as the timeline edit sheet.
if '#modal .mbox{height:70vh;max-height:70vh;min-height:0;}' not in s:
    s = s.replace('</style>', '\n#modal .mbox{height:70vh;max-height:70vh;min-height:0;}\n</style>', 1)

# The generic drag binder used to locate modal's header via .mhdr. Now that the
# extra .mhdr class is intentionally gone, bind the exact #modalSheetHead node.
old_bind = "const dlg=document.getElementById(id);\n  if(dlg) bindSheetDrag(dlg.querySelector('.mbox'), dlg.querySelector('.mhdr'), close);"
new_bind = "const dlg=document.getElementById(id);\n  if(dlg) bindSheetDrag(dlg.querySelector('.mbox'), id==='modal'?document.getElementById('modalSheetHead'):dlg.querySelector('.mhdr'), close);"
if old_bind in s:
    s = s.replace(old_bind, new_bind, 1)
elif new_bind not in s:
    raise SystemExit('shared sheet drag binding block not found')

p.write_text(s, encoding='utf-8')
