---
linkTitle: "Hot data store"
title: "Hot data store"
weight: 35
layout: "docs"
type: "docs"
description: "Store a rolling window of recent data for fast queries while continuing to write all data to blob storage."
date: "2025-01-30"
aliases:
  - /data/hot-data-store/
  - /build/data/hot-data-store/
  - /data-ai/data/hot-data-store/
---

Keep a rolling window of recent data in a fast-query database for significantly faster queries on the last few hours or days of captured data. All data continues to be written to blob storage regardless of hot data store settings. The hot data store is an additional copy, not a replacement.

## Configure

The hot data store is configured per capture method on each component. You
choose which components send data to it and how many hours of data to retain.

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to [app.viam.com](https://app.viam.com) and navigate to your machine's
   **CONFIGURE** tab.
2. Find the component you want to enable hot storage for (for example, your sensor).
3. Click **Advanced** to expand the advanced configuration.
4. Enable **Sync to Hot Data Store**.
5. Set the **Time frame** to the number of hours of data to retain (for example, 24
   for the last 24 hours).
6. Click **Save**.

{{% /tab %}}
{{% tab name="JSON" %}}

Add the `recent_data_store` configuration to your component's data capture
settings. Set `stored_hours` to the number of hours of recent data to store.

```json {class="line-numbers linkable-line-numbers" data-line="17-19"}
{
  "components": [
    {
      "name": "sensor-1",
      "api": "rdk:component:sensor",
      "model": "rdk:builtin:fake",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.5,
                "additional_params": {},
                "recent_data_store": {
                  "stored_hours": 24
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

The `stored_hours` field controls how many hours of data the hot data store
retains. A scheduled cleanup job runs hourly and removes documents with a
`time_received` timestamp older than the configured window.

{{% /tab %}}
{{< /tabs >}}

## Query

Queries execute against blob storage by default. To query the hot data store,
specify it as the data source in your query.

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.TabularDataByMQL`](/reference/apis/data-client/#tabulardatabymql) with `data_source` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`:

```python
from viam.gen.app.data.v1.data_pb2 import TabularDataSourceType

results = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {"$match": {"component_name": "temperature-sensor"}},
        {"$sort": {"time_received": -1}},
        {"$limit": 10},
    ],
    tabular_data_source_type=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE,
)

for entry in results:
    print(entry)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL) with `TabularDataSourceType` set to hot storage:

```go
hotQueryStages := []map[string]interface{}{
    {"$match": map[string]interface{}{
        "component_name": "temperature-sensor",
    }},
    {"$sort": map[string]interface{}{"time_received": -1}},
    {"$limit": 10},
}

hotData, err := dataClient.TabularDataByMQL(ctx, orgID, hotQueryStages,
    &app.TabularDataByMQLOptions{
        TabularDataSourceType: app.TabularDataSourceTypeHotStorage,
    },
)
if err != nil {
    logger.Fatal(err)
}

for _, entry := range hotData {
    fmt.Printf("%v\n", entry)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.TabularDataByMQL`](/reference/apis/data-client/#tabulardatabymql) with `dataSourceType` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE`:

{{< read-code-snippet file="/static/include/examples-generated/query.snippet.pipeline-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

The hot data store returns the same document schema as the standard data store.
The only difference is the data is limited to the configured time window and
queries execute faster because the dataset is smaller.

{{< alert title="Caution" color="caution" >}}

Queries to the hot data store _only_ return data within the configured time
window. For example, if your hot data store retains 24 hours of data and you
query for temperature readings above 25°C, but no readings above 25°C were
recorded in the last 24 hours, the query returns zero results, even if older
data in blob storage contains matching readings. To query your full data
history, use the default blob storage data source.

{{< /alert >}}
