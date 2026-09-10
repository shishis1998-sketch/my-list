from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Make the record edit sheet use the exact same header structure/classes as the timeline chapter sheet.
old_header = '''    <div class="mhdr modal-edit-head">\n      <div class="modal-edit-grip"></div>\n      <div class="modal-edit-headrow">\n        <button type="button" class="modal-edit-action" onclick="closeModal()">取消</button>\n        <div class="mtitle" id="mtitle">添加记录</div>\n        <button type="button" class="modal-edit-action" onclick="saveRec()">完成</button>\n      </div>\n    </div>'''
new_header = '''    <div class="tlsheet-head" id="modalSheetHead">\n      <div class="tlsheet-grip"></div>\n      <div class="tlsheet-headrow">\n        <button type="button" class="tlsheet-action" onclick="closeModal()">取消</button>\n        <div class="tlsheet-title" id="mtitle">添加记录</div>\n        <button type="button" class="tlsheet-action" onclick="saveRec()">完成</button>\n      </div>\n    </div>'''
if old_header not in s:
    raise SystemExit('record edit header not found')
s = s.replace(old_header, new_header, 1)

# 2) Share the timeline header/grip recipe literally, so dimensions and active color cannot drift.
repls = [
    (
        '#tlSheet .tlsheet-head{background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);}',
        '#tlSheet .tlsheet-head,#modal .tlsheet-head{background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);}'
    ),
    (
        '#tlSheet .tlsheet-grip{width:36px;height:4px;margin:0 auto 8px;background:rgba(86,86,90,.34);\n  transition:background .14s ease,transform .14s ease;}',
        '#tlSheet .tlsheet-grip,#modal .tlsheet-grip{width:36px;height:4px;margin:0 auto 8px;background:rgba(86,86,90,.34);\n  transition:background .14s ease,transform .14s ease;}'
    ),
    (
        '#tlSheet .tlsheet-head:active .tlsheet-grip,\n#tlSheet.dragging .tlsheet-grip{background:var(--accent);transform:scaleX(1.08);}',
        '#tlSheet .tlsheet-head:active .tlsheet-grip,#modal .tlsheet-head:active .tlsheet-grip,\n#tlSheet.dragging .tlsheet-grip,#modal .mbox.dragging .tlsheet-grip{background:var(--accent);transform:scaleX(1.08);}'
    ),
    (
        '#tlSheet .tlsheet-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}',
        '#tlSheet .tlsheet-headrow,#modal .tlsheet-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}'
    ),
    (
        '#tlSheet .tlsheet-title{min-width:0;text-align:center;color:var(--text-primary);}',
        '#tlSheet .tlsheet-title,#modal .tlsheet-title{min-width:0;text-align:center;color:var(--text-primary);}'
    ),
]
for old, new in repls:
    if old not in s:
        raise SystemExit('timeline shared rule not found: ' + old[:80])
    s = s.replace(old, new, 1)

# 3) Remove the modal-specific duplicate recipe; it was the source of the mismatch.
start = s.find('/* ADD/EDIT 记录抽屉：与时间线章节编辑统一顶部操作栏和高度 */')
if start == -1:
    raise SystemExit('modal-specific style block not found')
end = s.find('</style>', start)
if end == -1:
    raise SystemExit('style end not found')
block = s[start:end]
# Preserve only the height rule; delete the duplicated header/grip/button CSS.
height_rule = '/* ADD/EDIT 记录抽屉：与时间线章节编辑统一顶部操作栏和高度 */\n#modal .mbox{height:70vh;max-height:70vh;min-height:0;}\n\n'
s = s[:start] + height_rule + s[end:]

# 4) Mobile: the generic .mhdr pseudo-grip still painted a second handle on #modal.
#    Remove that old pseudo handle and let the real .tlsheet-grip be the only one.
old_mobile = '''  #modal .mhdr{position:relative;padding-top:var(--sp-20);}\n  #modal .mhdr::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);\n    width:36px;height:4px;border-radius:2px;background:var(--border);}'''
new_mobile = '''  #modal .tlsheet-head{position:relative;}'''
if old_mobile not in s:
    raise SystemExit('mobile modal pseudo-grip block not found')
s = s.replace(old_mobile, new_mobile, 1)

# 5) Match the timeline sheet height on mobile as well. The earlier mobile #modal .mbox rule used height:auto,
#    and because it appears before the later 70vh rule the two layouts could still diverge across breakpoints.
old_mobile_box = '''  #modal .mbox{\n    width:100%;max-width:100%;height:auto;max-height:min(88vh,100%);\n    border-radius:var(--rxl) var(--rxl) 0 0;\n    box-shadow:0 -4px 24px rgba(0,0,0,.18);\n    transform:translateZ(0);            /* 同 #noteModal：安卓 Chrome 的圆角裁剪 */\n  }'''
new_mobile_box = '''  #modal .mbox{\n    width:100%;max-width:100%;height:70vh;max-height:70vh;min-height:0;\n    border-radius:var(--rxl) var(--rxl) 0 0;\n    box-shadow:0 -4px 24px rgba(0,0,0,.18);\n    transform:translateZ(0);            /* 同 #noteModal：安卓 Chrome 的圆角裁剪 */\n  }'''
if old_mobile_box not in s:
    raise SystemExit('mobile modal box rule not found')
s = s.replace(old_mobile_box, new_mobile_box, 1)

# 6) Bind drag to the new exact header node and toggle the same dragging state used by timeline sheet.
old_bind_fn = '''function bindSheetDrag(box,head,close){\n  if(!box||!head||head._sheetDrag)return;\n  head._sheetDrag=true;\n  let sy=0,dy=0,drag=false;\n  head.addEventListener('pointerdown',e=>{\n    // 电脑上这个弹窗是居中的对话框，没有抓手也无从下拉；只在底部抽屉那套版式里认这一手势\n    if(getComputedStyle(box.parentNode).alignItems!=='flex-end')return;\n    if(e.target.closest('button'))return;      // ✕ 自己有事做，别把它当把手\n    sy=e.clientY;dy=0;drag=true;\n    box.style.transition='none';\n    try{head.setPointerCapture(e.pointerId);}catch(_){}\n  });\n  head.addEventListener('pointermove',e=>{\n    if(!drag)return;\n    dy=Math.max(0,e.clientY-sy);              // 只跟下拉，往上推不动\n    box.style.transform='translateY('+dy+'px)';\n  });\n  const end=()=>{\n    if(!drag)return;\n    drag=false;\n    box.style.transition='';box.style.transform='';\n    if(dy>100)close();\n  };\n  head.addEventListener('pointerup',end);\n  head.addEventListener('pointercancel',end);\n}'''
new_bind_fn = '''function bindSheetDrag(box,head,close){\n  if(!box||!head||head._sheetDrag)return;\n  head._sheetDrag=true;\n  let sy=0,dy=0,drag=false;\n  head.addEventListener('pointerdown',e=>{\n    // 电脑上这个弹窗是居中的对话框，没有抓手也无从下拉；只在底部抽屉那套版式里认这一手势\n    if(getComputedStyle(box.parentNode).alignItems!=='flex-end')return;\n    if(e.target.closest('button'))return;      // 按钮自己有事做，别把它当把手\n    sy=e.clientY;dy=0;drag=true;\n    box.classList.add('dragging');\n    box.style.transition='none';\n    try{head.setPointerCapture(e.pointerId);}catch(_){}\n  });\n  head.addEventListener('pointermove',e=>{\n    if(!drag)return;\n    dy=Math.max(0,e.clientY-sy);              // 只跟下拉，往上推不动\n    box.style.transform='translateY('+dy+'px)';\n  });\n  const end=()=>{\n    if(!drag)return;\n    drag=false;\n    box.classList.remove('dragging');\n    box.style.transition='';box.style.transform='';\n    if(dy>100)close();\n  };\n  head.addEventListener('pointerup',end);\n  head.addEventListener('pointercancel',end);\n}'''
if old_bind_fn not in s:
    raise SystemExit('bindSheetDrag function not found')
s = s.replace(old_bind_fn, new_bind_fn, 1)

old_binding = '''[['modal',()=>closeModal()],\n ['noteModal',()=>closeNoteModal()],\n ['icsColorModal',()=>closeIcsColor()],\n ['icsDelModal',()=>closeIcsDel()]].forEach(([id,close])=>{\n  const dlg=document.getElementById(id);\n  if(dlg) bindSheetDrag(dlg.querySelector('.mbox'), dlg.querySelector('.mhdr'), close);\n});'''
new_binding = '''[['modal',()=>closeModal()],\n ['noteModal',()=>closeNoteModal()],\n ['icsColorModal',()=>closeIcsColor()],\n ['icsDelModal',()=>closeIcsDel()]].forEach(([id,close])=>{\n  const dlg=document.getElementById(id);\n  if(dlg) bindSheetDrag(\n    dlg.querySelector('.mbox'),\n    id==='modal'?document.getElementById('modalSheetHead'):dlg.querySelector('.mhdr'),\n    close\n  );\n});'''
if old_binding not in s:
    raise SystemExit('sheet drag binding block not found')
s = s.replace(old_binding, new_binding, 1)

p.write_text(s, encoding='utf-8')
