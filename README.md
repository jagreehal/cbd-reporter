# cbd-reporter

Python consumer. Validates payment events against cbd-payments-service's
`contracts/events/*.json` at the tag pinned in [`reporter.py`](reporter.py), and
checks its own `docs/` against cbd-handbook's frontmatter schema with
`jsonschema`. No Node, no npm, no TypeScript.

```sh
pip install -r requirements.txt
python reporter.py --check     # self-check against the pinned schemas
python reporter.py events.ndjson
python check_docs.py           # this repo's docs follow the convention
```

## The six repositories

| Repo | Role |
|---|---|
| [cbd-handbook](https://github.com/jagreehal/cbd-handbook) | Owns the convention: docs frontmatter schema, docs checker, company policy |
| [cbd-payments-service](https://github.com/jagreehal/cbd-payments-service) | TypeScript producer: OpenAPI + event JSON Schemas + runbook |
| [cbd-dashboard](https://github.com/jagreehal/cbd-dashboard) | TypeScript consumer: typed client generated from the pinned OpenAPI |
| [cbd-reporter](https://github.com/jagreehal/cbd-reporter) | Python consumer: validates events against the pinned JSON Schemas |
| [cbd-docs-site](https://github.com/jagreehal/cbd-docs-site) | Aggregator: [one docs index](https://jagreehal.github.io/cbd-docs-site/) over every enrolled repo |
| [cbd-catalog](https://github.com/jagreehal/cbd-catalog) | Aggregator: [EventCatalog](https://jagreehal.github.io/cbd-catalog/) over every enrolled repo |

No repository imports another's source. Consumers read committed artifacts
at pinned tags over HTTPS; aggregators discover publishers by the
`cbd-publisher` GitHub topic.
