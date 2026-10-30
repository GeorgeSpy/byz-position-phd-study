"""Audit every Markdown file against the repository's eight math style rules.

Run: python scripts/check_markdown_math.py [--json report.json]
Code examples and escaped prose brackets are excluded. Joint variable indices
such as ij, pe and pwe retain mathematical italics; descriptive labels are upright.
This source audit complements visual inspection on GitHub.
"""
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(
    r'(?P<fence>^[ \t]*(?P<ticks>`{3,}|~{3,})(?P<lang>[^\n]*)\n(?P<body>.*?)^[ \t]*(?P=ticks)[ \t]*$)'
    r'|(?P<btmath>\$`(?P<btbody>[^`\n]*)`\$)'
    r'|(?P<display>(?<!\\)\$\$(?P<dbody>.*?)(?<!\\)\$\$)'
    r'|(?P<bracket>\\\[(?P<brbody>.*?)\\\])'
    r'|(?P<paren>\\\((?P<pbody>.*?)\\\))'
    r'|(?P<code>`+[^`\n]*`+)'
    r'|(?P<inline>(?<![\\$])\$(?!\$)(?P<ibody>[^$\n]*?)(?<!\\)\$(?!\$))',
    re.M | re.S,
)


def math_spans(text):
    """Yield (match, kind, TeX), keeping code examples atomic."""
    for match in TOKEN.finditer(text):
        if match.group('fence'):
            if match.group('lang').strip() == 'math':
                yield match, 'display', match.group('body')
        elif not match.group('code'):
            for key, kind in [('btbody', 'inline'), ('dbody', 'display'),
                              ('brbody', 'display'), ('pbody', 'inline'),
                              ('ibody', 'inline')]:
                body = match.group(key)
                if body is not None:
                    if key == 'brbody' and not re.search(r'[\\_^=]', body):
                        continue
                    yield match, kind, body
                    break


def group_end(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{' and (i == 0 or text[i-1] != '\\'):
            depth += 1
        elif text[i] == '}' and (i == 0 or text[i-1] != '\\'):
            depth -= 1
            if depth == 0:
                return i
    return None


# Only genuine sequences of independently defined variable indices are allowed
# without upright text; all other multi-letter labels require an explicit macro.
VARIABLE_INDICES = {'ij', 'iR', 'pe', 'pwe', 'we', 'pw', 'it'}


def bare_labels(tex):
    for match in re.finditer(r'[_^]\{', tex):
        end = group_end(tex, match.end()-1)
        if end is None:
            continue
        body = tex[match.end():end]
        # Skip commands together with their arguments, but examine plain labels
        # on either side: e.g. the second label in _{f,selected}.
        body = re.sub(r'\\[A-Za-z]+\s*\{[^{}]*\}', ' ', body)
        body = re.sub(r'\\[A-Za-z]+', ' ', body)
        for label in re.findall(r'[A-Za-z][A-Za-z0-9]*', body):
            if len(label) > 1 and label not in VARIABLE_INDICES:
                yield label


def audit(root):
    paths = sorted(root.rglob('*.md'))
    issues, expressions = [], []
    patterns = {
        'R1': r'\\tag\b',
        'R3': r'\\(?:operatorname|mathrel|rm)\b',
        'R4': r'\\[{}]',
        'R5': r'[<>]|&(?:lt|gt);',
        'R6': r'\||\\(?:mid|Vert|lvert|rvert|lVert|rVert)\b|\\\|',
    }
    for path in paths:
        text = path.read_text(encoding='utf-8')
        relative = path.relative_to(root).as_posix()
        consumed = []
        for match, kind, tex in math_spans(text):
            line = text.count('\n', 0, match.start()) + 1
            expressions.append({'file': relative, 'line': line, 'kind': kind, 'tex': tex})
            consumed.append(match.span())
            def add(rule, detail):
                issues.append({'file': relative, 'line': line, 'rule': rule, 'detail': detail})
            for rule, pattern in patterns.items():
                if re.search(pattern, tex):
                    add(rule, 'forbidden math syntax')
            if kind == 'display':
                before, after = text[:match.start()], text[match.end():]
                # The final newline at EOF also acts as the block boundary.
                if (not match.group('display') or '\n' in tex
                        or (before and not before.endswith('\n\n'))
                        or (after.strip() and not after.startswith('\n\n'))):
                    add('R2', 'use one standalone $$...$$ line with blank lines around it')
            else:
                before, after = text[match.start()-1:match.start()], text[match.end():match.end()+1]
                boundary = r'[\[\]()*\-\u0370-\u03ff\u1f00-\u1fff]'
                if re.fullmatch(boundary, before) or re.fullmatch(boundary, after):
                    add('R8', 'inline math touches brackets, emphasis, hyphens or Greek text')
                if match.group('paren'):
                    add('R8', 'use dollar delimiters for inline math')
            for label in bare_labels(tex):
                add('R7', 'plain descriptive index: ' + label)
            depth, bad = 0, False
            for char in re.sub(r'\\[{}]', '', tex):
                depth += (char == '{') - (char == '}')
                if depth < 0:
                    bad = True
                    break
            if bad or depth:
                add('syntax', 'unbalanced TeX braces')
        # Mask all code, links/HTML URLs, escaped prose brackets, and recognised
        # math before checking for stray dollar delimiters.
        masked = list(text)
        ranges = [m.span() for m in TOKEN.finditer(text)]
        ranges += [m.span() for m in re.finditer(r'\\\$|\]\([^\n]*?\)|<[^\n>]*>', text)]
        for start, end in ranges:
            masked[start:end] = ' ' * (end-start)
        rest = ''.join(masked)
        for match in re.finditer(r'(?<!\\)\$', rest):
            issues.append({'file': relative, 'line': text.count('\n', 0, match.start())+1,
                           'rule': 'syntax', 'detail': 'unmatched dollar delimiter'})
    return {'files': len(paths), 'math_files': len({e['file'] for e in expressions}),
            'inline': sum(e['kind']=='inline' for e in expressions),
            'display': sum(e['kind']=='display' for e in expressions),
            'issues': issues, 'expressions': expressions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    report = audit(ROOT)
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for issue in report['issues']:
        print('{file}:{line}: {rule}: {detail}'.format(**issue))
    print(('FAIL' if report['issues'] else 'PASS') + ': '
          + f"{report['files']} Markdown files; {report['math_files']} with math; "
          + f"{report['inline']} inline and {report['display']} display expressions; "
          + f"{len(report['issues'])} issues")
    return bool(report['issues'])


if __name__ == '__main__':
    sys.exit(main())
