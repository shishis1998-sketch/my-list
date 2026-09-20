from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        """.rg-head{position:relative;z-index:4;display:flex;align-items:center;gap:var(--sp-10);padding:calc(10px + env(safe-area-inset-top)) var(--sp-14) 10px;
  background:var(--bg);border-bottom:1px solid var(--border-soft);}
.rg-back{display:grid;place-items:center;width:40px;height:40px;padding:0;border:0;background:transparent;
  color:var(--text-primary);font-size:32px;line-height:1;cursor:pointer;}
.rg-title{min-width:0;flex:1;font-size:var(--fs-headline);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.rg-controls{position:relative;z-index:4;display:flex;align-items:center;gap:var(--sp-8);padding:10px var(--sp-14);background:var(--bg);}""",
        """.rg-head{position:relative;z-index:4;display:flex;align-items:center;gap:var(--sp-6);padding:calc(10px + env(safe-area-inset-top)) var(--sp-12) 10px var(--sp-8);
  background:var(--bg);border-bottom:1px solid var(--border-soft);}
.rg-back{display:grid;place-items:center;width:36px;height:40px;padding:0;border:0;background:transparent;
  color:var(--text-primary);font-size:32px;line-height:1;cursor:pointer;}
.rg-title{min-width:0;flex:1;font-size:var(--fs-headline);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.rg-head .people-toolbar{flex:0 0 auto;margin-left:0;}
.rg-head .people-tool{width:38px;height:38px;}""",
    ),
    (
        ".rg-filter{display:none;position:absolute;z-index:7;right:var(--sp-14);top:calc(112px + env(safe-area-inset-top));",
        ".rg-filter{display:none;position:absolute;z-index:7;right:var(--sp-12);top:calc(62px + env(safe-area-inset-top));",
    ),
    (
        """      <div class="rg-title" id="rgTitle">人物关系图</div>
    </div>
    <div class="rg-controls">
      <div class="people-toolbar">""",
        """      <div class="rg-title" id="rgTitle">人物关系图</div>
      <div class="people-toolbar">""",
    ),
]

for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one match, found {text.count(old)}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
