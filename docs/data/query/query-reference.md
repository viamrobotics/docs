---
linkTitle: "Query reference"
title: "Query reference"
weight: 15
layout: "docs"
type: "docs"
aliases:
  - /data/query-reference/
  - /manage/data/query/
  - /use-cases/sensor-data-query/
  - /use-cases/sensor-data-query-with-third-party-tools/
  - /how-tos/sensor-data-query-with-third-party-tools/
  - /data-ai/data/query/
date: "2024-12-03"
updated: "2025-09-12"
description: "Schema, supported operators, SQL limitations, and query optimization for captured data."
---

For step-by-step instructions on querying data, see [Query data](/data/query/query-data/).

## Readings table schema

All tabular data is stored in a single table called `readings` in the `sensorData` database. Each row represents one capture event from one resource. Understanding this schema is essential for writing queries.

### What a document looks like

Here is a complete document from the `readings` collection. This is what you get back when you run `SELECT * FROM readings LIMIT 1`:

```json
{
  "organization_id": "ab1c2d3e-1234-5678-abcd-ef1234567890",
  "location_id": "loc-1234-5678-abcd-ef1234567890",
  "robot_id": "robot-1234-5678-abcd-ef1234567890",
  "part_id": "part-1234-5678-abcd-ef1234567890",
  "component_type": "rdk:component:sensor",
  "component_name": "my-sensor",
  "method_name": "Readings",
  "time_requested": "2025-03-15T14:30:00.000Z",
  "time_received": "2025-03-15T14:30:01.234Z",
  "tags": ["production", "floor-2"],
  "additional_parameters": {},
  "data": {
    "readings": {
      "temperature": 23.5,
      "humidity": 61.2
    }
  }
}
```

Your actual sensor values are inside the `data` column, nested under a key that depends on the component type and capture method. Everything outside of `data` is metadata that Viam adds automatically.

### Column reference

| Column                  | Type      | Description                                                                                                        |
| ----------------------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| `organization_id`       | String    | Organization UUID. Set automatically from your machine's config.                                                   |
| `location_id`           | String    | Location UUID. The location this machine belongs to.                                                               |
| `robot_id`              | String    | Machine UUID. Identifies which machine captured this data.                                                         |
| `part_id`               | String    | Machine part UUID. Identifies which part of the machine.                                                           |
| `component_type`        | String    | Resource type as a triplet (for example, `rdk:component:sensor`).                                                  |
| `component_name`        | String    | The name you gave this component in your config (for example, `my-sensor`). This is what you filter on most often. |
| `method_name`           | String    | The capture method (for example, `Readings`, `GetImages`, `EndPosition`).                                          |
| `time_requested`        | Timestamp | When the capture was requested on the machine (machine's clock).                                                   |
| `time_received`         | Timestamp | When the cloud received and stored the data. Use this for time-range queries since it's indexed.                   |
| `tags`                  | Array     | User-applied tags from your data management config.                                                                |
| `additional_parameters` | JSON      | Method-specific parameters you configured (for example, `pin_name`, `reader_name`).                                |
| `data`                  | JSON      | Your actual captured values. Structure varies by component type and method.                                        |

{{< alert title="Note" color="note" >}}
The `readings` table does not include `robot_name` or `part_name` columns. These fields appear in data export responses but are not part of the queryable schema. To filter by machine, use `robot_id` or `part_id`.
{{< /alert >}}

### The data column

The `data` column contains your actual captured values as nested JSON. Its structure depends on what component and method captured the data. To find out what's inside `data` for your specific components, run:

```sql
SELECT data FROM readings WHERE component_name = 'my-sensor' LIMIT 1
```

Then use the field names you see to build more specific queries.

**Common data structures:**

{{< tabs >}}
{{% tab name="Sensor (Readings)" %}}

Keys inside `data.readings` are whatever your sensor returns. Each sensor is different.

```json
{
  "readings": {
    "temperature": 23.5,
    "humidity": 61.2
  }
}
```

To query: `data.readings.temperature`

Example:

```sql
SELECT time_received,
  data.readings.temperature AS temp,
  data.readings.humidity AS humidity
FROM readings
WHERE component_name = 'my-sensor'
ORDER BY time_received DESC
LIMIT 10
```

{{% /tab %}}
{{% tab name="Vision service (CaptureAllFromCamera)" %}}

Detections include bounding box coordinates and confidence scores.

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

To query detections, use MQL since SQL cannot easily traverse arrays:

```json
[
  { "$match": { "component_name": "my-vision" } },
  { "$unwind": "$data.detections" },
  { "$match": { "data.detections.confidence": { "$gt": 0.8 } } },
  {
    "$project": {
      "class": "$data.detections.class_name",
      "confidence": "$data.detections.confidence",
      "time": "$time_received"
    }
  }
]
```

{{% /tab %}}
{{% tab name="Motor (Position)" %}}

```json
{
  "position": 145.7
}
```

To query: `data.position`

{{% /tab %}}
{{% tab name="Encoder (Position)" %}}

```json
{
  "position": 12450,
  "position_type": 1
}
```

To query: `data.position`

{{% /tab %}}
{{< /tabs >}}

### Finding the structure of your data

If you're unsure what fields your component produces, use this process:

1. Run `SELECT DISTINCT component_name FROM readings` to see what components have captured data.
2. Pick one and run `SELECT data FROM readings WHERE component_name = 'YOUR-COMPONENT' LIMIT 1`.
3. Look at the JSON structure in the result. The keys you see are the fields you can query with dot notation.
4. Build your query using `data.` followed by the path to the field you want (for example, `data.readings.temperature`).

## Indexed fields and query optimization

When querying large datasets, you can improve performance by filtering on indexed fields early in your query. Viam stores data in blob storage using the path pattern:

`/organization_id/location_id/robot_id/part_id/component_type/component_name/method_name/capture_day/*`

The more specific you can be, starting with the beginning of the path, the faster your query. These fields are indexed:

- `organization_id`
- `location_id`
- `robot_id`
- `part_id`
- `component_type`
- `component_name`
- `method_name`
- `capture_day`

Additional optimization techniques:

- Filter and reduce data early. Use `$match` (MQL) or `WHERE` (SQL) before expensive operations like grouping or sorting.
- Use `$project` early to drop unneeded fields from the processing pipeline.
- Use `$limit` or `LIMIT` while developing queries to avoid scanning your entire dataset.
- For frequent queries on recent data, use the [hot data store](/data/query/hot-data-store/).
- For recurring queries (dashboards), use [data pipelines](/data/query/configure-data-pipelines/) to pre-compute materialized views.

## Supported MQL operators

Viam supports the following MongoDB aggregation pipeline stages:

- `$addFields`
- `$bucket`
- `$bucketAuto`
- `$count`
- `$densify`
- `$fill`
- `$geoNear`
- `$group`
- `$limit`
- `$match`
- `$project`
- `$redact`
- `$replaceRoot`
- `$replaceWith`
- `$sample`
- `$set`
- `$setWindowFields`
- `$skip`
- `$sort`
- `$sortByCount`
- `$unset`
- `$unwind`

See the [MQL documentation](https://www.mongodb.com/docs/manual/tutorial/query-documents/) for syntax details.

## SQL limitations

Viam supports the [MongoDB Atlas SQL dialect](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations):

- If a database, table, or column identifier begins with a digit, a reserved character, or conflicts with a reserved SQL keyword, surround it with backticks (`` ` ``) or double quotes (`"`).
- To include a single quote in a string literal, use two single quotes (use `o''clock` to represent `o'clock`).
- The `date` data type is not supported. Use `timestamp` instead.

For a full list of limitations, see the [MongoDB Atlas SQL Interface Language Reference](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations).

## Date queries

When using MQL to query by date or time range, use the BSON `date` type directly rather than the `$toDate` expression for better performance:

```mongodb
use sensorData

const startTime = new Date('2024-02-10T19:45:07.000Z')
const endTime = new Date()

db.readings.aggregate([
    { $match: {
        time_received: {
            $gte: startTime,
            $lte: endTime
        }
    }}
])
```

## Permissions

Users with owner or operator roles at the organization, location, or machine level can query data. See [Role-Based Access Control](/organization/rbac/) for details.
