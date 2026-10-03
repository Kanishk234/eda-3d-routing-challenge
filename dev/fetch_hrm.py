"""Fetch hash-pinned Apache-2.0 HRM inference source and public weights."""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, default=Path('docs/evidence/phase3/hrm-model-manifest.json'))
    p.add_argument('--out', type=Path, default=Path('dev/artifacts/hrm-pretrained'))
    a = p.parse_args()
    manifest = json.loads(a.manifest.read_text())
    for f in manifest['files']:
        source = 'git_blob' in f
        target = a.out / (('source/' if source else '') + f['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert hashlib.sha256(target.read_bytes()).hexdigest() == f['sha256']
            continue
        if source:
            url = f"https://raw.githubusercontent.com/Brown-Forces-Technology-Studio-Inc/hrm-chip-router/{manifest['revision']}/{f['path']}"
        else:
            url = f"https://huggingface.co/salvadordabrown/hrm-chip-router-7m/resolve/{f['revision']}/{f['path']}"
        temp = target.with_suffix(target.suffix + '.part')
        with urllib.request.urlopen(url, timeout=120) as response, temp.open('wb') as stream:
            while chunk := response.read(1024 * 1024): stream.write(chunk)
        assert hashlib.sha256(temp.read_bytes()).hexdigest() == f['sha256']
        temp.replace(target)
    (a.out/'manifest.json').write_bytes(a.manifest.read_bytes())
    print('Verified', len(manifest['files']), 'pinned files')


if __name__ == '__main__': main()
