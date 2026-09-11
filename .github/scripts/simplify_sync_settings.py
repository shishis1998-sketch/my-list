from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '备忘解密后明文会留在本机，只清主密码是不够的。借来的手机、副机用完点这个，云端不受影响。'
new = '仅清除本机数据，云端不受影响。'
if old not in s:
    raise SystemExit('local cleanup hint not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
