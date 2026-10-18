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

[`autocatalog.consumes.json`](autocatalog.consumes.json) says which payments
events the reporter reads, and which fields. The company catalog publishes it,
so a payments pull request names the reporter before it breaks a field the
reporter reads. The file is plain JSON; nothing here needs Node to keep it.

## The six repositories

| Repo | Role |
|---|---|
| [cbd-handbook](https://github.com/jagreehal/cbd-handbook) | Owns the convention: docs frontmatter schema, docs check, company policy |
| [cbd-payments-service](https://github.com/jagreehal/cbd-payments-service) | TypeScript producer: OpenAPI, event JSON Schemas, runbook |
| [cbd-dashboard](https://github.com/jagreehal/cbd-dashboard) | TypeScript consumer: generates a typed client from the pinned OpenAPI |
| [cbd-reporter](https://github.com/jagreehal/cbd-reporter) | Python consumer: validates events against the pinned JSON Schemas |
| [cbd-docs-site](https://github.com/jagreehal/cbd-docs-site) | Retired: redirects to cbd-catalog |
| [cbd-catalog](https://github.com/jagreehal/cbd-catalog) | Aggregator: [the one site](https://jagreehal.github.io/cbd-catalog/) over the enrolled repos: docs index, `llms.txt`, docs manifest, `catalog.json` |

Consumers fetch committed artifacts over HTTPS at a pinned tag. The
aggregator finds publishers by the `cbd-publisher` GitHub topic.

The pattern and the argument behind it: [convention-based-design](https://github.com/jagreehal/convention-based-design).
