from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacements = [
    ('<div class="dt-card dt-hd" onclick="editFromDetail(event)" data-edit="f-name">', '<div class="dt-card dt-hd">'),
    ('<div class="dt-card" onclick="editFromDetail(event)" data-edit="f-watch">', '<div class="dt-card">'),
    ('<div class="dt-card" onclick="editFromDetail(event)" data-edit="tinput">', '<div class="dt-card">'),
]
for old, new in replacements:
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'Expected exactly one occurrence, got {count}: {old}')
    s = s.replace(old, new, 1)

old = '''    ${tagsH?`<div class="dt-tags">${tagsH}</div>`:'<div class="dt-tl-empty">还没有标签</div>'}
  </div>`:''}'''
new = '''    ${tagsH?`<div class="dt-tags">${tagsH}</div>`:'<div class="dt-tl-empty">还没有标签</div>'}
  </div>
  <button class="dt-fab dt-edit-fab" onclick="openEdit(detailId)" aria-label="编辑记录"><svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>`:''}'''
count = s.count(old)
if count != 1:
    raise SystemExit(f'Expected one overview tag-card ending, got {count}')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
