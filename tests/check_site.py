"""Offline checks for AGF navigation, preserved research and new page links."""
from pathlib import Path
import re, subprocess, json
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self, content):
  super().__init__(); self.ids=[];self.links=[];self.json=[];self.in_json=False;self.feed(content)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag in ('a','link','script','img'):
   value=a.get('href') or a.get('src')
   if value:self.links.append(value)
  self.in_json=tag=='script' and a.get('type')=='application/ld+json'
 def handle_endtag(self,tag):
  if tag=='script': self.in_json=False
 def handle_data(self,data):
  if self.in_json:json.loads(data)
pages=[]
for p in ROOT.rglob('*.html'):
 s=p.read_text()
 if 'id="navLinks"' not in s: continue
 parsed=Page(s); pages.append(p)
 assert len(parsed.ids)==len(set(parsed.ids)),f'Duplicate ID: {p}'
 nav=re.search(r'<nav\b.*?</nav>',s,re.S)[0]
 assert 'href="/advisory/"' in nav,p
 assert s.count('/js/navigation.js')==1,p
 assert '/css/divisions.css' in s,p
 assert "classList.toggle('open')" not in s,p
 if p.parts[-3]=='reports':
  rel=str(p.relative_to(ROOT))
  old=subprocess.check_output(['git','show','677db239bba909920a1d38a8b3202abb27ef1f35:'+rel],cwd=ROOT,text=True)
  # Article content, figures, citations and downloads must remain untouched.
  old_body=re.search(r'<article\b.*?</article>',old,re.S)
  new_body=re.search(r'<article\b.*?</article>',s,re.S)
  if old_body:assert old_body[0]==new_body[0],f'Report article changed: {p}'
for name in ('advisory/index.html','editorial-independence/index.html','videos/index.html'):
 p=ROOT/name; data=Page(p.read_text())
 for link in data.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  target=(ROOT/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (p.parent/unquote(url.path)) if url.path else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'Missing target {name}: {link}'
  if url.fragment and target.suffix=='.html': assert url.fragment in Page(target.read_text()).ids,f'Missing anchor {link}'
old=subprocess.check_output(['git','show','677db239bba909920a1d38a8b3202abb27ef1f35:index.html'],cwd=ROOT,text=True)
new=(ROOT/'index.html').read_text()
for block in re.findall(r'<li class="report-item.*?</li>',old,re.S): assert block in new,'Homepage report removed'
assert len(re.findall('class="report-item',new))==67
for item in ['pillars','partners','founder','reports','join','videos','board-cta','divisions']:assert item in Page(new).ids
print(f'PASS: {len(pages)} navigation pages; original research articles and all 67 report cards retained; new links/anchors and JSON metadata valid.')
