#!/usr/bin/env python3
"""Reads payments events and validates them against cbd-payments-service's
committed JSON Schema contracts, fetched at a pinned tag. No TypeScript, no
payments source, no shared package.

Usage: python3 reporter.py [events.ndjson]   (default: ./events.ndjson)
       python3 reporter.py --check           (self-check)
"""
import json
import sys
from pathlib import Path
from urllib.request import urlopen

from jsonschema import Draft202012Validator

# Upgrading to a new contract is a one-line PR that changes this tag.
PAYMENTS_CONTRACT = "v1.0.0"
CONTRACTS = f"https://raw.githubusercontent.com/jagreehal/cbd-payments-service/{PAYMENTS_CONTRACT}/contracts/events"
# The events this consumer handles. Anything else is reported as unknown.
EVENTS = ("payment.completed", "payment.failed")


def fetch(url: str) -> dict:
    with urlopen(url) as response:
        return json.load(response)


VALIDATORS = {event: Draft202012Validator(fetch(f"{CONTRACTS}/{event}.json")) for event in EVENTS}


def report(line: str) -> str:
    event = json.loads(line)
    validator = VALIDATORS.get(event.get("type", ""))
    if validator is None:
        return f"UNKNOWN event type: {event.get('type')!r}"
    errors = sorted(validator.iter_errors(event), key=lambda e: e.json_path)
    if errors:
        return f"INVALID {event['type']}: {errors[0].json_path}: {errors[0].message}"
    payment = event.get("payment", {})
    detail = f" {payment['amount']} {payment['currency']}" if payment else ""
    return f"OK {event['type']}{detail}"


def self_check() -> None:
    good = {
        "type": "payment.completed",
        "payment": {
            "id": "p1", "amount": 10.5, "currency": "GBP",
            "status": "completed", "createdAt": "2026-07-27T12:00:00Z",
        },
        "settledAt": "2026-07-27T12:00:00Z",
    }
    bad = dict(good, payment=dict(good["payment"], amount=-1))
    assert report(json.dumps(good)).startswith("OK"), "valid event rejected"
    assert report(json.dumps(bad)).startswith("INVALID"), "off-contract event accepted"
    print("reporter self-check passed")


if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
        sys.exit(0)
    log = Path(sys.argv[1] if len(sys.argv) > 1 else "events.ndjson")
    for line in log.read_text().splitlines():
        print(report(line))
