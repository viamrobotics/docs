---
linkTitle: "Overview"
title: "Data pipelines"
weight: 1
layout: "docs"
type: "docs"
description: "How data pipelines work: scheduled MQL aggregations that transform raw captured data into precomputed summaries."
date: "2026-03-27"
---

A data pipeline runs a scheduled MQL aggregation query against your captured data and stores the results as precomputed summary documents. Instead of querying 86,000 raw sensor readings to compute an hourly average, you query a single summary document that the pipeline already computed.

## When to use pipelines

Pipelines are useful when:

- **Your aggregation queries take too long.** If computing averages, counts, or rollups over raw data takes more than a few seconds, a pipeline pre-computes the result so you query a summary instead of scanning raw readings.
- **You need the same computation on a schedule.** Hourly averages, daily counts, per-location rollups. A pipeline runs the query automatically and stores the result. No scripts, no cron jobs on your machine.
- **You're feeding results into other tools.** Dashboards, alerts, or downstream pipelines can query the pipeline sink directly. The output is a small, stable collection that doesn't grow with your raw data volume.

Pipelines are not necessary when:

- Your queries already return in under a second. Pipelines add complexity; use them when you need the performance gain.
- You need ad-hoc, one-time queries. Use the [query editor](/data/query-data/) instead.
- You need real-time results with sub-minute latency. Pipelines run on a cron schedule with at least a 2-minute execution delay.

{{< alert title="Pipelines don't reduce data transfer" color="note" >}}
Pipelines run in the cloud against data that has already been synced. They reduce query time, not bandwidth or storage volume. To reduce what gets sent from the machine, see [Filter at the edge](/data/filter-at-the-edge/).
{{< /alert >}}

## How pipelines work

A pipeline has four parts:

1. **An MQL aggregation query.** A sequence of MongoDB aggregation stages (`$match`, `$group`, `$project`, and others) that transforms raw documents into summary documents. You write the query; the pipeline runs it automatically.

2. **A cron schedule.** Determines how often the pipeline runs. The schedule also determines the query time window: an hourly schedule (`0 * * * *`) scopes each run to the previous hour of data. A 15-minute schedule (`*/15 * * * *`) scopes each run to the previous 15 minutes. Schedules are in UTC.

3. **A data source.** Either `standard` (the raw readings collection containing all historical data) or `hotstorage` (the [hot data store](/data/hot-data-store/) containing a rolling window of recent data).

4. **A pipeline sink.** The destination collection where results are stored. Each pipeline has its own sink. You query pipeline results by specifying the `pipeline_sink` data source type and the pipeline's ID.

### Execution flow

When a pipeline's cron schedule triggers:

1. The pipeline determines the time window from the schedule (for example, 02:00 to 03:00 PM for an hourly pipeline running at 03:00 PM).
2. It prepends a time constraint to your MQL query that limits it to documents within that window.
3. It executes the query against the configured data source with a 5-minute timeout.
4. If the query produces 10,000 or fewer documents, results are written to the pipeline sink.
5. The run is marked as completed or failed.

Each run processes exactly one time window with no gaps and no overlaps between consecutive runs.

### Backfill

When you enable backfill on a pipeline, Viam processes historical time windows that the pipeline missed. This is useful in two scenarios:

- **Late-arriving data.** If a machine syncs data with a delay (for example, it was offline and synced a backlog), the pipeline automatically reruns the affected time windows to include the late data.
- **New pipeline on existing data.** When you create a pipeline with backfill enabled, it processes historical data backward from the creation time to the earliest available data.

When backfill is disabled, each time window is processed exactly once. Late-arriving data is not incorporated into past summaries.

### Limits

- **Output size:** Each pipeline run can produce a maximum of 10,000 documents. Runs that exceed this limit fail.
- **Execution timeout:** MQL queries time out after 5 minutes. Complex aggregations on large datasets may need to be simplified or scoped with tighter `$match` filters.
- **Minimum schedule interval:** The cron schedule must have at least 1-minute granularity.

## Data source types

| Source type | What it queries | When to use |
| --- | --- | --- |
| `standard` | The raw `readings` collection containing all historical tabular data | Default. Use for aggregations over any time range. |
| `hotstorage` | The [hot data store](/data/hot-data-store/) containing a rolling window of recent data | Use when your pipeline only needs recent data and you want lower query latency. |
| `pipeline_sink` | The output of another pipeline | Use when chaining pipelines: one pipeline produces summaries, another aggregates those summaries further. Requires the source pipeline's ID. |

## What's next

- [Create a pipeline](/data/pipelines/create-a-pipeline/): step-by-step guide to creating your first pipeline
- [Manage pipelines](/data/pipelines/manage-pipelines/): list, enable, disable, monitor, and delete pipelines
- [Reference](/data/pipelines/reference/): configuration fields, run statuses, cron schedule syntax
