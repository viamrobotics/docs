---
linkTitle: "Query data"
title: "Query data"
weight: 10
layout: "docs"
type: "docs"
description: "Write SQL and MQL queries against captured data in the Viam app or programmatically."
date: "2025-01-30"
aliases:
  - /data/query-data/
  - /build/data/query-data/
---

You can query captured tabular data (sensor readings, motor positions, encoder ticks, and other structured key-value data) using SQL or MQL: in the Viam app's query editor or programmatically through the SDK.

Binary data such as images and point clouds is stored separately and is not queryable through SQL/MQL.
To access binary data programmatically, use the [data client API](/reference/apis/services/data/).

## Open the query editor

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click **Query** to open the query editor.
4. Select **SQL** or **MQL** mode depending on which language you want to use.

**SQL** is good for straightforward filtering, sorting, and limiting.
**MQL** (MongoDB Query Language) uses aggregation pipelines and is more powerful for grouping, computing averages, and restructuring nested data.

By default, queries run against the `readings` collection in the `sensorData` database.
See [Readings table reference](#readings-table-reference) for the full schema.

## Explore your data with basic SQL

Start with a broad query to see what data you have:

```sql
SELECT time_received, component_name, component_type, data
FROM readings
ORDER BY time_received DESC
LIMIT 10
```

This shows the 10 most recent readings across all components.
Most of the interesting values are in the `data` column, which contains your actual readings as nested JSON.
For example, a sensor reading looks like `{"readings": {"temperature": 23.5, "humidity": 61.2}}`.
You'll use dot notation to extract specific fields: `data.readings.temperature`.
See [Readings table reference](#readings-table-reference) for the full schema and more examples.

To narrow to a specific component:

```sql
SELECT time_received, data
FROM readings
WHERE component_name = 'my-sensor'
ORDER BY time_received DESC
LIMIT 10
```

To filter by time range:

```sql
SELECT time_received, component_name, data
FROM readings
WHERE time_received > '2025-01-15T00:00:00Z'
  AND time_received < '2025-01-16T00:00:00Z'
ORDER BY time_received ASC
```

## Extract fields from nested JSON

The `data` column contains JSON, so you need JSON functions to extract specific
values. Use dot notation to reach into the nested structure:

```sql
SELECT
  time_received,
  data.readings.temperature AS temperature,
  data.readings.humidity AS humidity
FROM readings
WHERE component_name = 'my-sensor'
ORDER BY time_received DESC
LIMIT 20
```

For detection results from a vision service:

```sql
SELECT
  time_received,
  data.detections
FROM readings
WHERE component_name = 'my-detector'
  AND component_type = 'rdk:service:vision'
ORDER BY time_received DESC
LIMIT 10
```

To filter by a specific machine:

```sql
SELECT time_received, component_name, data
FROM readings
WHERE robot_id = 'YOUR-MACHINE-ID'
ORDER BY time_received DESC
LIMIT 10
```

## Write MQL aggregation pipelines

Switch to **MQL** mode in the query editor. MQL queries are JSON arrays where
each element is a pipeline stage.

Get the last 10 readings from a component:

```json
[
  { "$match": { "component_name": "my-sensor" } },
  { "$sort": { "time_received": -1 } },
  { "$limit": 10 },
  {
    "$project": {
      "time_received": 1,
      "data": 1,
      "_id": 0
    }
  }
]
```

Count readings per component:

```json
[
  {
    "$group": {
      "_id": "$component_name",
      "count": { "$sum": 1 }
    }
  },
  { "$sort": { "count": -1 } }
]
```

Count readings per component over a specific time window:

```json
[
  {
    "$match": {
      "time_received": {
        "$gte": { "$date": "2025-01-15T00:00:00Z" },
        "$lt": { "$date": "2025-01-16T00:00:00Z" }
      }
    }
  },
  {
    "$group": {
      "_id": "$component_name",
      "count": { "$sum": 1 }
    }
  },
  { "$sort": { "count": -1 } }
]
```

Compute average, min, and max of a sensor value:

```json
[
  { "$match": { "component_name": "my-sensor" } },
  {
    "$group": {
      "_id": null,
      "avg_temperature": { "$avg": "$data.readings.temperature" },
      "min_temperature": { "$min": "$data.readings.temperature" },
      "max_temperature": { "$max": "$data.readings.temperature" },
      "total_readings": { "$sum": 1 }
    }
  }
]
```

Group readings by hour to see trends over time:

```json
[
  { "$match": { "component_name": "my-sensor" } },
  {
    "$group": {
      "_id": {
        "$dateToString": {
          "format": "%Y-%m-%d %H:00",
          "date": "$time_received"
        }
      },
      "avg_temperature": { "$avg": "$data.readings.temperature" },
      "count": { "$sum": 1 }
    }
  },
  { "$sort": { "_id": 1 } }
]
```

Find all detections above a confidence threshold:

```json
[
  { "$match": { "component_name": "my-detector" } },
  { "$unwind": "$data.detections" },
  { "$match": { "data.detections.confidence": { "$gte": 0.9 } } },
  {
    "$project": {
      "time_received": 1,
      "class_name": "$data.detections.class_name",
      "confidence": "$data.detections.confidence",
      "_id": 0
    }
  },
  { "$sort": { "time_received": -1 } },
  { "$limit": 20 }
]
```

The `$unwind` stage is important when your data contains arrays. It flattens
the array so each element becomes its own document, which you can then filter
and project individually.

## Query data programmatically

You can run the same SQL and MQL queries from your own code using the data client API.
After [connecting to the Viam app](/dev/reference/apis/data-client/#establish-a-connection), use `tabular_data_by_sql` or `tabular_data_by_mql`:

{{< tabs >}}
{{% tab name="Python" %}}

```python
data_client = viam_client.data_client

# SQL query
sql_results = await data_client.tabular_data_by_sql(
    organization_id=ORG_ID,
    sql_query=(
        "SELECT time_received, "
        "  data.readings.temperature AS temperature "
        "FROM readings "
        "WHERE component_name = 'my-sensor' "
        "ORDER BY time_received DESC "
        "LIMIT 5"
    ),
)

# MQL aggregation pipeline
mql_results = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {"$group": {
            "_id": "$component_name",
            "count": {"$sum": 1},
        }},
        {"$sort": {"count": -1}},
    ],
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
dataClient := viamClient.DataClient()

// SQL query
sqlResults, err := dataClient.TabularDataBySQL(ctx, orgID,
    "SELECT time_received, "+
        "data.readings.temperature AS temperature "+
        "FROM readings "+
        "WHERE component_name = 'my-sensor' "+
        "ORDER BY time_received DESC LIMIT 5")

// MQL aggregation pipeline
mqlResults, err := dataClient.TabularDataByMQL(ctx, orgID,
    []map[string]interface{}{
        {"$group": map[string]interface{}{
            "_id":   "$component_name",
            "count": map[string]interface{}{"$sum": 1},
        }},
        {"$sort": map[string]interface{}{"count": -1}},
    }, nil)
```

{{% /tab %}}
{{< /tabs >}}

Find your organization ID in the Viam app under **Settings** in the left navigation.

If you need to export data for use outside of Viam: in a Jupyter notebook, your
own database, or a BI tool: see
[Sync data to your database](/data/export/sync-data-to-your-database/).

## Try it

To get oriented with your own data:

1. Open the query editor and run `SELECT DISTINCT component_name FROM readings` to see what components have captured data.
2. Pick a component and run `SELECT data FROM readings WHERE component_name = 'YOUR-COMPONENT' LIMIT 1` to see the JSON structure of its readings.
3. Use the field names from step 2 to write a query that extracts a specific value with dot notation (for example, `data.readings.temperature`).

## Readings table reference

All tabular data is stored in a single table called `readings` in the `sensorData` database.
Each row represents one capture event from one resource.

| Column                  | Type      | Description                                                         |
| ----------------------- | --------- | ------------------------------------------------------------------- |
| `organization_id`       | String    | Organization UUID                                                   |
| `location_id`           | String    | Location UUID                                                       |
| `robot_id`              | String    | Machine UUID                                                        |
| `part_id`               | String    | Machine part UUID                                                   |
| `component_type`        | String    | Resource type (for example, `rdk:component:sensor`)                 |
| `component_name`        | String    | Resource name (for example, `my-sensor`)                            |
| `method_name`           | String    | Capture method (for example, `Readings`, `EndPosition`)             |
| `time_requested`        | Timestamp | When the capture was requested on the machine                       |
| `time_received`         | Timestamp | When the cloud received the data                                    |
| `tags`                  | Array     | User-applied tags                                                   |
| `additional_parameters` | JSON      | Method-specific parameters (for example, `pin_name`, `reader_name`) |
| `data`                  | JSON      | The captured reading: nested structure varies by resource type      |

{{< alert title="Note" color="note" >}}
The `readings` table does not include `robot_name` or `part_name` columns. These fields appear in data export responses but are not part of the queryable schema. To filter by machine, use `robot_id` or `part_id`.
{{< /alert >}}

### The data column

The `data` column contains the actual reading as nested JSON. Its structure depends on what was captured:

{{< tabs >}}
{{% tab name="Sensor reading" %}}

```json
{
  "readings": {
    "temperature": 23.5,
    "humidity": 61.2
  }
}
```

{{% /tab %}}
{{% tab name="Vision service detection" %}}

```json
{
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.94,
      "x_min": 120,
      "y_min": 50,
      "x_max": 340,
      "y_max": 480
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Use dot notation in queries to reach into nested fields (for example, `data.readings.temperature`).

## Troubleshooting

{{< expand "Query returns empty results" >}}

- **Check the component name.** Component names are case-sensitive and must match
  exactly. Run `SELECT DISTINCT component_name FROM readings` to see all
  available component names.
- **Check the time range.** If you're filtering by time, make sure your range
  covers a period when data was actually captured. Remove the time filter first
  to confirm data exists, then add it back.
- **Verify data has synced.** Data must sync from the machine to the cloud before
  it is queryable. Check the **DATA** tab to confirm entries are visible.

{{< /expand >}}

{{< expand "Query returns data but fields are null" >}}

- **Check the JSON path.** The nested path must match the actual structure of
  your data. Run `SELECT data FROM readings LIMIT 1` to see the raw JSON, then
  build your dot-notation path to match. A common mistake is using
  `data.temperature` when the actual path is `data.readings.temperature`.

{{< /expand >}}

{{< expand "MQL pipeline returns unexpected results" >}}

- **Build incrementally.** Start with just the `$match` stage and verify it
  returns the documents you expect. Then add one stage at a time. This makes it
  easy to identify which stage is producing unexpected output.
- **Check field references.** In MQL, field references use `$` prefix
  (for example, `$component_name`, `$data.readings.temperature`). Missing the `$` is
  a common source of errors.

{{< /expand >}}

{{< expand "Query is slow" >}}

- **Add filters early.** Always include a `$match` stage (MQL) or `WHERE`
  clause (SQL) to narrow the data before doing expensive operations like
  grouping or sorting. Filtering by `component_name` and `time_received` is
  particularly effective.
- **Use LIMIT.** While developing queries, always include a `LIMIT` clause (SQL)
  or `$limit` stage (MQL) to avoid scanning your entire dataset.

{{< /expand >}}

{{< expand "Programmatic query fails with authentication error" >}}

- **Verify your API key and API key ID.** Both values are required and they
  serve different purposes. The API key is the secret; the API key ID identifies
  which key is being used.
- **Verify your organization ID.** Find it in the Viam app under **Settings** in
  the left navigation. It is a UUID, not your organization name.
- **Check that the API key has data access.** API keys can be scoped to specific
  resources. Ensure yours has access to the data service.

{{< /expand >}}

## What's next

- [Configure data pipelines](/data/query/configure-data-pipelines/): create precomputed summaries for faster queries.
- [Hot data store](/data/query/hot-data-store/): query a rolling window of recent data with lower latency.
- [Sync data to your database](/data/export/sync-data-to-your-database/): export data to your own MongoDB instance.
- [Visualize data](/data/visualize-data/): build dashboards from your captured data.
