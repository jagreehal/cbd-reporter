---
title: The daily settlement report
owner: data-platform
tags: [product, finance, reporting]
related: [cbd-payments-service/how-payments-work, cbd-reporter/team]
---

# The daily settlement report

Finance gets one figure per currency per day: the total that actually settled.
It goes out at 06:00 and covers the previous day.

## What counts

A `payment.completed` event with a `settledAt` timestamp inside the reporting
day, in UTC.

Nothing else counts. Not payments created that day, not payments showing
`completed` in the dashboard right now, and not failures. A payment created at
23:58 on Tuesday and settled at 00:03 on Wednesday belongs to Wednesday, which
is the single most common question finance asks.

## Why we read events instead of the API

The payments API answers what is true now. The report needs what happened, and
when. Those differ every time a payment settles after midnight or a status
changes between the report running and someone checking it.

Reading events also means we never ask the payments team for a database export,
and their schema changes cannot break our report without first breaking their
own contract check.

## Invalid records

Every record is validated against the committed JSON Schema before it is
counted. An invalid record is logged as `INVALID` and excluded from the total,
and the run still completes.

A single invalid record is worth a look. More than a handful means the producer
has shipped something off-contract, and the total for that day should not go to
finance until someone has read the events. Silently dropping bad records would
turn a producer bug into a reporting discrepancy nobody traces back for a
quarter.

## When the number looks wrong

Check the invalid count first, then the day boundary, then whether the event
file covers the whole period. In that order. Most disputed totals are a
timezone question wearing a costume.

Who to ask is in [the team page](team.md).
