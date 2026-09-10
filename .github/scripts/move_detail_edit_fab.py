from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_header = '''    <div class="mhdr">
      <div class="mtitle" id="mtitle">添加记录</div>
      <button class="mclose" onclick="closeModal()">✕</button>
    </div>'''
new_header = '''    <div class="mhdr modal-edit-head">
      <div class="modal-edit-grip"></div>
      <div class="modal-edit-headrow">
        <button type="button" class="modal-edit-action" onclick="closeModal()">取消</button>
        <div class="mtitle" id="mtitle">添加记录</div>
        <button type="button" class="modal-edit-action" onclick="saveRec()">完成</button>
      </div>
    </div>'''
if old_header not in s:
    raise SystemExit('Edit modal header not found')
s = s.replace(old_header, new_header, 1)

old_footer = '''    </div><!-- /mbody -->
    <div class="mftr">
      <button class="btn btn-g" onclick="closeModal()">取消</button>
      <button class="btn btn-p" onclick="saveRec()">保存</button>
    </div>
  </div>
</div>

<!-- ===== CAT MANAGER ===== -->'''
new_footer = '''    </div><!-- /mbody -->
  </div>
</div>

<!-- ===== CAT MANAGER ===== -->'''
if old_footer not in s:
    raise SystemExit('Edit modal footer not found')
s = s.replace(old_footer, new_footer, 1)

css = r'''
/* ADD/EDIT 记录抽屉：与时间线章节编辑统一顶部操作栏和高度 */
#modal .mbox{height:70vh;max-height:70vh;min-height:0;}
#modal .modal-edit-head{display:block;background:var(--surface);padding:7px 16px 12px;border-bottom:1px solid var(--border-soft);flex:0 0 auto;}
#modal .modal-edit-grip{width:36px;height:4px;border-radius:2px;margin:0 auto 8px;background:rgba(86,86,90,.34);}
#modal .modal-edit-headrow{display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;gap:8px;}
#modal .modal-edit-headrow .mtitle{min-width:0;text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
#modal .modal-edit-action{height:36px;padding:0 14px;border:0;border-radius:18px;background:rgba(118,118,128,.08);color:var(--text-primary);font:inherit;font-size:var(--fs-body);font-weight:600;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:background .12s,transform .12s;}
#modal .modal-edit-action:first-child{justify-self:start;}
#modal .modal-edit-action:last-child{justify-self:end;color:var(--accent);}
#modal .modal-edit-action:active{background:rgba(118,118,128,.16);transform:scale(.97);}
'''
marker = '</style>'
if css.strip() not in s:
    if marker not in s:
        raise SystemExit('style end not found')
    s = s.replace(marker, css + '\n' + marker, 1)

p.write_text(s, encoding='utf-8')
