import re,json,pathlib,hashlib
root=pathlib.Path(__file__).resolve().parent.parent
base='https://framerusercontent.com/sites/2ubKVffv4PbSRvQcWG4I6c/'
manifest_path=root/'assets/manifest.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
texts=[p.read_text() for p in (root/'reference').rglob('*.html')]+[p.read_text() for p in (root/'assets/modules').glob('*.mjs') if not p.name.startswith(('google-','fontshare-','framer-font-'))]
for p in (root/'assets/modules').glob('*.mjs'):
 for name in re.findall(r'["\x27`](\./[^"\x27`]+\.mjs)["\x27`]',p.read_text()):
  url=base+name[2:];manifest[url]='assets/modules/'+name[2:]
for s in texts:
 for u in re.findall(r'https://(?:framerusercontent\.com|fonts\.gstatic\.com)/[^\s"\x27`<>\\()]+',s):
  u=u.split('?')[0].rstrip(';,')
  if not re.search(r'\.(?:mjs|woff2?|ttf|png|jpe?g|webp|svg|gif|mp4|webm|avif)$',u):continue
  name=u.rsplit('/',1)[-1]
  manifest[u]=('assets/modules/' if u.endswith('.mjs') else 'assets/media/')+name
(root/'assets/media').mkdir(exist_ok=True)
manifest_path.write_text(json.dumps(manifest,indent=2))
missing=[(u,p) for u,p in manifest.items() if not (root/p).exists()]
with open('/tmp/mazur-curl.conf','w') as f:
 for u,p in missing:f.write(f'url = "{u}"\noutput = "{root/p}"\n')
print(f'{len(manifest)} resources; {len(missing)} to download')
