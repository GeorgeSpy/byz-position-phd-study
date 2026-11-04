"""Re-apply the repository's more detailed M1/M2 design text to the reader.

The reader pages are generated from documents/analytical-proposal.tex by
import_proposal.py. Where the repository documents the M1/M2 design in more
detail than the PDF, that text is kept in sources/reader-detail/:

  <page>-<anchor>.md.txt  replaces the body of the section that starts at
                      <a id="anchor">; the heading line of the generated page
                      (number and title from the PDF) is kept.
  <page>-append.md.txt    is added at the end of the page body, before the footer.

The script also refreshes the heading list of each affected page in
sources/reader-manifest.json.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / 'sources/reader-detail'
PAGES = {p.stem: p for p in list((ROOT/'docs/full').glob('*.md')) + list((ROOT/'docs/appendices').glob('*.md'))}
HEAD = re.compile(r'<a id="(r\d+)"></a>\s*\n\s*\n?(#+) ')
FOOTER = '\n---\n\n[Προηγούμενη'


def section_span(text, anchor):
    start = text.index(f'<a id="{anchor}"></a>')
    level = len(HEAD.match(text, start).group(2))
    for m in HEAD.finditer(text, start + 5):
        if len(m.group(2)) <= level:
            return start, m.start()
    return start, text.index(FOOTER, start) + 1


def body_after_heading(block):
    m = re.search(r'^#+ .*\n', block, re.M)
    return block[m.end():]


changed = set()
for item in sorted(DETAIL.glob('*.md.txt')):
    page, key = item.name[:-len('.md.txt')].rsplit('-', 1)
    path = PAGES[page]; text = path.read_text(encoding='utf-8')
    detail = item.read_text(encoding='utf-8')
    if key == 'append':
        k = text.index(FOOTER)
        text = text[:k].rstrip('\n') + '\n\n' + detail.rstrip('\n') + '\n' + text[k:]
    else:
        s, e = section_span(text, key)
        block = text[s:e]
        heading = re.search(r'^#+ .*\n', block, re.M)
        text = text[:s] + block[:heading.end()] + body_after_heading(detail).rstrip('\n') + '\n\n' + text[e:]
    path.write_text(text, encoding='utf-8'); changed.add(path)

manifest_path = ROOT/'sources/reader-manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for section in manifest['sections']:
    path = ROOT/section['path']
    if path not in changed:
        continue
    text = path.read_text(encoding='utf-8')
    section['headings'] = [{'level': len(m.group(2)), 'anchor': m.group(1),
                            'title': re.sub(r'\s+', ' ', text[m.end():text.index('\n', m.end())]).strip()}
                           for m in HEAD.finditer(text)]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('reader detail applied to', ', '.join(sorted(p.name for p in changed)))
