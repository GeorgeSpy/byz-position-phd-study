from pathlib import Path
import copy, hashlib, json, os, re, shutil, subprocess, unicodedata
import fitz

ROOT = Path(__file__).resolve().parents[1]
import tempfile
WORK = Path(tempfile.mkdtemp(prefix='byz-reader-'))
SOURCE = ROOT / 'sources/proposal-v871e-candidate.tex'
PDF = ROOT / 'sources/proposal-v871e-candidate.pdf'
for directory in ['docs/full','docs/appendices','docs/bibliography/entries','docs/research','docs/musicology','docs/start','docs/examples','docs/assets','sources','scripts']:
    (ROOT / directory).mkdir(parents=True, exist_ok=True)

def pandoc(text, source='latex', target='json'):
    return subprocess.run(['pandoc','-f',source,'-t',target,'--wrap=none'], input=text, text=True, capture_output=True, check=True).stdout

def plain(obj):
    if isinstance(obj,dict):
        typ=obj.get('t')
        if typ=='Str': return obj['c']
        if typ in ('Space','SoftBreak','LineBreak'): return ' '
        if typ=='Math': return obj['c'][1]
        if typ=='Code': return obj['c'][1]
        return plain(obj.get('c',[]))
    if isinstance(obj,list): return ''.join(plain(x) for x in obj)
    return ''

def traverse(obj):
    if isinstance(obj,dict):
        yield obj
        for val in obj.values(): yield from traverse(val)
    elif isinstance(obj,list):
        for val in obj: yield from traverse(val)

def inlines(text): return [{'t':'Str','c':text}]
def para(text): return {'t':'Para','c':inlines(text)}
def md(blocks):
    doc={'pandoc-api-version':[1,23], 'meta':{}, 'blocks':blocks}
    return pandoc(json.dumps(doc,ensure_ascii=False),'json','gfm+tex_math_dollars+footnotes').strip()+'\n'

original=json.loads(pandoc(SOURCE.read_text()))
original_refs={o['c'][2][0]:copy.deepcopy(o['c'][1]) for o in traverse(original) if o.get('t')=='Link' and o['c'][2][0].startswith('#')}
normalized=SOURCE.read_text()
tables=[]

def group(s,i):
    while s[i].isspace():i+=1
    assert s[i]=='{'
    start=i+1;depth=1;i+=1
    while depth:
        if s[i]=='{' and s[i-1]!='\\':depth+=1
        if s[i]=='}' and s[i-1]!='\\':depth-=1
        i+=1
    return s[start:i-1],i

# Normalize custom width-aware LaTeX table environments before Pandoc parsing.
while (match:=re.search(r'\\begin\{(xltabular|tabularx)\}',normalized)):
    environment=match.group(1)
    width,end=group(normalized,match.end());spec,end=group(normalized,end)
    pos=0;columns=0
    while pos<len(spec):
        char=spec[pos]
        if char in '@><!' and pos+1<len(spec) and spec[pos+1]=='{':_,pos=group(spec,pos+1);continue
        if char in 'pmb' and pos+1<len(spec) and spec[pos+1]=='{':columns+=1;_,pos=group(spec,pos+1);continue
        if char in 'lcrXY':columns+=1
        pos+=1
    normalized=normalized[:match.start()]+'\\begin{longtable}{'+'l'*columns+'}'+normalized[end:]
    normalized=normalized.replace('\\end{'+environment+'}',r'\end{longtable}',1)

def table_replace(match):
    text=match.group(0)
    while (m:=re.search(r'\\multicolumn',text)):
        n,i=group(text,m.end()); spec,i=group(text,i); content,i=group(text,i)
        text=text[:m.start()]+content+(' & '*(int(n)-1))+text[i:]
    doc=json.loads(pandoc(text))
    parsed=[o for o in doc['blocks'] if o['t']=='Table']
    assert len(parsed)==1, ('table conversion failed',len(tables)+1)
    tables.append(parsed[0])
    return '\n\\texttt{READER_TABLE_'+str(len(tables))+'}\n'

normalized=re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}',table_replace,normalized,flags=re.S)

# Retain all three figures from the authoritative restored PDF.
pdf=fitz.open(PDF)
shutil.copyfile(ROOT/'sources/formula_position_example.png',ROOT/'docs/assets/formula-variation.png')
for n,page in [(2,12),(3,22)]:
    pdf[page].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(ROOT/f'docs/assets/proposal-figure-{n}-page.png')
figures=[]
def figure_replace(match):
    text=match.group(0)
    label=re.search(r'\\label\{([^}]+)\}',text).group(1)
    m=re.search(r'\\caption',text); caption,_=group(text,m.end())
    figures.append((label,caption))
    return '\n\\texttt{READER_FIGURE_'+str(len(figures))+'}\n'
normalized=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}',figure_replace,normalized,flags=re.S)
normalized=normalized.replace('\\noindent','')
ast=json.loads(pandoc(normalized))
(WORK/'placeholders_ast.json').write_text(json.dumps(ast,ensure_ascii=False))
(WORK/'placeholders.tex').write_text(normalized)

def inject(blocks):
    result=[]
    for block in blocks:
        text=plain(block).strip()
        if block['t'] in ('Para','Plain') and re.fullmatch(r'READER_TABLE_\d+',text):
            result.append(copy.deepcopy(tables[int(text.rsplit('_',1)[1])-1]));continue
        if block['t'] in ('Para','Plain') and re.fullmatch(r'READER_FIGURE_\d+',text):
            n=int(text.rsplit('_',1)[1]); label,caption=figures[n-1]
            path='formula-variation.png' if n==1 else f'proposal-figure-{n}-page.png'
            image={'t':'Image','c':[['',[],[]],inlines(f'Σχήμα {n} της πρότασης'),['../assets/'+path,'']]}
            cap=json.loads(pandoc(caption))['blocks']
            result.append({'t':'Div','c':[[label,[],[]],[{'t':'Para','c':[image]}]+cap]});continue
        if block['t']=='Div':block['c'][1]=inject(block['c'][1])
        result.append(block)
    return result
ast['blocks']=inject(ast['blocks'])
(WORK/'injected_ast.json').write_text(json.dumps(ast,ensure_ascii=False))
assert sum(o.get('t')=='Table' for o in traverse(ast))==17
assert sum(o.get('t')=='Image' for o in traverse(ast))==3

# Split at original major sections, keeping the abstract and every appendix.
slugs=['introduction','literature','questions','architecture','m1','eise','validation','data','nikolaos','contribution']
sections=[];current=None;main=0;appendix=0
for b in ast['blocks']:
    if b['t']=='Header' and b['c'][0]==1:
        title=plain(b['c'][2])
        if title=='Περίληψη': path='docs/full/00-abstract.md';number='';kind='abstract'
        elif title=='Βιβλιογραφία': path='docs/bibliography/source-list.md';number='';kind='bibliography'
        elif main<10:
            main+=1;number=str(main);kind='chapter';path=f'docs/full/{main:02d}-{slugs[main-1]}.md'
        else:
            number=chr(65+appendix);appendix+=1;kind='appendix';path=f'docs/appendices/{number.lower()}.md'
        current={'path':path,'number':number,'kind':kind,'title':title,'blocks':[],'headings':[]}
        sections.append(current)
    if current is not None: current['blocks'].append(b)
assert main==10 and appendix==10

# Stable ASCII targets preserve cross-chapter references in GitHub as well as HTML.
targets={};counter=0
for section in sections:
    sub=0;subsub=0
    for obj in traverse(section['blocks']):
        typ=obj.get('t')
        if typ=='Header':
            level,attr,content=obj['c']
            old=attr[0];counter+=1;anchor=f'r{counter:03d}';attr[0]=anchor
            targets[old]=(section['path'],anchor)
            number=section['number']
            if level==2:sub+=1;subsub=0;number+=f'.{sub}'
            elif level==3:subsub+=1;number+=f'.{sub}.{subsub}'
            elif level>=4:number=''
            if number:obj['c'][2]=inlines(number+' · ')+content
            section['headings'].append({'level':level,'anchor':anchor,'title':plain(obj['c'][2])})
        elif typ in ('Span','Div') and obj['c'][0][0]:
            old=obj['c'][0][0];counter+=1;anchor=f'r{counter:03d}'
            obj['c'][0][0]=anchor;targets[old]=(section['path'],anchor)

missing=[];link_count=0
for section in sections:
    for obj in traverse(section['blocks']):
        if obj.get('t')=='Link' and obj['c'][2][0].startswith('#'):
            old=obj['c'][2][0][1:]
            if '#'+old in original_refs:obj['c'][1]=copy.deepcopy(original_refs['#'+old])
            if old in targets:
                path,anchor=targets[old]
                relative=os.path.relpath(ROOT/path,ROOT/section['path']).replace('\\','/')
                relative=os.path.relpath(ROOT/path,(ROOT/section['path']).parent).replace('\\','/')
                obj['c'][2][0]=relative+'#'+anchor;link_count+=1
                obj['c'][0]=['',[],[]]
            else:missing.append(old)
assert not missing,missing

def emit_anchors(blocks):
    out=[]
    for b in blocks:
        if b['t']=='Header':
            out.append({'t':'RawBlock','c':['html',f'<a id="{b["c"][1][0]}"></a>']})
        if b['t']=='Div':
            anchor=b['c'][0][0]
            if anchor:out.append({'t':'RawBlock','c':['html',f'<a id="{anchor}"></a>']})
            out.extend(emit_anchors(b['c'][1]));continue
        out.append(b)
    return out

pages={}
for i,section in enumerate(sections):
    path=ROOT/section['path'];number=section['number']
    nav='[Αναλυτικός χάρτης](../full/index.md) · [Σύνοψη](../start/overview.md) · [Βιβλιογραφία](../bibliography/index.md)'
    meta='Μεταφορά του πλήρους κειμένου της υποψήφιας v8.71e. [Πρωτότυπο PDF](../../sources/proposal-v871e-candidate.pdf) · [Προέλευση και έκδοση](../reference.md).'
    toc='\n'.join(f'- [{h["title"]}](#{h["anchor"]})' for h in section['headings'] if h['level'] in (2,3))
    body=md(emit_anchors(section['blocks']))
    if toc:
        pos=body.find('\n',body.find('# '));body=body[:pos+1]+'\n'+nav+'\n\n'+meta+'\n\n**Σε αυτή την ενότητα**\n\n'+toc+'\n\n'+body[pos+1:]
    else:body=nav+'\n\n'+meta+'\n\n'+body
    previous=sections[i-1] if i else None;following=sections[i+1] if i+1<len(sections) else None
    footer=[]
    for label,other in [('Προηγούμενη',previous),('Επόμενη',following)]:
        if other:footer.append(f'[{label}: {other["number"]} {other["title"]}]({os.path.relpath(ROOT/other["path"],path.parent)})')
    path.write_text(body+'\n---\n\n'+' · '.join(footer)+'\n')
    pages[section['path']]=plain(section['blocks'])

# Complete bibliography: preserve source order and add stable per-entry pages.
bibsection=next(s for s in sections if s['kind']=='bibliography')
refs=[];language=''
for b in bibsection['blocks']:
    if b['t']=='Para':language=plain(b)
    if b['t']=='OrderedList':
        for local_i,blocks in enumerate(b['c'][1],1):
            refs.append({'id':f'b{len(refs)+1:03d}','language':language,'source_number':local_i,'blocks':blocks,'text':plain(blocks)})
assert len(refs)==135,len(refs)

def fold(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
for ref in refs:
    text=ref['text'];first=text.split(',')[0].strip();year=re.search(r'\b(?:18|19|20)\d{2}[a-z]?\b',text)
    if ',' not in text.split('(')[0]:first=text.split('(')[0].strip().rstrip('.')
    nodate=re.search(r'\(n\.d\.(-[a-z])?\)',text)
    ref['author']=first;ref['year']=('χ.χ.'+(nodate.group(1) or '')) if nodate else (year.group(0) if year else '')
    ref['matches']=[]
    for s in sections:
        if s['kind']=='bibliography':continue
        if fold(first) in fold(pages[s['path']]) and (not year or year.group(0)[:4] in pages[s['path']]):ref['matches'].append(s)
    title=f'{first} ({ref["year"]})' if year else first
    full=md(copy.deepcopy(ref['blocks']))
    related='\n'.join(f'- [{s["number"]} {s["title"]}]({os.path.relpath(ROOT/s["path"],ROOT/"docs/bibliography/entries")})' for s in ref['matches'])
    note='Οι παρακάτω σύνδεσμοι είναι αυτόματος εντοπισμός ονόματος και έτους μέσα σε ολόκληρη την ενότητα. Η ακριβής χρήση εξετάζεται στο κείμενό της.' if related else 'Η εγγραφή περιλαμβάνεται στη βιβλιογραφία της πρότασης. Η πλοήγηση μπορεί να συνεχιστεί από τους θεματικούς χάρτες ή την αναζήτηση ονόματος στο πλήρες κείμενο.'
    card=f'# {title}\n\n[Πλήρης βιβλιογραφία](../index.md) · [Αρχική σειρά εγγραφών](../source-list.md) · [Πεδία έρευνας](../../research/index.md)\n\n{full}\n**Σταθερό αναγνωριστικό:** `{ref["id"]}` · **Κατηγορία πηγής:** {ref["language"]} · **Αρίθμηση πρωτοτύπου:** {ref["source_number"]}\n\n## Σχετικές ενότητες της πρότασης\n\n{note}\n\n{related}\n'
    (ROOT/f'docs/bibliography/entries/{ref["id"]}.md').write_text(card)

index='# Πλήρης βιβλιογραφία\n\nΗ υποψήφια πρόταση περιλαμβάνει **135 εγγραφές**: 24 στην ελληνόγλωσση και 111 στην ξενόγλωσση ενότητα. Κάθε εγγραφή έχει σταθερή σελίδα, διαθέσιμους συνδέσμους της πηγής και πρόσβαση σε σχετικές ενότητες.\n\n[Αρχική σειρά και πλήρες κείμενο](source-list.md) · [Θεματικοί χάρτες](../research/index.md) · [Νεότερες προτεινόμενες προσθήκες](supplementary.md)\n\n'
for language in ['Ελληνόγλωσση Βιβλιογραφία','Ξενόγλωσση Βιβλιογραφία']:
    index+='## '+language+'\n\n| Συγγραφέας | Έτος | Πλήρης εγγραφή |\n|---|---|---|\n'
    for ref in refs:
        if language not in ref['language']:continue
        summary=ref['text'].replace('|','\\|')
        index+=f'| [{ref["author"]}](entries/{ref["id"]}.md) | {ref["year"]} | {summary} |\n'
    index+='\n'
(ROOT/'docs/bibliography/index.md').write_text(index)

# Topic-to-section targets are exported for the editorial layer.
manifest={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'sections':[{k:v for k,v in s.items() if k!='blocks'} for s in sections],'targets':targets,'bibliography':[{k:v for k,v in r.items() if k not in ('blocks','matches')} for r in refs],'statistics':{'major_sections':main,'appendices':appendix,'bibliography_entries':len(refs),'tables':len(tables),'figures':len(figures),'internal_cross_references':link_count,'math_nodes':sum(o.get('t')=='Math' for o in traverse(ast)),'footnotes':sum(o.get('t')=='Note' for o in traverse(ast))}}
(WORK/'reader_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(ROOT/'sources/reader-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

# Per-section routes to candidate bibliography entries.
for section in sections:
    if section['kind']=='bibliography':continue
    links=[]
    for ref in refs:
        if section in ref['matches']:
            links.append(f'[{ref["author"]} ({ref["year"]})](../bibliography/entries/{ref["id"]}.md)')
    if links:
        path=ROOT/section['path']
        path.write_text(path.read_text()+'\n<details>\n<summary>Βιβλιογραφικές διαδρομές της ενότητας</summary>\n\nΑυτόματος εντοπισμός ονόματος και έτους· η ακριβής χρήση ελέγχεται στο κείμενο.\n\n'+' · '.join(links)+'\n\n</details>\n')

print(json.dumps(manifest['statistics'],ensure_ascii=False))
