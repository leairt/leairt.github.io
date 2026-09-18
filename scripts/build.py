from pathlib import Path
import shutil,json
root=Path(__file__).resolve().parent.parent
dist=root/'dist'
(dist/'server').mkdir(parents=True,exist_ok=True)
client=dist/'client';client.mkdir(exist_ok=True)
for name in ['index.html','assets','about','lets-connect','playground','projects','work','profile.css','profile.js','portfolio.css','portfolio.js']:
 source=root/name;target=client/name
 if source.is_dir():shutil.copytree(source,target,dirs_exist_ok=True)
 else:shutil.copy2(source,target)
(dist/'server/index.js').write_text('export default { async fetch(request, env) { return env.ASSETS.fetch(request); } };\n')
print('Built static site and Worker entrypoint.')
