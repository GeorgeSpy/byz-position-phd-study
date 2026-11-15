#!/usr/bin/env python3
"""Mechanical consistency checks for the public Karagkounis catalogue CSVs.

Usage: python docs/research/corpus/tools/validate_karagkounis_inventory.py
"""
from pathlib import Path
from collections import Counter
import csv
import json

DATA=Path(__file__).resolve().parents[1]/'data'

def rows(name):
    with (DATA/name).open(encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))

def main():
    works=rows('karagkounis2003_all_works_1_933.csv')
    period=rows('karagkounis2003_period_vii_691_933.csv')
    composers=rows('karagkounis2003_composers_period_vii.csv')
    supplements=rows('karagkounis2005_three_supplementary_hymn_catalogs.csv')
    refs=rows('karagkounis2003_named_position_work_references.csv')
    modes_unresolved={int(x['catalog_no']) for x in works if x['mode_quality']=='UNRESOLVED_SOURCE_MODE'}
    assert len(works)==933
    assert [int(x['catalog_no']) for x in works]==list(range(1,934))
    assert len({x['record_id'] for x in works})==933
    assert len(period)==243 and period==works[690:]
    assert len(composers)==24 and sum(int(x['works_in_catalog']) for x in composers)==243
    assert len(supplements)==118
    assert Counter(x['hymn_group'] for x in supplements)=={'THU':23,'SAT':22,'PRE':73}
    assert len(refs)==206 and len({x['work_id'] for x in refs})==161
    assert all(x['work_id']==f"K03-W{int(x['catalog_no']):03d}" for x in refs)
    assert all(int(x['catalog_no'])<=690 for x in refs)
    assert Counter(x['formula_id'] for x in refs)=={'K03-F01':88,'K03-F02':34,'K03-F03':8,'K03-F04':10,'K03-F07':66}
    assert {int(x['catalog_no']) for x in works if x['catalog_id_editorial_note']}=={327,690}
    assert modes_unresolved=={56,291,455,575,824,895}
    assert all(x['st_anthony_match_status']=='NOT_ASSESSED' for x in works)
    assert all(x['position_annotation_status']=='NOT_ANNOTATED' for x in works)
    assert all(x['evidence_granularity']=='CATALOG_NUMBER_CROSS_REFERENCE' for x in refs)
    assert len(rows('karagkounis_position_and_chain_register.csv'))==10
    assert len(rows('karagkounis_musicological_evidence_register.csv'))==13
    assert len(rows('karagkounis_historical_relation_candidates.csv'))==6
    assert len(rows('karagkounis_gheorghita_terminology_crosswalk.csv'))==6
    assert len(rows('source_verification_queue.csv'))==12
    manifest=json.loads((DATA/'karagkounis_inventory_manifest.json').read_text(encoding='utf-8'))
    assert manifest['catalog_2003']==len(works)
    assert manifest['catalog_period_VII']==len(period)
    assert manifest['named_position_references']==len(refs)
    print('Karagkounis inventories: all mechanical tests passed.')

if __name__=='__main__':main()
