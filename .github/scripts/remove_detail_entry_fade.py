from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old=""".detail-view.open{display:flex;flex-direction:column;flex:1;overflow-y:auto;background:var(--bg);\n  animation:mboxPopIn var(--nav-dur) var(--nav-ease);}"""
new=""".detail-view.open{display:flex;flex-direction:column;flex:1;overflow-y:auto;background:var(--bg);\n  /* 详情页直接显示，不在整个父容器上做淡入。\n     FAB 位于 detailRoot 内，父级 opacity 动画会连固定按钮一起淡入，\n     单独关闭 .dt-fab 自身 transition 也挡不住父级透明度。 */\n  animation:none;}"""
if old not in s:
    if new in s:
        raise SystemExit('already patched')
    raise SystemExit('detail-view open animation block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
