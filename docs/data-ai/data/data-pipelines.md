---
linkTitle: "Precompute data pipelines"
title: "Precompute data pipelines"
weight: 25
description: "Create scheduled data pipelines that automatically aggregate and process data."
type: "docs"
tags: ["data pipelines", "aggregation", "materialized views"]
icon: true
images: ["/services/icons/data-capture.svg"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
date: "2025-07-02"
updated: "2025-09-12"
---

Data pipelines automatically transform raw sensor readings into summaries and insights at scheduled intervals.
Precomputing these results makes subsequent queries more efficient.

For example, you might often query the average temperature across multiple sensors for each hour of the day.
To make these queries faster, you can use a data pipeline to precalculate the results, saving significant computational resources.

Data pipelines work with all available data, even when the data is incomplete.
If a machine goes offline, data collection continues but sync pauses.
`viam-server` stores the data locally and syncs later, when the machine reconnects to Viam.
Once the machine reconnects and syncs the stored data, Viam automatically re-runs any pipeline whose results would change based on the new data.

## Prerequisites

{{% expand "Captured sensor data" %}}

While not a requirement, it's easier to test data pipelines if you have already enabled data capture from at least one component and begun syncing data with Viam before setting up a pipeline.

See [capture sensor data](/data-ai/capture-data/capture-sync/) to capture and sync data to Viam.

{{% /expand%}}

{{% expand "Owner role" %}}

Only users with [organization owner permissions](/manage/manage/rbac/) can create a data pipeline.

{{% /expand%}}

## Pipeline management

### Create a pipeline

To define a data pipeline, specify a name, the associated organization, a schedule, a data source type, and the query:

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines create`](/dev/tools/cli/#datapipelines):

```sh {class="command-line" data-prompt="$" data-continuation-prompt="2-5"}
viam datapipelines create \
  --org-id=<org-id> \
  --name=sensor-counts \
  --schedule="0 * * * *" \
  --data-source-type="standard" \
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$location_id", "avg_temp": {"$avg": "$data.readings.temperature"}, "count": {"$sum": 1}}}, {"$project": {"location": "$_id", "avg_temp": 1, "count": 1, "_id": 0}}]' \
  --enable-backfill=True
```

To pass your query as a file instead of specifying it inline, pass the `--mql-path` flag instead of `--mql`.

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), specify `--data-source-type hotstorage`.

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline):

{{< read-code-snippet file="/static/include/examples-generated/pipeline-create.snippet.pipeline-create.py" lang="py" class="line-numbers linkable-line-numbers" data-line="31-55" >}}

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `data_source` to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.CreateDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.CreateDataPipeline):

{{< read-code-snippet file="/static/include/examples-generated/pipeline-create.snippet.pipeline-create.go" lang="go" class="line-numbers linkable-line-numbers" data-line="47-57" >}}

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `data_source` field to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline):

{{< read-code-snippet file="/static/include/examples-generated/pipeline-create.snippet.pipeline-create.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18-29" >}}

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `dataSource` field to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{< /tabs >}}

Once configured, the pipeline will be run based on the defined schedule.

#### Schedule format

To create a schedule for your pipeline, specify a [cron expression](https://en.wikipedia.org/wiki/Cron) in UTC.
The schedule determines both execution frequency and the range of time queried by each execution.
The following table contains some common schedules:

| Schedule       | Frequency        | Query Time Range    |
| -------------- | ---------------- | ------------------- |
| `0 * * * *`    | Hourly           | Previous hour       |
| `0 0 * * *`    | Daily            | Previous day        |
| `*/15 * * * *` | Every 15 minutes | Previous 15 minutes |

#### Query limitations

Data pipeline queries only support a subset of MQL aggregation operators.
For more information, see [Supported aggregation operators](/data-ai/data/query/#supported-aggregation-operators).

#### Common issues

Non-unique IDs will trigger duplicate key errors, preventing the pipeline from saving subsequent results.
Avoid returning an `_id` value in your pipeline's final group stage unless you can guarantee its uniqueness across all pipeline runs.

The `$group` stage returns an `_id` value by default.
To remove it, follow any final `$group` stage with a `$project` stage that renames the `_id` field to a different name.

#### Performance considerations

For optimal performance when querying large datasets, see [query optimization and performance best practices](/data-ai/data/query/#query-optimization-and-performance-best-practices).

### Query pipeline results

Once the pipeline has run at least once, you can query its results.

{{< tabs >}}
{{% tab name="Python" %}}

To query the processed results of your data pipeline, call [`DataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql), using the following parameters:

- `type`: `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK`
- `pipeline_id`: your pipeline ID

{{< read-code-snippet file="/static/include/examples-generated/pipeline-query.snippet.pipeline-query.py" lang="py" class="line-numbers linkable-line-numbers" data-line="31-44" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To query the processed results of your data pipeline, call [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL), using the following parameters:

- `Type`: `app.TabularDataSourceTypePipelineSink`
- `PipelineId`: your pipeline ID

{{< read-code-snippet file="/static/include/examples-generated/pipeline-query.snippet.pipeline-query.go" lang="go" class="line-numbers linkable-line-numbers" data-line="34-37" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To query the processed results of your data pipeline, call [`dataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql), using the following parameters:

- `type`: `3`
- `pipelineId`: your pipeline ID

{{< read-code-snippet file="/static/include/examples-generated/pipeline-query.snippet.pipeline-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="19-30" >}}

{{% /tab %}}
{{< /tabs >}}

### List pipelines

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines list`](/dev/tools/cli/#datapipelines) to fetch a list of pipeline configurations in an organization:

```sh {class="command-line" data-prompt="$" }
viam datapipelines list --org-id=<org-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a list of pipeline configurations in an organization:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-list.snippet.pipeline-list.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.ListDataPipelines`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelines) to fetch a list of pipeline configurations in an organization:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-list.snippet.pipeline-list.go" lang="go" class="line-numbers linkable-line-numbers" data-line="27" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a list of pipeline configurations in an organization:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-list.snippet.pipeline-list.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}

### Enable a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines enable`](/dev/tools/cli/#datapipelines) to enable a disabled data pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines enable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.EnableDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.EnableDataPipeline) to enable a disabled data pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-enable.snippet.pipeline-enable.go" lang="go" class="line-numbers linkable-line-numbers" data-line="27" >}}

{{% /tab %}}
{{< /tabs >}}

### Disable a pipeline

Disabling a data pipeline lets you pause data pipeline execution without fully deleting the pipeline configuration from your organization.
The pipeline immediately stops aggregating data.

You can re-enable the pipeline at any time to resume execution.
When a pipeline is re-enabled, Viam does not backfill missed time windows from the period of time when a pipeline was disabled.

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines disable`](/dev/tools/cli/#datapipelines) to disable a data pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines disable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.DisableDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DisableDataPipeline) to disable a data pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-disable.snippet.pipeline-disable.go" lang="go" class="line-numbers linkable-line-numbers" data-line="27" >}}

{{% /tab %}}
{{< /tabs >}}

### Delete a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines delete`](/dev/tools/cli/#datapipelines) to delete a data pipeline, its execution history, and all output generated by that pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines delete --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.DeleteDataPipeline`](/dev/reference/apis/data-client/#deletedatapipeline) to delete a data pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-delete.snippet.pipeline-delete.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.DeleteDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteDataPipeline) to delete a data pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-delete.snippet.pipeline-delete.go" lang="go" class="line-numbers linkable-line-numbers" data-line="27" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.DeleteDataPipeline`](/dev/reference/apis/data-client/#deletedatapipeline) to delete a data pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-delete.snippet.pipeline-delete.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}

### View pipeline execution history

Data pipeline executions may have any of the following statuses:

- `SCHEDULED`: pending execution
- `STARTED`: currently processing
- `COMPLETED`: successfully finished
- `FAILED`: execution error

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view information about past and in-progress executions of a pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-execution.snippet.pipeline-execution.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.ListDataPipelineRuns`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelineRuns) to view information about past executions of a pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-execution.snippet.pipeline-execution.go" lang="go" class="line-numbers linkable-line-numbers" data-line="27" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view information about past executions of a pipeline:

{{< read-code-snippet file="/static/include/examples-generated/pipeline-execution.snippet.pipeline-execution.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18" >}}

{{% /tab %}}
{{< /tabs >}}
