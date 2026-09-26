# cbd-reporter

Python consumer. The reporter validates payment events against the
cbd-payments-service `contracts/events/*.json` at the tag in
[`reporter.py`](reporter.py). It checks its own `docs/` against the
cbd-handbook frontmatter schema with `jsonschema`. It runs without Node.

```sh
pip install -r requirements.txt
python reporter.py --check     # self-check against the pinned schemas
python reporter.py events.ndjson
python check_docs.py           # our docs follow the convention
```

## The six repositories

| Repo | Role |
|---|---|
| [cbd-handbook](https://github.com/jagreehal/cbd-handbook) | Owns the convention: docs frontmatter schema, docs check, company policy |
| [cbd-payments-service](https://github.com/jagreehal/cbd-payments-service) | TypeScript producer: OpenAPI, event JSON Schemas, runbook |
| [cbd-dashboard](https://github.com/jagreehal/cbd-dashboard) | TypeScript consumer: generates a typed client from the pinned OpenAPI |
| [cbd-reporter](https://github.com/jagreehal/cbd-reporter) | Python consumer: validates events against the pinned JSON Schemas |
| [cbd-docs-site](https://github.com/jagreehal/cbd-docs-site) | Aggregator: [docs index](https://jagreehal.github.io/cbd-docs-site/) over the enrolled repos |
| [cbd-catalog](https://github.com/jagreehal/cbd-catalog) | Aggregator: [EventCatalog](https://jagreehal.github.io/cbd-catalog/) over the enrolled repos |

Consumers fetch committed artifacts over HTTPS at a pinned tag. The
aggregators find publishers by the `cbd-publisher` GitHub topic.
