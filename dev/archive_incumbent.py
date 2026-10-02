"""Preserve checked run routes/source/provenance compactly without scratch logs."""
import argparse,gzip,io,json,tarfile
from pathlib import Path
from measure import digest,save

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists() or a.out.with_suffix(a.out.suffix+'.json').exists():p.error('archive exists')
    r=a.run.resolve();m=json.loads((r/'manifest.json').read_text());assert m['success'] and m['result']['complete']
    for name,sha in m['outputs'].items():assert digest(r/name)==sha
    files=[r/'manifest.json',r/'coverage-rescore.json',*sorted((r/'routes').glob('*.sol.json')),*sorted((r/'development-source').glob('*'))]
    buffer=io.BytesIO()
    with tarfile.open(fileobj=buffer,mode='w') as archive:
        for path in files:
            assert path.is_file()
            content=path.read_bytes();entry=tarfile.TarInfo(r.name+'/'+str(path.relative_to(r)));entry.size=len(content);entry.mode=0o644;entry.mtime=0
            archive.addfile(entry,io.BytesIO(content))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_bytes(gzip.compress(buffer.getvalue(),mtime=0))
    with tarfile.open(a.out,'r:gz') as archive:
        for path in files:
            assert archive.extractfile(r.name+'/'+str(path.relative_to(r))).read()==path.read_bytes()
    save(a.out.with_suffix(a.out.suffix+'.json'),{'run_id':r.name,'score':m['result']['aggregate_score'],'archive_sha256':digest(a.out),'members':{str(path.relative_to(r)):digest(path) for path in files},'limitations':'Preserves scored outputs and their recorded source/manifest; missing raw ancestors are not reconstructed. See coverage evidence for case-portfolio and donor ancestry.'})
    print(a.out,a.out.stat().st_size)

if __name__=='__main__':main()
