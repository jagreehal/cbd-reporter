#!/usr/bin/env python3
"""Validates this repo's own docs/ against the company convention.

Reads cbd-handbook's contracts/docs-frontmatter.json at a pinned tag, the same
committed artifact a TypeScript repo loads with z.fromJSONSchema. Nothing here
imports Zod, npm, or the handbook's source.

Enforces the same three rules as cbd-handbook's src/check-docs.ts — schema, no relative
links into another repo, no dangling or orphaned `related` edges — without
sharing a line of code with it. That is the point: the contract is the JSON
Schema, not a shared library.

Usage: python3 check_docs.py
"""
import json
import re
import sys
from pathlib import Path

from urllib.error import HTTPError
from urllib.request import urlopen

import yaml
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent
# The convention version this repo follows. Bumped by PR, like any contract.
HANDBOOK = "v1.0.0"
SCHEMA = f"https://raw.githubusercontent.com/jagreehal/cbd-handbook/{HANDBOOK}/contracts/docs-frontmatter.json"
# Published by cbd-docs-site on its last run.
MANIFEST = "https://jagreehal.github.io/cbd-docs-site/contracts/docs-manifest.json"

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
FENCED = re.compile(r"^```.*?^```", re.M | re.S)
ESCAPING_LINK = re.compile(r"]\((\.\./\.\./[^)]+)\)")


def doc_id_of(path: Path) -> str:
    """docs/daily-settlement-report.md -> cbd-reporter/daily-settlement-report"""
    return f"{REPO.name}/{path.relative_to(REPO / 'docs').with_suffix('')}"


def fetch(url: str):
    try:
        with urlopen(url) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None  # no manifest published yet
        raise


def main() -> int:
    validator = Draft202012Validator(fetch(SCHEMA))
    manifest = fetch(MANIFEST)
    failures = []
    docs = sorted((REPO / "docs").glob("**/*.md"))
    # Built before the loop: a doc may link to one that sorts after it.
    present = {doc_id_of(path) for path in docs}

    for path in docs:
        doc_id = doc_id_of(path)
        text = path.read_text()
        match = FRONTMATTER.match(text)
        if not match:
            failures.append(f"{doc_id}: no frontmatter")
            continue

        # Frontmatter is YAML, so it is parsed by a YAML parser.
        fields = yaml.safe_load(match.group(1)) or {}
        errors = sorted(validator.iter_errors(fields), key=lambda e: e.json_path)
        for error in errors:
            failures.append(f"{doc_id}: {error.json_path}: {error.message}")
        if errors:
            continue

        # A relative path that escapes the repo only resolves for someone with
        # every repo checked out as siblings. Fenced blocks are excluded: docs
        # teach this rule by showing the wrong form.
        for link in ESCAPING_LINK.findall(FENCED.sub("", text)):
            failures.append(f"{doc_id}: links into another repo by path ({link}) — use related: instead")

        for target in fields.get("related", []):
            # Own docs resolve against the filesystem. Cross-repo targets exist
            # only in the manifest, so before the first one is published there
            # is nothing to check them against. A stale manifest rejects a link
            # that would have worked and never accepts one that is broken, so
            # publish the target first, then link to it.
            if target.startswith(f"{REPO.name}/"):
                dangling = target not in present
            else:
                dangling = manifest is not None and target not in manifest
            if dangling:
                failures.append(f"{doc_id}: related '{target}' does not resolve")

    # Renaming or deleting a doc breaks whoever links to it, and only the
    # manifest records who that is.
    for doc_id, entry in (manifest or {}).items():
        if doc_id.startswith(f"{REPO.name}/") and doc_id not in present and entry["linkedFrom"]:
            linked = ", ".join(entry["linkedFrom"])
            failures.append(f"{doc_id} no longer exists but is linked from {linked}")

    for failure in failures:
        print(f"✗ {failure}")
    if failures:
        return 1
    scope = "schema + links" if manifest else "schema only, no manifest yet"
    print(f"docs check passed: {len(docs)} doc(s) in {REPO.name} ({scope})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
