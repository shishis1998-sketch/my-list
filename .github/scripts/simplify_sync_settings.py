from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
before = s

old = '''if(tid){
    sb.innerHTML='<b style="color:var(--success)">✓ 云同步已启用</b><br>数据会在保存时自动同步，也可以手动拉取/推送。';
  }else{
    sb.innerHTML='<b>尚未启用云同步</b><br>填入 token 后，所有修改会自动同步到你的 GitHub 私密 Gist；在任何设备打开同一份 HTML 都能看到最新数据。';
  }'''
new = '''if(tid){
    sb.innerHTML='<b style="color:var(--success)">✓ 云同步已启用</b>';
  }else{
    sb.innerHTML='<b>尚未启用云同步</b>';
  }'''
if old not in s:
    raise SystemExit('sync status block not found')
s = s.replace(old, new, 1)

patches = [
    (
        r'\n\s*<!-- 二维码配置传输：新设备扫码一键接入，无需手填 token -->\s*\n\s*<div style="display:flex;gap:var\(--sp-8\);margin-top:var\(--sp-14\)">.*?</div>\s*\n\s*<div style="font-size:var\(--fs-foot\);color:var\(--text-muted\);margin-top:var\(--sp-6\);line-height:var\(--lh-normal\)">.*?</div>',
        '',
        'QR controls',
    ),
    (
        r'(<span class="local-toggle-title">👀 只读模式（这台设备只看不传）</span>)\s*<span class="local-toggle-desc">.*?</span>',
        r'\1',
        'read-only explanation',
    ),
    (
        r'(<input type="password" id="f-gh-pw"[^>]*>\s*<div style="font-size:var\(--fs-foot\);color:var\(--text-muted\);margin-top:var\(--sp-6\);line-height:var\(--lh-normal\)">)\s*.*?\s*(</div>)',
        r'\1\n        主密码只存本机，<b>不会上传</b>；换设备时填写同一密码即可解密。忘记后无法恢复云端备忘。\n      \2',
        'master-password helper',
    ),
    (
        r'\n<!-- ===== SYNC QR SHOW MODAL ===== -->.*?(?=\n<!-- ===== SYNC SCAN MODAL ===== -->)',
        '\n',
        'QR display modal',
    ),
    (
        r'\n<!-- ===== SYNC SCAN MODAL ===== -->.*?(?=\n<!-- ===== [A-Z])',
        '\n',
        'QR scanner modal',
    ),
    (
        r'\n<!-- jsQR \(QR decoder, Apache-2\.0\).*?</script>\s*',
        '\n',
        'jsQR library',
    ),
    (
        r'<!-- QR Code Generator \(Kazuhiko Arase, MIT\).*?</script>\s*',
        '',
        'QR generator library',
    ),
    (
        r'\n// ── 二维码配置传输（token \+ Gist ID，无需手填/不显示明文）.*?(?=\n// ── Filter & Sort)',
        '\n',
        'QR sync behavior',
    ),
    (
        r'\ncheckIncomingSyncLink\(\);\s*',
        '\n',
        'QR startup hook',
    ),
]

for pattern, replacement, label in patches:
    s, count = re.subn(pattern, replacement, s, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')

required = [
    '尚未启用云同步',
    '只读模式（这台设备只看不传）',
    '清除这台设备的本机数据',
    '主密码只存本机',
]
for text in required:
    if text not in s:
        raise SystemExit(f'missing required text: {text}')

removed = [
    '扫码导入', '生成二维码', 'showSyncQR', 'openSyncScan',
    'qrModal', 'scanModal', 'checkIncomingSyncLink', 'jsQR v1.4.0',
    'QR Code Generator (Kazuhiko Arase',
]
for text in removed:
    if text in s:
        raise SystemExit(f'QR cleanup incomplete: {text}')

if s == before:
    raise SystemExit('no changes produced')

p.write_text(s, encoding='utf-8')
