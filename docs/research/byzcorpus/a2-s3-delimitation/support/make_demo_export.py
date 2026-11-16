"""Create explicitly synthetic, integrity-checked A2-S3 score-export fixtures."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

from test_a2s3_ingest import synthetic_bundle


def create(folder: str | Path, full: bool = False) -> dict[str, str]:
    root = Path(folder)
    root.mkdir(parents=True, exist_ok=True)
    manifest, annotations, scores = synthetic_bundle(5,10) if full else synthetic_bundle(1,1)
    checksums = {}
    for filename, payload in [('annotations.json',annotations), ('scores.json',scores)]:
        data = (json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')
        (root/filename).write_bytes(data)
        checksums[filename] = hashlib.sha256(data).hexdigest()
    manifest['annotation_sha256'] = checksums['annotations.json']
    manifest['scores_sha256'] = checksums['scores.json']
    (root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return checksums


if __name__ == '__main__':
    if len(sys.argv) not in (2,3) or (len(sys.argv)==3 and sys.argv[2]!='--full'):
        raise SystemExit('usage: python make_demo_export.py OUTPUT_DIRECTORY [--full]')
    print(json.dumps(create(sys.argv[1],len(sys.argv)==3),sort_keys=True,indent=2))
