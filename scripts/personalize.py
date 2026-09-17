"""Personalize both SSR and Framer modules; preserve original motion code."""
import json,re,html
from pathlib import Path
root=Path(__file__).resolve().parent.parent
profile=json.loads((root/'content/profile.json').read_text())
link=profile['linkedin']
previous_path=root/'content/replacements.json'
previous=json.loads(previous_path.read_text()) if previous_path.exists() else {}
replacements={
"Bartek 'Mazi' Mazur":profile['name'],
'Bartek Mazur - Digital Designer & No-code developer':'Lea Irt — Software Engineer · Visual Computing & AI',
"Bartek Mazur - digital designer specializing in web design, UI/UX and no-code development. Let's create something cool!":profile['bio'],
'Hello, I\'m Bartek':"Hello, I'm Lea",
'Digital designer':'Software engineer','& no-code dev':'& AI student',
'available for September':'VICAI · 2026–2028','Official Framer Expert.':'Visual computing & AI.','Official Framer Expert':'Visual computing & AI',
'I help brands go from idea to live website — through UI/UX design, prototyping, and Framer no-code development. Based in Poland, working with clients across the whole globe.':profile['bio'],
'Currently open to freelance projects and full-time positions.':profile['research'],
'I design custom websites and digital experiences — built around your brand, not a template.':'Software, visual computing and interactive experiences.',
'I design clean, modern websites that guide your users from first impression to clear action.':'Applications, interfaces and the systems behind them.',
'I build fast, responsive websites in Framer – no heavy code, full control over the details.':'Exploring how machines understand images and learn from data.',
'I craft cohesive projects and turn them into real-world visuals – from visual identity to posters and social media content.':'Algorithms, game mechanics and playful interactions.',
'Web & UI/UX':'Software engineering','No-code development':'Visual computing & AI','Branding & visual assets':'Games & interaction',
'FRAMER DEVELOPMENT':'SOFTWARE DEVELOPMENT','WEB DESIGN':'APPLICATIONS','UI DESIGN':'ALGORITHMS','UX/UI DESIGN':'DATA SCIENCE','UX RESEARCH':'MACHINE LEARNING','PROTOTYPES':'ANALYSIS','PROTOTYPING':'VISUALIZATION','BRANDING':'GAME DEVELOPMENT','GRAPHIC DESIGN':'CREATIVE CODING','CMS INTEGRATION':'DEEP LEARNING','MAINTENANCE':'COMPUTER VISION','RESPONSIVE WEB DESIGN':'IMAGE ANALYSIS','CONTENT STRATEGY':'GAME MECHANICS','INTERACTION DESIGN':'SYSTEM DESIGN',
'Experiments, side projects, and things I built just to see if I could.':'Experiments in algorithms, games and creative programming.',
'Got a project in mind, an idea you want to talk through, or just want to say hello?':"Let's talk about software, AI or a new idea.",
"I'm all ears — whether it's a potential collaboration, a full-time opportunity, or a question about design. I'll get back to you within 24 hours.":'Connect with me on LinkedIn.',
'Answers to common questions to help you understand the process and how we can work together.':'Education, interests and projects.',
'Services & Scope':'Education & interests','Process & Timeline':'Projects & contact',
'Bartek, can you tell me more about what you do?':'What do you focus on?',
'I already have a brand, will you just do the web design?':'What are you studying?',
'I already have a developer. Will you do the web design?':'What was your thesis about?',
"Essentially, I specialize in designing custom-tailored websites. The whole process starts from complex research about project's topic, then with the consultation with you I will bring your idea to life.":'Software engineering, visual computing and AI.',
'Yes. If you already have brand and style guidelines, I will use them to design a website tailored to your brand.':profile['bio'],
'Of course. If you already have a web developer, I will work with them to ensure a smooth transition.':profile['research'],
'What’s your typical project timeline?':'Where can I see your projects?',
'What do you need from me to get started?':'How can I get in touch?',
'Do you offer revisions?':'What do you enjoy building?',
'Do you provide post-project support?':'Where can I learn more?',
'Do you use AI in your design process?':'What are you exploring next?',
'(FUN ACTIVITIES)':'(BEYOND CODE)','Afterhours':'Beyond code',
"When I'm not crafting pixels, you'll find me in the studio and on stage with my hip-hop crew or playing basketball.":'EESTEC LC Belgrade volunteer; former student representative and programming guest lecturer.',
'Projects completed':'BSc · Belgrade','On-Time Delivery':'MSc · École Polytechnique',
'Bartek Mazur':'Lea Irt','Bartek':'Lea',
'bp.mazur21@gmail.com':'Connect on LinkedIn',
'mailto:bp.mazur21@gmail.com':link,
'https://www.linkedin.com/in/bart%C5%82omiejmazur/':link,
'https://www.instagram.com/mazi.digital/?hl=pl':link,
'https://drive.google.com/file/d/1e9GUF9RyhdJiEspq47UDAH_KhMh1SOqz/view?usp=sharing':link,
'https://api.framer.com/forms/v1/forms/f3473990-c719-4fc2-8a7f-d2d854c89078/submit':'/contact-disabled',
}
home=next((root/'assets/modules').glob('983Pg1*.mjs')).read_text()
about=next((root/'assets/modules').glob('E1uOd*.mjs')).read_text()
def literal_prefix(source,prefix,new):
 for old in re.findall(r'`('+re.escape(prefix)+r'[^`]*)`',source):
  if old.startswith(prefix):
   replacements[old]=new
   replacements[old.replace(r'\xA0','\xa0')]=new
literal_prefix(about,'UI/UX designer and no-code developer from Poland',profile['bio']+' ')
literal_prefix(about,'I design and build custom websites in Figma',profile['research'])
literal_prefix(about,'Available for freelance projects','Connect with me on LinkedIn.')
for prefix,new in [
 ('The timeline depends','Explore the selected projects on this site.'),
 ('To kick things off','Connect with me on LinkedIn.'),
 ('Yes! I believe','Applications, AI experiments and games.'),
 ('Yes! I offer support','My LinkedIn profile has more details.'),
 ('Yes. AI helps','Visual computing and artificial intelligence.')]:literal_prefix(about,prefix,new)
prefixes=['A portfolio and promotional website','A site taken over mid-build','Final project of flight search','A UX/UI case study developed','Whole branding project for non-existing']
for p,prefix in zip(profile['projects'],prefixes):
 replacements[p['oldTitle']]=p['title']
 literal_prefix(home,prefix,p['description'])

replacements={**previous,**replacements}
replacements['or drop me an e-mail:']='Find me on LinkedIn:'
replacements['Lea Irt - Digital Designer & No-code developer']='Lea Irt — Software Engineer · Visual Computing & AI'

def transform(s):
 for old,new in sorted(replacements.items(),key=lambda x:-len(x[0])):
  s=s.replace(old,new).replace(html.escape(old,quote=False),html.escape(new,quote=False))
 s=re.sub(r'(?<=children:)`BM`','`LI`',s)
 s=re.sub(r'>BM<','>LI<',s)
 s=s.replace('children:`Services`','children:`Focus`').replace('>Services<','>Focus<')
 s=s.replace('children:`IG`','children:`IN`').replace('>IG<','>IN<')
 s=s.replace('children:`CV`','children:`PROFILE`').replace('>CV<','>PROFILE<')
 # The original portrait and mockups are never presented as Lea's work.
 s=re.sub(r'https://www\.framer\.com/@[^`"<> ]+',link,s)
 return s

for p in (root/'assets/modules').glob('*.mjs'):
 s=transform(p.read_text());p.write_text(s)
# Write HTML from localized snapshots with matching text, including split animated headings.
for p in [root/'index.html',root/'about/index.html',root/'lets-connect/index.html']:
 s=p.read_text()
 def rich(m):
  inner=m.group(2);plain=html.unescape(re.sub(r'<[^>]+>','',inner))
  for old,new in sorted(replacements.items(),key=lambda x:-len(x[0])):
   if re.sub(r'\s+','',plain)==re.sub(r'\s+','',old):return m.group(1)+html.escape(new)+m.group(3)
  return m.group(0)
 s=re.sub(r'(<(?:h[1-6]|p)\b[^>]*>)(.*?)(</(?:h[1-6]|p)>)',rich,s,flags=re.S)
 s=transform(s)
 s=re.sub(r'(<(?:h[1-6]|p)\b[^>]*>)(.*?)(</(?:h[1-6]|p)>)',lambda m: m.group(1)+'Software engineer<br>&amp; AI student'+m.group(3) if re.sub(r'\s+','',html.unescape(re.sub(r'<[^>]+>','',m.group(2))))=='Digitaldesigner&no-codedev' else m.group(0),s,flags=re.S)
 s=s.replace('>2024<','>2026<')
 s=re.sub(r'<meta[^>]*(?:property|name)="(?:og:image|twitter:image)"[^>]*>','',s)
 if '/profile.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/profile.css"><script defer src="/profile.js"></script></head>')
 p.write_text(s)
# Normalize SSR text split by animated spans and remove stale metadata.
for path in [root/'index.html',root/'about/index.html',root/'lets-connect/index.html']:
 s=path.read_text()
 def normalized(value):return re.sub(r'\s+',' ',value).strip()
 def polish(m):
  plain=normalized(html.unescape(re.sub('<[^>]+>','',m.group(2))));new=plain
  for old,value in sorted(replacements.items(),key=lambda x:-len(x[0])):
   old=normalized(old.replace(r'\xA0',' '))
   if len(old)>25:new=new.replace(old,value.strip())
  return m.group(1)+html.escape(new)+m.group(3) if new!=plain else m.group(0)
 s=re.sub(r'(<(?:h[1-6]|p)\b[^>]*>)(.*?)(</(?:h[1-6]|p)>)',polish,s,flags=re.S)
 s=re.sub(r'(<meta\b[^>]*(?:name|property)="(?:description|og:description|twitter:description)"[^>]*content=")[^"]*',lambda m:m.group(1)+html.escape(profile['bio'],quote=True),s)
 s=re.sub(r'<meta[^>]*name="framer-search-index"[^>]*>','',s)
 s=re.sub(r'<link[^>]*rel="icon"[^>]*>','',s)
 path.write_text(s)
for path in (root/'assets/modules').glob('*.mjs'):
 s=path.read_text()
 s=re.sub(r'`Get to know (?:Bartek|Lea) - digital designer from Poland[^`]*`',lambda m:'`'+profile['bio']+'`',s)
 s=re.sub(r'socialImage:`/assets/media/[^`]+`','socialImage:void 0',s)
 s=s.replace('children:`2024`','children:`2026`')
 path.write_text(s)
(root/'content/replacements.json').write_text(json.dumps(replacements,ensure_ascii=False,indent=2))
print('Personalized original HTML and runtime modules.')
