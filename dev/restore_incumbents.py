"""Restore selected route archives, verifying archive and every member hash."""
import argparse,hashlib,json,os,shutil,tarfile,tempfile
from pathlib import Path
from measure import digest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selection',type=Path,default=Path('dev/incumbents/selected.json'));p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    selection=json.loads(a.selection.read_text());root=a.out.resolve();root.mkdir(parents=True,exist_ok=True)
    for row in selection['tiers']:
        archive=Path(row['archive']);assert digest(archive)==row['archive_sha256']
        inventory=json.loads(archive.with_suffix(archive.suffix+'.json').read_text());assert inventory['run_id']==row['run_id']
        destination=root/row['run_id']
        if destination.exists():p.error('destination already exists: '+str(destination))
        temporary=Path(tempfile.mkdtemp(prefix='.restore-',dir=root))
        try:
            with tarfile.open(archive,'r:gz') as tar:
                expected={row['run_id']+'/'+name:sha for name,sha in inventory['members'].items()}
                members=tar.getmembers();assert len(members)==len(expected)
                assert {m.name for m in members}==set(expected)
                for member in members:
                    path=Path(member.name)
                    assert member.isfile() and not path.is_absolute() and '..' not in path.parts
                    content=tar.extractfile(member).read();assert hashlib.sha256(content).hexdigest()==expected[member.name]
                    target=temporary/Path(*path.parts[1:]);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
            os.replace(temporary,destination)
        except BaseException:
            shutil.rmtree(temporary);raise
        print(row['tier'],destination/'routes')

if __name__=='__main__':main()
