"""Contract tests for real-score A2-S3 ingestion using synthetic fixtures only."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from a2s3_ingest import InputError, evaluate, load, validate


def synthetic_bundle(repetitions=1, perturbations=1):
    groups = {'base_train': ['gB'], 'head_train': ['gH'],
              'development': ['gD'], 'holdout': ['gT']}
    reps = [f'r{j:02d}' for j in range(1, repetitions+1)]
    perts = [f'p{j:02d}' for j in range(1, perturbations+1)]
    cells = ['FV', 'DV'] + [f'{c}:{p}' for c in ('FP', 'DP') for p in perts]
    manifest = {
        'schema':'a2s3-ingestion/v1','dataset_id':'SYNTHETIC_UNIT_TEST',
        'dataset_origin':'synthetic','annotation_guide_version':'toy-reviewed-1',
        'source_manifest_id':'toy-synthetic-source','rights_status':'cleared',
        'indexing':'global_zero_based_inclusive_events',
        'candidate_indexing':'window_local_zero_based_inclusive',
        'family_catalogue':['A','B'],'max_span_length':5,
        'replications':reps,'perturbations':perts,
        'partitions':groups,'leakage_clusters':{g:g for arr in groups.values() for g in arr},
        'base_models':{r:{'checkpoint_id':f'base-{r}','trained_groups':['gB'],'temperature':1.0} for r in reps},
        'cell_models':{r:{c:{'model_id':f'{r}-{c}','base_checkpoint_id':f'base-{r}',
                                'trained_groups':['gH'],'tuned_groups':['gD']}
                           for c in cells} for r in reps}
    }
    annotations=[]
    base=[]
    exports=[]
    for gi,g in enumerate(['gB','gH','gD','gT']):
        for family in ('A','B'):
            first = 100+gi*30+(0 if family == 'A' else 10)
            good_end = first + (3 if family == 'A' else 4)
            start = first+1
            trunc_end,extension_end = good_end-1,good_end+1
            oid = f'{g}-{family}'
            annotations.append({
                'occurrence_id':oid,'group_id':g,'work_id':f'work-{g}',
                'witness_id':f'witness-{g}','status':'eligible','family_id':family,
                'preferred_start':start,'window':{'start':first,'end':first+7},
                'accepted_bounds':[{'start':start,'end':good_end}],
                'variants':{'truncation':{'start':start,'end':trunc_end},
                            'extension':{'start':start,'end':extension_end}},
                'candidate_endpoints':{'truncation':[trunc_end],'extension':[extension_end]},
                'reviewer_ids':['e1','e2'],
                'gap_judgements':{str(x+1):{'e1':'continuation','e2':'continuation'}
                                  for x in (trunc_end,extension_end)},
                'agreed_boundary_gaps':[first,first+8],
                'articulation_by_end_gap':{str(x+1):2 for x in (trunc_end,extension_end)},
                'connective_events':[extension_end],
                'next_formula_start':extension_end+1,
            })
            candidates=[{'start':1,'end':length,'family':f,'base_score':0.01*length,
                         'articulation':float(length%2),'text_boundary':0.0}
                        for f in ('A','B') for length in range(2,6)]
            for r in reps:
                base.append({'occurrence_id':oid,'replication_id':r,
                    'checkpoint_id':f'base-{r}','score_kind':'calibrated_unnormalized_log_potential',
                    'skip_scores':[0.0]*8,'candidates':candidates})
                for c in cells:
                    cell,_,pert = c.partition(':')
                    scores=[{'start':k['start'],'end':k['end'],'family':k['family'],
                             'score':0.02* k['end'] + (0.03 if cell.startswith('D') else 0)
                                + (0.005 if pert else 0)} for k in candidates]
                    exports.append({'occurrence_id':oid,'replication_id':r,
                        'cell':cell,'perturbation_id':pert if pert else None,
                        'model_id':f'{r}-{c}','base_checkpoint_id':f'base-{r}',
                        'score_kind':'unnormalized_log_potential','candidate_scores':scores})
    return manifest, {'schema':'a2s3-annotations/v1','records':annotations}, {'schema':'a2s3-scores/v1','base':base,'cells':exports}


class IngestTests(unittest.TestCase):
    def setUp(self):
        self.manifest,self.annotations,self.scores=synthetic_bundle()

    def assertReject(self, reason, manifest=None, annotations=None, scores=None):
        with self.assertRaisesRegex((InputError, ValueError, KeyError, TypeError),reason):
            validate(manifest if manifest is not None else self.manifest,
                     annotations if annotations is not None else self.annotations,
                     scores if scores is not None else self.scores)

    def test_valid_minimal_pilot(self):
        result=validate(self.manifest,self.annotations,self.scores)
        self.assertEqual(len(result.annotations),8)
        self.assertEqual(len(result.cell_scores),32)

    def test_holdout_is_not_used_to_fit_bl(self):
        result=evaluate(validate(self.manifest,self.annotations,self.scores))
        self.assertEqual(result['reproducibility_status'],'pilot_interface')
        self.assertEqual(len(result['replications']['r01']['holdout_contrasts']),2)
        self.assertIn('delta_know',result['replications']['r01']['macro_by_fixed_family']['truncation'])
        self.assertEqual(set(result['replications']['r01']['holdout_contrasts'][0]['contrasts']),
                         {'truncation','extension'})

    def test_reject_partial_five_by_one_configuration(self):
        m,a,s=synthetic_bundle(5,1)
        self.assertReject('1/1 for interface pilot or 5/10',manifest=m,annotations=a,scores=s)

    def test_complete_five_by_ten_layout(self):
        m,a,s=synthetic_bundle(5,10)
        out=validate(m,a,s)
        self.assertEqual(len(out.cell_scores),8*5*22)

    def test_indexing_contract_rejected(self):
        self.manifest['indexing']='one_based'
        self.assertReject('index convention')

    def test_manifest_missing_group_rejected(self):
        self.manifest['partitions']['development']=['gH']
        self.assertReject('group reused')

    def test_related_work_cluster_across_splits_rejected(self):
        self.manifest['leakage_clusters']['gT']='gH'
        self.assertReject('related groups')

    def test_same_work_across_splits_rejected(self):
        self.annotations['records'][-1]['work_id']='work-gH'
        self.assertReject('work_id crosses')

    def test_base_trained_on_holdout_rejected(self):
        self.manifest['base_models']['r01']['trained_groups']=['gT']
        self.assertReject('base checkpoint trained')

    def test_head_trained_on_holdout_rejected(self):
        self.manifest['cell_models']['r01']['FV']['trained_groups']=['gT']
        self.assertReject('A2 head trained')

    def test_cell_cross_base_rejected(self):
        self.manifest['cell_models']['r01']['DV']['base_checkpoint_id']='another'
        self.assertReject('different frozen base')

    def test_wrong_base_score_temperature_convention_rejected(self):
        self.scores['base'][0]['score_kind']='unnormalized_log_potential'
        self.assertReject('calibrated frozen temperature')

    def test_missing_family_for_candidate_span_rejected(self):
        self.scores['base'][0]['candidates'].pop(-1)
        self.assertReject('every candidate span')

    def test_wrong_score_type_rejected(self):
        self.scores['cells'][0]['score_kind']='log_posterior'
        self.assertReject('unnormalized')

    def test_score_export_includes_truth_rejected(self):
        self.scores['cells'][0]['true_family']='A'
        self.assertReject('expected')

    def test_missing_condition_rejected(self):
        self.scores['cells'].pop()
        self.assertReject('incomplete factorial')

    def test_family_candidate_space_disagreement_rejected(self):
        self.scores['cells'][0]['candidate_scores'].pop()
        self.assertReject('different candidate universe')

    def test_nonfinite_score_rejected(self):
        self.scores['cells'][0]['candidate_scores'][0]['score']=float('nan')
        self.assertReject('finite number')

    def test_unreviewed_gap_rejected(self):
        self.annotations['records'][0]['gap_judgements'][str(103)].pop('e2')
        self.assertReject('unreviewed_gap')

    def test_accepted_variant_rejected(self):
        a=self.annotations['records'][0]
        a['variants']['truncation']=a['accepted_bounds'][0]
        a['candidate_endpoints']['truncation']=[a['accepted_bounds'][0]['end']]
        a['articulation_by_end_gap'][str(a['accepted_bounds'][0]['end']+1)] = 2
        a['gap_judgements'][str(a['accepted_bounds'][0]['end']+1)] = {'e1':'continuation','e2':'continuation'}
        self.assertReject('accepted_extent|not_strict_truncation')

    def test_nonshared_window_rejected(self):
        self.annotations['records'][0]['agreed_boundary_gaps']=[101,108]
        self.assertReject('not the canonical')

    def test_weak_articulation_variant_rejected(self):
        a=self.annotations['records'][0]
        a['candidate_endpoints']['truncation']=[a['variants']['truncation']['end'],
                                                a['variants']['truncation']['end']-1]
        a['articulation_by_end_gap'][str(a['variants']['truncation']['end'])]=10
        self.assertReject('articulation selection')

    def test_hash_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for fn,obj in [('annotations',self.annotations),('scores',self.scores)]:
                b=(json.dumps(obj,sort_keys=True)+'\n').encode()
                (root/(fn+'.json')).write_bytes(b)
                self.manifest['annotation_sha256' if fn=='annotations' else 'scores_sha256']=hashlib.sha256(b).hexdigest()
            (root/'manifest.json').write_text(json.dumps(self.manifest))
            load(root/'manifest.json',root/'annotations.json',root/'scores.json')
            (root/'scores.json').write_text((root/'scores.json').read_text()+' ')
            with self.assertRaisesRegex(InputError,'SHA-256'):
                load(root/'manifest.json',root/'annotations.json',root/'scores.json')

    def test_excluded_occurrence_keeps_reason(self):
        self.annotations['records'].append({'occurrence_id':'excluded','group_id':'gT',
             'work_id':'work-gT','witness_id':'witness-gT','status':'excluded','reason':'missing_review'})
        out=validate(self.manifest,self.annotations,self.scores)
        self.assertEqual(out.excluded['excluded'],'missing_review')


if __name__=='__main__':
    unittest.main()
