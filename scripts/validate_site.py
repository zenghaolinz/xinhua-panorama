"""Validate all deployed panorama paths and the browser script using stdlib."""
from pathlib import Path
import json
import re
import subprocess
import tempfile

SITE = Path(__file__).resolve().parents[1] / 'site'
data = json.loads((SITE / 'scenes.json').read_text(encoding='utf-8'))
scenes = data['scenes']
assert len(scenes) == 8, 'Expected eight scenes'
ids = {scene['id'] for scene in scenes}
assert len(ids) == 8
images = []
for scene in scenes:
    sid = scene['id']
    assert re.fullmatch(r'\d{2}', sid)
    for level in ['l2', 'l3', 'l4']:
        for face in 'fbrlud':
            images.append(SITE / 'faces' / sid / level / f'{face}.jpg')
    images.append(SITE / 'panoramas' / f'{sid}.jpg')
    for hotspot in scene['hotspots']:
        assert hotspot['target'] in ids, f'Broken hotspot: {hotspot}'
for path in images:
    assert path.is_file(), f'Missing: {path}'
    assert path.stat().st_size < 100_000_000, f'Image too large for GitHub: {path}'
    with path.open('rb') as image:
        assert image.read(3) == b'\xff\xd8\xff', f'Not a JPEG: {path}'
        image.seek(-2, 2)
        assert image.read() == b'\xff\xd9', f'Truncated JPEG: {path}'
html = (SITE / 'index.html').read_text(encoding='utf-8')
assert 'faces/${sid}/${level}/${f}.jpg' in html
assert 'panoramas/${sid}.jpg' in html
assert not re.search(r'(?:src|href)=["\']/(?!/)', html), 'Project Pages needs relative asset paths'
scripts = re.findall(r'<script>([\s\S]*?)</script>', html)
with tempfile.TemporaryDirectory() as temp:
    script = Path(temp) / 'viewer.js'
    script.write_text('\n'.join(scripts), encoding='utf-8')
    subprocess.run(['node', '--check', str(script)], check=True)
total = sum(path.stat().st_size for path in SITE.rglob('*') if path.is_file())
assert total < 1_000_000_000, 'Site exceeds GitHub Pages size limit'
print(f'Validated {len(scenes)} scenes, {len(images)} images, relative paths and JavaScript; {total:,} bytes')
