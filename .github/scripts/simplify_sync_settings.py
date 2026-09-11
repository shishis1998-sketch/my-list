from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
before = s

status_pattern = re.compile(
    r'''(if\(!getToken\(\)\)\{\s*sb\.innerHTML=)'<b style="color:var\(--text-primary\)">尚未启用云同步</b><br>[^']*';''',
    re.S,
)
s, count = status_pattern.subn(
    r'''\1'<b style="color:var(--text-primary)">尚未启用云同步</b>';''',
    s,
    count=1,
)
if count != 1:
    raise SystemExit(f'sync status block: expected 1 match, found {count}')

patches = [
    (
        r'\n\s*<!-- 二维码配置传输：新设备扫码一键接入，无需手填 token -->.*?(?=\n\s*<!-- 覆盖前的本机备份)',
        '\n',
        'QR controls',
    ),
    (
        r'(<div class="local-toggle-title">👀 只读模式（这台设备只看不传）</div>)\s*<div class="local-toggle-desc">.*?</div>',
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
