from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''#modal .mbox{height:70vh;max-height:70vh;min-height:0;}\n#modal .modal-edit-head'''
new = '''#modal .mbox{height:70vh;max-height:70vh;min-height:0;background:var(--bg);}\n#modal .modal-edit-head'''

# Current version now reuses tlsheet-head instead of modal-edit-head, so handle both safely.
if old in s:
    s = s.replace(old, new, 1)
else:
    old2 = '''#modal .mbox{height:70vh;max-height:70vh;min-height:0;}'''
    new2 = '''#modal .mbox{height:70vh;max-height:70vh;min-height:0;background:var(--bg);}'''
    if old2 not in s:
        raise SystemExit('record edit sheet height rule not found')
    s = s.replace(old2, new2, 1)

# The shared timeline header rule paints the header white. Period edit uses the gray sheet background,
# so override only this modal's header to inherit the same gray surface while keeping cards/fields white.
marker = '</style>'
css = '''\n/* 概览编辑抽屉：背景与编辑经期一致（--bg 灰底），表单控件继续保持白色 surface。 */\n#modal .tlsheet-head{background:var(--bg);}\n'''
if css.strip() not in s:
    if marker not in s:
        raise SystemExit('style end not found')
    s = s.replace(marker, css + marker, 1)

p.write_text(s, encoding='utf-8')
