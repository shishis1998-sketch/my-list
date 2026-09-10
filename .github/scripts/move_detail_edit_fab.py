from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_css = '''#modal .modal-edit-head{display:block;background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);flex:0 0 auto;}\n#modal .modal-edit-grip{width:36px;height:4px;border-radius:2px;margin:0 auto 8px;background:rgba(86,86,90,.34);}'''
new_css = '''#modal .modal-edit-head{display:block;background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);flex:0 0 auto;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none;}\n#modal .modal-edit-head:active{cursor:grabbing;}\n#modal .modal-edit-grip{width:36px;height:4px;border-radius:2px;margin:0 auto 8px;background:rgba(86,86,90,.34);transition:background .14s ease,transform .14s ease;}\n#modal .modal-edit-head:active .modal-edit-grip,#modal .mbox.dragging .modal-edit-grip{background:var(--accent);transform:scaleX(1.08);}'''
if old_css not in s:
    raise SystemExit('modal grip css not found')
s = s.replace(old_css, new_css, 1)

old_bind = '''[['noteModal',()=>closeNoteModal()],\n ['icsColorModal',()=>closeIcsColor()],\n ['icsDelModal',()=>closeIcsDel()]].forEach(([id,close])=>{'''
new_bind = '''[['modal',()=>closeModal()],\n ['noteModal',()=>closeNoteModal()],\n ['icsColorModal',()=>closeIcsColor()],\n ['icsDelModal',()=>closeIcsDel()]].forEach(([id,close])=>{'''
if old_bind not in s:
    raise SystemExit('sheet drag binding list not found')
s = s.replace(old_bind, new_bind, 1)

# bindSheetDrag already adds/removes the `dragging` class on the box while moving;
# adding #modal to that shared binding gives this sheet the same downward drag-to-close behavior.
p.write_text(s, encoding='utf-8')
