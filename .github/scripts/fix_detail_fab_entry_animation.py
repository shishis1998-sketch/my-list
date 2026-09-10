from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# The FAB should still animate when scroll direction hides/shows it, but not when
# entering a detail page. During renderDetail() the old global fab-hidden class is
# removed after the FAB node is inserted; because .dt-fab has opacity/transform
# transitions, that removal currently looks like an unwanted fade-in.
css_anchor = '''  .dt-fab:active{transform:scale(.92);}\n  .dt-fab svg{width:20px;height:20px;}'''
css_new = '''  .dt-fab:active{transform:scale(.92);}\n  .dt-fab svg{width:20px;height:20px;}\n  /* 进入详情页时按钮直接就位，不播放淡入；滚动隐藏/恢复仍沿用 .dt-fab 的 transition。 */\n  body.detail-fab-entering .dt-fab{transition:none!important;}'''
if css_new not in s:
    if css_anchor not in s:
        raise SystemExit('dt-fab CSS anchor not found')
    s = s.replace(css_anchor, css_new, 1)

old_open = '''function openDetail(id){\n  const item=data.find(d=>d.id===id); if(!item) return;\n  detailId=id; dtTab='info';\n  renderDetail();\n  document.body.classList.remove('tabs-hidden');   // 同 openCalendar：这页底栏是唯一导航\n  document.body.classList.add('detail-open');'''
new_open = '''function openDetail(id){\n  const item=data.find(d=>d.id===id); if(!item) return;\n  detailId=id; dtTab='info';\n  // 进详情页这一帧禁用 FAB 自身 transition：renderDetail 会清掉 fab-hidden，\n  // 若不先关 transition，按钮就会从上一个页面遗留的隐藏态淡入/滑入。\n  // 下一帧立即恢复，因此用户真正上下滚动时的隐藏/出现动效完全不受影响。\n  document.body.classList.add('detail-fab-entering');\n  renderDetail();\n  requestAnimationFrame(()=>document.body.classList.remove('detail-fab-entering'));\n  document.body.classList.remove('tabs-hidden');   // 同 openCalendar：这页底栏是唯一导航\n  document.body.classList.add('detail-open');'''
if new_open not in s:
    if old_open not in s:
        raise SystemExit('openDetail block not found')
    s = s.replace(old_open, new_open, 1)

p.write_text(s, encoding='utf-8')
