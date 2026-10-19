"""Validate local navigation and required coverage of the proposal reader."""
from pathlib import Path
import hashlib, json, re, sys
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'sources/reader-manifest.json').read_text(encoding='utf-8'))
errors=[]; checked=0
retained=set()
if len(sys.argv)==3 and sys.argv[1]=='--baseline-tree':
 retained={x['path'] for x in json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))['tree'] if x['type']=='blob'}

def slug(s):
 s=re.sub(r'<[^>]*>','',s).strip().lower()
 s=re.sub(r'[^\w\s-]','',s,flags=re.UNICODE)
 return re.sub(r'\s','-',s)

anchors={}
for path in ROOT.rglob('*.md'):
 text=path.read_text(encoding='utf-8')
 explicit=set(re.findall(r'<a\s+id="([^"]+)"',text))
 headings=[slug(x) for x in re.findall(r'^#{1,6}\s+(.+)$',text,re.M)]
 anchors[path.resolve()]=explicit|set(headings)
 for note in set(re.findall(r'\[\^([^\]]+)\]',text)):
  if not re.search(r'^\[\^'+re.escape(note)+r'\]:',text,re.M):errors.append(f'{path.relative_to(ROOT)}: undefined footnote {note}')

for path in ROOT.rglob('*.md'):
 text=path.read_text(encoding='utf-8')
 urls=re.findall(r'!?\[[^\]\n]*\]\(([^\s\n)]+)(?:\s+"[^"]*")?\)',text)
 urls+=re.findall(r'<a\s[^>]*href="([^"]+)"',text)
 for url in urls:
  url=url.strip('<>');parsed=urlsplit(url)
  if parsed.scheme or url.startswith('//'):continue
  checked+=1
  dest=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path.resolve()
  if not dest.exists():
   relative=dest.relative_to(ROOT).as_posix() if dest.is_relative_to(ROOT) else ''
   if relative in retained:continue
   errors.append(f'{path.relative_to(ROOT)} -> missing {url}');continue
  if parsed.fragment and dest.suffix=='.md' and unquote(parsed.fragment) not in anchors.get(dest,set()):errors.append(f'{path.relative_to(ROOT)} -> missing anchor {url}')

sections=manifest['sections']
assert len([s for s in sections if s['kind']=='chapter'])==10
assert len([s for s in sections if s['kind']=='appendix'])==10
assert len(list((ROOT/'docs/bibliography/entries').glob('b*.md')))==135
assert len(list((ROOT/'docs/research').glob('*.md')))==9
for s in sections:
 if not (ROOT/s['path']).is_file():errors.append('missing section '+s['path'])
 for h in s['headings']:
  if h['anchor'] not in anchors.get((ROOT/s['path']).resolve(),set()):errors.append('missing heading '+h['anchor'])
for filename,key in [('proposal-v871e-candidate.tex','source_sha256'),('proposal-v871e-candidate.pdf','pdf_sha256')]:
 if hashlib.sha256((ROOT/'sources'/filename).read_bytes()).hexdigest()!=manifest[key]:errors.append('source hash mismatch '+filename)
for image in ['formula-variation.png','proposal-figure-2-page.png','proposal-figure-3-page.png']:
 if not (ROOT/'docs/assets'/image).is_file():errors.append('missing image '+image)
if errors:
 for error in errors:print(error)
 print(f'FAILED: {len(errors)} problems, {checked} local links checked')
 sys.exit(1)
print(f'PASS: {checked} local links; 10 chapters, 10 appendices, 135 bibliography entries; all source hashes match.')
