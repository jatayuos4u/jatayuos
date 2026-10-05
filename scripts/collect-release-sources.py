#!/usr/bin/env python3
"""Plan or download exact source versions from a release package manifest.
No ISO builds, package installations or APT configuration changes are performed.
"""
import argparse,csv,hashlib,json,re,subprocess,sys
from pathlib import Path
CUSTOM={'calamares':('3.3.14-1+jatayu3','3.3.14-1','scripts/patch-calamares.py'),
        'fcitx5':('5.1.12-2+jatayu1','5.1.12-2','scripts/build-fcitx.sh')}
LOCAL={'jatayu-integration','jatayu-tools','jatayu-wallpaper'}
def plan(path):
 entries={}; binaries=0
 for number,row in enumerate(csv.reader(Path(path).open(),delimiter='\t'),1):
  if not row:continue
  if len(row)!=4:raise ValueError(f'Line {number}: expected four TSV columns')
  binary,version,source,source_version=row
  source=source or binary.split(':')[0];source_version=source_version or version
  if not re.fullmatch(r'[a-z0-9][a-z0-9+.-]*',source) or not re.fullmatch(r'[0-9][A-Za-z0-9.+:~\-]*',source_version):
   raise ValueError(f'Line {number}: unsafe or invalid source identity')
  binaries+=1;key=(source,source_version)
  entry=entries.setdefault(key,{'source':source,'shipped_source_version':source_version,'fetch_version':source_version,'binary_packages':[],'kind':'debian'})
  entry['binary_packages'].append({'name':binary,'version':version})
  if source in LOCAL:entry['kind']='local-project';entry['fetch_version']=None
  elif '+jatayu' in source_version:
   mapping=CUSTOM.get(source)
   if not mapping or source_version!=mapping[0]:raise ValueError(f'Unknown custom source version: {source}={source_version}')
   entry.update(kind='modified-debian',fetch_version=mapping[1],patch_material=mapping[2])
 if not entries:raise ValueError('Manifest is empty')
 return {'schema_version':1,'binary_package_count':binaries,'source_package_count':len(entries),'manifest_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'sources':sorted(entries.values(),key=lambda x:(x['source'],x['shipped_source_version']))}
def verify_dsc(directory):
 files=list(directory.glob('*.dsc'))
 if len(files)!=1:raise ValueError('Expected one downloaded .dsc')
 text=files[0].read_text();match=re.search(r'^Checksums-Sha256:\n((?:[ \t].*\n)+)',text,re.M)
 if not match:raise ValueError('Missing SHA256 list in .dsc')
 for line in match.group(1).splitlines():
  digest,size,name=line.split()
  if Path(name).name!=name:raise ValueError('Invalid .dsc filename')
  p=directory/name
  if not p.is_file() or p.stat().st_size!=int(size) or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Source checksum mismatch: '+name)
 return files[0]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--output',required=True);p.add_argument('--download',action='store_true');a=p.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 result=plan(a.manifest);(out/'source-plan.json').write_text(json.dumps(result,indent=2)+'\n')
 if not a.download:print('Source plan written. No downloads performed.');return
 failures=[]
 for e in result['sources']:
  if e['kind']=='local-project':continue
  dest=out/'debian'/e['source']/e['fetch_version'].replace(':','_');dest.mkdir(parents=True,exist_ok=True)
  if any(dest.iterdir()):failures.append({'source':e['source'],'error':'Nonempty directory; use a fresh output or verify existing files separately'});continue
  r=subprocess.run(['apt-get','source','--download-only','--only-source',e['source']+'='+e['fetch_version']],cwd=dest,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (dest/'download.log').write_text(r.stdout)
  try:
   if r.returncode:raise ValueError('Exact APT source download failed')
   dsc=verify_dsc(dest)
   # Verify archive completeness/extraction using Debian's source tooling too.
   subprocess.run(['dpkg-source','-x',str(dsc),str(dest/'verify-extracted')],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  except (ValueError,subprocess.CalledProcessError) as error:failures.append({'source':e['source'],'error':str(error)})
 hashes=[]
 for f in sorted((out/'debian').rglob('*')) if (out/'debian').exists() else []:
  if f.is_file() and 'verify-extracted' not in f.parts and f.name!='download.log':hashes.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(out)))
 (out/'SOURCE-SHA256SUMS').write_text('\n'.join(hashes)+'\n')
 (out/'source-download-report.json').write_text(json.dumps({'failures':failures,'local_project_sources_require_separate_validation':True,'publication_complete':False},indent=2)+'\n')
 print('Exact source collection finished; publication still requires local project sources, notices, license review and hosting.')
 if failures:raise SystemExit(1)
if __name__=='__main__':main()
