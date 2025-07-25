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
---

The hot data store stores a rolling window of recent data while continuing to write all data to blob storage.
Queries to the hot data store execute significantly faster than queries to blob storage.

## Configure

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

## Query

Queries execute on blob storage by default which is slower than queries to a hot data store.
If you have configured a hot data store, you must specify it in any queries as the data source to be used for the query.

{{< tabs >}}
{{% tab name="Python" %}}

Use [`DataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) with `data_source` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

```python
data_client = DataClient.from_api_key(
    api_key="<api-key>",
    api_key_id="<api-key-id>"
)

results = data_client.tabular_data_by_mql(
    organization_id="<org-id>",
    mql_binary=[
        bson.encode({"$match": {"location_id": "warehouse-1"}}),
        bson.encode({"$sort": {"_id": -1}}),
        bson.encode({"$limit": 100})
    ],
    data_source=TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE
)

for document in results:
    print(document)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use [`DataClient.TabularDataByMQL`](https://pkg.go.dev/go.viam.com/rdk/app#DataClient.TabularDataByMQL) with `DataSource` set to `datapb.TabularDataSourceType_TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

```go
client, err := utils.NewViamClient(context.Background(), utils.WithAPIKey("<api-key>", "<api-key-id>"))
if err != nil {
    panic(err)
}
defer client.Close()

dataClient := client.DataClient()

query := [][]byte{
    bson.Marshal(bson.M{"$match": bson.M{"location_id": "warehouse-1"}}),
    bson.Marshal(bson.M{"$sort": bson.M{"_id": -1}}),
    bson.Marshal(bson.M{"$limit": 100}),
}

resp, err := dataClient.TabularDataByMQL(context.Background(), &datapb.TabularDataByMQLRequest{
    OrganizationId: "<org-id>",
    MqlBinary: query,
    DataSource: datapb.TabularDataSourceType_TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE,
})

for _, doc := range resp.Data {
    fmt.Println(doc)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use [`dataClient.TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) with `dataSource` set to `TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE` to query your hot data store:

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

const query = [
  BSON.serialize({ $match: { location_id: "warehouse-1" } }),
  BSON.serialize({ $sort: { _id: -1 } }),
  BSON.serialize({ $limit: 100 }),
];

const response = await dataClient.tabularDataByMQL({
  organizationId: "<org-id>",
  mqlBinary: query,
  dataSource: TabularDataSourceType.TABULAR_DATA_SOURCE_TYPE_HOT_STORAGE,
});

response.data.forEach((doc) => {
  console.log(BSON.deserialize(doc));
});
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Caution" color="caution" >}}

Queries to the hot data store _only_ return data from the hot data store, which only contains data from the time window you specified in your configuration.
For example, if you queried a hot data store with 24 hours of rolling storage for temperature data above 25C, and no temperature above 25C was recorded in the last 24 hours, your query would return zero results.
To query the entire history of your data, use blob storage.

{{< /alert >}}

### Query limitations

Hot data store queries only support a subset of MQL aggregation operators.
For more information, see [Supported aggregation operators](/data-ai/data/query/#supported-aggregation-operators).
