---
linkTitle: "Captured data schema"
title: "Captured data schema"
weight: 19
layout: "docs"
type: "docs"
description: "Structure of captured tabular data: document format, column reference, the data column, and common per-component data structures."
date: "2025-02-10"
---

Captured tabular data (sensor readings, motor positions, encoder ticks, and other structured key-value data) is stored in a single table called `readings` in the `sensorData` database. Each row represents one capture event from one resource. This page describes the structure of that table and the nested `data` column.

For query syntax, optimization tips, and supported operators, see [Data reference](/data/reference/).

## What a document looks like

Here is a complete document:

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

## Column reference

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

## The data column

The `data` column contains your actual captured values as nested JSON. Its structure depends on what component and method captured the data. To find out what's inside `data` for your specific components, run:

```sql
SELECT data FROM readings
WHERE component_name = 'my-sensor'
  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
LIMIT 1
```

Then use the field names you see to build more specific queries.

{{< alert title="Known issue: SQL queries need an explicit lower time bound" color="caution" >}}
SQL queries against `readings` currently return no rows unless the `WHERE` clause includes an explicit lower bound on `time_received`. Include `AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)` in any SQL example on this page if you copy it. MQL queries are not affected. Tracked as APP-10891.
{{< /alert >}}

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
  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
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

## Finding the structure of your data

If you're unsure what fields your component produces:

1. Run the following to see what components have captured data:

   ```sql
   SELECT DISTINCT component_name FROM readings
   WHERE time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
   ```

2. Pick one and run the following:

   ```sql
   SELECT data FROM readings
   WHERE component_name = 'YOUR-COMPONENT'
     AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
   LIMIT 1
   ```

3. Look at the JSON structure in the result. The keys you see are the fields you can query with dot notation.
4. Build your query using `data.` followed by the path to the field you want (for example, `data.readings.temperature`).
