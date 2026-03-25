---
linkTitle: "Advanced configuration"
title: "Advanced configuration"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "JSON-level configuration for retention policies, sync optimization, remote parts capture, and direct MongoDB capture."
aliases:
  - /data/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/
date: "2025-02-10"
updated: "2025-12-04"
---

Some data use cases require configuration beyond what the UI exposes.
You can switch to **JSON** mode in the Viam app to configure these attributes directly.

This page covers:

- [Data management service attributes](#data-management-service-attributes): sync threads, deletion thresholds, file size limits, MongoDB capture
- [Data capture attributes](#data-capture-attributes): per-resource capture methods, frequency, retention policies, hot data store
- [Remote parts capture](#remote-parts-capture): capture data from resources on remote parts
- [Direct MongoDB capture](#direct-mongodb-capture): write tabular data to MongoDB alongside disk capture

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
| Name               | Type   | Required? | Description | `viam-micro-server` Support |
| ------------------ | ------ | --------- | ----------- | ------------------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Even if capture is enabled for the whole part, data is only captured from components that have capture individually configured. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `capture_dir`      | string | Optional | Path to the directory where captured data is stored. If you change this, only new data goes to the new directory; existing data stays where it was. <br> Default: `~/.viam/capture` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `tags` | array of strings | Optional | Tags applied to all data captured by this machine part. May include alphanumeric characters, underscores, and dashes. |  |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` |  |
| `additional_sync_paths` | string array | Optional | Additional directories to sync to the cloud. Data is deleted from the directory after syncing. Use absolute paths. For help finding the default capture directory, see [Capture directories](/data/#capture-directories). |  |
| `sync_interval_mins` | float | Optional | Minutes between sync attempts. Your hardware or network speed may impose practical limits. <br> Default: `0.1` (every 6 seconds). |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `selective_syncer_name` | string | Optional | Name of the sensor that controls selective sync. Also add this sensor to the `depends_on` field. See [Conditional sync](/data/capture-sync/conditional-sync/#configure-the-data-manager-to-sync-based-on-sensor). |  |
| `delete_data_on_part_deletion` | bool | Optional | Whether deleting this {{< glossary_tooltip term_id="machine" text="machine" >}} or {{< glossary_tooltip term_id="part" text="machine part" >}} also deletes all its captured cloud data. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_every_nth_when_disk_full` | int | Optional | When local storage meets the [fullness criteria](/data/#automatic-data-deletion), the service deletes every Nth captured file. <br> Default: `5` |   |
| `maximum_num_sync_threads` | int | Optional | Max CPU threads for syncing to the cloud. Higher values may improve throughput but can cause instability on constrained devices. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2 |   |
| `mongo_capture_config.uri` | string | Optional | [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) for writing tabular data alongside disk capture. See [Direct MongoDB capture](#direct-mongodb-capture). |   |
| `mongo_capture_config.database` | string | Optional | Database name for MongoDB capture. <br> Default: `"sensorData"` |   |
| `mongo_capture_config.collection` | string | Optional | Collection name for MongoDB capture. <br> Default: `"readings"` |   |
| `maximum_capture_file_size_bytes` | int | Optional | Maximum size in bytes of each capture file on disk. When a capture file reaches this size, a new file is created. <br> Default: `262144` (256 KB) |   |
| `file_last_modified_millis` | float | Optional | How long (in ms) an arbitrary file must be unmodified before it is eligible for sync. Normal `.capture` files sync immediately. <br> Default: `10000` |   |
| `disk_usage_deletion_threshold` | float | Optional | Disk usage ratio (0–1) at or above which captured files are deleted, provided the capture directory also meets `capture_dir_deletion_threshold`. <br> Default: `0.9` |  |
| `capture_dir_deletion_threshold` | float | Optional | Ratio (0–1) of disk usage attributable to the capture directory, at or above which deletion occurs (if `disk_usage_deletion_threshold` is also met). <br> Default: `0.5` |   |

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
| `cache_size_kb` | float | Optional | `viam-micro-server` only. Max storage (KB) per data collector. <br> Default: `1` |

## Remote parts capture

You can capture data from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.
This is useful when a part lacks the OS or resources to run `viam-server`. You add it as a remote and capture its data from the main part.

Remote part capture is configured in JSON only.
Add a `service_config` with `type: data_manager` inside the `remote` object in the `remotes` array.
Each capture method object takes the following fields:

<!-- prettier-ignore -->
| Key | Type | Description |
| --- | ---- | ----------- |
| `name` | string | Fully qualified resource name. Example: `"rdk:component:sensor/spacesensor"`. |
| `method` | string | Depends on the component or service type. See [Supported resources](/data/#supported-resources). Individual tabular readings larger than 4&nbsp;MB are rejected at upload time. |
| `capture_frequency_hz` | float | Frequency in hertz. |
| `additional_params` | object | Method-specific parameters. |
| `disabled` | boolean | Whether capture is disabled for this method. |
| `cache_size_kb` | float | `viam-micro-server` only. Max storage (KB) per data collector. Default: `1`. |

{{< expand "Example: ESP32 remote part configuration" >}}

The following is the configuration for the ESP32 board itself (the remote part).
This config is the same as any non-remote part. The remote connection is established by the main part.

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-esp32",
      "model": "esp32",
      "api": "rdk:component:board",
      "attributes": {
        "pins": [27],
        "analogs": [
          {
            "pin": "34",
            "name": "A1"
          },
          {
            "pin": "35",
            "name": "A2"
          }
        ]
      },
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Analogs",
                "additional_params": {
                  "reader_name": "A1"
                },
                "cache_size_kb": 10,
                "capture_frequency_hz": 10
              },
              {
                "method": "Analogs",
                "additional_params": {
                  "reader_name": "A2"
                },
                "cache_size_kb": 10,
                "capture_frequency_hz": 10
              }
            ]
          }
        }
      ]
    }
  ]
}
```

{{< /expand >}}

{{< expand "Example: main part capturing from an ESP32 remote (analog readers and GPIO)" >}}

This main part configuration captures data from two analog readers and pin 27 of the GPIO on the ESP32 configured above:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": ["tag1", "tag2"]
      }
    }
  ],
  "remotes": [
    {
      "name": "esp-home",
      "address": "esp-home-main.33vvxnbbw9.viam.cloud:80",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Analogs",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A1" },
                "disabled": false
              },
              {
                "method": "Analogs",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A2" },
                "disabled": false
              },
              {
                "method": "Gpios",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": {
                  "pin_name": "27"
                },
                "disabled": false
              }
            ]
          }
        }
      ],
      "secret": "REDACTED"
    }
  ]
}
```

{{< /expand >}}

{{< expand "Example: main part capturing from a remote camera" >}}

This main part configuration captures from the `GetImages` method of a camera on a remote part:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": []
      }
    }
  ],
  "remotes": [
    {
      "name": "pi-test-main",
      "address": "pi-test-main.vw3iu72d8n.viam.cloud",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 1,
                "name": "rdk:component:camera/cam",
                "disabled": false,
                "method": "GetImages",
                "additional_params": {
                  "filter_source_names": ["color"],
                  "reader_name": "cam1"
                }
              }
            ]
          }
        }
      ],
      "secret": "REDACTED"
    }
  ]
}
```

{{< /expand >}}

## Direct MongoDB capture

You can write tabular data directly to a MongoDB instance alongside the normal disk capture.
This is useful for powering real-time dashboards before data syncs from the edge to the cloud.
The MongoDB instance can be local or a cloud cluster.

{{< alert title="Caution" color="caution" >}}

- Data written to MongoDB may not also make it to disk (and therefore may never sync to cloud storage).
- Failed MongoDB writes are logged but not retried. Not all captured data is guaranteed to reach MongoDB.
- The added write latency may reduce the maximum achievable capture frequency.

{{< /alert >}}

Configure using the `mongo_capture_config` attributes in your data management service.
MongoDB capture and cloud sync are independent. You can enable either or both.

{{< expand "Example: MongoDB capture with cloud sync" >}}

This configuration captures sensor readings to both a local MongoDB instance and disk, with cloud sync enabled:

```json
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
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "services": [
    {
      "name": "data_manager-1",
      "api": "rdk:service:data_manager",
      "attributes": {
        "mongo_capture_config": {
          "uri": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
        },
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "sync_disabled": false,
        "tags": []
      }
    }
  ]
}
```

To capture to MongoDB without cloud sync, set `"sync_disabled": true`.

{{< /expand >}}

If writes to MongoDB fail, data capture logs an error for each failed write and continues capturing.
MongoDB write failures do not prevent data from being captured to disk or synced to the cloud.
