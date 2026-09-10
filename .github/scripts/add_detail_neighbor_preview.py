from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

pattern=r"// 详情页左右滑切换栏目 \+ 轻量跟手：正文和顶部白色胶囊跟随横向拖动。.*?\n\}\)\(\);\nlet dtTabTransitionDir=0;"

replacement=r'''// 详情页左右滑切换栏目 + 跟手预览：当前页随手指移出，同时让相邻页从边缘进入。
// 仍保持纵向滚动优先；不在最左/最右越界切换。
(function bindDetailTabSwipe(){
  const root=document.getElementById('detailRoot');
  if(!root||root.dataset.tabSwipeBound==='1')return;
  root.dataset.tabSwipeBound='1';
  let sx=0,sy=0,tracking=false,blocked=false,horizontal=false,lastDx=0;
  let moved=[],peek=null,peekIndex=-1;
  const interactive='input,textarea,select,[contenteditable="true"],.dt-fab';

  function getMovables(){
    const body=document.getElementById('dtBody');
    if(!body)return [];
    const out=[];
    function walk(parent){
      Array.from(parent.children).forEach(el=>{
        if(el.classList.contains('dt-top')||el.classList.contains('dt-swipe-peek'))return;
        if(el.classList.contains('dt-fab')||getComputedStyle(el).position==='fixed')return;
        if(el.querySelector('.dt-fab')) walk(el);
        else out.push(el);
      });
    }
    walk(body);
    return out;
  }

  function removePeek(){
    if(peek&&peek.remove)peek.remove();
    peek=null;peekIndex=-1;
  }

  // 用现有 renderDetail 临时生成相邻栏目的真实内容，再取一份静态副本作为拖动预览。
  // 随后立刻重画回当前栏目，所以预览与真正切过去看到的内容保持一致。
  function ensurePeek(dx){
    const i=DT_TABS.findIndex(x=>x.id===dtTab);
    const ni=i+(dx<0?1:-1);
    if(ni<0||ni>=DT_TABS.length){removePeek();return null;}
    if(peek&&peekIndex===ni)return peek;
    removePeek();

    const current=dtTab;
    const savedDir=dtTabTransitionDir;
    dtTabTransitionDir=0;
    dtTab=DT_TABS[ni].id;
    renderDetail();
    const rendered=document.getElementById('dtBody');
    const html=rendered?Array.from(rendered.children)
      .filter(el=>!el.classList.contains('dt-top')&&!el.classList.contains('dt-fab'))
      .map(el=>el.outerHTML).join(''):'';

    dtTab=current;
    dtTabTransitionDir=0;
    renderDetail();
    dtTabTransitionDir=savedDir;

    const body=document.getElementById('dtBody');
    if(!body||!html)return null;
    moved=getMovables();
    const top=body.querySelector('.dt-top');
    peek=document.createElement('div');
    peek.className='dt-swipe-peek';
    peek.innerHTML=html;
    peekIndex=ni;
    Object.assign(peek.style,{
      position:'absolute',
      top:(top?top.offsetHeight:0)+'px',
      left:'0',width:'100%',
      zIndex:'2',
      pointerEvents:'none',
      willChange:'transform',
      transform:'translate3d(0,0,0)'
    });
    body.style.position='relative';
    body.style.overflowX='clip';
    body.appendChild(peek);
    return peek;
  }

  function applyDrag(dx){
    const i=DT_TABS.findIndex(x=>x.id===dtTab);
    if(i<0)return;
    const ni=i+(dx<0?1:-1);
    const hasNext=ni>=0&&ni<DT_TABS.length;
    const px=hasNext?dx:dx*.22;

    moved.forEach(el=>{
      el.style.transition='none';
      el.style.willChange='transform';
      el.style.transform=`translate3d(${px}px,0,0)`;
    });

    const p=hasNext?ensurePeek(dx):null;
    if(p){
      const w=root.getBoundingClientRect().width||window.innerWidth;
      const base=dx<0?w:-w;
      p.style.transition='none';
      p.style.transform=`translate3d(${base+dx}px,0,0)`;
    }

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
    const p=peek;
    if(p){
      if(animate){
        const i=DT_TABS.findIndex(x=>x.id===dtTab);
        const dir=peekIndex>i?1:-1;
        const w=root.getBoundingClientRect().width||window.innerWidth;
        p.style.transition='transform .16s cubic-bezier(.4,0,.2,1)';
        p.style.transform=`translate3d(${dir*w}px,0,0)`;
        setTimeout(()=>{if(p===peek)removePeek();},180);
      }else removePeek();
    }
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
    removePeek();
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
let dtTabTransitionDir=0;'''

ns,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'detail swipe block not found or ambiguous: {n}')
p.write_text(ns,encoding='utf-8')
