---
title: Validating payment events in Python
owner: data-platform
tags: [python, events, json-schema]
related: [cbd-payments-service/contract-reach, cbd-handbook/repository-layout]
---

# Validating payment events in Python

The reporter joined this system by reading one file. It has no TypeScript
toolchain, no access to the producer's source, and no shared package with the
payments team.

```sh
pip install -r requirements.txt
python3 reporter.py --check
```

## What it reads

`contracts/events/payment.completed.json` from `cbd-payments-service`, at the
tag pinned in `reporter.py`. The payments build generates this JSON Schema
from the Zod schema the producer validates against at runtime. The
same file the EventCatalog build reads, and the same file any Go or JVM
consumer would read.

Every record is validated before it is counted. An invalid record is reported,
not silently dropped, because a consumer that quietly skips malformed events
turns a producer bug into a slow reporting discrepancy nobody traces back.

## The transport is not the contract

The demo reads `events.ndjson` from disk. A deployment reads a Kafka topic, a
NATS subject, or an SQS queue.

The adapter unwraps whatever envelope the broker adds and hands the payload to
the same validation. Swapping brokers changes delivery configuration, not this
file and not the schema.

## Checking our own documentation

`check_docs.py` validates the frontmatter of every document in this
repository against `contracts/docs-frontmatter.json` from `cbd-handbook`, using the
`jsonschema` package already installed for events.

That check matters more than its twenty lines suggest. If it did not exist,
participating in the documentation convention would require Node, and a
convention that only one language can honour is a shared package wearing a
different hat.

## Honest scope

This reporter is about fifty lines and exists to prove a consumer can join
without the producer's toolchain. It counts events and validates them. Anything
you would want in production, including offsets, retries, dead-letter handling,
and idempotency, is out of scope here and belongs to the transport adapter.
