---
linkTitle: "Pipeline reference"
title: "Data pipelines reference"
weight: 30
layout: "docs"
type: "docs"
description: "Configuration fields, run statuses, cron schedule syntax, data source types, and execution limits."
date: "2026-03-27"
---

Configuration fields, execution behavior, and limits for data pipelines. For an overview of how pipelines work, see [Data pipelines overview](/data/pipelines/overview/).

## Pipeline configuration fields

These are the underlying fields on the pipeline resource. The CLI flags and SDK parameters you use to create a pipeline each set one of these fields.

| Field              | Type   | Required | CLI flag                | Description                                                                                                                     |
| ------------------ | ------ | -------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `name`             | string | Yes      | `--name`                | Pipeline name. Must be unique within the organization.                                                                          |
| `organization_id`  | string | Yes      | `--org-id`              | Organization UUID.                                                                                                              |
| `schedule`         | string | Yes      | `--schedule`            | Cron expression in UTC. Determines both when the pipeline runs and the query time window. See [Cron schedule](#cron-schedule).  |
| `mql_binary`       | array  | Yes      | `--mql` or `--mql-path` | MQL aggregation pipeline as an array of stage objects. See [Supported MQL operators](/data/reference/#supported-mql-operators). |
| `enable_backfill`  | bool   | Yes      | `--enable-backfill`     | Whether to process historical time windows. See [Backfill behavior](#backfill-behavior).                                        |
| `data_source_type` | enum   | Yes      | `--data-source-type`    | Data source to query. Accepts `standard` or `hotstorage`. See [Data source types](#data-source-types).                          |

## Cron schedule

The `schedule` field uses standard five-field cron syntax: `minute hour day-of-month month day-of-week`. All times are UTC.

The schedule determines both when the pipeline runs and the time range it queries. Each run processes the time window between the previous two schedule ticks.

| Schedule       | Frequency        | Query time range per run |
| -------------- | ---------------- | ------------------------ |
| `0 * * * *`    | Hourly           | Previous hour            |
| `0 0 * * *`    | Daily            | Previous day             |
| `*/15 * * * *` | Every 15 minutes | Previous 15 minutes      |
| `*/5 * * * *`  | Every 5 minutes  | Previous 5 minutes       |

For example, a pipeline with schedule `0 * * * *` that triggers at 03:00 PM UTC processes data from 02:00 PM to 03:00 PM UTC. The time window is `[start, end)` (start inclusive, end exclusive).

Choose a schedule that matches how frequently you need updated summaries. Shorter intervals produce more granular summaries but create more pipeline sink documents.

## Data source types

Pipelines support three data source types. You use them in two contexts: when creating a pipeline (the pipeline reads from this source) and when querying pipeline results (the query targets this source). Not every type is valid in both contexts.

| Type          | Value string    | Description                                                                                                                                                                                      |
| ------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Standard      | `standard`      | The raw `readings` collection containing all historical tabular data.                                                                                                                            |
| Hot storage   | `hotstorage`    | The [hot data store](/data/hot-data-store/). A rolling window of recent data, with lower latency.                                                                                                |
| Pipeline sink | `pipeline_sink` | The output of another pipeline. **Query-time only**: you cannot pass `pipeline_sink` to `--data-source-type` when creating a pipeline; use it in query calls alongside the source pipeline's ID. |

The SDK constants for each type:

| Type          | Python SDK                                                     | Go SDK                                  |
| ------------- | -------------------------------------------------------------- | --------------------------------------- |
| Standard      | `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_STANDARD`      | `app.TabularDataSourceTypeStandard`     |
| Hot storage   | `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`   | `app.TabularDataSourceTypeHotStorage`   |
| Pipeline sink | `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK` | `app.TabularDataSourceTypePipelineSink` |

To query the output of another pipeline, use `pipeline_sink` in your query call alongside the source pipeline's ID. See [Query pipeline results](/data/pipelines/query-results/).

## Run statuses

| Status        | Value | CLI label   | Description                                                           |
| ------------- | ----- | ----------- | --------------------------------------------------------------------- |
| `UNSPECIFIED` | 0     | `Unknown`   | Unknown or not set.                                                   |
| `SCHEDULED`   | 1     | `Scheduled` | Run is queued. Execution begins after a 2-minute delay.               |
| `STARTED`     | 2     | `Running`   | MQL query is executing against the data source.                       |
| `COMPLETED`   | 3     | `Success`   | Run finished successfully. Results are in the pipeline sink.          |
| `FAILED`      | 4     | `Failed`    | Run encountered an error. Check the `error_message` field on the run. |

SDK methods return the enum `Status` values. The `viam datapipelines describe` CLI command prints the friendly "CLI label" form.

If a run stays in `STARTED` for more than 10 minutes, it is automatically marked as `FAILED` and a new run is created for that time window.

## Run fields

Each pipeline run record contains:

| Field             | Type      | Description                                                   |
| ----------------- | --------- | ------------------------------------------------------------- |
| `id`              | string    | Run identifier.                                               |
| `status`          | enum      | Current status. See [Run statuses](#run-statuses).            |
| `start_time`      | timestamp | When the run started executing.                               |
| `end_time`        | timestamp | When the run completed or failed.                             |
| `data_start_time` | timestamp | Start of the data time window this run processed (inclusive). |
| `data_end_time`   | timestamp | End of the data time window this run processed (exclusive).   |
| `error_message`   | string    | Error details if the run failed. Empty on success.            |

## Backfill behavior

When `enable_backfill` is `true`:

- On pipeline creation, Viam processes historical time windows backward from the creation time to the earliest available data.
- When data syncs with a delay (machine was offline), the pipeline automatically reruns affected time windows to include the late-arriving data.
- Backfill processes in batches of up to 10 concurrent time windows with a 2-minute delay between batches.
- For `standard` data source, backfill may provision an Atlas Data Federation instance for faster historical queries.
- Backfill results replace any existing results for the same time window.

When `enable_backfill` is `false`:

- Each time window is processed exactly once.
- Late-arriving data is not incorporated into past summaries.

Backfill does not apply to windows missed while a pipeline was disabled. If you disable a pipeline for 3 hours and re-enable it, those 3 hours are not backfilled.

## Pipeline sink

Each pipeline stores its output in a dedicated sink collection named `sink-<pipeline-id>`. Each result document includes metadata:

```json
{
  "_viam_pipeline_run": {
    "id": "run-id",
    "interval": {
      "start": "2025-03-15T14:00:00.000Z",
      "end": "2025-03-15T15:00:00.000Z"
    },
    "organization_id": "org-id"
  },
  "location": "warehouse-a",
  "avg_temp": 23.5,
  "count": 3600
}
```

The `_viam_pipeline_run` field is added automatically. Your pipeline's `$project` output fields appear alongside it.

To query the sink, use data source type `pipeline_sink` with the pipeline's ID. See [Query pipeline results](/data/pipelines/query-results/).

{{< alert title="Deleting a pipeline is irreversible" color="caution" >}}
Deleting a pipeline removes its sink collection and every result stored in it. Export the results first if you need to preserve them. See [Delete a pipeline](/data/pipelines/manage-pipelines/#delete-a-pipeline).
{{< /alert >}}

## Execution limits

| Limit                            | Value                                                          |
| -------------------------------- | -------------------------------------------------------------- |
| Maximum output documents per run | 10,000                                                         |
| MQL execution timeout            | 5 minutes                                                      |
| Execution start delay            | 2 minutes after scheduled time                                 |
| Hung run detection               | 2x execution timeout (currently 10 minutes) in `STARTED` state |
| Backfill batch size              | 10 concurrent time windows                                     |
| Backfill throttle                | 2-minute delay between batches                                 |

## Permissions

Only organization owners can create, modify, and delete data pipelines. Query access to pipeline results follows the same permissions as other data queries. See [Permissions](/data/reference/#permissions).
