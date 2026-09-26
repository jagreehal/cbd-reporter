---
title: Data platform team
owner: data-platform
tags: [team]
related: [cbd-reporter/daily-settlement-report, cbd-payments-service/team]
---

# Data platform team

We own the reporter and the numbers finance receives.

| Name | Role |
|---|---|
| Priya Raman | Engineering lead |
| Jonas Weber | Data engineer |
| Amina Sow | Analytics engineer |

Slack: `#data-platform`. Office hours only. A late report is not an incident,
and a wrong report is worse than a late one, so we would rather hold it.

## We are a Python shop

No TypeScript, no Node, no npm. We consume
`cbd-payments-service/contracts/events/*.json` with `jsonschema` and that is the
entire integration. See
[validating payment events in Python](validating-events-in-python.md).

This matters when someone proposes distributing a schema as an npm package. We
cannot use one, and the committed JSON Schema artifact is what keeps us a
first-class consumer rather than a special case.

## If your team emits events we should read

Tell us before you ship, not after. We need the event in the catalog with a
schema we can validate against, and we will want to know your retention, because
a report cannot be rebuilt from events that have aged out.

## Finance escalations

Finance comes to us first when a total looks wrong, and we go to the payments
platform team only once we have ruled out the day boundary and the invalid count. Most disputes resolve at our end.
