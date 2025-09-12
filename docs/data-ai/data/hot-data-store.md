---
linkTitle: "Speed up recent data queries"
title: "Speed up recent data queries"
weight: 25
description: "Store a rolling window of recent data for fast queries while continuing to write all data to blob storage."
type: "docs"
tags: ["hot data store", "aggregation", "materialized views"]
icon: true
images: ["/services/icons/data-capture.svg"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
date: "2024-12-03"
updated: "2025-09-12"
---

The hot data store stores a rolling window of recent data in a database while continuing to write all data to {{< glossary_tooltip term_id="blob-storage" text="blob storage" >}}.
Queries to the hot data store execute significantly faster than queries to blob storage.

## Configure

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Find the resource you are capturing data from on the **CONFIGURE** tab
2. Click on **Advanced**.
3. Enable **Sync to Hot Data Store**.
4. Specify a **Time frame**.
5. Save.

{{% /tab %}}
{{% tab name="JSON" %}}

To configure the hot data store, add the `recent_data_store` configuration to your component's data capture settings.
Set the value of the `stored_hours` field to the number of hours of recent data you would like to store.
For example, the following configuration stores 24 hours of data in the hot data store:

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

{{% /tab %}}
{{< /tabs >}}

## Query

Queries execute on blob storage by default, which is slower than queries to a hot data store.
To query data from the hot data store, you must specify it as the data source in your queries.

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) with `data_source` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

{{< read-code-snippet file="/static/include/examples-generated/query.snippet.pipeline-query.py" lang="py" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL) with `DataSource` set to `datapb.TabularDataSourceType_TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

{{< read-code-snippet file="/static/include/examples-generated/query.snippet.pipeline-query.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) with `dataSource` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

{{< read-code-snippet file="/static/include/examples-generated/query.snippet.pipeline-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Caution" color="caution" >}}

Queries to the hot data store _only_ return data from the hot data store, which only contains data from the time window you specified in your configuration.
For example, if you query a hot data store which has 24 hours of the most recent data for temperature data above 25C, and no temperature above 25C was recorded in the last 24 hours, your query would return zero results even if other readings outside that time period contain readings above 25C.
To query the entire history of your data, use blob storage as the data source in queries.

{{< /alert >}}

### Query limitations

Hot data store queries only support a subset of MQL aggregation operators.
For more information, see [Supported aggregation operators](/data-ai/data/query/#supported-aggregation-operators).
