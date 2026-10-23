"""Check English/Greek correspondence without changing the existing reader.

Run from a full checkout. --baseline-tree accepts a GitHub recursive-tree JSON
for a partial local review; missing local blobs use its recorded paths/hashes.
--preserve-originals additionally verifies the first bilingual release baseline.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SWITCH = re.compile(
    r"\n<!-- language-switch:start -->\n[^\n]*\n<!-- language-switch:end -->\n"
)
LABELS = {
    r"\text{μη μέλος}": r"\text{non-member}",
    r"\text{μέλος}": r"\text{member}",
    r"\text{αμφίσημο}": r"\text{ambiguous}",
}


def original_bytes(data):
    return SWITCH.sub("", data.decode("utf-8")).encode("utf-8")


def blob_sha(data):
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def anchors(text):
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    seen = {}
    for title in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        title = re.sub(r"<[^>]*>", "", title).strip().lower()
        title = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
        title = re.sub(r"\s", "-", title)
        n = seen.get(title, 0)
        result.add(title if n == 0 else f"{title}-{n}")
        seen[title] = n + 1
    return result


def equations(text):
    blocks = re.findall(r"^" + chr(96)*3 + r"math\n([\s\S]*?)\n" + chr(96)*3, text, re.M)
    for old, new in LABELS.items():
        blocks = [x.replace(old, new) for x in blocks]
    return blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-tree", type=Path)
    parser.add_argument("--preserve-originals", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "en/manifest.json").read_text(encoding="utf-8"))
    navigation = json.loads((ROOT / "en/navigation.json").read_text(encoding="utf-8"))
    remote = {}
    if args.baseline_tree:
        remote = {
            x["path"]: x for x in json.loads(args.baseline_tree.read_text(encoding="utf-8"))["tree"]
            if x["type"] == "blob"
        }
    errors = []
    checked_links = 0
    deferred_anchors = set()
    translated = [x for x in manifest["pages"] if x["status"] == "translated"]
    page_pairs = {x["source"]: x["target"] for x in translated}
    if len(page_pairs) != len(translated):
        errors.append("duplicate translated source")
    if len({x["target"] for x in manifest["pages"]}) != len(manifest["pages"]):
        errors.append("duplicate English target")
    if {x["el"]: x["en"] for x in navigation["language_pairs"]} != page_pairs:
        errors.append("navigation language pairs differ from manifest")
    english_paths = [x["target"] for x in translated] + manifest["editorial_pages"]
    for p in [navigation["home"], navigation["translation_status"]]:
        if p not in english_paths:
            errors.append(f"unknown navigation page: {p}")
    for section in navigation["sections"]:
        for p in section["pages"]:
            if p not in english_paths:
                errors.append(f"unknown navigation page: {p}")

    for item in translated:
        source, target = ROOT / item["source"], ROOT / item["target"]
        if not source.is_file() or not target.is_file():
            errors.append(f"missing translation pair: {item['source']}")
            continue
        source_data = source.read_bytes()
        source_text = source_data.decode("utf-8")
        target_text = target.read_text(encoding="utf-8")
        if blob_sha(original_bytes(source_data)) != item["source_blob_sha"]:
            errors.append(f"translation needs source review: {item['source']}")
        for path, text, counterpart in [
            (source, source_text, target), (target, target_text, source)
        ]:
            switches = SWITCH.findall(text)
            if len(switches) != 1:
                errors.append(f"{path.relative_to(ROOT)}: expected one language selector")
                continue
            urls = re.findall(r"\]\(([^)]+)\)", switches[0])
            if counterpart.resolve() not in {
                (path.parent / unquote(urlsplit(u).path)).resolve() for u in urls
            }:
                errors.append(f"{path.relative_to(ROOT)}: missing counterpart link")
        if equations(source_text) != equations(target_text):
            errors.append(f"display equations differ: {item['target']}")

    for entry in manifest["original_files"]:
        path = ROOT / entry["path"]
        if not path.is_file() and entry["path"] not in remote:
            errors.append(f"original file missing: {entry['path']}")
            continue
        if args.preserve_originals:
            if path.is_file():
                data = path.read_bytes()
                if entry["path"] in page_pairs:
                    data = original_bytes(data)
                actual = blob_sha(data)
            else:
                actual = remote[entry["path"]]["sha"]
            if actual != entry["sha"]:
                errors.append(f"original content changed: {entry['path']}")

    for relative in english_paths:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing English page: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"⟦|⟧|@@M\d+@@", text):
            errors.append(f"unresolved translation placeholder: {relative}")
        if len(re.findall(r"^# ", text, re.M)) != 1:
            errors.append(f"expected one page title: {relative}")
        if len(re.findall(r"^" + chr(96)*3, text, re.M)) % 2:
            errors.append(f"unbalanced code/math fences: {relative}")
        urls = re.findall(r'!?\[[^\]\n]*\]\(([^\s\n)]+)(?:\s+"[^"]*")?\)', text)
        urls += re.findall(r'<a\s[^>]*href="([^"]+)"', text)
        for url in urls:
            parsed = urlsplit(url.strip("<>"))
            if parsed.scheme or url.startswith("//"):
                continue
            checked_links += 1
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not dest.is_relative_to(ROOT):
                errors.append(f"{relative}: link escapes repository: {url}")
                continue
            dest_relative = dest.relative_to(ROOT).as_posix()
            if not dest.exists():
                if dest_relative not in remote:
                    errors.append(f"{relative}: missing {url}")
                    continue
                if parsed.fragment and dest.suffix == ".md":
                    deferred_anchors.add(dest_relative)
                continue
            if parsed.fragment and dest.suffix == ".md":
                if unquote(parsed.fragment) not in anchors(dest.read_text(encoding="utf-8")):
                    errors.append(f"{relative}: missing anchor {url}")
    if errors:
        print("\n".join(errors))
        print(f"FAILED: {len(errors)} problems")
        return 1
    print(f"PASS: {len(translated)} translation pairs; {len(english_paths)} English pages; "
          f"{checked_links} local links; {len(manifest['original_files'])} original paths preserved.")
    if args.preserve_originals:
        print("PASS: all original content matches the recorded baseline after removing selectors.")
    if deferred_anchors:
        print(f"PARTIAL CHECK: anchors in {len(deferred_anchors)} remote-only pages not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
