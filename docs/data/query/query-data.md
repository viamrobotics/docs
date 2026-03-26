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

Explore and analyze your captured data using SQL or MQL queries. You can run queries interactively in the Viam app's query editor or programmatically through the SDK for ad-hoc analysis, building dashboards, or integrating with your own tools.

Tabular data (sensor readings, motor positions, encoder ticks, and other structured key-value data) is queryable through SQL and MQL. Binary data (images, point clouds) is stored separately and accessible through the [data client API](/dev/reference/apis/data-client/).

## Open the query editor

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click **Query** to open the query editor.
4. Select **SQL** or **MQL** mode depending on which language you want to use.

**SQL** is good for straightforward filtering, sorting, and limiting.
**MQL** (MongoDB Query Language) uses aggregation pipelines and is more powerful for grouping, computing averages, and restructuring nested data.

By default, queries run against the `readings` collection in the `sensorData` database.
See [Query reference](/data/reference/#readings-table-schema) for the full schema.

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

To see the structure of your data, run this query for a specific component:

```sql
SELECT data FROM readings WHERE component_name = 'my-sensor' LIMIT 1
```

Switch to **table view** (the table icon in the results area) to see nested fields automatically flattened into dot-notation column headers like `data.readings.temperature`. These dot-notation paths are exactly what you use in your queries to extract specific values.

For the full schema and per-component examples, see the [readings table schema](/data/reference/#readings-table-schema).

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

## Query from code

You can run the same SQL and MQL queries from Python or Go using the data client API. See [Query data from code](/data/query/query-data-from-code/) for setup instructions and examples.

## Try it

To get oriented with your own data:

1. Open the query editor and run `SELECT DISTINCT component_name FROM readings` to see what components have captured data.
2. Pick a component and run `SELECT data FROM readings WHERE component_name = 'YOUR-COMPONENT' LIMIT 1` to see the JSON structure of its readings.
3. Use the field names from step 2 to write a query that extracts a specific value with dot notation (for example, `data.readings.temperature`).

For the full schema of the readings table, see [Query reference](/data/reference/#readings-table-schema).

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
- [Sync data to your database](/data/sync-data-to-your-database/): export data to your own MongoDB instance.
- [Visualize data](/data/visualize-data/): build dashboards from your captured data.
