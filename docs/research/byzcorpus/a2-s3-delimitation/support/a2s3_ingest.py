"""Strict input gateway for A2-S3 accepted-extent comparisons.

Consumes *unnormalised segment log potentials*, source-reviewed annotations,
and explicit frozen-model and split manifests. Scores are never inferred from
labels; every cell shares the same candidate and skip-score space. Inputs can
be synthetic or an independently prepared empirical export.

Run: python a2s3_ingest.py manifest.json annotations.json scores.json
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from a2s3_reference import (Span, admissible_variant, choose_endpoint,
                            forward_logprobs, shared_window, family_balanced_mean)
from bl_train import Candidate, FeatureSpec, Window, choose_l2, endpoint_log_contrast


class InputError(ValueError):
    """A source, split, annotation or model-score contract was violated."""


def _fail(message: str) -> None:
    raise InputError(message)


def _required(obj: dict, names: set[str], where: str, optional: set[str] = frozenset()) -> None:
    if not isinstance(obj, dict) or not names.issubset(obj) or set(obj) - names - optional:
        _fail(f"{where}: expected {sorted(names)} (+ {sorted(optional)}); got {sorted(obj) if isinstance(obj, dict) else type(obj).__name__}")


def _unique_strings(values: Any, where: str) -> tuple[str, ...]:
    if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() for v in values):
        _fail(f"{where}: nonempty string array required")
    if len(set(values)) != len(values):
        _fail(f"{where}: duplicate identifier")
    return tuple(values)


def _number(x: Any, where: str) -> float:
    if isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x):
        _fail(f"{where}: finite number required")
    return float(x)


def _integer(x: Any, where: str) -> int:
    if isinstance(x, bool) or not isinstance(x, int) or x < 0:
        _fail(f"{where}: nonnegative integer required")
    return x


def _pair(v: Any, where: str) -> Span:
    _required(v, {'start', 'end'}, where)
    return Span(_integer(v['start'], where+'.start'), _integer(v['end'], where+'.end'))


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: str | Path) -> tuple[Any, str]:
    raw = Path(path).read_bytes()
    return json.loads(raw), _sha(raw)


@dataclass(frozen=True)
class Annotation:
    occurrence_id: str
    group_id: str
    work_id: str
    witness_id: str
    family_id: str
    start_event: int
    n_events: int
    accepted: frozenset[tuple[int, int, str]]
    all_accepted: frozenset[tuple[int, int, str]]
    variants: dict[str, tuple[int, int, str]]


@dataclass(frozen=True)
class Validated:
    manifest: dict[str, Any]
    annotations: dict[str, Annotation]
    base: dict[tuple[str, str], Window]
    cell_scores: dict[tuple[str, str, str], dict[tuple[int, int, str], float]]
    partitions: dict[str, tuple[str, ...]]
    excluded: dict[str, str]


def validate(manifest: dict, annotations: dict, scores: dict) -> Validated:
    _required(manifest, {'schema', 'dataset_id', 'dataset_origin', 'annotation_guide_version',
                         'source_manifest_id', 'rights_status', 'indexing', 'candidate_indexing', 'family_catalogue',
                         'max_span_length', 'replications', 'perturbations', 'partitions',
                         'leakage_clusters', 'base_models', 'cell_models'}, 'manifest',
              {'annotation_sha256', 'scores_sha256'})
    if manifest['schema'] != 'a2s3-ingestion/v1':
        _fail('unknown ingestion schema')
    if manifest['dataset_origin'] not in ('synthetic', 'empirical'):
        _fail('dataset origin must be declared')
    if manifest['indexing'] != 'global_zero_based_inclusive_events' or manifest['candidate_indexing'] != 'window_local_zero_based_inclusive':
        _fail('index convention differs from A2-S3 protocol')
    if manifest['rights_status'] not in ('cleared', 'restricted', 'review_pending'):
        _fail('rights review status required')
    for name in ('dataset_id', 'annotation_guide_version', 'source_manifest_id'):
        if not isinstance(manifest[name], str) or not manifest[name].strip():
            _fail(f'manifest.{name}: identifier required')
    families = _unique_strings(manifest['family_catalogue'], 'family_catalogue')
    repetitions = _unique_strings(manifest['replications'], 'replications')
    perturbations = _unique_strings(manifest['perturbations'], 'perturbations')
    length_max = _integer(manifest['max_span_length'], 'max_span_length')
    if length_max < 2:
        _fail('max span length must be at least 2')
    if (len(repetitions), len(perturbations)) not in ((1, 1), (5, 10)):
        _fail('use 1/1 for interface pilot or 5/10 for full A2 export')

    partitions = manifest['partitions']
    _required(partitions, {'base_train', 'head_train', 'development', 'holdout'}, 'partitions')
    groups = {k: _unique_strings(v, 'partition '+k) for k, v in partitions.items()}
    owner = {}
    for part, vals in groups.items():
        for group in vals:
            if group in owner:
                _fail(f'group reused between partitions: {group}')
            owner[group] = part
    clusters = manifest['leakage_clusters']
    if not isinstance(clusters, dict) or set(clusters) != set(owner):
        _fail('each independent group requires a leakage cluster')
    cluster_parts = defaultdict(set)
    for group, cl in clusters.items():
        if not isinstance(cl, str) or not cl:
            _fail('invalid leakage cluster')
        cluster_parts[cl].add(owner[group])
    if any(len(x) != 1 for x in cluster_parts.values()):
        _fail('related groups cross partition boundary')

    base_models, cell_models = manifest['base_models'], manifest['cell_models']
    if set(base_models) != set(repetitions) or set(cell_models) != set(repetitions):
        _fail('frozen base and A2 model manifests must cover each repetition')
    expected_cells = {'FV', 'DV'} | {f'{cell}:{pert}' for cell in ('FP', 'DP') for pert in perturbations}
    for r in repetitions:
        b = base_models[r]
        _required(b, {'checkpoint_id', 'trained_groups', 'temperature'}, 'base model '+r)
        if not isinstance(b['checkpoint_id'], str) or not b['checkpoint_id']:
            _fail('missing base checkpoint ID')
        if not set(_unique_strings(b['trained_groups'], 'base groups')).issubset(set(groups['base_train'])):
            _fail('base checkpoint trained on an invalid group')
        if _number(b['temperature'], 'temperature') <= 0:
            _fail('temperature must be positive')
        if set(cell_models[r]) != expected_cells:
            _fail(f'incomplete A2 condition / perturbation inventory for {r}')
        for key, meta in cell_models[r].items():
            _required(meta, {'model_id', 'base_checkpoint_id', 'trained_groups', 'tuned_groups'}, 'cell '+key)
            if not meta['model_id'] or meta['base_checkpoint_id'] != b['checkpoint_id']:
                _fail('condition model references a different frozen base')
            if not set(_unique_strings(meta['trained_groups'], 'head groups')).issubset(set(groups['head_train'])):
                _fail('A2 head trained on other groups')
            if not set(_unique_strings(meta['tuned_groups'], 'tuning groups')).issubset(set(groups['development'])):
                _fail('A2 head tuned using another partition')

    _required(annotations, {'schema', 'records'}, 'annotations')
    if annotations['schema'] != 'a2s3-annotations/v1' or not isinstance(annotations['records'], list):
        _fail('annotation schema / records invalid')
    ann: dict[str, Annotation] = {}
    excluded: dict[str, str] = {}
    seen_work, seen_witness = {}, {}
    for row in annotations['records']:
        expected = {'occurrence_id', 'group_id', 'work_id', 'witness_id', 'status'}
        _required(row, expected, 'annotation record',
                  {'reason', 'family_id', 'preferred_start', 'window', 'accepted_bounds',
                   'variants', 'reviewer_ids', 'gap_judgements', 'agreed_boundary_gaps',
                   'connective_events', 'next_formula_start', 'candidate_endpoints',
                   'articulation_by_end_gap'})
        oid = row['occurrence_id']
        if not isinstance(oid, str) or not oid or oid in ann or oid in excluded:
            _fail('missing/duplicate occurrence ID')
        group = row['group_id']
        if group not in owner or any(not row.get(k) or not isinstance(row[k], str) for k in ('work_id', 'witness_id')):
            _fail('missing independent group, work or witness')
        for seen, id_name in ((seen_work, 'work_id'), (seen_witness, 'witness_id')):
            key = row[id_name]
            if key in seen and seen[key] != owner[group]:
                _fail(f'{id_name} crosses experimental partitions: {key}')
            seen[key] = owner[group]
        if row['status'] == 'excluded':
            if not isinstance(row.get('reason'), str) or not row['reason']:
                _fail('excluded records need an explicit reason')
            excluded[oid] = row['reason']
            continue
        if row['status'] != 'eligible':
            _fail('unknown annotation status')
        for field in ('family_id', 'preferred_start', 'window', 'accepted_bounds', 'variants',
                      'reviewer_ids', 'gap_judgements', 'agreed_boundary_gaps',
                      'connective_events', 'next_formula_start', 'candidate_endpoints',
                      'articulation_by_end_gap'):
            if field not in row:
                _fail(f'{oid}: missing {field}')
        if row['family_id'] not in families:
            _fail(f'{oid}: family outside fixed catalog')
        start = _integer(row['preferred_start'], 'preferred_start')
        _required(row['window'], {'start','end'}, 'window')
        first = _integer(row['window']['start'], 'window.start')
        last = _integer(row['window']['end'], 'window.end')
        if last < first or start < first or start > last:
            _fail('invalid reviewed window or preferred start')
        accepted_abs = [_pair(v, oid+'.accepted_bounds') for v in row['accepted_bounds']]
        if not accepted_abs or len(set(accepted_abs)) != len(accepted_abs):
            _fail('nonempty unique accepted bounds required')
        if not any(a.start == start for a in accepted_abs):
            _fail('preferred start has no accepted extent')
        for a in accepted_abs:
            if not (first <= a.start <= a.end <= last) or a.length > length_max:
                _fail('accepted extent outside window / maximum segment length')
        variants = row['variants']
        _required(variants, {'truncation', 'extension'}, 'variants')
        parsed = {kind: _pair(v, kind) for kind, v in variants.items()}
        proposed = row['candidate_endpoints']
        _required(proposed, {'truncation', 'extension'}, 'candidate_endpoints')
        articulation = {int(k): _integer(v, 'articulation score')
                        for k, v in row['articulation_by_end_gap'].items()}
        reviewers = _unique_strings(row['reviewer_ids'], 'reviewers')
        gap_judgements = {int(k): v for k,v in row['gap_judgements'].items()}
        agreed = {_integer(x, 'agreed gap') for x in row['agreed_boundary_gaps']}
        connective = {_integer(x, 'connective event') for x in row['connective_events']}
        next_start = row['next_formula_start']
        if next_start is not None:
            _integer(next_start, 'next formula start')
        for kind, span in parsed.items():
            if span.length > length_max or not first <= span.start <= span.end <= last:
                _fail('variant exceeds candidate domain / window')
            proposals = [_integer(end, 'candidate endpoint') for end in proposed[kind]]
            if not proposals or len(set(proposals)) != len(proposals):
                _fail('candidate endpoint set missing or duplicated')
            accepted_ref = min(a.end for a in accepted_abs if a.start == start) if kind == 'truncation' else max(a.end for a in accepted_abs)
            if choose_endpoint(proposals, articulation, accepted_ref) != span.end:
                _fail('variant fails prespecified articulation selection rule')
            valid, reason = admissible_variant(kind=kind, variant=span,
                accepted=accepted_abs, preferred_start=start, opinions=gap_judgements,
                expected_experts=reviewers, connective_events=connective,
                next_formula_start=next_start)
            if not valid:
                _fail(f'{oid}.{kind}: {reason}')
            if span in accepted_abs:
                _fail('candidate variant is accepted as complete')
        common = shared_window(accepted_abs, list(parsed.values()), agreed)
        if common != Span(first, last):
            _fail(f'{oid}: declared common window is not the canonical enclosing window')
        accepted_local = frozenset((a.start-first, a.end-first, row['family_id'])
                                   for a in accepted_abs if a.start == start)
        variant_local = {kind: (v.start-first, v.end-first, row['family_id'])
                         for kind, v in parsed.items()}
        all_local = frozenset((a.start-first,a.end-first,row['family_id'])
                              for a in accepted_abs)
        ann[oid] = Annotation(oid, group, row['work_id'], row['witness_id'],
                              row['family_id'], first, last-first+1,
                              accepted_local, all_local, variant_local)
    if not ann:
        _fail('no eligible reviewed occurrences')

    _required(scores, {'schema', 'base', 'cells'}, 'score export')
    if scores['schema'] != 'a2s3-scores/v1':
        _fail('incorrect score format')
    if not isinstance(scores['base'], list) or not isinstance(scores['cells'], list):
        _fail('base and A2 cells must be arrays')
    baseline: dict[tuple[str,str], Window] = {}
    for row in scores['base']:
        _required(row, {'occurrence_id', 'replication_id', 'checkpoint_id',
                        'score_kind', 'skip_scores', 'candidates'}, 'base-score row')
        oid, rep = row['occurrence_id'], row['replication_id']
        key = (oid, rep)
        if oid not in ann or rep not in repetitions or key in baseline:
            _fail('unknown/duplicate base row')
        if row['checkpoint_id'] != base_models[rep]['checkpoint_id']:
            _fail('incorrect frozen base checkpoint')
        if row['score_kind'] != 'calibrated_unnormalized_log_potential':
            _fail('expected b_r/T_r potentials with calibrated frozen temperature; no second division applied')
        record = ann[oid]
        if not isinstance(row['skip_scores'], list) or len(row['skip_scores']) != record.n_events:
            _fail('missing per-event skip potentials')
        skips = tuple(_number(v, 'skip potential') for v in row['skip_scores'])
        if not isinstance(row['candidates'], list):
            _fail('missing candidate scores')
        cand = []
        for c in row['candidates']:
            _required(c, {'start','end','family','base_score','articulation','text_boundary'}, 'base candidate')
            a,b = _integer(c['start'],'candidate start'), _integer(c['end'],'candidate end')
            if b < a or b >= record.n_events or b-a+1 > length_max or c['family'] not in families:
                _fail('candidate invalid or outside max span length')
            cand.append(Candidate(a,b,c['family'],_number(c['base_score'],'base'),
                                  _number(c['articulation'],'articulation'),
                                  _number(c['text_boundary'],'text boundary')))
        window = Window(record.occurrence_id, record.group_id,record.n_events,
                        skips,tuple(cand),record.accepted)
        keys = {c.key for c in cand}
        if len(keys) != len(cand) or not set(record.variants.values()).issubset(keys) or not record.all_accepted.issubset(keys):
            _fail('accepted/variant paths not fully covered')
        by_span = defaultdict(set)
        for c in cand:
            by_span[(c.start,c.end)].add(c.family)
        if any(fset != set(families) for fset in by_span.values()):
            _fail('every candidate span must be scored for every family')
        baseline[key] = window
    expected_base = {(oid, rep) for oid in ann for rep in repetitions}
    if set(baseline) != expected_base:
        _fail('missing eligible occurrence / replication base export')

    a2: dict[tuple[str,str,str], dict[tuple[int,int,str],float]] = {}
    for row in scores['cells']:
        _required(row, {'occurrence_id','replication_id','cell','perturbation_id',
                        'model_id','base_checkpoint_id','score_kind','candidate_scores'}, 'A2 cell row')
        oid, rep, cell = row['occurrence_id'], row['replication_id'], row['cell']
        pert = row['perturbation_id']
        if cell not in ('FV','DV','FP','DP'):
            _fail('invalid A2 condition')
        if cell in ('FP','DP') and pert not in perturbations:
            _fail('incorrect perturbation ID')
        if cell in ('FV','DV') and pert is not None:
            _fail('valid knowledge cells must have null perturbation ID')
        label = cell if pert is None else f'{cell}:{pert}'
        key = (oid,rep,label)
        if (oid,rep) not in baseline or key in a2:
            _fail('unexpected or duplicate A2 scoring row')
        registry = cell_models[rep][label]
        if row['model_id'] != registry['model_id'] or row['base_checkpoint_id'] != base_models[rep]['checkpoint_id']:
            _fail('model provenance mismatch')
        if row['score_kind'] != 'unnormalized_log_potential' or not isinstance(row['candidate_scores'],list):
            _fail('expected all unnormalized per-candidate segment potentials')
        value_map = {}
        for entry in row['candidate_scores']:
            _required(entry, {'start','end','family','score'}, 'cell segment')
            ck = (_integer(entry['start'],'start'),_integer(entry['end'],'end'),entry['family'])
            if ck in value_map:
                _fail('duplicate cell candidate')
            value_map[ck] = _number(entry['score'],'cell score')
        if set(value_map) != {c.key for c in baseline[(oid,rep)].candidates}:
            _fail('A2 condition has different candidate universe')
        a2[key] = value_map
    expected_scores = {(oid,rep,label) for oid in ann for rep in repetitions for label in expected_cells}
    if set(a2) != expected_scores:
        _fail('incomplete factorial cells / perturbations / score alignment')
    return Validated(manifest, ann, baseline, a2,groups,excluded)


def load(manifest_path: str | Path, annotations_path: str | Path, scores_path: str | Path) -> Validated:
    manifest,_ = _read_json(manifest_path)
    annotations,a_hash = _read_json(annotations_path)
    scores,s_hash = _read_json(scores_path)
    if 'annotation_sha256' not in manifest or 'scores_sha256' not in manifest:
        _fail('frozen SHA-256 of both exports must be included in manifest')
    if a_hash != manifest['annotation_sha256'] or s_hash != manifest['scores_sha256']:
        _fail('export SHA-256 provenance mismatch')
    return validate(manifest, annotations, scores)


def _d(window: Window, accepted: frozenset, variant: tuple, values: dict) -> float:
    span_scores = {key:score for key,score in values.items()}
    log_ok,_ = forward_logprobs(window.n_events,window.skip_scores,span_scores,set(accepted))
    log_variant,_ = forward_logprobs(window.n_events,window.skip_scores,span_scores,{variant})
    if not all(map(math.isfinite,(log_ok, log_variant))):
        _fail('nonfinite probability contrast')
    return log_ok - log_variant


def evaluate(valid: Validated, *, l2_grid: tuple[float,...] = (.01,.1,1.0)) -> dict[str, Any]:
    ann,groups = valid.annotations, valid.partitions
    by_group = {part: [oid for oid, rec in ann.items() if rec.group_id in set(ids)]
                for part,ids in groups.items()}
    if not by_group['head_train'] or not by_group['development'] or not by_group['holdout']:
        _fail('eligible rows required in head-training, development and holdout')
    out = {}
    repetitions = valid.manifest['replications']
    perturbations = valid.manifest['perturbations']
    for rep in repetitions:
        train = [valid.base[(oid,rep)] for oid in by_group['head_train']]
        dev = [valid.base[(oid,rep)] for oid in by_group['development']]
        spec = FeatureSpec(tuple(valid.manifest['family_catalogue']),valid.manifest['max_span_length'])
        model=choose_l2(train,dev,spec,l2_grid)
        cell_labels = ('FV','DV')+tuple(f'{cell}:{p}' for cell in ('FP','DP') for p in perturbations)
        holdout = []
        for oid in sorted(by_group['holdout']):
            rec=ann[oid];w=valid.base[(oid,rep)]
            d = {}
            for kind,v in rec.variants.items():
                base_scores={c.key:c.base_score for c in w.candidates}
                d[kind]={'B_L':endpoint_log_contrast(w,model,v),
                         'BASE':_d(w,rec.accepted,v,base_scores)}
                for label in cell_labels:
                    d[kind][label]=_d(w,rec.accepted,v,valid.cell_scores[(oid,rep,label)])
            holdout.append({'occurrence_id':oid,'group_id':rec.group_id,
                            'family_id':rec.family_id,'contrasts':d})
        family_catalogue=tuple(valid.manifest['family_catalogue'])
        macro={}
        for kind in ('truncation','extension'):
            cell_keys=tuple(holdout[0]['contrasts'][kind])
            macro[kind]={label: family_balanced_mean(
                    [(row['group_id'],row['family_id'],row['contrasts'][kind][label]) for row in holdout],
                    family_catalogue) for label in cell_keys}
            avg_p=lambda cell: sum(macro[kind][f'{cell}:{pert}'] for pert in perturbations)/len(perturbations)
            macro[kind]['delta_know_S3']=.5*((macro[kind]['DV']-avg_p('DP'))
                                              +(macro[kind]['FV']-avg_p('FP')))
            macro[kind]['delta_logic_valid_S3']=macro[kind]['DV']-macro[kind]['FV']
            macro[kind]['delta_DV_vs_B_L_S3']=macro[kind]['DV']-macro[kind]['B_L']
            macro[kind]['delta_DV_vs_BASE_S3']=macro[kind]['DV']-macro[kind]['BASE']
            macro[kind]['delta_DV_vs_perturbed_S3']=macro[kind]['DV']-avg_p('DP')
        directional_fields=('delta_DV_vs_perturbed_S3','delta_DV_vs_BASE_S3','delta_DV_vs_B_L_S3')
        two_sided_directional=all(macro[k][x]>0 for k in ('truncation','extension') for x in directional_fields)
        out[rep]={'two_sided_directional_only':two_sided_directional,
                  'base_checkpoint_id':valid.manifest['base_models'][rep]['checkpoint_id'],
                  'bl_selected_l2':model.l2,'bl_train_objective':model.train_objective,
                  'macro_by_fixed_family':macro,
                  'holdout_contrasts':holdout}
    return {'schema':'a2s3-bridge-output/v1','dataset_id':valid.manifest['dataset_id'],
            'origin':valid.manifest['dataset_origin'],
            'reproducibility_status':'pilot_interface' if len(repetitions)==1 else 'complete_score_schema',
            'rights_status':valid.manifest['rights_status'],
            'source_verification':'source_registry_only; independent musicological validation required',
            'eligible_occurrences':len(ann),'excluded_occurrences':valid.excluded,
            'group_counts':{k:len(v) for k,v in groups.items()},
            'replications':out,
            'note':'Per-occurrence scores; aggregation requires fixed F0, matched groups and independent evaluation plan. No empirical effect is inferred from a synthetic pilot.'}


def main(argv: list[str]) -> int:
    if len(argv)!=4:
        print('usage: python a2s3_ingest.py manifest.json annotations.json scores.json',file=sys.stderr)
        return 2
    try:
        x = evaluate(load(argv[1],argv[2],argv[3]))
        print(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2))
        return 0
    except (InputError, ValueError, KeyError, TypeError, OSError) as err:
        print(f'A2-S3 input rejected: {err}',file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
