from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

old = """function toggleGraphSearch(){const bar=document.getElementById('rgSearchbar');bar.classList.toggle('open');document.getElementById('rgFilter').classList.remove('open');if(bar.classList.contains('open'))setTimeout(()=>document.getElementById('rgSearch')?.focus(),30);}
function toggleGraphFilter(){document.getElementById('rgFilter').classList.toggle('open');document.getElementById('rgSearchbar').classList.remove('open');}"""
new = """function resetGraphSearch(){
  const search=document.getElementById('rgSearch');if(search)search.value='';
  rgState.selectedId='';closeGraphPersonCard();updateGraphHighlights();drawGraphLines(currentGraphData().relations);
}
function toggleGraphSearch(){
  const bar=document.getElementById('rgSearchbar'),opening=!bar.classList.contains('open');
  bar.classList.toggle('open',opening);document.getElementById('rgFilter').classList.remove('open');
  if(opening)setTimeout(()=>document.getElementById('rgSearch')?.focus(),30);else resetGraphSearch();
}
function toggleGraphFilter(){
  const bar=document.getElementById('rgSearchbar'),wasSearching=bar.classList.contains('open');
  document.getElementById('rgFilter').classList.toggle('open');bar.classList.remove('open');
  if(wasSearching)resetGraphSearch();
}"""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exactly one match, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
