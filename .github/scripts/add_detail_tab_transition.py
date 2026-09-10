from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""function setDetailTab(v){ dtSortPeople=false;  // 换栏目就退出排序态（顺序落手时已存）\n  dtTab=DT_TABS.some(t=>t.id===v)?v:'info'; renderDetail(); }"""
new="""let dtTabTransitionDir=0;\nfunction setDetailTab(v){ dtSortPeople=false;  // 换栏目就退出排序态（顺序落手时已存）\n  const next=DT_TABS.some(t=>t.id===v)?v:'info';\n  const oldI=DT_TABS.findIndex(t=>t.id===dtTab);\n  const newI=DT_TABS.findIndex(t=>t.id===next);\n  dtTabTransitionDir=newI>oldI?1:(newI<oldI?-1:0);\n  dtTab=next; renderDetail(); }"""
if old not in s:
    if new not in s: raise SystemExit('setDetailTab anchor not found')
else:
    s=s.replace(old,new,1)

anchor="""    ${footTxt?`<div class=\"dt-foot\">${footTxt}</div>`:''}`;\n  // 重画一次就把圆钮放出来：换栏目、改完正文回来，都不该看见一颗还收着的按钮。"""
insert="""    ${footTxt?`<div class=\"dt-foot\">${footTxt}</div>`:''}`;\n\n  // 栏目切换后的轻量过渡：新内容从切换方向的右/左侧短距离滑入。\n  // 只作用于正文，不动顶部标题/分段控件，也不影响进入详情页本身的动画设置。\n  if(dtTabTransitionDir){\n    const dir=dtTabTransitionDir;\n    dtTabTransitionDir=0;\n    const parts=Array.from(box.children).filter(el=>\n      !el.classList.contains('dt-top') && !el.classList.contains('dt-fab')\n    );\n    parts.forEach(el=>{\n      el.style.transition='none';\n      el.style.opacity='.82';\n      el.style.transform=`translate3d(${dir*22}px,0,0)`;\n      el.style.willChange='transform,opacity';\n    });\n    requestAnimationFrame(()=>requestAnimationFrame(()=>{\n      parts.forEach(el=>{\n        el.style.transition='transform .18s cubic-bezier(.22,1,.36,1), opacity .16s ease';\n        el.style.opacity='';\n        el.style.transform='';\n      });\n      setTimeout(()=>parts.forEach(el=>{el.style.transition='';el.style.willChange='';}),210);\n    }));\n  }\n\n  // 重画一次就把圆钮放出来：换栏目、改完正文回来，都不该看见一颗还收着的按钮。"""
if anchor not in s:
    if '栏目切换后的轻量过渡' not in s: raise SystemExit('renderDetail tail anchor not found')
else:
    s=s.replace(anchor,insert,1)

p.write_text(s,encoding='utf-8')
