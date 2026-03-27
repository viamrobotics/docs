---
linkTitle: "Create a pipeline"
title: "Create a data pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Create a scheduled MQL pipeline that automatically aggregates captured data."
date: "2026-03-27"
aliases:
  - /data/configure-data-pipelines/
  - /build/data/configure-data-pipelines/
  - /data-ai/data/data-pipelines/
---

Create a pipeline that runs a scheduled MQL aggregation against your captured data and stores the results as precomputed summaries. For an overview of how pipelines work, see [Data pipelines overview](/data/pipelines/overview/).

## Prerequisites

- Captured tabular data in the cloud (see [Start data capture](/data/capture-sync/capture-and-sync-data/))
- Your organization ID (find it in the Viam app under **Settings**)
- Viam CLI installed, or the Python/Go SDK

## Create with the CLI

This example creates a pipeline that computes hourly temperature averages grouped by location:

```bash
viam datapipelines create \
  --org-id=<org-id> \
  --name=hourly-temp-avg \
  --schedule="0 * * * *" \
  --data-source-type=standard \
  --mql='[{"$match": {"component_name": "temperature-sensor"}}, {"$group": {"_id": "$location_id", "avg_temp": {"$avg": "$data.readings.temperature"}, "count": {"$sum": 1}}}, {"$project": {"location": "$_id", "avg_temp": 1, "count": 1, "_id": 0}}]' \
  --enable-backfill=true
```

The CLI prints the pipeline ID on success. Save this ID to query results and manage the pipeline.

### CLI flags

| Flag | Required | Description |
| --- | --- | --- |
| `--org-id` | Yes | Your organization ID. |
| `--name` | Yes | A descriptive name. Must be unique within the organization. |
| `--schedule` | Yes | A cron expression in UTC. Also determines the query time window. See [Cron schedule](/data/pipelines/reference/#cron-schedule). |
| `--mql` | One of `--mql` or `--mql-path` | The MQL aggregation pipeline as a JSON string. |
| `--mql-path` | One of `--mql` or `--mql-path` | Path to a file containing the MQL aggregation pipeline as JSON. |
| `--enable-backfill` | Yes | Whether to process historical time windows. `true` or `false`. |
| `--data-source-type` | Yes | `standard` or `hotstorage`. |

For complex queries, use `--mql-path` to read from a file:

```bash
viam datapipelines create \
  --org-id=<org-id> \
  --name=hourly-temp-avg \
  --schedule="0 * * * *" \
  --data-source-type=standard \
  --mql-path=./my-pipeline.json \
  --enable-backfill=true
```

Where `my-pipeline.json` contains:

```json
[
  { "$match": { "component_name": "temperature-sensor" } },
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

## Create with the SDK

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.app.viam_client import ViamClient
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType

API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def main():
    opts = ViamClient.Options.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID
    )
    client = await ViamClient.create_from_dial_options(opts)
    data_client = client.data_client

    # Returns the pipeline ID
    pipeline_id = await data_client.create_data_pipeline(
        organization_id=ORG_ID,
        name="hourly-temp-avg",
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
    client.close()

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
    ctx := context.Background()
    logger := logging.NewDebugLogger("pipeline")

    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, "YOUR-API-KEY", "YOUR-API-KEY-ID", logger)
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
        ctx, "YOUR-ORGANIZATION-ID", "hourly-temp-avg",
        mqlStages, "0 * * * *", false,
        &app.CreateDataPipelineOptions{
            TabularDataSourceType: app.TabularDataSourceTypeStandard,
        },
    )
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Created pipeline: %s\n", pipelineID)
}
```

{{% /tab %}}
{{< /tabs >}}

To get your credentials:

1. Go to your machine's page in the Viam app.
2. Click the **CONNECT** tab.
3. Select **SDK code sample**.
4. Toggle **Include API key** on.
5. Copy the **API key** and **API key ID**.

Find your organization ID in the Viam app by clicking your organization name and selecting **Settings**.

After creating a pipeline, see [Query pipeline results](/data/pipelines/query-results/) to access the output, and [Examples and tips](/data/pipelines/examples/) for MQL patterns for common robotics use cases.

## Troubleshooting

{{< expand "Pipeline creation fails with permission error" >}}

Only organization owners can create data pipelines. Verify your API key has owner-level permissions. In the Viam app, go to **Settings** and check the role associated with your key.

{{< /expand >}}

{{< expand "Pipeline runs but produces no results" >}}

- **Check the `$match` stage.** Field names and values must match your actual data. Run the same MQL query in the query editor to verify it returns results.
- **Check the time window.** If no data was captured during the pipeline's time window, the run produces no output.
- **Check the data source type.** If you set `hotstorage` but the hot data store is not configured for your components, the pipeline has no data to query.

{{< /expand >}}

{{< expand "Duplicate key error in pipeline results" >}}

Follow `$group` with `$project` to rename `_id` to a descriptive field name and set `_id` to 0. See [MQL tips](/data/pipelines/examples/#always-rename-_id-in-project).

{{< /expand >}}

{{< expand "Pipeline results are stale or delayed" >}}

Pipelines run on a cron schedule with a 2-minute execution delay. Results for the 02:00-03:00 PM window are not available until shortly after 03:00 PM. For faster updates, use a more frequent schedule (for example, `*/15 * * * *`).

{{< /expand >}}
