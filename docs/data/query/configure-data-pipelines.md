---
linkTitle: "Configure data pipelines"
title: "Configure data pipelines"
weight: 30
layout: "docs"
type: "docs"
description: "Create scheduled MQL pipelines that automatically aggregate and summarize captured data."
date: "2025-01-30"
aliases:
  - /data/configure-data-pipelines/
  - /build/data/configure-data-pipelines/
  - /data-ai/data/data-pipelines/
---

## What Problem This Solves

A single sensor capturing once per second produces over 86,000 readings per day. Querying raw readings directly works at small scale, but aggregations like hourly averages or per-location counts become slow as data grows.

Data pipelines run scheduled MQL aggregation queries against your raw data and store the results as precomputed summaries. Query the summary documents instead of scanning the full dataset.

## Concepts

### Raw data versus precomputed summaries

When you capture data with Viam, every reading is stored as a separate document
in the `readings` collection. This is your raw data -- complete, granular, and
append-only. Querying it directly works for small volumes, but at scale you
want precomputed summaries: documents that already contain the averages, counts,
minimums, and maximums you care about. Pipelines create these summaries
automatically.

### How pipelines work

A data pipeline has four parts:

1. **An MQL aggregation query** -- a sequence of stages (`$match`, `$group`,
   `$project`, etc.) that transforms raw documents into summary documents.
2. **A cron schedule** -- determines how often the pipeline runs. The schedule
   also determines the query time range: an hourly schedule scopes each run to
   the previous hour of data.
3. **A data source type** -- either `standard` (queries the raw readings
   collection) or `hotstorage` (queries the hot data store).
4. **A pipeline sink** -- the destination where results are stored. You query
   pipeline results using the `pipeline_sink` data source type and the
   pipeline's ID.

When a pipeline runs, Viam executes the MQL query against documents that fall
within the time window for that run, writes the results to the pipeline sink,
and records the execution status.

**Backfill:** When you enable backfill on a pipeline, Viam re-runs the pipeline
for past time windows when late-arriving data would change the results. This is
useful when machines sync data with a delay. When backfill is disabled, each
time window is processed exactly once.

### The hot data store

The hot data store is a rolling window of recent raw data stored in a database
optimized for fast queries. Unlike the standard data store (which holds all
historical data), the hot data store only retains data within its configured
time window -- for example, the last 24 hours.

Use the hot data store when you need:

- Fast queries against recent data (dashboards, live monitoring)
- A data source for pipelines that only need to process recent readings
- Lower query latency than scanning the full historical dataset

The hot data store is configured per capture method on each component. You
choose which components send data to it and how many hours of data to retain.

## Create a pipeline with the CLI

The fastest way to create a pipeline is with the Viam CLI. This example creates
a pipeline that computes hourly temperature averages grouped by location.

```bash
viam datapipelines create \
  --org-id=<org-id> \
  --name=sensor-counts \
  --schedule="0 * * * *" \
  --data-source-type="standard" \
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$location_id", "avg_temp": {"$avg": "$data.readings.temperature"}, "count": {"$sum": 1}}}, {"$project": {"location": "$_id", "avg_temp": 1, "count": 1, "_id": 0}}]' \
  --enable-backfill=True
```

Replace `<org-id>` with your organization ID. Find it in the Viam app under
**Settings** in the left navigation.

The key arguments:

- `--name` -- a descriptive name for the pipeline.
- `--schedule` -- a cron expression that controls how often the pipeline runs.
  See the [schedule format table](#schedule-format) below.
- `--data-source-type` -- `standard` to query the raw readings collection, or
  `hotstorage` to query the hot data store.
- `--mql` -- the MQL aggregation pipeline as a JSON string.
- `--enable-backfill` -- when `True`, re-runs past windows if late data arrives.

For complex queries, use `--mql-path` to read the MQL from a file instead of
passing it inline:

```bash
viam datapipelines create \
  --org-id=<org-id> \
  --name=sensor-counts \
  --schedule="0 * * * *" \
  --data-source-type="standard" \
  --mql-path=./my-pipeline.json \
  --enable-backfill=True
```

Where `my-pipeline.json` contains the MQL array:

```json
[
  { "$match": { "component_name": "sensor" } },
  {
    "$group": {
      "_id": "$location_id",
      "avg_temp": { "$avg": "$data.readings.temperature" },
      "count": { "$sum": 1 }
    }
  },
  {
    "$project": {
      "location": "$_id",
      "avg_temp": 1,
      "count": 1,
      "_id": 0
    }
  }
]
```

The CLI prints the pipeline ID on success. Save this ID -- you need it to query
pipeline results and manage the pipeline.

## Create a pipeline programmatically

You can also create pipelines from your own code using the Python SDK or Go SDK.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType


API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def connect() -> ViamClient:
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID,
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    pipeline_id = await data_client.create_data_pipeline(
        name="hourly-temperature-avg",
        organization_id=ORG_ID,
        mql_binary=[
            {"$match": {"component_name": "temperature-sensor"}},
            {"$group": {
                "_id": "$location_id",
                "avg_temp": {"$avg": "$data.readings.temperature"},
                "count": {"$sum": 1},
            }},
            {"$project": {
                "location": "$_id",
                "avg_temp": 1,
                "count": 1,
                "_id": 0,
            }},
        ],
        schedule="0 * * * *",
        data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_STANDARD,
        enable_backfill=False,
    )

    print(f"Created pipeline: {pipeline_id}")

    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

func main() {
    apiKey := "YOUR-API-KEY"
    apiKeyID := "YOUR-API-KEY-ID"
    orgID := "YOUR-ORGANIZATION-ID"

    ctx := context.Background()
    logger := logging.NewDebugLogger("data-pipeline")

    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, apiKey, apiKeyID, logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    mqlStages := []map[string]interface{}{
        {"$match": map[string]interface{}{
            "component_name": "temperature-sensor",
        }},
        {"$group": map[string]interface{}{
            "_id":      "$location_id",
            "avg_temp": map[string]interface{}{"$avg": "$data.readings.temperature"},
            "count":    map[string]interface{}{"$sum": 1},
        }},
        {"$project": map[string]interface{}{
            "location": "$_id",
            "avg_temp": 1,
            "count":    1,
            "_id":      0,
        }},
    }

    pipelineID, err := dataClient.CreateDataPipeline(
        ctx, orgID, "hourly-temperature-avg", mqlStages, "0 * * * *", false,
        &app.CreateDataPipelineOptions{TabularDataSourceType: app.TabularDataSourceTypeStandard},
    )
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Created pipeline: %s\n", pipelineID)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/pipeline-create.snippet.pipeline-create.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18-29" >}}

To create a pipeline that reads data from the hot data store, set the `dataSourceType` parameter to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{< /tabs >}}

To get your credentials, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**. Toggle **Include API key** on and copy the API key and API key ID. Find your organization ID under **Settings** in the left navigation. Run the script to create the pipeline.

## Schedule format

The `schedule` field uses standard cron syntax with five fields:
`minute hour day-of-month month day-of-week`. The schedule determines both when
the pipeline runs and the time range it queries.

| Schedule       | Frequency        | Query Time Range    |
| -------------- | ---------------- | ------------------- |
| `0 * * * *`    | Hourly           | Previous hour       |
| `0 0 * * *`    | Daily            | Previous day        |
| `*/15 * * * *` | Every 15 minutes | Previous 15 minutes |

For example, a pipeline with schedule `0 * * * *` runs at the top of every hour.
When it runs at 03:00 PM, it queries data from 02:00 PM to 03:00 PM. Each run
processes exactly one window of data with no gaps and no overlaps.

Choose a schedule that matches how frequently you need updated summaries.
Shorter intervals produce more granular summaries but create more pipeline sink
documents. Longer intervals produce fewer documents but with longer delays
before summaries are available.

## Query pipeline results

Pipeline results are stored in a separate data source called the pipeline sink.
To query them, specify the pipeline sink data source type and the pipeline ID.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType

PIPELINE_ID = "YOUR-PIPELINE-ID"

tabular_data = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {"$match": {"location": {"$exists": True}}},
        {"$limit": 10},
    ],
    tabular_data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
    pipeline_id=PIPELINE_ID,
)

for entry in tabular_data:
    print(entry)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
queryStages := []map[string]interface{}{
    {"$match": map[string]interface{}{
        "location": map[string]interface{}{"$exists": true},
    }},
    {"$limit": 10},
}

tabularData, err := dataClient.TabularDataByMQL(ctx, orgID, queryStages,
    &app.TabularDataByMQLOptions{
        TabularDataSourceType: app.TabularDataSourceTypePipelineSink,
        PipelineID:            pipelineID,
    },
)
if err != nil {
    logger.Fatal(err)
}

for _, entry := range tabularData {
    fmt.Printf("%v\n", entry)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/pipeline-query.snippet.pipeline-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="19-30" >}}

{{% /tab %}}
{{< /tabs >}}

The query runs against the pipeline's output documents, not the raw readings.
The fields available depend on what your pipeline's `$project` stage produces.

## Use the hot data store as a pipeline data source

Pipelines can query the [hot data store](/data/query/hot-data-store/) instead of blob
storage. The hot data store keeps a rolling window of recent raw data optimized
for fast reads. This is useful when your pipeline only needs to process recent
readings.

To use it, set `--data-source-type hotstorage` in the CLI or set the data
source type to `TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` in the SDK. See
[Hot Data Store](/data/query/hot-data-store/) for setup and configuration.

## Manage pipelines

Use the CLI, Python, or Go to list, enable, disable, and delete pipelines.

### List pipelines

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines list --org-id=<org-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
pipelines = await data_client.list_data_pipelines(organization_id=ORG_ID)
for p in pipelines:
    print(f"{p.id}: {p.name} (enabled={p.enabled})")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
pipelines, err := dataClient.ListDataPipelines(ctx, orgID)
if err != nil {
    logger.Fatal(err)
}
for _, p := range pipelines {
    fmt.Printf("%s: %s (enabled=%v)\n", p.ID, p.Name, p.Enabled)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/pipeline-list.snippet.pipeline-list.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}

### Enable a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines enable --org-id=<org-id> --pipeline-id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.enable_data_pipeline(pipeline_id=PIPELINE_ID)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.EnableDataPipeline(ctx, pipelineID)
```

{{% /tab %}}
{{< /tabs >}}

### Disable a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines disable --org-id=<org-id> --pipeline-id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.disable_data_pipeline(pipeline_id=PIPELINE_ID)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.DisableDataPipeline(ctx, pipelineID)
```

{{% /tab %}}
{{< /tabs >}}

Disabling a pipeline stops future scheduled runs. It does not delete existing
results in the pipeline sink. When you re-enable a pipeline, it resumes from the
next scheduled window -- it does not backfill the windows it missed while
disabled.

### Delete a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines delete --org-id=<org-id> --pipeline-id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.delete_data_pipeline(pipeline_id=PIPELINE_ID)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.DeleteDataPipeline(ctx, pipelineID)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/pipeline-delete.snippet.pipeline-delete.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}

Deleting a pipeline removes the pipeline configuration, its execution history,
and all output results stored in the pipeline sink.

## Monitor pipeline execution

Each pipeline run produces an execution record with a status. Use this to verify
your pipelines are running correctly and to diagnose failures.

The possible statuses are:

| Status      | Meaning                                                    |
| ----------- | ---------------------------------------------------------- |
| `SCHEDULED` | The run is queued and waiting to execute.                  |
| `STARTED`   | The run is currently executing the MQL aggregation.        |
| `COMPLETED` | The run finished successfully and results are in the sink. |
| `FAILED`    | The run encountered an error. Check the error message.     |

{{< tabs >}}
{{% tab name="Python" %}}

```python
runs = await data_client.list_data_pipeline_runs(pipeline_id=PIPELINE_ID)
for run in runs:
    print(f"{run.id}: {run.status} ({run.start_time} - {run.end_time})")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
runs, err := dataClient.ListDataPipelineRuns(ctx, pipelineID)
if err != nil {
    logger.Fatal(err)
}
for _, run := range runs {
    fmt.Printf("%s: %s (%s - %s)\n", run.ID, run.Status, run.StartTime, run.EndTime)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/pipeline-execution.snippet.pipeline-execution.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}

Failed runs include an error message that describes what went wrong -- typically
an invalid MQL stage, a permission issue, or a timeout.

If a pipeline consistently fails, check the MQL query by running it manually
in the Viam app query editor (using MQL mode) against the same data source. This
helps isolate whether the issue is in the query itself or in the pipeline
configuration.

## Try It

1. **Create your first pipeline.** Using the CLI command from [Create a pipeline with the CLI](#create-a-pipeline-with-the-cli), create a
   pipeline that counts readings per component per hour. Use this MQL:

   ```json
   [
     {
       "$group": {
         "_id": "$component_name",
         "count": { "$sum": 1 }
       }
     },
     {
       "$project": {
         "component": "$_id",
         "count": 1,
         "_id": 0
       }
     }
   ]
   ```

   Set the schedule to `0 * * * *` (hourly). Wait for the next hour boundary
   and verify results appear in the pipeline sink.

2. **Query the results.** Using the Python or Go code from [Query pipeline results](#query-pipeline-results), query your
   pipeline sink. You should see one document per component with a `count` field
   showing how many readings were captured in that hour.

3. **Enable the hot data store.** Follow the [Hot Data Store](/data/query/hot-data-store/)
   guide to enable hot storage on a sensor component with a 24-hour window.
   Query it using the hot storage data source type and verify you get recent
   readings back quickly.

4. **Disable and re-enable.** Disable your pipeline, wait an hour, then
   re-enable it. Verify that the missed window is not backfilled (no results for
   the hour the pipeline was disabled).

## Troubleshooting

{{< expand "Pipeline creation fails with permission error" >}}

Only organization owners can create data pipelines. Verify your API key has
owner-level permissions. In the Viam app, go to **Settings** > **API Keys** and
check the role associated with your key.

{{< /expand >}}

{{< expand "Pipeline runs but produces no results" >}}

- **Check the `$match` stage.** The field names and values must match your actual
  data. Run the same MQL query in the Viam app query editor to verify it returns
  results against the raw data.
- **Check the time window.** If no data was captured during the pipeline's time
  window, the run produces no output. Verify that data is being captured and
  synced during the hours your pipeline is scheduled.
- **Check the data source type.** If you set `hotstorage` but the hot data store
  is not configured for your components, the pipeline has no data to query.

{{< /expand >}}

{{< expand "Duplicate key error in pipeline results" >}}

The `$group` stage produces documents with an `_id` field. If your pipeline runs
multiple times and produces documents with the same `_id`, you get a duplicate
key error. Always follow `$group` with `$project` to rename `_id` to a
descriptive field name and set `_id` to 0:

```json
{ "$project": { "location": "$_id", "avg_temp": 1, "count": 1, "_id": 0 } }
```

This ensures each output document gets a unique auto-generated `_id` instead of
reusing the group key.

{{< /expand >}}

{{< expand "Hot data store query returns no data" >}}

See [Hot Data Store](/data/query/hot-data-store/) for configuration and query details.
Common causes: the time window has expired (data older than `stored_hours` is
removed), hot storage is not enabled on the component, or data has not yet been
captured and synced.

{{< /expand >}}

{{< expand "Pipeline results are stale or delayed" >}}

Pipelines run on a cron schedule. Results are only available after the scheduled
run completes. If your pipeline runs hourly, results for the 02:00-03:00 PM window
are not available until shortly after 03:00 PM. For faster updates, use a more
frequent schedule (for example, `*/15 * * * *` for every 15 minutes).

{{< /expand >}}

{{< expand "Re-enabled pipeline has gaps in results" >}}

This is expected behavior. When you disable a pipeline, scheduled runs do not
execute. When you re-enable it, it resumes from the next scheduled window.
Missed windows are not retroactively processed, even if backfill is enabled.
Backfill only applies to late-arriving data within windows the pipeline was
active for.

{{< /expand >}}

## What's Next

- [Hot Data Store](/data/query/hot-data-store/) -- configure fast recent-data queries
  and use the hot data store as a pipeline data source.
- [Query Data](/data/query/query-data/) -- learn more MQL patterns to use in
  your pipeline aggregation queries.
- [Filter at the Edge](/data/filter-at-the-edge/) -- reduce the volume of
  raw data before it reaches the cloud, making your pipelines faster and cheaper.
- [Visualize Data](/data/visualize-data/) -- build dashboards on top of
  your precomputed pipeline summaries.
