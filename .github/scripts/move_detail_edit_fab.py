from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

repls = [
    ('<div class="mhdr modal-edit-head">', '<div class="mhdr tlsheet-head" id="modalSheetHead">'),
    ('<div class="modal-edit-grip"></div>', '<div class="tlsheet-grip"></div>'),
    ('<div class="modal-edit-headrow">', '<div class="tlsheet-headrow">'),
    ('<button type="button" class="modal-edit-action" onclick="closeModal()">取消</button>', '<button type="button" class="tlsheet-action" onclick="closeModal()">取消</button>'),
    ('<div class="mtitle" id="mtitle">添加记录</div>', '<div class="mtitle tlsheet-title" id="mtitle">添加记录</div>'),
    ('<button type="button" class="modal-edit-action" onclick="saveRec()">完成</button>', '<button type="button" class="tlsheet-action" onclick="saveRec()">完成</button>'),
]
for old, new in repls:
    if old not in s:
        raise SystemExit(f'not found: {old}')
    s = s.replace(old, new, 1)

# Reuse the exact visual/interaction recipe of the timeline chapter sheet.
css = r'''
/* 记录编辑顶部：直接照搬时间线章节抽屉的把手/标题栏 */
#modal .tlsheet-head{background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);display:block;flex:0 0 auto;cursor:grab;touch-action:none;user-select:none;-webkit-user-select:none;}
#modal .tlsheet-head:active{cursor:grabbing;}
#modal .tlsheet-grip{width:36px;height:4px;border-radius:2px;margin:0 auto 8px;background:rgba(86,86,90,.34);transition:background .14s ease,transform .14s ease;}
#modal .tlsheet-head:active .tlsheet-grip,#modal .mbox.dragging .tlsheet-grip{background:var(--accent);transform:scaleX(1.08);}
#modal .tlsheet-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}
#modal .tlsheet-title{min-width:0;text-align:center;color:var(--text-primary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
#modal .tlsheet-action{height:36px;padding:0 14px;border:0;border-radius:18px;background:rgba(118,118,128,.08);color:var(--text-primary);font:inherit;font-size:var(--fs-body);font-weight:600;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:background .12s,transform .12s;}
#modal .tlsheet-action:first-child{justify-self:start;}
#modal .tlsheet-action:last-child{justify-self:end;color:var(--accent);}
#modal .tlsheet-action:active{background:rgba(118,118,128,.16);transform:scale(.97);}
'''
if css.strip() not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
