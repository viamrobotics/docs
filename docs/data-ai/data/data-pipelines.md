---
linkTitle: "Aggregate data automatically"
title: "Aggregate data automatically"
weight: 25
description: "Create scheduled data pipelines that automatically aggregate and process data."
type: "docs"
tags: ["data pipelines", "aggregation", "materialized views"]
icon: true
images: ["/services/icons/data-capture.svg"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
date: "2025-07-02"
---

Data pipelines automatically transform raw sensor readings into summaries and insights at a schedule that you choose.
Viam stores the output of these pipelines in a separate, queryable database.

For example, you may often query the average temperature across multiple sensors for each hour of the day.
To make these queries faster, you can use a data pipeline to pre-calculate the results, saving significant computational resources.

{{< alert title="Tip" color="tip" >}}

When a machine goes offline, data collection continues but sync pauses.
`viam-server` stores the data locally and syncs later, when your machine reconnects to Viam.

Once the machine reconnects and syncs this stored data, Viam automatically re-runs affected pipelines to include the new data.

{{< /alert >}}

## Prerequisites

While not a requirement, it is easier to test data pipelines if you have already enabled data capture from at least one component and begun syncing data with Viam before setting up a pipeline.

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
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$location_id", "avg_temp": {"$avg": "$data.readings.temperature"}, "count": {"$sum": 1}}, {"$project": {"location": "$_id", "avg_temp": 1, "count": 1}}]'
```

To pass your query as a file instead of specifying it as inline MQL, pass the `--mql-path` flag instead of `--mql`.
To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), specify `--data-source-type hotstorage`.

{{% /tab %}}
{{% tab name="Python" %}}

To define a new pipeline, call [`DataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline):

```python
from viam import DataClient
import bson

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
        }),
        bson.encode({
            "$project": {
                "location": "$_id",
                "avg_temp": 1,
                "count": 1
            }
        })
    ],
    schedule="0 * * * *"  # Run hourly
)
```

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `data_source` to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{% tab name="Go" %}}

To define a new pipeline, call [`DataClient.CreateDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.CreateDataPipeline):

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
    datapb "go.viam.com/rdk/app/data/v1"
    "go.viam.com/rdk/app/data/v1/bson"
)

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
    bson.Marshal(bson.M{
        "$group": bson.M{
            "location": "$_id",
            "avg_temp": 1,
            "count": 1,
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

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `data_source` field to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{% tab name="TypeScript" %}}

To define a new pipeline, call [`dataClient.CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline):

```typescript
import { createViamClient } from "@viamrobotics/sdk";
import {
  TabularDataSource,
  TabularDataSourceType,
} from "@viamrobotics/sdk/dist/gen/app/data/v1/data_pb";
import { BSON } from "bson";

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
  BSON.serialize({
    $project: {
      location: "$_id",
      avg_temp: 1,
      count: 1,
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

To create a pipeline that reads data from the [hot data store](/data-ai/data/hot-data-store/), set your query's `dataSource` field to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`.

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Caution" color="caution" >}}

Avoid specifying an `_id` value in your pipeline's final group stage unless you can guarantee its uniqueness across all pipeline runs.
Non-unique IDs will trigger duplicate key errors, preventing the pipeline from saving subsequent results.
Because the `$group` stage requires an `_id` value, follow any final `$group` stage with a `$project` stage that renames the `_id` field to a different name.

{{< /alert >}}

#### Schedule format

To create a schedule for your pipeline, specify a [cron expression](https://en.wikipedia.org/wiki/Cron) in UTC.
The schedule determines both execution frequency and the range of time queried by each execution.
The following table contains some common schedules, which correspond to the listed execution frequencies and query time range:

| Schedule       | Frequency        | Query Time Range    |
| -------------- | ---------------- | ------------------- |
| `0 * * * *`    | Hourly           | Previous hour       |
| `0 0 * * *`    | Daily            | Previous day        |
| `*/15 * * * *` | Every 15 minutes | Previous 15 minutes |

#### Query limitations

Data pipeline queries only support a subset of MQL aggregation operators.
For more information, see [Supported aggregation operators](/data-ai/data/query/#supported-aggregation-operators).

### Query pipeline results

{{< tabs >}}
{{% tab name="Python" %}}

To query the results of your data pipeline, call [`DataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql).
Configure the `data_source` argument with the following fields:

- `type`: `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK`
- `pipeline_id`: your pipeline ID

```python
from viam import DataClient
from viam.app.data.v1.data_pb import TabularDataSource, TabularDataSourceType
import bson

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

To query the results of your data pipeline, call [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL).
Configure the `DataSource` argument with the following fields:

- `Type`: `datapb.TabularDataSourceType_TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK`
- `PipelineId`: your pipeline's ID

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
    datapb "go.viam.com/rdk/app/data/v1"
    "go.viam.com/rdk/app/data/v1/bson"
)

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

To query the results of your data pipeline, call [`dataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql).
Configure the `data_source` argument with the following fields:

- `type`: `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_PIPELINE_SINK`
- `pipelineId`: your pipeline's ID

```typescript
import { createViamClient } from '@viamrobotics/sdk';
import { TabularDataSource, TabularDataSourceType } from '@viamrobotics/sdk/dist/gen/app/data/v1/data_pb';
import { BSON } from 'bson';

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
  "<org-id>",
  query,
  false,
  new TabularDataSource({
    type: TabularDataSourceType.PIPELINE_SINK,
    pipelineId: "<pipeline-id>",
  }),
});

response.data.forEach((doc) => {
  console.log(BSON.deserialize(doc));
});
```

{{% /tab %}}
{{< /tabs >}}

### List pipelines

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines list`](/dev/tools/cli/#datapipelines) to fetch a list of pipeline configurations in an organization:

```sh {class="command-line" data-prompt="$" class="command-line"}
viam datapipelines list --org-id=<org-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`DataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a list of pipeline configurations in an organization:

```python
from viam import DataClient
import bson

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

Use [`DataClient.ListDataPipelines`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelines) to fetch a list of pipeline configurations in an organization:

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
)

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

Use [`dataClient.ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) to fetch a list of pipeline configurations in an organization:

```typescript
import { createViamClient } from "@viamrobotics/sdk";
import { BSON } from "bson";

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

{{< alert title="Caution" color="caution" >}}

Use caution when updating the query or schedule of a data pipeline.
Changing either value can lead to inconsistent pipeline output history.

{{< /alert >}}

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines update`](/dev/tools/cli/#datapipelines) to alter an existing data pipeline:

```sh {class="command-line" data-prompt="$" class="command-line" data-continuation-prompt="2-5"}
viam datapipelines update \
  --org-id=<org-id> \
  --id=<pipeline-id> \
  --schedule="0 * * * *" \
  --name="updated-name" \
  --mql='[{"$match": {"component_name": "sensor"}}, {"$group": {"_id": "$part_id", "total": {"$sum": "$1"}}, {"$project": {"part": "$_id", "avg_temp": 1, "count": 1}}]'
```

To pass your query from a file instead of from inline MQL, pass the `--mql-path` flag instead of `--mql`.

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.UpdateDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.UpdateDataPipeline) to alter an existing data pipeline:

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
    "go.viam.com/rdk/app/data/v1/bson"
)

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
    bson.Marshal(bson.M{
        "$group": bson.M{
            "part": "$_id",
            "total": 1,
        },
    }),
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

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
)

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
{{< /tabs >}}

### Disable a pipeline

Disabling a data pipeline lets you pause data pipeline execution without fully deleting the pipeline configuration from your organization.
The pipeline immediately stops aggregating data.
You can re-enable the pipeline at any time to resume execution.
When a pipeline is re-enabled, Viam will not backfill missed time windows from the period of time when a pipeline was disabled.

{{< tabs >}}
{{% tab name="CLI" %}}

Use [`datapipelines disable`](/dev/tools/cli/#datapipelines) to disable a data pipeline:

```sh {class="command-line" data-prompt="$"}
viam datapipelines disable --id=<pipeline-id>
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.DisableDataPipeline`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.DisableDataPipeline) to disable a data pipeline:

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
)

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

```python
from viam import DataClient

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
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
)

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
import { createViamClient } from "@viamrobotics/sdk";

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

Use [`DataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view information about past and in-progress executions of a pipeline:

```python
from viam import DataClient

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

Use [`DataClient.ListDataPipelineRuns`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.ListDataPipelineRuns) to view information about past executions of a pipeline:

```go
import (
    "context"
    "fmt"
    "go.viam.com/rdk/app/utils"
)

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

Use [`dataClient.ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) to view information about past executions of a pipeline:

```typescript
import { createViamClient } from "@viamrobotics/sdk";

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
