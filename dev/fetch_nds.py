"""Fetch hash-pinned MIT-licensed NDS source and published CPU probe weights."""
import argparse
import json
import urllib.request
from pathlib import Path
from measure import digest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,default=Path('docs/evidence/phase3/nds-model-manifest.json'))
    p.add_argument('--out',type=Path,default=Path('dev/artifacts/nds-pretrained'))
    a=p.parse_args();manifest=json.loads(a.manifest.read_text())
    for f in manifest['files']:
        target=a.out/f['path'];target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert digest(target)==f['sha256'];continue
        url=f"https://raw.githubusercontent.com/ahottung/NDS/{manifest['revision']}/{f['path']}"
        temp=target.with_suffix(target.suffix+'.part')
        with urllib.request.urlopen(url,timeout=120) as response,temp.open('wb') as stream:
            while chunk:=response.read(1024*1024):stream.write(chunk)
        assert digest(temp)==f['sha256'];temp.replace(target)
    (a.out/'manifest.json').write_bytes(a.manifest.read_bytes())
    print('Verified',len(manifest['files']),'pinned files')


if __name__=='__main__':main()
