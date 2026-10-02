"""Fetch pinned, licensed REST CPU probe inputs through the GitHub API.
Requires authenticated gh; downloads only explicitly inventoried source/weights.
"""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists(),'Use a new output directory'
 manifest=json.loads((Path(__file__).resolve().parents[1]/'docs/evidence/phase3/rest-model-manifest.json').read_text());a.out.mkdir(parents=True)
 for row in manifest['files']:
  raw=subprocess.run(['gh','api','repos/cuhk-eda/REST/git/blobs/'+row['git_blob']],capture_output=True,text=True,check=True)
  data=base64.b64decode(json.loads(raw.stdout)['content']);assert hashlib.sha256(data).hexdigest()==row['sha256']
  target=a.out/row['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
