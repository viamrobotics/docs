---
linkTitle: "Aggregate data automatically"
title: "Aggregate data automatically"
weight: 25
description: "Make processed data automatically available for faster, simpler queries."
type: "docs"
tags: ["data pipelines", "aggregation", "materialized views"]
icon: true
images: ["/services/icons/data-capture.svg"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
date: "2025-07-02"
---

Data pipelines automatically transform raw sensor readings into summaries and insights at a schedule that you choose.
Viam stores the output of these pipelines in a cache so that you can access complex aggregation results more efficiently.
When late-arriving data syncs to Viam, pipelines automatically re-run to keep summaries accurate.

For example, you could use a data pipeline to pre-calculate results like "average temperature per hour".
If you query that information frequently, this can save significant computational resources.

## Prerequisites

Before creating a data pipeline, you must enable data capture from at least one component and begin syncing data with Viam.

Only users with organization owner permissions can create a data pipeline.

## Pipeline management

### Create a pipeline

To define a data pipeline, specify a name, organization, schedule, data source type, and query:

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines create`](/dev/tools/cli/#datapipelines) to create your pipeline:

```sh {class="command-line" data-prompt="$" class="command-line" data-continuation-prompt="2-5"}
viam datapipelines create \
  --org-id=<org-id> \
  --name=sensor-counts \
  --schedule="0 * * * *" \
  --data-source-type="standard" \
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$location_id", "avg": {"$avg": "$data.readings.value"}}}]'
```

To pass your query from a file instead of from inline MQL, pass the `--mql-path` flag instead of `--mql`.
To query data from the [hot data store](/data-ai/data/hot-data-store/), specify `--data-source-type hotstorage`.

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline) to define a new pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

request = data_client.create_data_pipeline(
    organization_id="<org-id>",
    name="hourly-temp-average",
    mql_binary=[
        bson.encode({"$match": {"component_name": "temperature-sensor"}}),
        bson.encode({
            "$group": {
                "_id": "$location_id",
                "avg_temp": {"$avg": "$data.readings.temperature"},
                "count": {"$sum": 1}
            }
        })
    ],
    schedule="0 * * * *"  # Run hourly
)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.CreateDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.CreateDataPipeline) to define a new pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

pipeline := [][]byte{
    bson.Marshal(bson.M{"$match": bson.M{"component_name": "temperature-sensor"}}),
    bson.Marshal(bson.M{
        "$group": bson.M{
            "_id": "$location_id",
            "avg_temp": bson.M{"$avg": "$data.readings.temperature"},
            "count": bson.M{"$sum": 1},
        },
    }),
}

resp, err := dataClient.CreateDataPipeline(context.Background(), &datapb.CreateDataPipelineRequest{
    OrganizationId: "<org-id>",
    Name: "hourly-temp-average",
    MqlBinary: pipeline,
    Schedule: "0 * * * *", // Run hourly
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline) to define a new pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

const pipeline = [
  BSON.serialize({ $match: { component_name: "temperature-sensor" } }),
  BSON.serialize({
    $group: {
      _id: "$location_id",
      avg_temp: { $avg: "$data.readings.temperature" },
      count: { $sum: 1 },
    },
  }),
];

const response = await dataClient.createDataPipeline({
  organizationId: "<org-id>",
  name: "hourly-temp-average",
  mqlBinary: pipeline,
  schedule: "0 * * * *", // Run hourly
});
```

{{% /tab %}}
{{< /tabs >}}

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), specify a `dataSourceType` in your pipeline configuration.

#### Schedule format

To create a schedule for your pipeline, specify a [cron expression](https://en.wikipedia.org/wiki/Cron) in UTC.
The schedule determines both execution frequency and input time window.
The following table contains some common schedules, which correspond to the listed execution frequencies and input time windows:

| Schedule       | Frequency        | Time Window         |
| -------------- | ---------------- | ------------------- |
| `0 * * * *`    | Hourly           | Previous hour       |
| `0 0 * * *`    | Daily            | Previous day        |
| `*/15 * * * *` | Every 15 minutes | Previous 15 minutes |

### List pipelines

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines list`](/dev/tools/cli/#datapipelines) to see a summary of all pipelines in an organization:

```sh {class="command-line" data-prompt="$" class="command-line"}
viam datapipelines list --org-id=<org-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a summary of all pipelines in an organization:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

pipelines = data_client.list_data_pipelines(organization_id="<org-id>")

for pipeline in pipelines:
    print(f"{pipeline.name} (id: {pipeline.id})")
    print(f"Schedule: {pipeline.schedule}")
    print(f"Enabled: {pipeline.enabled}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.ListDataPipelines`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelines) to fetch a summary of all pipelines in an organization:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

resp, err := dataClient.ListDataPipelines(context.Background(), &datapb.ListDataPipelinesRequest{
    OrganizationId: "<org-id>",
})

for _, pipeline := range resp.DataPipelines {
    fmt.Printf("%s (id: %s)\n", pipeline.Name, pipeline.Id)
    fmt.Printf("Schedule: %s\n", pipeline.Schedule)
    fmt.Printf("Enabled: %v\n", pipeline.Enabled)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a summary of all pipelines in an organization:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

const response = await dataClient.listDataPipelines({
  organizationId: "<org-id>",
});

response.dataPipelines.forEach((pipeline) => {
  console.log(`${pipeline.name} (id: ${pipeline.id})`);
  console.log(`Schedule: ${pipeline.schedule}`);
  console.log(`Enabled: ${pipeline.enabled}`);
});
```

{{% /tab %}}
{{< /tabs >}}

### Update a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines update`](/dev/tools/cli/#datapipelines) to alter an existing data pipeline:

```sh {class="command-line" data-prompt="$" class="command-line" data-continuation-prompt="2-5"}
viam datapipelines update \
  --org-id=<org-id> \
  --id=<pipeline-id> \
  --schedule="0 * * * *" \
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$location_id", "avg": {"$avg": "$data.readings.value"}}}]'
```

To pass your query from a file instead of from inline MQL, pass the `--mql-path` flag instead of `--mql`.

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.UpdateDataPipeline`](/dev/reference/apis/data-client/#updatedatapipeline) to alter an existing data pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

data_client.update_data_pipeline(
    id="<pipeline-id>",
    name="updated-name",
    mql_binary=[
        bson.encode({"$match": {"component_name": "sensor"}}),
        bson.encode({"$group": {"_id": "$part_id", "total": {"$sum": 1}}})
    ],
    schedule="0 * * * *"
)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.UpdateDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.UpdateDataPipeline) to alter an existing data pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

pipeline := [][]byte{
    bson.Marshal(bson.M{"$match": bson.M{"component_name": "sensor"}}),
    bson.Marshal(bson.M{
        "$group": bson.M{
            "_id": "$part_id",
            "total": bson.M{"$sum": 1},
        },
    }),
}

_, err := dataClient.UpdateDataPipeline(context.Background(), &datapb.UpdateDataPipelineRequest{
    Id: "<pipeline-id>",
    Name: "updated-name",
    MqlBinary: pipeline,
    Schedule: "0 * * * *",
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.UpdateDataPipeline`](/dev/reference/apis/data-client/#updatedatapipeline) to alter an existing data pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

const pipeline = [
  BSON.serialize({ $match: { component_name: "sensor" } }),
  BSON.serialize({
    $group: {
      _id: "$part_id",
      total: { $sum: 1 },
    },
  }),
];

await dataClient.updateDataPipeline({
  id: "<pipeline-id>",
  name: "updated-name",
  mqlBinary: pipeline,
  schedule: "0 0 * * *", // Change to daily
});
```

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
{{% tab name="Python" %}}

Use [`DataClient.EnableDataPipeline`](/dev/reference/apis/data-client/#enabledatapipeline) to enable a disabled data pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

data_client.enable_data_pipeline(id="<pipeline-id>")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.EnableDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.EnableDataPipeline) to enable a disabled data pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

_, err := dataClient.EnableDataPipeline(context.Background(), &datapb.EnableDataPipelineRequest{
    Id: "<pipeline-id>",
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.EnableDataPipeline`](/dev/reference/apis/data-client/#enabledatapipeline) to enable a disabled data pipeline:

```typescript
const apiKey = '<api-key>';
const apiKeyID = '<api-key-id>';

const client = await createViamClient({
  credential: {
    type: 'api-key',
    payload: { key: apiKey, keyId: apiKeyID }
  }
});

const dataClient = client.dataClient;

const pipeline = [

await dataClient.enableDataPipeline({ id: "<pipeline-id>" });
```

{{% /tab %}}
{{< /tabs >}}

### Disable a pipeline

Disabling a data pipeline lets you pause data pipeline execution without fully deleting the pipeline configuration from your organization.

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines disable`](/dev/tools/cli/#datapipelines) to disable a data pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines disable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.DisableDataPipeline`](/dev/reference/apis/data-client/#disabledatapipeline) to disable a data pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

data_client.disable_data_pipeline(id="<pipeline-id>")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.DisableDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DisableDataPipeline) to disable a data pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

_, err := dataClient.DisableDataPipeline(context.Background(), &datapb.DisableDataPipelineRequest{
    Id: "<pipeline-id>",
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.DisableDataPipeline`](/dev/reference/apis/data-client/#disabledatapipeline) to disable a data pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

await dataClient.disableDataPipeline({ id: "<pipeline-id>" });
```

{{% /tab %}}
{{< /tabs >}}

### Delete a pipeline

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines delete`](/dev/tools/cli/#datapipelines) to delete a data pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines delete --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.DeleteDataPipeline`](/dev/reference/apis/data-client/#deletedatapipeline) to delete a data pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

data_client.delete_data_pipeline(id="<pipeline-id>")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.DeleteDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DeleteDataPipeline) to delete a data pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

_, err := dataClient.DeleteDataPipeline(context.Background(), &datapb.DeleteDataPipelineRequest{
    Id: "<pipeline-id>",
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.DeleteDataPipeline`](/dev/reference/apis/data-client/#deletedatapipeline) to delete a data pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

await dataClient.deleteDataPipeline({ id: "<pipeline-id>" });
```

{{% /tab %}}
{{< /tabs >}}

### Check pipeline execution history

Data pipeline executions may have any of the following statuses:

- `SCHEDULED`: pending execution
- `STARTED`: currently processing
- `COMPLETED`: successfully finished
- `FAILED`: execution error

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view the statuses of past executions of a pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

runs = data_client.list_data_pipeline_runs(
    id="<pipeline-id>",
    page_size=10
)

for run in runs:
    print(f"Run {run.id}: {run.status}")
    print(f"Data window: {run.data_start_time} to {run.data_end_time}")
    print(f"Started: {run.started}, Ended: {run.ended}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.ListDataPipelineRuns`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelineRuns) to view the statuses of past executions of a pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

resp, err := dataClient.ListDataPipelineRuns(context.Background(), &datapb.ListDataPipelineRunsRequest{
    Id: "<pipeline-id>",
    PageSize: 10,
})

for _, run := range resp.Executions {
    fmt.Printf("Run %s: %s\n", run.Id, run.Status)
    fmt.Printf("Data window: %s to %s\n", run.DataStartTime, run.DataEndTime)
    fmt.Printf("Started: %s, Ended: %s\n", run.Started, run.Ended)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view the statuses of past executions of a pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

const response = await dataClient.listDataPipelineRuns({
  id: "<pipeline-id>",
  pageSize: 10,
});

response.executions.forEach((run) => {
  console.log(`Run ${run.id}: ${run.status}`);
  console.log(`Data window: ${run.dataStartTime} to ${run.dataEndTime}`);
  console.log(`Started: ${run.started}, Ended: ${run.ended}`);
});
```

{{% /tab %}}
{{< /tabs >}}

### Query pipeline results

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) to query the results of your data pipeline:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

results = data_client.tabular_data_by_mql(
    organization_id="<org-id>",
    mql_binary=[
        bson.encode({}),
    ],
    data_source=TabularDataSource(
        type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
        pipeline_id="<pipeline-id>"
    )
)

for document in results:
    print(document)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL) to query the results of your data pipeline:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

query := [][]byte{
    bson.Marshal(bson.M{}),
}

resp, err := dataClient.TabularDataByMQL(context.Background(), &datapb.TabularDataByMQLRequest{
    OrganizationId: "<org-id>",
    MqlBinary: query,
    DataSource: &datapb.TabularDataSource{
        Type: datapb.TabularDataSourceType_TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
        PipelineId: proto.String("<pipeline-id>"),
    },
})

for _, doc := range resp.Data {
    fmt.Println(doc)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) to query the results of your data pipeline:

```typescript
const apiKey = "<api-key>";
const apiKeyID = "<api-key-id>";

const client = await createViamClient({
  credential: {
    type: "api-key",
    payload: { key: apiKey, keyId: apiKeyID },
  },
});

const dataClient = client.dataClient;

const query = [BSON.serialize({})];

const response = await dataClient.tabularDataByMQL({
  organizationId: "<org-id>",
  mqlBinary: query,
  dataSource: {
    type: TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK,
    pipelineId: "<pipeline-id>",
  },
});

response.data.forEach((doc) => {
  console.log(BSON.deserialize(doc));
});
```

{{% /tab %}}
{{< /tabs >}}
