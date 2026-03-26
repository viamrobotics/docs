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
