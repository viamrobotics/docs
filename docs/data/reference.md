---
linkTitle: "Reference"
title: "Data management reference"
weight: 999
layout: "docs"
type: "docs"
description: "Data schema, query operators, configuration fields, supported resources, and storage behavior."
aliases:
  - /data/query-reference/
  - /manage/data/query/
  - /use-cases/sensor-data-query/
  - /use-cases/sensor-data-query-with-third-party-tools/
  - /how-tos/sensor-data-query-with-third-party-tools/
  - /data-ai/data/query/
  - /data/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/
  - /data/query/query-reference/
  - /data/capture-sync/advanced-data-capture-sync/
date: "2025-02-10"
---

## Data schema and querying

This section describes the structure of captured data and how to query it effectively.

### What a document looks like

All tabular data is stored in a single table called `readings` in the `sensorData` database. Each row represents one capture event from one resource. Here is a complete document:

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

If you're unsure what fields your component produces:

1. Run `SELECT DISTINCT component_name FROM readings` to see what components have captured data.
2. Pick one and run `SELECT data FROM readings WHERE component_name = 'YOUR-COMPONENT' LIMIT 1`.
3. Look at the JSON structure in the result. The keys you see are the fields you can query with dot notation.
4. Build your query using `data.` followed by the path to the field you want (for example, `data.readings.temperature`).

### Indexed fields and query optimization

You can improve query performance by filtering on indexed fields early in your query. Viam stores data in blob storage using the path pattern:

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
- For frequent queries on recent data, use the [hot data store](/data/hot-data-store/).
- For recurring queries (dashboards), use [data pipelines](/data/pipelines/create-a-pipeline/) to pre-compute materialized views.

### Supported MQL operators

Viam supports a subset of MongoDB aggregation pipeline stages. Operators not on this list will return an error.

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

### SQL limitations

Viam supports the [MongoDB Atlas SQL dialect](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations):

- If a database, table, or column identifier begins with a digit, a reserved character, or conflicts with a reserved SQL keyword, surround it with backticks (`` ` ``) or double quotes (`"`).
- To include a single quote in a string literal, use two single quotes (use `o''clock` to represent `o'clock`).
- The `date` data type is not supported. Use `timestamp` instead.

For a full list of limitations, see the [MongoDB Atlas SQL Interface Language Reference](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations).

### Date queries

MQL time-range queries perform better with the BSON `date` type than with `$toDate`. Use JavaScript `Date()` constructors in `mongosh`:

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

### Permissions

Users with owner or operator roles at the organization, location, or machine level can query data. See [Role-Based Access Control](/organization/rbac/) for details.

## Capture and sync configuration

This section describes the configuration fields for data capture and cloud sync.

### Data management service attributes

The data management service controls sync behavior, storage paths, and deletion policies. Most of these settings are configured through the Viam app UI. Edit JSON directly for settings not exposed in the UI, such as deletion thresholds, sync thread limits, and MongoDB capture.

{{< tabs >}}
{{% tab name="viam-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "my-data-manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "sync_interval_mins": 1,
        "capture_dir": "",
        "tags": [],
        "capture_disabled": false,
        "sync_disabled": true,
        "delete_every_nth_when_disk_full": 5,
        "maximum_num_sync_threads": 250
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "my-data-manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": [],
        "sync_interval_mins": 3
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

<!-- prettier-ignore -->
<!-- markdownlint-disable MD060 -->

| Name                              | Type             | Required? | Description                                                                                                                                                                                                                                                     | `viam-micro-server` Support                                         |
| --------------------------------- | ---------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `capture_disabled`                | bool             | Optional  | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Even if capture is enabled for the whole part, data is only captured from components that have capture individually configured. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `capture_dir`                     | string           | Optional  | Path to the directory where captured data is stored. If you change this, only new data goes to the new directory; existing data stays where it was. <br> Default: `~/.viam/capture`                                                                             | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `tags`                            | array of strings | Optional  | Tags applied to all data captured by this machine part. May include alphanumeric characters, underscores, and dashes.                                                                                                                                           |                                                                     |
| `sync_disabled`                   | bool             | Optional  | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false`                                                                                                                                   |                                                                     |
| `additional_sync_paths`           | string array     | Optional  | Additional directories to sync to the cloud. Data is deleted from the directory after syncing. Use absolute paths.                                                                                                                                              |                                                                     |
| `sync_interval_mins`              | float            | Optional  | Minutes between sync attempts. Your hardware or network speed may impose practical limits. <br> Default: `0.1` (every 6 seconds).                                                                                                                               | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `selective_syncer_name`           | string           | Optional  | Name of the sensor that controls selective sync. Also add this sensor to the `depends_on` field. See [Conditional sync](/data/capture-sync/conditional-sync/).                                                                                                  |                                                                     |
| `delete_every_nth_when_disk_full` | int              | Optional  | When local storage meets the fullness criteria, the service deletes every Nth captured file. <br> Default: `5`                                                                                                                                                  |                                                                     |
| `maximum_num_sync_threads`        | int              | Optional  | Max CPU threads for syncing to the cloud. Higher values may improve throughput but can cause instability on constrained devices. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2                                                            |                                                                     |
| `mongo_capture_config.uri`        | string           | Optional  | [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) for writing tabular data alongside disk capture. See [Direct MongoDB capture](/data/capture-sync/direct-mongodb-capture/).                                                        |                                                                     |
| `mongo_capture_config.database`   | string           | Optional  | Database name for MongoDB capture. <br> Default: `"sensorData"`                                                                                                                                                                                                 |                                                                     |
| `mongo_capture_config.collection` | string           | Optional  | Collection name for MongoDB capture. <br> Default: `"readings"`                                                                                                                                                                                                 |                                                                     |
| `maximum_capture_file_size_bytes` | int              | Optional  | Maximum size in bytes of each capture file on disk. When a capture file reaches this size, a new file is created. <br> Default: `262144` (256 KB)                                                                                                               |                                                                     |
| `file_last_modified_millis`       | int              | Optional  | How long (in ms) an arbitrary file must be unmodified before it is eligible for sync. Normal `.capture` files sync immediately. <br> Default: `10000`                                                                                                           |                                                                     |
| `disk_usage_deletion_threshold`   | float            | Optional  | Disk usage ratio (0-1) at or above which captured files are deleted, provided the capture directory also meets `capture_dir_deletion_threshold`. <br> Default: `0.9`                                                                                            |                                                                     |
| `capture_dir_deletion_threshold`  | float            | Optional  | Ratio (0-1) of disk usage attributable to the capture directory, at or above which deletion occurs (if `disk_usage_deletion_threshold` is also met). <br> Default: `0.5`                                                                                        |                                                                     |

#### Platform-managed service settings

The following settings appear in your machine's configuration but are not processed by `viam-server` on your machine. They are read and enforced by the Viam cloud platform:

| Name | Type | Description |
| --- | --- | --- |
| `delete_data_on_part_deletion` | bool | Whether deleting this machine or machine part also deletes all its captured cloud data. Default: `false`. |

### Data capture method attributes

Data capture is configured per-resource in the `service_configs` array of a component or service. When you configure capture through the Viam app UI, these fields are set automatically. The table below is the JSON-level reference for manual configuration.

{{< alert title="Caution" color="caution" >}}
Avoid configuring capture rates higher than your hardware can handle. This leads to performance degradation.
{{< /alert >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `name` | string | **Required** | Fully qualified resource name (for example, `rdk:component:sensor/my-sensor`). |
| `method` | string | **Required** | Depends on the component or service type. See [Supported resources](#supported-resources). Individual tabular readings larger than 4&nbsp;MB are rejected at upload time and will not sync to the cloud. |
| `capture_frequency_hz` | float   | **Required** | Frequency in hertz. For example, `0.5` = one reading every 2 seconds. |
| `additional_params` | object | Optional | Method-specific parameters. For example, `DoCommand` requires a `docommand_input` object; `GetImages` accepts a `filter_source_names` list. |
| `disabled` | boolean | Optional | Whether capture is disabled for this method. |
| `tags` | array of strings | Optional | Tags applied to data captured by this specific method. Added alongside any tags set at the service level. |
| `capture_directory` | string | Optional | Override the capture directory for this specific resource. If not set, uses the service-level `capture_dir`. |
| `capture_queue_size` | int | Optional | Size of the buffer between the capture goroutine and the file writer. <br> Default: `250` |
| `capture_buffer_size` | int | Optional | Size in bytes of the buffer used when writing captured data to disk. <br> Default: `4096` |
| `cache_size_kb` | float | Optional | `viam-micro-server` only. Max storage (KB) per data collector. <br> Default: `1` |

#### Platform-managed capture settings

The following capture method settings are processed by the Viam cloud platform, not by `viam-server`:

<!-- prettier-ignore -->
| Name | Type | Description |
| --- | --- | --- |
| `retention_policy` | object | How long captured data is retained in the cloud. Options: `"days": <int>`, `"binary_limit_gb": <int>`, `"tabular_limit_gb": <int>`. Days are in UTC. |
| `recent_data_store` | object | Store a rolling window of recent data in a [hot data store](/data/hot-data-store/) for faster queries. Example: `{ "stored_hours": 24 }` |

For remote parts capture, see [Capture from remote parts](/data/capture-sync/remote-parts-capture/). For direct MongoDB capture, see [Direct MongoDB capture](/data/capture-sync/direct-mongodb-capture/).

### Supported resources

The following components and services support data capture and cloud sync. The table shows which capture methods are available for each resource type. Not all models support all methods listed for their type.

{{< readfile "/static/include/data/capture-supported.md" >}}

## Local storage

This section describes how captured data is stored on the machine before syncing.

### Capture directories

By default, captured data is stored in `~/.viam/capture`.
The actual path depends on your platform:

<!-- prettier-ignore -->
| Platform | Default directory |
| -------- | ----------------- |
| Windows | With `viam-agent`: <FILE>C:\Windows\system32\config\systemprofile\.viam\capture</FILE>. Manual installation: <FILE>C:\Users\admin\.viam\capture</FILE>. |
| Linux | With root or sudo: <FILE>/root/.viam/capture</FILE>. |
| macOS | <FILE>/Users/\<username\>/.viam/capture</FILE>. |

{{% expand "Can't find the capture directory?" %}}

The path depends on where `viam-server` runs and the operating system.
Check your machine's startup logs for the `$HOME` value:

```sh
2025-01-15T14:27:26.073Z    INFO    rdk    server/entrypoint.go:77    Starting viam-server with following environment variables    {"HOME":"/home/johnsmith"}
```

{{% /expand%}}

You can change the capture directory with the `capture_dir` attribute in the [data management service attributes](#data-management-service-attributes).

### Automatic deletion

After data syncs successfully, it is automatically deleted from local storage.
While a machine is offline, captured data accumulates locally.

{{< alert title="Warning" color="warning" >}}
If your machine is offline and its disk fills up, the data management service will delete captured data to free space and keep the machine running.
{{< /alert >}}

Automatic deletion triggers when _all_ of these conditions are met:

- Data capture is enabled
- Local disk usage is at or above the `disk_usage_deletion_threshold` (default: 90%)
- The capture directory accounts for at least the `capture_dir_deletion_threshold` proportion of disk usage (default: 50%)

Control deletion behavior with the `delete_every_nth_when_disk_full` attribute.

### Micro-RDK

The micro-RDK (for ESP32 and similar microcontrollers) supports data capture with a smaller set of resources than `viam-server`. See the **Micro-RDK** tab in the [supported resources table](#supported-resources) for the specific methods available.

On micro-RDK devices, captured data is stored in the ESP32's flash memory until it is uploaded to the cloud. If the machine restarts before all data is synced, unsynced data since the last sync point is lost.
