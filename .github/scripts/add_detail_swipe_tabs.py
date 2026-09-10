from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
needle="const DT_TABS=[{id:'info',lbl:'概览'},{id:'note',lbl:'备注'},{id:'tl',lbl:'时间线'}];\nlet dtTab='info';"
insert="""const DT_TABS=[{id:'info',lbl:'概览'},{id:'note',lbl:'备注'},{id:'tl',lbl:'时间线'}];
let dtTab='info';

// 详情页左右滑切换栏目：只在明确的横向手势完成后切换，不做内容跟手动画。
// 纵向滚动优先，避免读长文时轻微斜滑误切栏目；交互控件起手也不接管。
(function bindDetailTabSwipe(){
  const root=document.getElementById('detailRoot');
  if(!root||root.dataset.tabSwipeBound==='1')return;
  root.dataset.tabSwipeBound='1';
  let sx=0,sy=0,tracking=false,blocked=false;
  const interactive='input,textarea,select,button,a,[contenteditable="true"],.tl-item,.dt-person';
  root.addEventListener('touchstart',e=>{
    if(e.touches.length!==1){tracking=false;return;}
    const t=e.touches[0]; sx=t.clientX; sy=t.clientY; tracking=true;
    blocked=!!e.target.closest(interactive);
  },{passive:true});
  root.addEventListener('touchend',e=>{
    if(!tracking||blocked||!document.body.classList.contains('detail-open')){tracking=false;return;}
    tracking=false;
    const t=e.changedTouches&&e.changedTouches[0]; if(!t)return;
    const dx=t.clientX-sx,dy=t.clientY-sy;
    // 至少 50px，且横向位移明显大于纵向，才认作切页。
    if(Math.abs(dx)<50||Math.abs(dx)<=Math.abs(dy)*1.25)return;
    const i=DT_TABS.findIndex(x=>x.id===dtTab); if(i<0)return;
    const ni=dx<0?i+1:i-1;
    if(ni>=0&&ni<DT_TABS.length)setDetailTab(DT_TABS[ni].id);
  },{passive:true});
  root.addEventListener('touchcancel',()=>{tracking=false;},{passive:true});
})();"""
if needle not in s: raise SystemExit('DT_TABS anchor not found')
s=s.replace(needle,insert,1)
p.write_text(s,encoding='utf-8')
