import re,json,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'assets/manifest.json').read_text())
def localize(s):
 for url,path in sorted(manifest.items(),key=lambda x:-len(x[0])):
  s=s.replace(url,'/'+path)
 s=re.sub(r'<script\b[^>]*src="https://events\.framer\.com/[^>]*></script>','',s)
 s=re.sub(r'<script>\s*try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\).*?</script>','',s,flags=re.S)
 s=re.sub(r'<link[^>]*rel="canonical"[^>]*>','',s)
 s=s.replace('<head>','<head>\n<meta name="robots" content="noindex, nofollow">')
 return s
for p in (root/'reference').rglob('*.html'):
 relative=p.relative_to(root/'reference')
 target=root/'index.html' if relative.as_posix()=='home.html' else root/relative.with_suffix('')/'index.html'
 target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(localize(p.read_text()))
for p in (root/'assets/modules').glob('*.mjs'):
 s=localize(p.read_text());p.write_text(s)
print('Localized all pages and runtime modules.')

# Apply the personal content whenever snapshots are regenerated.
import subprocess,sys
if (root/'content/profile.json').exists():
 subprocess.run([sys.executable,str(root/'scripts/personalize.py')],check=True)
 subprocess.run([sys.executable,str(root/'scripts/build-profile-pages.py')],check=True)
