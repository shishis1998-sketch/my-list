from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('  function applyDrag(dx){')
end=s.find('\n\n  function clearDrag', start)
if start<0 or end<0:
    raise SystemExit('applyDrag block not found')
new=r'''  function applyDrag(dx){
    const i=DT_TABS.findIndex(x=>x.id===dtTab);
    if(i<0)return;
    const ni=i+(dx<0?1:-1);
    const hasNext=ni>=0&&ni<DT_TABS.length;
    const w=root.getBoundingClientRect().width||window.innerWidth;
    const raw=hasNext?dx:dx*.22;
    const progress=Math.max(-1,Math.min(1,raw/w));
    const px=progress*w;

    moved.forEach(el=>{
      el.style.transition='none';
      el.style.willChange='transform';
      el.style.transform=`translate3d(${px}px,0,0)`;
    });

    const p=hasNext?ensurePeek(dx):null;
    if(p){
      const dir=dx<0?1:-1;
      // 相邻页与当前页严格共用同一个 progress：
      // 当前页走 50%，相邻页也只进入 50%。
      p.style.transition='none';
      p.style.transform=`translate3d(${dir*w+px}px,0,0)`;
    }

    const thumb=root.querySelector('.dt-tabs .cvt-thumb');
    if(thumb){
      const step=thumb.getBoundingClientRect().width;
      // 白色胶囊也按同一个 progress 换算到一个 tab 的位移。
      // 这样页面进度和顶部指示条始终 1:1 同步。
      const target=Math.max(0,Math.min(step*(DT_TABS.length-1),i*step-progress*step));
      thumb.style.transition='none';
      thumb.style.transform=`translate3d(${target}px,0,0)`;
    }
  }'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
