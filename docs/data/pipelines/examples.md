---
linkTitle: "Examples and tips"
title: "Pipeline examples and MQL tips"
weight: 25
layout: "docs"
type: "docs"
description: "MQL patterns for common robotics use cases and tips for writing effective pipeline queries."
date: "2026-03-27"
---

MQL patterns for common robotics data pipeline use cases. Each example can be passed to `--mql` or `--mql-path` when [creating a pipeline](/data/pipelines/create-a-pipeline/).

## MQL tips

### Always rename `_id` in `$project`

The `$group` stage produces documents with an `_id` field. If your pipeline runs multiple times and produces documents with the same `_id`, you get a duplicate key error. Always follow `$group` with `$project` to rename `_id` and set it to 0:

```json
{ "$project": { "location": "$_id", "avg_temp": 1, "count": 1, "_id": 0 } }
```

### Test your query first

Before creating a pipeline, run the MQL query manually in the [query editor](/data/query-data/) using MQL mode. This lets you verify the query returns the results you expect. The pipeline runs the same query with an automatic time constraint prepended.

### Use `$match` early

Place `$match` stages at the beginning of your pipeline to reduce the amount of data processed by later stages. Filter by `component_name`, `component_type`, or other indexed fields for best performance. See [indexed fields](/data/reference/#indexed-fields-and-query-optimization).

## Downsample high-frequency sensor data

A sensor capturing at 10 Hz produces 36,000 readings per hour. This pipeline computes 1-minute averages, reducing the data to 60 summary documents per hour:

```json
[
  { "$match": { "component_name": "accel-sensor" } },
  {
    "$group": {
      "_id": {
        "$dateTrunc": {
          "date": "$time_received",
          "unit": "minute"
        }
      },
      "avg_x": { "$avg": "$data.readings.x" },
      "avg_y": { "$avg": "$data.readings.y" },
      "avg_z": { "$avg": "$data.readings.z" },
      "sample_count": { "$sum": 1 }
    }
  },
  {
    "$project": {
      "minute": "$_id",
      "avg_x": 1,
      "avg_y": 1,
      "avg_z": 1,
      "sample_count": 1,
      "_id": 0
    }
  },
  { "$sort": { "minute": 1 } }
]
```

## Count detection events per hour per machine

A vision service captures detection results. This pipeline counts how many detections of each class occurred per machine per hour:

```json
[
  { "$match": { "component_type": "rdk:service:vision" } },
  { "$unwind": "$data.detections" },
  {
    "$group": {
      "_id": {
        "machine": "$robot_id",
        "hour": {
          "$dateTrunc": {
            "date": "$time_received",
            "unit": "hour"
          }
        },
        "class": "$data.detections.class_name"
      },
      "count": { "$sum": 1 },
      "avg_confidence": { "$avg": "$data.detections.confidence" }
    }
  },
  {
    "$project": {
      "machine": "$_id.machine",
      "hour": "$_id.hour",
      "class": "$_id.class",
      "count": 1,
      "avg_confidence": { "$round": ["$avg_confidence", 2] },
      "_id": 0
    }
  }
]
```

## Compute derived metrics

A sensor reports voltage and current. This pipeline computes power (voltage \* current) and summarizes per hour:

```json
[
  { "$match": { "component_name": "power-monitor" } },
  {
    "$addFields": {
      "power_watts": {
        "$multiply": ["$data.readings.voltage", "$data.readings.current"]
      }
    }
  },
  {
    "$group": {
      "_id": {
        "$dateTrunc": {
          "date": "$time_received",
          "unit": "hour"
        }
      },
      "avg_power": { "$avg": "$power_watts" },
      "max_power": { "$max": "$power_watts" },
      "readings": { "$sum": 1 }
    }
  },
  {
    "$project": {
      "hour": "$_id",
      "avg_power_watts": { "$round": ["$avg_power", 2] },
      "max_power_watts": { "$round": ["$max_power", 2] },
      "readings": 1,
      "_id": 0
    }
  }
]
```

## Fleet-wide aggregation by location

Aggregate sensor readings across all machines at each location to compare performance across sites:

```json
[
  { "$match": { "component_name": "temperature-sensor" } },
  {
    "$group": {
      "_id": "$location_id",
      "avg_temp": { "$avg": "$data.readings.temperature" },
      "min_temp": { "$min": "$data.readings.temperature" },
      "max_temp": { "$max": "$data.readings.temperature" },
      "machine_count": { "$addToSet": "$robot_id" },
      "reading_count": { "$sum": 1 }
    }
  },
  {
    "$project": {
      "location": "$_id",
      "avg_temp": { "$round": ["$avg_temp", 1] },
      "min_temp": 1,
      "max_temp": 1,
      "machines_reporting": { "$size": "$machine_count" },
      "reading_count": 1,
      "_id": 0
    }
  }
]
```
