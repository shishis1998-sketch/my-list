from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 12px;width:176px;padding:11px 12px;",
        "display:grid;grid-template-columns:72px minmax(0,1fr);gap:9px 12px;width:212px;padding:11px 12px;",
    ),
    (
        "const gapX=225,gapY=150,w=140+(maxCount-1)*gapX,h=70+last*gapY,placements=[];",
        "const gapX=195,gapY=125,w=140+(maxCount-1)*gapX,h=70+last*gapY,placements=[];",
    ),
    (
        "const mainRadiusX=Math.max(220,maxLevel*220,people.length*24),mainRadiusY=Math.max(190,maxLevel*190);",
        "const mainRadiusX=Math.max(190,maxLevel*190,people.length*22),mainRadiusY=Math.max(165,maxLevel*165);",
    ),
    (
        "const radiusX=Math.max(l*220,arr.length*48),radiusY=Math.max(l*190,arr.length*43);",
        "const radiusX=Math.max(l*190,arr.length*44),radiusY=Math.max(l*165,arr.length*38);",
    ),
    (
        "let y=cy+mainRadiusY+95;",
        "let y=cy+mainRadiusY+75;",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
