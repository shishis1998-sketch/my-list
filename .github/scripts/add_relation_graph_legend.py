from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        """.rg-edge{fill:none;stroke-width:2;}.rg-edge.conflict{stroke-dasharray:7 5;}
.rg-edge-label{font:600 13px var(--zh);paint-order:stroke;stroke:var(--bg);stroke-width:8px;stroke-linejoin:round;}""",
        """.rg-edge{fill:none;stroke-width:2;}.rg-edge.conflict{stroke-dasharray:7 5;}
.rg-legend{position:absolute;z-index:5;right:var(--sp-12);bottom:calc(12px + env(safe-area-inset-bottom));
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 12px;width:176px;padding:11px 12px;
  box-sizing:border-box;border:1px solid var(--border);border-radius:var(--r);background:var(--surface);
  pointer-events:none;}
.rg-legend-item{display:flex;align-items:center;gap:7px;min-width:0;color:var(--text-secondary);font-size:var(--fs-caption);white-space:nowrap;}
.rg-legend-line{flex:0 0 20px;height:0;border-top:2px solid var(--rg-rel-color);}
.rg-legend-line.conflict{border-top-style:dashed;}""",
    ),
    (
        """    <div class="rg-stage" id="rgStage"><div class="rg-canvas" id="rgCanvas"></div></div>
    <div class="rg-person-card" id="rgPersonCard"></div>""",
        """    <div class="rg-stage" id="rgStage"><div class="rg-canvas" id="rgCanvas"></div></div>
    <div class="rg-legend" id="rgLegend" aria-label="关系颜色图例"></div>
    <div class="rg-person-card" id="rgPersonCard"></div>""",
    ),
    (
        """  const filter=document.getElementById('rgFilter');
  filter.innerHTML=REL_TYPES.map(t=>`<button type="button" class="on" data-type="${t.id}" onclick="toggleGraphType('${t.id}',this)">${t.lbl}</button>`).join('');
}""",
        """  const filter=document.getElementById('rgFilter');
  filter.innerHTML=REL_TYPES.map(t=>`<button type="button" class="on" data-type="${t.id}" onclick="toggleGraphType('${t.id}',this)">${t.lbl}</button>`).join('');
  const legend=document.getElementById('rgLegend');
  legend.innerHTML=REL_TYPES.map(t=>`<div class="rg-legend-item"><span class="rg-legend-line ${t.id}" style="--rg-rel-color:${t.color}"></span><span>${t.lbl}</span></div>`).join('');
}""",
    ),
    (
        """    const from=edgePoint(a,b),to=edgePoint(b,a),t=relType(r.type);
    const mx=(from.x+to.x)/2,my=(from.y+to.y)/2;
    const hi=rgState.selectedId&&(r.a===rgState.selectedId||r.b===rgState.selectedId);
    return `<line class="rg-edge ${r.type}${hi?' highlight':''}" x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="${t.color}" style="${rgState.selectedId&&!hi?'opacity:.18':hi?'stroke-width:3':''}"/><text class="rg-edge-label" x="${mx}" y="${my}" dominant-baseline="middle" text-anchor="middle" fill="${t.color}" style="${rgState.selectedId&&!hi?'opacity:.18':''}">${t.lbl}</text>`;""",
        """    const from=edgePoint(a,b),to=edgePoint(b,a),t=relType(r.type);
    const hi=rgState.selectedId&&(r.a===rgState.selectedId||r.b===rgState.selectedId);
    return `<line class="rg-edge ${r.type}${hi?' highlight':''}" x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="${t.color}" style="${rgState.selectedId&&!hi?'opacity:.18':hi?'stroke-width:3':''}"/>`;""",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
