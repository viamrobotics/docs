---
linkTitle: "Query captured data"
title: "Query captured data"
weight: 70
layout: "docs"
type: "docs"
description: "Query sensor and binary data from a client app using SQL and MQL through DataClient."
date: "2026-04-10"
---

Query data that your Viam machines have captured and synced to the cloud, from inside a client app. This page covers the SDK calls for running SQL and MQL queries from app code. For the query languages themselves (schema, operators, examples), see [Query data](/data/query-data/) in the data section.

## Prerequisites

- A project with a cloud connection (see [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/))
- The organization ID that owns the data you want to query
- Data capture configured on at least one machine so there is something to query (see [Capture and sync data](/data/capture-sync/capture-and-sync-data/))

## Run a SQL query

SQL is the simplest entry point. The query runs against your organization's captured tabular data.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
const orgId = "your-organization-id";

const rows = await client.dataClient.tabularDataBySQL(
  orgId,
  `SELECT component_name, time_received, data
   FROM readings
   WHERE component_name = 'temperature_sensor'
   ORDER BY time_received DESC
   LIMIT 20`,
);

console.log(`Got ${rows.length} rows`);
for (const row of rows) {
  console.log(row);
}
```

`tabularDataBySQL` returns an array of row objects. The shape of each row depends on your query's `SELECT` list.

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
final orgId = 'your-organization-id';

final rows = await viam.dataClient.tabularDataBySql(
  orgId,
  '''
  SELECT component_name, time_received, data
  FROM readings
  WHERE component_name = 'temperature_sensor'
  ORDER BY time_received DESC
  LIMIT 20
  ''',
);

print('Got ${rows.length} rows');
for (final row in rows) {
  print(row);
}
```

`tabularDataBySql` returns a `List<Map<String, dynamic>>` where each map is one row.

{{% /tab %}}
{{% tab name="Python" %}}

```python
org_id = "your-organization-id"

rows = await client.data_client.tabular_data_by_sql(
    org_id,
    """SELECT component_name, time_received, data
       FROM readings
       WHERE component_name = 'temperature_sensor'
       ORDER BY time_received DESC
       LIMIT 20"""
)

print(f"Got {len(rows)} rows")
for row in rows:
    print(row)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
orgID := "your-organization-id"

rows, err := client.DataClient().TabularDataBySQL(
    context.Background(),
    orgID,
    "SELECT component_name, time_received, data FROM readings WHERE component_name = 'temperature_sensor' ORDER BY time_received DESC LIMIT 20",
)
if err != nil {
    logger.Fatal(err)
}

fmt.Printf("Got %d rows\n", len(rows))
```

{{% /tab %}}
{{< /tabs >}}

## Run an MQL query

MQL (MongoDB Query Language) supports aggregation pipelines: `$match`, `$group`, `$project`, and so on. Use MQL when you need to aggregate data across machines or compute derived values.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
const orgId = "your-organization-id";

const pipeline = [
  {
    $match: {
      component_name: "air_quality_sensor",
      time_received: { $gte: new Date(Date.now() - 3600 * 1000) },
    },
  },
  {
    $group: {
      _id: "$robot_id",
      avg_pm_25: { $avg: "$data.readings.pm_2_5" },
      max_pm_25: { $max: "$data.readings.pm_2_5" },
      sample_count: { $sum: 1 },
    },
  },
];

const results = await client.dataClient.tabularDataByMQL(orgId, pipeline);
console.log(results);
```

The SDK serializes plain JavaScript objects into BSON automatically. You can also pass pre-serialized `Uint8Array[]` if you are generating the pipeline elsewhere.

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
final orgId = 'your-organization-id';

final pipeline = [
  {
    '\$match': {
      'component_name': 'air_quality_sensor',
      'time_received': {
        '\$gte': DateTime.now().subtract(const Duration(hours: 1)),
      },
    },
  },
  {
    '\$group': {
      '_id': '\$robot_id',
      'avg_pm_25': {'\$avg': '\$data.readings.pm_2_5'},
      'max_pm_25': {'\$max': '\$data.readings.pm_2_5'},
      'sample_count': {'\$sum': 1},
    },
  },
];

final results = await viam.dataClient.tabularDataByMql(orgId, pipeline);
print(results);
```

Flutter's `tabularDataByMql` also accepts either `List<Map<String, dynamic>>` (auto-serialized) or `List<Uint8List>` (pre-serialized with `BsonCodec.serialize`).

Note that `$` is a special character in Dart string interpolation, so MQL operators must be escaped as `\$match`, `\$group`, and so on inside string literals.

{{% /tab %}}
{{% tab name="Python" %}}

```python
from datetime import datetime, timedelta

org_id = "your-organization-id"

pipeline = [
    {
        "$match": {
            "component_name": "air_quality_sensor",
            "time_received": {"$gte": datetime.now() - timedelta(hours=1)},
        }
    },
    {
        "$group": {
            "_id": "$robot_id",
            "avg_pm_25": {"$avg": "$data.readings.pm_2_5"},
            "max_pm_25": {"$max": "$data.readings.pm_2_5"},
            "sample_count": {"$sum": 1},
        }
    },
]

results = await client.data_client.tabular_data_by_mql(org_id, pipeline)
print(results)
```

Python's `tabular_data_by_mql` accepts either a list of dicts (auto-serialized) or pre-serialized BSON bytes.

{{% /tab %}}
{{% tab name="Go" %}}

```go
orgID := "your-organization-id"

pipeline := []map[string]interface{}{
    {
        "$match": map[string]interface{}{
            "component_name": "air_quality_sensor",
        },
    },
    {
        "$group": map[string]interface{}{
            "_id":          "$robot_id",
            "avg_pm_25":    map[string]interface{}{"$avg": "$data.readings.pm_2_5"},
            "sample_count": map[string]interface{}{"$sum": 1},
        },
    },
}

results, err := client.DataClient().TabularDataByMQL(
    context.Background(), orgID, pipeline, nil,
)
if err != nil {
    logger.Fatal(err)
}
fmt.Println(results)
```

{{% /tab %}}
{{< /tabs >}}

## SQL or MQL, when to use each

- **SQL** for simple selects, filters, and joins against captured tabular data. Familiar syntax, works well for dashboards that show raw or lightly filtered data.
- **MQL** for aggregation pipelines: averages, windowed sums, grouping across components, computing derived fields. Required for fleet-wide aggregations that SQL cannot express cleanly.

The two query languages run against the same underlying data. Pick the one that matches how you want to think about the query, not based on any performance difference.

## Refresh data on a timer

Dashboards typically refresh on a timer. Neither the TypeScript nor the Flutter SDK provides a subscription API for live data: you poll on a `setInterval` or `Timer.periodic` and update your UI when the results come back.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
const intervalId = setInterval(async () => {
  try {
    const rows = await client.dataClient.tabularDataBySQL(orgId, query);
    updateDashboard(rows);
  } catch (err) {
    console.error("Query failed:", err);
  }
}, 10_000);

// Later, when the component unmounts or the user navigates away:
clearInterval(intervalId);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
Timer.periodic(const Duration(seconds: 10), (timer) async {
  try {
    final rows = await viam.dataClient.tabularDataBySql(orgId, query);
    setState(() {
      _rows = rows;
    });
  } catch (e) {
    print('Query failed: $e');
  }
});
```

Cancel the timer in your `State.dispose()` method.

{{% /tab %}}
{{< /tabs >}}

Pick a refresh interval that balances UI freshness against query cost. Every query is a network round trip to the Viam cloud and a database query against your captured data. For a dashboard showing minute-scale aggregations, refresh every 10-30 seconds. For near-real-time displays, refresh every 1-5 seconds but expect higher data transfer.

## Query binary data

The same `DataClient` can filter binary data (images, point clouds) captured by the data manager. Use `binaryDataByFilter` with a filter specification:

```ts
const binaries = await client.dataClient.binaryDataByFilter({
  componentName: "front_camera",
  startTime: new Date("2026-04-01T00:00:00Z"),
  endTime: new Date("2026-04-02T00:00:00Z"),
  tags: ["training"],
});
```

Binary data responses include metadata and a URL to download the file. See the [Data API reference](/reference/apis/data-client/) for the full request shape.

## Next

- [Query data](/data/query-data/) for the SQL and MQL query languages, the schema, and operator reference
- [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/) for setting up the cloud connection that `dataClient` requires
- [Data API reference](/reference/apis/data-client/) for the full `DataClient` method list
