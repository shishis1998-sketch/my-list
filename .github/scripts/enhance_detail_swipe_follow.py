from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('// 详情页左右滑切换栏目：')
end=s.find('function setDetailTab(v)', start)
if start<0 or end<0:
    raise SystemExit('detail swipe block not found')
new="""// 详情页左右滑切换栏目 + 轻量跟手：正文和顶部白色胶囊跟随横向拖动。
// 不预渲染相邻页，只让当前内容位移；松手超过阈值后切换，否则顺滑回弹。
(function bindDetailTabSwipe(){
  const root=document.getElementById('detailRoot');
  if(!root||root.dataset.tabSwipeBound==='1')return;
  root.dataset.tabSwipeBound='1';
  let sx=0,sy=0,tracking=false,blocked=false,horizontal=false,lastDx=0;
  let moved=[];
  const interactive='input,textarea,select,[contenteditable="true"],.dt-fab';

  function getMovables(){
    const body=document.getElementById('dtBody');
    if(!body)return [];
    const out=[];
    function walk(parent){
      Array.from(parent.children).forEach(el=>{
        if(el.classList.contains('dt-top'))return;
        if(el.classList.contains('dt-fab')||getComputedStyle(el).position==='fixed')return;
        if(el.querySelector('.dt-fab')) walk(el);
        else out.push(el);
      });
    }
    walk(body);
    return out;
  }

  function applyDrag(dx){
    const i=DT_TABS.findIndex(x=>x.id===dtTab);
    if(i<0)return;
    const hasNext=dx<0?i<DT_TABS.length-1:i>0;
    const px=hasNext?dx:dx*.22;
    moved.forEach(el=>{
      el.style.transition='none';
      el.style.willChange='transform';
      el.style.transform=`translate3d(${px}px,0,0)`;
    });
    const thumb=root.querySelector('.dt-tabs .cvt-thumb');
    if(thumb){
      const step=thumb.getBoundingClientRect().width;
      const target=Math.max(0,Math.min(step*(DT_TABS.length-1),i*step-dx));
      thumb.style.transition='none';
      thumb.style.transform=`translate3d(${target}px,0,0)`;
    }
  }

  function clearDrag(animate){
    moved.forEach(el=>{
      el.style.transition=animate?'transform .16s cubic-bezier(.4,0,.2,1)':'';
      el.style.transform='';
      el.style.willChange='';
    });
    const thumb=root.querySelector('.dt-tabs .cvt-thumb');
    if(thumb){
      thumb.style.transition=animate?'transform .16s cubic-bezier(.4,0,.2,1)':'';
      thumb.style.transform='';
    }
    if(animate)setTimeout(()=>{
      moved.forEach(el=>el.style.transition='');
      const t=root.querySelector('.dt-tabs .cvt-thumb');if(t)t.style.transition='';
    },180);
    moved=[];
  }

  root.addEventListener('touchstart',e=>{
    if(e.touches.length!==1){tracking=false;return;}
    const t=e.touches[0];
    sx=t.clientX;sy=t.clientY;lastDx=0;horizontal=false;tracking=true;
    blocked=!!e.target.closest(interactive);
    moved=blocked?[]:getMovables();
  },{passive:true});

  root.addEventListener('touchmove',e=>{
    if(!tracking||blocked||e.touches.length!==1)return;
    const t=e.touches[0],dx=t.clientX-sx,dy=t.clientY-sy;
    if(!horizontal){
      if(Math.abs(dy)>10&&Math.abs(dy)>=Math.abs(dx)){tracking=false;clearDrag(false);return;}
      if(Math.abs(dx)<8||Math.abs(dx)<=Math.abs(dy)*1.15)return;
      horizontal=true;
    }
    if(horizontal){
      e.preventDefault();
      lastDx=dx;
      applyDrag(dx);
    }
  },{passive:false});

  root.addEventListener('touchend',e=>{
    if(!tracking||blocked){tracking=false;clearDrag(false);return;}
    tracking=false;
    const t=e.changedTouches&&e.changedTouches[0];if(!t){clearDrag(true);return;}
    const dx=horizontal?lastDx:t.clientX-sx,dy=t.clientY-sy;
    const i=DT_TABS.findIndex(x=>x.id===dtTab);
    const ni=i+(dx<0?1:-1);
    const valid=horizontal&&Math.abs(dx)>=50&&Math.abs(dx)>Math.abs(dy)*1.25&&ni>=0&&ni<DT_TABS.length;
    if(valid){
      e.preventDefault();
      clearDrag(false);
      setDetailTab(DT_TABS[ni].id);
    }else clearDrag(true);
  },{passive:false});

  root.addEventListener('touchcancel',()=>{tracking=false;clearDrag(true);},{passive:true});
})();
"""
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
