---
linkTitle: "Data capture reference"
title: "Data capture reference"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Configuration reference for data management service attributes, capture methods, supported resources, and storage behavior."
aliases:
  - /data/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/
date: "2025-02-10"
updated: "2025-12-04"
---

## Data management service attributes

The data management service controls sync behavior, storage paths, and deletion policies.

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
        "delete_data_on_part_deletion": true,
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
| `additional_sync_paths`           | string array     | Optional  | Additional directories to sync to the cloud. Data is deleted from the directory after syncing. Use absolute paths. For help finding the default capture directory, see [Capture directories](/data/#capture-directories).                                       |                                                                     |
| `sync_interval_mins`              | float            | Optional  | Minutes between sync attempts. Your hardware or network speed may impose practical limits. <br> Default: `0.1` (every 6 seconds).                                                                                                                               | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `selective_syncer_name`           | string           | Optional  | Name of the sensor that controls selective sync. Also add this sensor to the `depends_on` field. See [Conditional sync](/data/capture-sync/conditional-sync/#configure-the-data-manager-to-sync-based-on-sensor).                                               |                                                                     |
| `delete_data_on_part_deletion`    | bool             | Optional  | Whether deleting this {{< glossary_tooltip term_id="machine" text="machine" >}} or {{< glossary_tooltip term_id="part" text="machine part" >}} also deletes all its captured cloud data. <br> Default: `false`                                                  | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_every_nth_when_disk_full` | int              | Optional  | When local storage meets the [fullness criteria](/data/#automatic-data-deletion), the service deletes every Nth captured file. <br> Default: `5`                                                                                                                |                                                                     |
| `maximum_num_sync_threads`        | int              | Optional  | Max CPU threads for syncing to the cloud. Higher values may improve throughput but can cause instability on constrained devices. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2                                                            |                                                                     |
| `mongo_capture_config.uri`        | string           | Optional  | [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) for writing tabular data alongside disk capture. See [Direct MongoDB capture](/data/capture-sync/direct-mongodb-capture/).                                                                           |                                                                     |
| `mongo_capture_config.database`   | string           | Optional  | Database name for MongoDB capture. <br> Default: `"sensorData"`                                                                                                                                                                                                 |                                                                     |
| `mongo_capture_config.collection` | string           | Optional  | Collection name for MongoDB capture. <br> Default: `"readings"`                                                                                                                                                                                                 |                                                                     |
| `maximum_capture_file_size_bytes` | int              | Optional  | Maximum size in bytes of each capture file on disk. When a capture file reaches this size, a new file is created. <br> Default: `262144` (256 KB)                                                                                                               |                                                                     |
| `file_last_modified_millis`       | int              | Optional  | How long (in ms) an arbitrary file must be unmodified before it is eligible for sync. Normal `.capture` files sync immediately. <br> Default: `10000`                                                                                                           |                                                                     |
| `disk_usage_deletion_threshold`   | float            | Optional  | Disk usage ratio (0–1) at or above which captured files are deleted, provided the capture directory also meets `capture_dir_deletion_threshold`. <br> Default: `0.9`                                                                                            |                                                                     |
| `capture_dir_deletion_threshold`  | float            | Optional  | Ratio (0–1) of disk usage attributable to the capture directory, at or above which deletion occurs (if `disk_usage_deletion_threshold` is also met). <br> Default: `0.5`                                                                                        |                                                                     |

## Data capture attributes

Data capture is configured per-resource in the `service_configs` array of a component or service.

{{< alert title="Caution" color="caution" >}}
Avoid configuring capture rates higher than your hardware can handle. This leads to performance degradation.
{{< /alert >}}

{{< tabs >}}
{{% tab name="viam-server" %}}

This example captures from the `GetImages` method of a camera with a 5-day retention policy:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "cam",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 0.333,
                "disabled": false,
                "method": "GetImages",
                "additional_params": {
                  "reader_name": "cam1"
                }
              }
            ],
            "retention_policy": {
              "days": 5
            }
          }
        }
      ],
      "depends_on": ["local"]
    }
  ],
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "sync_interval_mins": 5,
        "capture_dir": "",
        "sync_disabled": false,
        "tags": []
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

This example captures from the `Readings` method of a temperature sensor and a wifi signal sensor:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "tmp36",
      "api": "rdk:component:sensor",
      "model": "tmp36",
      "attributes": {
        "analog_reader": "temp",
        "num_readings": 15
      },
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 0.2,
                "cache_size_kb": 10,
                "additional_params": {},
                "method": "Readings"
              }
            ]
          }
        }
      ]
    },
    {
      "name": "my-wifi-sensor",
      "api": "rdk:component:sensor",
      "model": "wifi-rssi",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "additional_params": {},
                "method": "Readings",
                "capture_frequency_hz": 0.1,
                "cache_size_kb": 10
              }
            ]
          }
        }
      ]
    }
  ],
  "services": [
    {
      "name": "dm",
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
{{% tab name="Vision service" %}}

This example captures from the `CaptureAllFromCamera` method of a vision service, filtering detections with a minimum confidence of 0.7:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "camera-1",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {}
    }
  ],
  "services": [
    {
      "name": "vision-1",
      "api": "rdk:service:vision",
      "model": "mlmodel",
      "attributes": {
        "mlmodel_name": "my_mlmodel_service",
        "camera_name": "camera-1"
      },
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "CaptureAllFromCamera",
                "capture_frequency_hz": 1,
                "additional_params": {
                  "mime_type": "image/jpeg",
                  "camera_name": "camera-1",
                  "min_confidence_score": "0.7"
                }
              }
            ]
          }
        }
      ]
    },
    {
      "name": "data_manager-1",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": []
      }
    },
    {
      "name": "mlmodel-1",
      "api": "rdk:service:mlmodel",
      "model": "viam:mlmodel-tflite:tflite_cpu",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_tflite_cpu",
      "module_id": "viam:tflite_cpu",
      "version": "0.0.3"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_frequency_hz` | float   | **Required** | Frequency in hertz. For example, `0.5` = one reading every 2 seconds. |
| `method` | string | **Required** | Depends on the component or service type. See [Supported resources](/data/#supported-resources). Individual tabular readings larger than 4&nbsp;MB are rejected at upload time and will not sync to the cloud. |
| `retention_policy` | object | Optional | How long captured data is retained in the cloud. Processed by the Viam cloud platform. Options: `"days": <int>`, `"binary_limit_gb": <int>`, `"tabular_limit_gb": <int>`. Days are in UTC: a 1-day policy means data is deleted the following day in UTC. You can set size limits for binary, tabular, or both. Does not affect logs (see [Logging](/reference/platform/viam-server/#logging)). |
| `recent_data_store` | object | Optional | Store a rolling window of recent data in a [hot data store](/data/query/hot-data-store/) for faster queries. Example: `{ "stored_hours": 24 }` |
| `additional_params` | object | Optional | Method-specific parameters. For example, `DoCommand` requires a `docommand_input` object; `GetImages` accepts a `filter_source_names` list. |
| `disabled` | boolean | Optional | Whether capture is disabled for this method. |
| `tags` | array of strings | Optional | Tags applied to data captured by this specific method. These are added alongside any tags set at the service level. |
| `capture_directory` | string | Optional | Override the capture directory for this specific resource. If not set, uses the service-level `capture_dir`. |
| `capture_queue_size` | int | Optional | Size of the buffer between the capture goroutine and the file writer. <br> Default: `250` |
| `capture_buffer_size` | int | Optional | Size in bytes of the buffer used when writing captured data to disk. <br> Default: `4096` |
| `cache_size_kb` | float | Optional | `viam-micro-server` only. Max storage (KB) per data collector. <br> Default: `1` |

For remote parts capture, see [Capture from remote parts](/data/capture-sync/remote-parts-capture/). For direct MongoDB capture, see [Direct MongoDB capture](/data/capture-sync/direct-mongodb-capture/).

## Supported resources

The following components and services support data capture and cloud sync.
Not all models support all methods. For example, webcams do not capture point clouds.

{{< readfile "/static/include/data/capture-supported.md" >}}

## Capture directories

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

## Local storage and automatic deletion

After data syncs successfully, it is automatically deleted from local storage.
While a machine is offline, captured data accumulates locally.
Make sure your machine has enough storage to buffer data during expected offline periods.

{{< alert title="Warning" color="warning" >}}
If your machine is offline and its disk fills up, the data management service will delete captured data to free space and keep the machine running.
{{< /alert >}}

Automatic deletion triggers when _all_ of these conditions are met:

- Data capture is enabled
- Local disk usage is at or above the `disk_usage_deletion_threshold` (default: 90%)
- The capture directory accounts for at least the `capture_dir_deletion_threshold` proportion of disk usage (default: 50%)

Control deletion behavior with the `delete_every_nth_when_disk_full` attribute. If your machine captures a large amount of data or frequently goes offline, consider pointing `capture_dir` to a larger, dedicated storage device.

## Micro-RDK

The micro-RDK (for ESP32 and similar microcontrollers) supports data capture with a limited set of resources.
See the **Micro-RDK** tab in the supported resources table above for details.

On micro-RDK devices, captured data is stored in the ESP32's flash memory until it is uploaded to the cloud.
If the machine restarts before all data is synced, unsynced data since the last sync point is lost.
