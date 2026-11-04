r"""Write Markdown math in the forms GitHub renders without loss.

GitHub applies Markdown escapes and emphasis before MathJax reads $...$ and
$$...$$, so \{ \} \, \! \| \% and subscripts can be lost. Inline math is
rewritten as $`...`$ and display math as a fenced ```math block. Labels such
as \mathrm{B2_{fam}} take the LaTeX form \mathrm{B2}_{\mathrm{fam}}.

Usage: python3 scripts/github_math.py FILE.md [...]
"""
import re,sys,json
FENCE=re.compile(r'^(\s*(?:>\s*)*)(`{3,}|~{3,})')
def split_fences(lines):
    out=[];buf=[];i=0;infence=None
    for ln in lines:
        m=FENCE.match(ln)
        if infence:
            out[-1][1].append(ln)
            if m and m.group(2)[0]==infence[0] and len(m.group(2))>=len(infence) and ln.strip().strip(infence[0]).strip()=='' : infence=None
            continue
        if m:
            if buf: out.append(('text',buf)); buf=[]
            infence=m.group(2); out.append(('code',[ln])); continue
        buf.append(ln)
    if buf: out.append(('text',buf))
    return out
def line_ctx(text,pos):
    s=text.rfind('\n',0,pos)+1; e=text.find('\n',pos); e=len(text) if e<0 else e
    return s,e,text[s:e]
def cont_prefix(line):
    m=re.match(r'^((?:\s*>\s?)*)(\s*)((?:[-*+]|\d+[.)])\s+)?',line)
    bq,ws,mk=m.group(1),m.group(2),m.group(3) or ''
    return bq+ws+' '*len(mk)
report=[]
def convert_text(text,fname):
    out=[];i=0;n=len(text)
    while i<n:
        c=text[i]
        if text.startswith('<!--',i):
            j=text.find('-->',i); j=n if j<0 else j+3; out.append(text[i:j]); i=j; continue
        if text.startswith('$`',i):
            j=text.find('`$',i+2)
            if j<0: report.append((fname,'unclosed $`',text[i:i+60])); out.append(c); i+=1; continue
            out.append(text[i:j+2]); i=j+2; continue
        if c=='`':
            k=i
            while k<n and text[k]=='`': k+=1
            run=text[i:k]; j=text.find(run,k)
            if j<0: out.append(run); i=k; continue
            out.append(text[i:j+len(run)]); i=j+len(run); continue
        if c=='\\' and i+1<n: out.append(text[i:i+2]); i+=2; continue
        if text.startswith('$$',i):
            j=text.find('$$',i+2)
            if j<0: report.append((fname,'unclosed $$',text[i:i+60])); out.append(text[i:]); break
            X=text[i+2:j]; s,e,line=line_ctx(text,i)
            if line.lstrip().startswith('|'):
                out.append('$`'+X.strip()+'`$'); i=j+2; report.append((fname,'display-in-table->inline',X[:50])); continue
            pfx=cont_prefix(line)
            body='\n'.join(l.rstrip() for l in X.split('\n')).strip()
            bl=[l[len(pfx):] if pfx.strip() and l.startswith(pfx) else l for l in body.split('\n')]
            k=j+2
            while k<len(text) and text[k] in ' \t': k+=1
            if k<len(text) and text[k] in ',.;·:':
                if not bl[-1].rstrip().endswith(('.',',',';')): bl[-1]=bl[-1]+text[k]
                k+=1
                while k<len(text) and text[k] in ' \t': k+=1
            cur=''.join(out); curline=cur[cur.rfind('\n')+1:]
            if curline.strip() and curline.strip()!=pfx.strip():
                out=[cur.rstrip(' \t')+'\n']
            elif curline:
                out=[cur[:len(cur)-len(curline)]]
            block=[pfx+'```math']+[(pfx+l) if l.strip() else pfx.rstrip() for l in bl]+[pfx+'```']
            out.append('\n'.join(block))
            if k<len(text) and text[k]!='\n': out.append('\n'+pfx)
            i=k; continue
        if c=='$':
            e=text.find('\n',i); e=n if e<0 else e
            j=text.find('$',i+1)
            while j>=0 and j<e and text[j-1]=='\\': j=text.find('$',j+1)
            if j<0 or j>=e or j==i+1:
                report.append((fname,'lone $',text[max(0,i-30):i+40])); out.append(c); i+=1; continue
            X=text[i+1:j]
            if '`' in X: report.append((fname,'backtick in math',X)); out.append(text[i:j+1]); i=j+1; continue
            s,_,line=line_ctx(text,i)
            if line.lstrip().startswith('|') and '|' in X:
                report.append((fname,'pipe-in-table-math',X))
            out.append('$`'+X.strip()+'`$'); i=j+1; continue
        out.append(c); i+=1
    return ''.join(out)
def convert_file(p):
    src=open(p,encoding='utf-8').read()
    lines=src.split('\n')
    parts=split_fences(lines)
    res=[]
    for kind,ls in parts:
        t='\n'.join(ls)
        res.append(convert_text(t,p) if kind=='text' else t)
    new='\n'.join(res)
    new=re.sub(r'\\mathrm\{(B2|AP|B0)_\{([A-Za-z]+)\}\}',r'\\mathrm{\1}_{\\mathrm{\2}}',new)
    if new!=src: open(p,'w',encoding='utf-8').write(new); return True
    return False
if __name__=='__main__':
    ch=[p for p in sys.argv[1:] if convert_file(p)]
    print('changed',len(ch))
    for r in report: print('REPORT',r)
