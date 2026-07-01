---
linkTitle: "Manage pipelines"
title: "Manage data pipelines"
weight: 20
layout: "docs"
type: "docs"
description: "List, monitor, enable, disable, rename, and delete data pipelines."
date: "2026-03-27"
---

Monitor and manage your data pipelines after creation. For creating pipelines, see [Create a pipeline](/data/pipelines/create-a-pipeline/).

## View pipelines in the Viam app

Navigate to the [**DATA** page](https://app.viam.com/data) in the Viam app, then select the **Pipelines** subtab.

The pipelines list shows each pipeline's name, schedule, last execution time, and error count.
Disabled pipelines display a **Disabled** badge next to the name.
Pipelines with backfill in progress show the completion percentage.

Click a pipeline name to open its detail page, which has three tabs:

- **Runs**: A table of all pipeline executions with the data window, status, runtime, and start time for each run.
  Failed runs show an error icon you can expand for details.
- **Details**: The pipeline's configuration, including its ID, schedule, data source type, creation date, backfill status, and the full MQL query.
- **Custom indexes**: MongoDB indexes on the pipeline's output collection.
  See [Manage custom indexes](#manage-custom-indexes) for details.

Use the three-dot menu next to any pipeline to **Copy ID**, **Query pipeline data**, **Enable** or **Disable** the pipeline, or **Delete** it.

## List pipelines

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines list --org-id=<org-id>
```

Example output (one line per pipeline):

```text
hourly-temp-avg (ID: 64f3a1b2c4d5e6f7a8b9c0d1) [Enabled] [Data Source Type: Standard]
daily-summary (ID: 64f3a1b2c4d5e6f7a8b9c0d2) [Disabled] [Data Source Type: Hot Storage]
```

If the command prints nothing, the organization has no pipelines. This is not an error.

{{% /tab %}}
{{% tab name="Python" %}}

```python
pipelines = await data_client.list_data_pipelines(organization_id=ORG_ID)
for p in pipelines:
    print(f"{p.id}: {p.name} (enabled={p.enabled}, schedule={p.schedule})")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
pipelines, err := dataClient.ListDataPipelines(ctx, orgID)
if err != nil {
    logger.Fatal(err)
}
for _, p := range pipelines {
    fmt.Printf("%s: %s (enabled=%v, schedule=%s)\n", p.ID, p.Name, p.Enabled, p.Schedule)
}
```

{{% /tab %}}
{{< /tabs >}}

## Get pipeline details

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines describe --id=<pipeline-id>
```

Example output:

```text
ID: 64f3a1b2c4d5e6f7a8b9c0d1
Name: hourly-temp-avg
Enabled: true
Schedule: 0 * * * *
MQL query: [
  {
    "$match": {
      "component_name": "temperature-sensor"
    }
  },
  ...
]
DataSourceType: TABULAR_DATA_SOURCE_TYPE_STANDARD
Last run:
  Status: Success
  Started: 2026-03-15T15:02:13Z
  Data range: [2026-03-15T14:00:00Z, 2026-03-15T15:00:00Z]
  Ended: 2026-03-15T15:02:18Z
```

If the pipeline has never run, the last section reads `Has not run yet.` instead.

{{% /tab %}}
{{% tab name="Python" %}}

```python
pipeline = await data_client.get_data_pipeline(id="YOUR-PIPELINE-ID")
print(f"Name: {pipeline.name}")
print(f"Schedule: {pipeline.schedule}")
print(f"Enabled: {pipeline.enabled}")
print(f"Data source: {pipeline.data_source_type}")
print(f"Created: {pipeline.created_on}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
pipeline, err := dataClient.GetDataPipeline(ctx, "YOUR-PIPELINE-ID")
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Name: %s\nSchedule: %s\nEnabled: %v\n", pipeline.Name, pipeline.Schedule, pipeline.Enabled)
```

{{% /tab %}}
{{< /tabs >}}

## Monitor pipeline runs

Each pipeline run has a status and an associated time window showing which data it processed.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Returns a page of runs (default page size: 10)
page = await data_client.list_data_pipeline_runs(id="YOUR-PIPELINE-ID")
for run in page.runs:
    print(f"Run {run.id}: {run.status}")
    print(f"  Data window: {run.data_start_time} to {run.data_end_time}")
    if run.error_message:
        print(f"  Error: {run.error_message}")

# Get the next page if there are more runs
if page.next_page_token:
    next_page = await page.next_page()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Returns a page of runs (default page size: 10)
page, err := dataClient.ListDataPipelineRuns(ctx, "YOUR-PIPELINE-ID", 10)
if err != nil {
    logger.Fatal(err)
}
for _, run := range page.Runs {
    fmt.Printf("Run %s: %d\n", run.ID, run.Status)
    fmt.Printf("  Data window: %s to %s\n", run.DataStartTime, run.DataEndTime)
    if run.ErrorMessage != "" {
        fmt.Printf("  Error: %s\n", run.ErrorMessage)
    }
}

// Get the next page
nextPage, err := page.NextPage(ctx)
```

{{% /tab %}}
{{< /tabs >}}

Run statuses:

| SDK status  | CLI label   | Meaning                                                                            |
| ----------- | ----------- | ---------------------------------------------------------------------------------- |
| `SCHEDULED` | `Scheduled` | The run is queued and waiting to execute (2-minute delay before execution starts). |
| `STARTED`   | `Running`   | The run is executing the MQL aggregation against the data source.                  |
| `COMPLETED` | `Success`   | The run finished and results are in the pipeline sink.                             |
| `FAILED`    | `Failed`    | The run encountered an error. Check the `error_message` field.                     |

SDK methods return the enum `Status` value on the left. The `viam datapipelines describe` CLI output uses the label on the right.

If a run stays in `STARTED` for more than 10 minutes, it is automatically marked as failed and a new run is created for that time window.

## Enable a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines enable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.EnableDataPipeline(ctx, "YOUR-PIPELINE-ID")
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
The Python SDK does not currently have `enable_data_pipeline` or `disable_data_pipeline` methods. Use the CLI or Go SDK.
{{< /alert >}}

## Disable a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines disable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.DisableDataPipeline(ctx, "YOUR-PIPELINE-ID")
```

{{% /tab %}}
{{< /tabs >}}

Disabling a pipeline stops future scheduled runs but does not delete existing results. When you re-enable a pipeline, it resumes from the next scheduled time window. It does not backfill windows it missed while disabled.

## Rename a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines rename --id=<pipeline-id> --name=new-name
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.rename_data_pipeline(id="YOUR-PIPELINE-ID", name="new-name")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.RenameDataPipeline(ctx, "YOUR-PIPELINE-ID", "new-name")
```

{{% /tab %}}
{{< /tabs >}}

## Delete a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

```bash
viam datapipelines delete --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.delete_data_pipeline(id="YOUR-PIPELINE-ID")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.DeleteDataPipeline(ctx, "YOUR-PIPELINE-ID")
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Deleting a pipeline is irreversible" color="caution" >}}
Deleting a pipeline removes the pipeline configuration, its execution history, and all output data in the pipeline sink. If you need to preserve pipeline results, export them first.
{{< /alert >}}

## Manage custom indexes

Custom indexes speed up queries against a pipeline's output collection.
You can create, list, and delete indexes from the Viam app, the CLI, or the SDK.

### Create an index in the Viam app

1. Open the pipeline detail page by clicking the pipeline name on the **Pipelines** subtab.
1. Select the **Custom indexes** tab.
1. Click **Create custom index**.
1. Enter a [MongoDB index specification](https://www.mongodb.com/docs/manual/reference/method/db.collection.createIndex/#options-for-all-index-types) in JSON format with a `key` field and optional `options`:

   ```json
   {
     "key": { "location_id": 1, "avg_temp": -1 },
     "options": { "name": "location-avg-temp" }
   }
   ```

1. Click **Create index**.

The index build starts in the background.
The **Custom indexes** tab shows the build status, which progresses from **Pending** to **In progress** to **Completed**.
If the build fails, the tab shows the error.

To delete an index, click the delete icon on the index card.

### Create an index with the CLI or SDK

See [Manage data indexes](/cli/manage-data/#manage-data-indexes) for CLI commands, or use the SDK's `CreateIndex`, `ListIndexes`, and `DeleteIndex` methods documented in the [data client API reference](/reference/apis/data-client/).

## Troubleshooting

{{< expand "Pipeline consistently fails" >}}

1. Check the error message in the run details (`list_data_pipeline_runs` or `describe`).
2. Run the same MQL query manually in the [query editor](/data/query-data/) using MQL mode against the same data source. This isolates whether the issue is in the query or the pipeline configuration.
3. Common failure causes:
   - Invalid MQL stage or syntax error
   - Query timeout (5-minute limit) on large datasets. Add a `$match` filter to reduce data.
   - Output exceeds 10,000 documents. Add `$limit` or make the `$group` less granular.

{{< /expand >}}

{{< expand "Re-enabled pipeline has gaps in results" >}}

This is expected. When you disable a pipeline, scheduled runs do not execute. When you re-enable it, it resumes from the next scheduled window. Missed windows are not retroactively processed, even if backfill is enabled. Backfill only applies to late-arriving data within windows the pipeline was active for.

{{< /expand >}}

{{< expand "Hot data store query returns no data" >}}

- Verify the hot data store is enabled on the component. See [Hot data store](/data/hot-data-store/).
- Check that data falls within the configured `stored_hours` window. Older data is removed hourly.
- Verify data has been captured and synced within the retention window.

{{< /expand >}}
