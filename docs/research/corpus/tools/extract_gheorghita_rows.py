"""Draft extraction of row metadata from the per-mode tables of Gheorghiță (2009), §7.2.1–7.2.8.

Input: page images of the printed tables (pp. 153–206), rendered at 200 dpi as p-NNN.png,
where NNN is the page number of the scanned PDF. The scans are not part of this repository.
For every table row it records the composer cell (A), the exegete sub-cells (E) and the
row number. Captions give table and formula numbers. The notation itself is not
transcribed. The output is an OCR draft for manual verification.

Usage: python3 extract_gheorghita_rows.py rows.csv 26 27 28 ...
Requires tesseract, pytesseract, opencv-python and numpy.
"""
import csv, re, sys, subprocess
from pathlib import Path
import cv2
import numpy as np
import pytesseract


def lines(mask_axis, img, min_frac, axis):
    # binary dark pixels
    dark = (img < 128).astype(np.uint8)
    if axis == 'v':
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(15, int(img.shape[0] * min_frac))))
    else:
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(15, int(img.shape[1] * min_frac)), 1))
    opened = cv2.morphologyEx(dark, cv2.MORPH_OPEN, k)
    prof = opened.sum(0 if axis == 'v' else 1)
    idx = np.where(prof > 0)[0]
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 3:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [int(np.mean(g)) for g in groups], opened

def hlines_in(img, x0, x1, min_len):
    sub = (img[:, x0:x1] < 128).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(10, int(min_len)), 1))
    opened = cv2.morphologyEx(sub, cv2.MORPH_OPEN, k)
    prof = opened.sum(1)
    idx = np.where(prof > 0)[0]
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 3:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [int(np.mean(g)) for g in groups]

def ocr(img):
    t = pytesseract.image_to_string(img, config='--psm 6 -l eng')
    return re.sub(r'\s+', ' ', t).strip()

def norm_composer(t):
    u = t.upper().replace('0', 'O').replace(' ', '')
    m = re.search(r'(PLP|PLE|DP|PB|PIP|>LP|LP|FL)', u)
    comp = None
    if m:
        comp = {'PLE': 'PLP', 'PIP': 'PLP', '>LP': 'PLP', 'LP': 'PLP', 'FL': 'PLP'}.get(m.group(1), m.group(1))
    s = re.search(r'[S$5]\s*([1-4])', t.upper().replace('PLP',''))
    return comp, (int(s.group(1)) if s else None)

def norm_exegetes(t):
    u = t.upper().replace('C C', 'CC')
    out = []
    if re.fullmatch(r'\W*A\W*', u):
        return ['A']
    for m in re.finditer(r'(CC|GP|CP|GF|EE|CE|OP|6P|EC|C€|€C)', u):
        g = m.group(1)
        out.append('GP' if g in ('GP', 'CP', 'GF', 'OP', '6P') else 'CC')
    return out

CAP = re.compile(r'TABEL\s*([0-9IlO]+)\s*[:.]?\s*EHUL\s*([IVXl1 ]+?)\s*(PLAGAL)?\s*[-–]\s*FORMULA\s*([0-9IlO]+)', re.I)

def num(s):
    return int(s.replace('I', '1').replace('l', '1').replace('O', '0'))

def table_boxes(img):
    dark = (img < 128).astype(np.uint8)
    H, W = img.shape
    hk = cv2.getStructuringElement(cv2.MORPH_RECT, (int(W * 0.25), 1))
    vk = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    grid = cv2.morphologyEx(dark, cv2.MORPH_OPEN, hk) | cv2.morphologyEx(dark, cv2.MORPH_OPEN, vk)
    grid = cv2.dilate(grid, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in cnts]
    boxes = [b for b in boxes if b[2] > W * 0.4 and b[3] > 60]
    return sorted(boxes, key=lambda b: b[1])

def vlines_box(img, x, y, w, h):
    sub = (img[y:y + h, x:x + w] < 128).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(20, int(h * 0.5))))
    opened = cv2.morphologyEx(sub, cv2.MORPH_OPEN, k)
    prof = opened.sum(0)
    idx = np.where(prof > 0)[0]
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 3:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [x + int(np.mean(g)) for g in groups]

RANGES = [((26, 34), 'I'), ((38, 45), 'II'), ((50, 57), 'III'), ((61, 66), 'IV'),
          ((67, 78), 'I pl.'), ((79, 83), 'II pl.'), ((87, 92), 'Varys'), ((93, 100), 'IV pl.')]
def MODE_OF(p):
    for (a, b), m in RANGES:
        if a <= p <= b:
            return m
TF = {'I': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'II': [1, 3, 4, 5, 6, 7, 8, 9, 10],
      'III': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'IV': [1, 3, 5, 7, 8, 9, 10],
      'I pl.': [1, 2, 3, 5, 8, 9, 10, 11], 'II pl.': [1, 3, 5, 8, 9],
      'Varys': [1, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'IV pl.': [1, 2, 3, 5, 6, 8, 9, 10, 11]}

def vtop(img, x, y0, y1):
    col = (img[y0:y1, x - 2:x + 3] < 160).any(1)
    run = 0
    for i, v in enumerate(col):
        run = run + 1 if v else 0
        if run >= 30:
            return y0 + i - 29
    return None

KEYS = ('TABEL', 'VECHEA', 'NOUA', 'GRAFIE', 'FORMULA', 'EHUL')
def score(img):
    t = pytesseract.image_to_string(cv2.resize(img, None, fx=0.6, fy=0.6), config='--psm 11 -l eng').upper()
    return sum(t.count(k) for k in KEYS) + sum(t.count(k) for k in (' DP', ' GP', ' CC', ' PB', 'PLP'))

def orient(img):
    cands = [img, cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE), cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)]
    s0 = score(cands[0])
    if s0 >= 3:
        return img
    scores = [s0] + [score(c) for c in cands[1:]]
    return cands[int(np.argmax(scores))]

def main(pages, out):
    rows = []
    current = None
    tcount = {}
    for pdf_page in pages:
        img = orient(cv2.imread(f'p-{pdf_page:03d}.png', cv2.IMREAD_GRAYSCALE))
        H, W = img.shape
        for (bx, by, bw, bh) in table_boxes(img):
            vx = vlines_box(img, bx, by, bw, bh)
            if len(vx) < 4:
                continue
            xa0, xa1, xe1 = vx[-3], vx[-2], vx[-1]
            hy = hlines_in(img[by:by + bh], bx, bx + bw, bw * 0.6)
            hy = [by + y for y in hy]
            # caption: text in band between first two full-width lines, if it contains TABEL
            top = vtop(img, xa1, by, by + bh)
            cap = ''
            if top and top - by > 25:
                band = img[by + 2:top - 2, bx + 5:bx + bw - 5]
                cap = pytesseract.image_to_string(cv2.resize(band, None, fx=2, fy=2), config='--psm 7 -l eng')
            capu = cap.upper()
            is_cap = bool(re.search(r'FORMULA|EHUL|TABEL|MULA', capu))
            if is_cap:
                mode = MODE_OF(pdf_page)
                mt = re.search(r'([0-9]{1,2})\s*[:;,.]', capu)
                mf = re.search(r'(?:FORMULA|MULA)\s*([0-9]{1,2})', capu)
                t_no = int(mt.group(1)) if mt else None
                f_no = int(mf.group(1)) if mf else None
                prev_t = current[0] if current and current[1] == mode else 0
                if t_no is None or not (1 <= t_no <= len(TF[mode])):
                    t_no = prev_t + 1
                    how = 'inferred_T'
                else:
                    how = 'ocr_T'
                exp_f = TF[mode][t_no - 1] if t_no <= len(TF[mode]) else None
                if f_no is None:
                    f_no, how = exp_f, how + '+inferred_F'
                status = 'ok' if f_no == exp_f and t_no == prev_t + 1 else 'CHECK'
                current = (t_no, mode, f_no, f'{status}:{how}')
            flag = '' if len(vx) >= 5 else 'MANUAL_columns'
            ya = hlines_in(img[by:by + bh], xa0 + 3, xa1 - 3, (xa1 - xa0) * 0.7)
            ya = sorted(set([by + y for y in ya] + [by + bh - 1]))
            ye = [by + y for y in hlines_in(img[by:by + bh], xa1 + 3, xe1 - 3, (xe1 - xa1) * 0.7)]
            for y0, y1 in zip(ya, ya[1:]):
                if y1 - y0 < 25:
                    continue
                at = ocr(img[y0 + 3:y1 - 3, xa0 + 4:xa1 - 4])
                nr_img = img[y0 + 3:min(y1 - 3, y0 + 70), vx[0] + 3:vx[1] - 3]
                nr_txt = pytesseract.image_to_string(cv2.resize(nr_img, None, fx=2, fy=2), config='--psm 7 -l eng -c tessedit_char_whitelist=0123456789.').strip()
                mnr = re.match(r'(\d{1,2})', nr_txt)
                nr = int(mnr.group(1)) if mnr else None
                header = bool(re.fullmatch(r'\W*[AE][.,]?\W*', at.strip())) or 'TABEL' in at.upper() or 'VECHEA' in at.upper()
                if header or (nr is None and (not at or len(at) > 25)):
                    continue
                comp, stasis = norm_composer(at)
                ecuts = [y for y in ye if y0 + 5 < y < y1 - 5]
                bounds = [y0] + ecuts + [y1]
                subs = []
                for e0, e1 in zip(bounds, bounds[1:]):
                    et = ocr(img[e0 + 3:e1 - 3, xa1 + 4:xe1 - 4])
                    subs.append((et, norm_exegetes(et)))
                rows.append(dict(
                    pdf_page=pdf_page,
                    table=current[0] if current else None,
                    mode=current[1] if current else None,
                    formula=current[2] if current else None,
                    tf_check=current[3] if current else None,
                    page_flag=flag,
                    y_top=y0,
                    row_nr=nr,
                    composer_raw=at, composer=comp, stasis=stasis,
                    new_method_lines=len(subs),
                    exegete_cells=' | '.join(s for s, _ in subs),
                    exegetes_per_line=' | '.join('+'.join(e) for _, e in subs),
                ))
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), 'rows')

if __name__ == '__main__':
    pages = [int(x) for x in sys.argv[2:]]
    main(pages, sys.argv[1])
