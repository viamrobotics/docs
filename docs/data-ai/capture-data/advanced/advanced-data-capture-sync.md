---
linkTitle: "Advanced data capture and sync configurations"
title: "Advanced data capture and sync configurations"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Advanced data capture and data sync configurations."
date: "2025-02-10"
updated: "2025-12-04"
---

Some data use cases require advanced configuration beyond the attributes accessible in the UI.
You can use raw JSON to configure additional attributes for both data management and data capture.
You can also configure data capture for remote parts.

## Cloud data retention

Configure how long your synced data remains stored in the cloud:

- **Retain data up to a certain size (for example, 100GB) or for a specific length of time (for example, 14 days):** Set `retention_policy` at the resource level.
  See the `retention_policy` field in [data capture configuration attributes](/data-ai/capture-data/advanced/advanced-data-capture-sync/#click-to-view-data-capture-attributes).
- **Delete data captured by a machine when you delete the machine:** Control whether your cloud data is deleted when a machine or machine part is removed.
  See the `delete_data_on_part_deletion` field in the [data management service configuration attributes](/data-ai/capture-data/advanced/advanced-data-capture-sync/#click-to-view-data-management-attributes).

## Sync optimization

**Configurable sync threads:** You can control how many concurrent sync operations occur by adjusting the `maximum_num_sync_threads` setting.
Higher values may improve throughput on more powerful hardware, but raising it too high may introduce instability on resource-constrained devices.

**Wait time before syncing arbitrary files:** If you choose to sync arbitrary files (beyond those captured by the data management service), the `file_last_modified_millis` configuration attribute specifies how long a file must remain unmodified before the data manager considers it for syncing.
The default is 10 seconds.

## Advanced data management service configuration

To configure the data manager in JSON, see the following example configurations:

{{< tabs >}}
{{% tab name="viam-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
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
  "components": [],
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

The following attributes are available for the data management service:

{{< expand "Click to view data management attributes" >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description | `viam-micro-server` Support |
| ------------------ | ------ | --------- | ----------- | ------------------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Note that even if capture is on for the whole part, if it is not on for any individual {{< glossary_tooltip term_id="component" text="component" >}}, data is not being captured. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `capture_dir`      | string | Optional | Path to the directory on your machine where you want to store captured data. If you change the directory for data capture, only new data is stored in the new directory. Existing data remains in the directory where it was stored. <br> Default: `~/.viam/capture` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `tags` | array of strings | Optional | Tags to apply to all images or tabular data captured by this machine part. May include alphanumeric characters, underscores, and dashes. |  |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` |  |
| `additional_sync_paths` | string array | Optional | Paths to any other directories on your machine from which you want to sync data to the cloud. Once data is synced from a directory, it is automatically deleted from your machine. We recommend using absolute paths. For relative paths, see [How sync works](/data-ai/capture-data/advanced/how-sync-works/#cant-find-the-directory-data-is-stored-in-click-here). |  |
| `sync_interval_mins` | float | Optional | Time interval in minutes between syncing to the cloud. Viam does not impose a minimum or maximum on the frequency of data syncing. However, in practice, your hardware or network speed may impose limits. <br> Default: `0.1`, meaning once every 6 seconds. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `selective_syncer_name` | string | Optional | The name for the sensor that should determine selective sync. Also add this sensor to the `depends_on` field. For more information, see [Configure the data manager to sync based on sensor](/data-ai/capture-data/conditional-sync/#configure-the-data-manager-to-sync-based-on-sensor). |  |
| `delete_data_on_part_deletion` | bool | Optional | Whether deleting this {{< glossary_tooltip term_id="machine" text="machine" >}} or {{< glossary_tooltip term_id="part" text="machine part" >}} should result in deleting all the data captured by that machine part. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_every_nth_when_disk_full` | int | Optional | How many files to delete when local storage meets the [fullness criteria](/data-ai/capture-data/advanced/how-sync-works/#storage). The data management service will delete every Nth file that has been captured upon reaching this threshold. Use JSON mode to configure this attribute. <br> Default: `5`, meaning that every fifth captured file will be deleted. |   |
| `maximum_num_sync_threads` | int | Optional | Max number of CPU threads to use for syncing data to the Viam Cloud. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2 so half the number of logical CPUs available to viam-server |   |
| `mongo_capture_config.uri` | string | Optional | The [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) to which data capture will attempt to write tabular data after it is enqueued to be written to disk. When non-empty, data capture will write tabular data to the configured MongoDB database and collection at that URI.<br>See `mongo_capture_config.database` and `mongo_capture_config.collection` below for database and collection defaults.<br>See [Capture directly to your own MongoDB cluster](/data-ai/capture-data/advanced/advanced-data-capture-sync/#capture-directly-to-your-own-mongodb-cluster) for example configurations.|   |
| `mongo_capture_config.database` | string | Optional | When `mongo_capture_config.uri` is non-empty, changes the database data capture will write tabular data to. <br> Default: `"sensorData"`   |   |
| `mongo_capture_config.collection` | string | Optional | When `mongo_capture_config.uri` is non-empty, changes the collection data capture will write tabular data to.<br> Default: `"readings"`   |   |
| `cache_size_kb` | float | Optional | `viam-micro-server` only. The maximum amount of storage (in kilobytes) allocated to a data collector. <br> Default: `1` KB. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `file_last_modified_millis` | float | Optional | The amount of time to pass since arbitrary files were last modified until they are synced. Normal <file>.capture</file> files are synced as soon as they are able to be synced. <br> Default: `10000` milliseconds. |   |
| `disk_usage_deletion_threshold` | float | Optional | The disk usage ratio at or above which files will be deleted if the capture directory makes up at least the specified `capture_dir_deletion_threshold` of the disk usage. If disk usage is at or above the disk usage threshold, but the capture directory is below the capture directory threshold, then file deletion will not occur but a warning will be logged periodically. Default: `0.9`. |  |
| `capture_dir_deletion_threshold` | float | Optional | The ratio of disk usage made up by the capture directory at or above which files will be deleted if the disk usage ratio is also above the `disk_usage_deletion_threshold`. If the ratio of disk usage of the capture directory is at or above the threshold but the disk usage is below the disk usage threshold, then file deletion will not occur but a warning will be logged periodically. Default: `0.5`. |   |

{{< /expand >}}

You can edit the JSON directly by switching to **JSON** mode in the UI.

## Advanced data capture configuration

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Part or sub-part" %}}

{{< tabs >}}
{{% tab name="viam-server" %}}

This example configuration captures data from the `GetImages` method of a camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    ...
    ,
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
  ],
  "remotes": [
    {
        ...
    }
  ],
  "components": [
        ...
    ,
    {
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
      "model": "webcam",
      "name": "cam",
      "api": "rdk:component:camera",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": [
        "local"
      ]
    },
    ...
  ]
}
```

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

This example configuration captures data from the `Readings` method of a temperature sensor and wifi signal sensor:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "attributes": {
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": [],
        "sync_interval_mins": 3
      },
      "name": "dm",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin"
    }
  ],
  "components": [
    {
      "api": "rdk:component:sensor",
      "model": "tmp36",
      "attributes": {
        "analog_reader": "temp",
        "num_readings": 15
      },
      "depends_on": [],
      "service_configs": [
        {
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 0.2,
                "cache_size_kb": 10,
                "additional_params": {},
                "method": "Readings"
              }
            ]
          },
          "type": "data_manager"
        }
      ],
      "name": "tmp36"
    },
    {
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
      ],
      "name": "my-wifi-sensor"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Example configuration for a vision service:

This example configuration captures data from the `CaptureAllFromCamera` method of the vision service:

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

The following attributes are available for data capture configuration:

{{< expand "Click to view data capture attributes" >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_frequency_hz` | float   | **Required** | Frequency in hertz at which to capture data. For example, to capture a reading every 2 seconds, enter `0.5`. |
| `method` | string | **Required** | Depends on the type of component or service. See [Supported components and services](/data-ai/capture-data/capture-sync/#click-to-see-resources-that-support-data-capture-and-cloud-sync). **Note:** For tabular data, Viam enforces a maximum size of 4MB for any single reading. |
| `retention_policy` | object | Optional | Option to configure how long data collected by this component or service should remain stored in the Viam Cloud. You must set this in JSON mode. See the JSON example for a camera component. <br> **Options:** `"days": <int>`, `"binary_limit_gb": <int>`, `"tabular_limit_gb": <int>`. <br> Days are in UTC time. Setting a retention policy of 1 day means that data stored now will be deleted the following day **in UTC time**. You can set either or both of the size limit options; size is in gigabytes. The `retention_policy` does not affect logs. For information about logs, see [Logging](/operate/reference/viam-server/#logging). |
| `recent_data_store` | object | Optional | Configure a rolling time frame of recent data to store in a [hot data store](/data-ai/data/hot-data-store/) for faster access. Example: `{ "stored_hours": 24 }` |
| `additional_params` | object | Optional | Varies based on the method. For example, `DoCommand` requires `docommand_input` with an object of the command object to pass to `DoCommand`, and `GetImages` can optionally intake a `filter_source_names` list of strings to indicate which source names to return images from. |
| `disabled` | boolean | Optional | Whether data capture is disabled. |

{{< /expand >}}

You can edit the JSON directly by switching to **JSON** mode in the UI.

{{% /tab %}}
{{% tab name="Remote parts" %}}

Viam supports data capture from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.
For example, if you use a {{< glossary_tooltip term_id="part" text="part" >}} that does not have a Linux operating system or does not have enough storage or processing power to run `viam-server`, you can still process and capture the data from that part's resources by adding it as a remote part.

Currently, you can only configure data capture from remote resources in your JSON configuration.
To add them to your JSON configuration, you must explicitly add a `service_config` for the data manager in the `remote` object in the `remotes` array.
The service config array must contain an object with `type: data_manager` and an `attributes` object with an array of `capture_methods`.
Each capture method object contains the following fields:

<!-- prettier-ignore -->
| Key | Type | Description |
| --- | ---- | ----------- |
| `name` | string | The name specifies the fully qualified name of the part. Example: `"rdk:component:sensor/spacesensor"`. |
| `additional_params` | Object | Varies based on the method. For example, `DoCommand` requires `docommand_input` with an object of the command object to pass to `DoCommand`, and `GetImages` can optionally intake a `filter_source_names` list of strings to indicate which source names to return images from. |
| `disabled` | boolean | Whether data capture for the method is disabled. |
| `method` | string | Depends on the type of component or service. See [Supported components and services](/data-ai/capture-data/capture-sync/#click-to-see-resources-that-support-data-capture-and-cloud-sync). **Note:** For tabular data, Viam enforces a maximum size of 4MB for any single reading. |
| `capture_frequency_hz` | float | Frequency in hertz at which to capture data. For example, to capture a reading every 2 seconds, enter `0.5`. |
| `cache_size_kb` | float | `viam-micro-server` only. The maximum amount of storage (in kilobytes) allocated to a data collector. <br> Default: `1` KB. |

{{< expand "Click to view example JSON configuration for an ESP32 board that will be established as a remote part" >}}

The following example shows the configuration of the part that we will establish as a remote, in this case an [ESP32 board](/operate/reference/components/board/esp32/).
This config is just like that of a non-remote part; the remote connection is established by the main part (in the next expandable example).

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

{{< expand "Click to view the JSON configuration for capturing data from two analog readers and a pin of the board's GPIO" >}}

The following example of a configuration with a remote part captures data from two analog readers that provide a voltage reading and from pin 27 of the GPIO of the board that we configured in the previous example:

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
  "components": [],
  "remotes": [
    {
      "name": "esp-home",
      "address": "esp-home-main.33vvxnbbw9.viam.cloud:80",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              // Captures data from two analog readers (A1 and A2)
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
              // Captures data from pin 27 of the board's GPIO
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

{{< expand "Click to view the JSON configuration for capturing data from a camera" >}}

The following example of a configuration with a remote part captures data from the `GetImages` method of a camera:

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
  "components": [],
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

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

## Capture directly to your own MongoDB cluster

You can configure direct capture of tabular data to a MongoDB instance alongside disk storage on your edge device.
This can be useful for powering real-time dashboards before data is synced from the edge to the cloud.
The MongoDB instance can be a locally running instance or a cluster in the cloud.

Configure using the `mongo_capture_config` attributes in your data manager service.
You can configure data sync to a MongoDB instance separately from data sync to the Viam Cloud.

{{< expand "Click to view sample configuration with MongoDB data store." >}}

This sample configuration captures fake sensor readings both to the configured MongoDB URI as well as to the `~/.viam/capture` directory on disk.
It does not sync the data to the Viam Cloud.

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
        }
      }
    }
  ]
}
```

{{< /expand >}}

{{< expand "Click to view sample configuration with MongoDB data store and sync to the Viam Cloud." >}}

This sample configuration captures fake sensor readings both to the configured MongoDB URI as well as to the `~/.viam/capture` directory on disk.
It syncs data to the Viam Cloud every 0.1 minutes.

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
        "additional_sync_paths": [],
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "capture_disabled": false,
        "sync_disabled": false,
        "tags": []
      }
    }
  ]
}
```

{{< /expand >}}

When `mongo_capture_config.uri` is configured, data capture will attempt to connect to the configured MongoDB server and write captured tabular data to the configured `mongo_capture_config.database` and `mongo_capture_config.collection` (or their defaults if unconfigured) after enqueuing that data to be written to disk.

If writes to MongoDB fail for any reason, data capture will log an error for each failed write and continue capturing.

Failing to write to MongoDB doesn't affect capturing and syncing data to cloud storage other than adding capture latency.

{{< alert title="Caution" color="caution" >}}

- Capturing directly to MongoDB may write data to MongoDB that later fails to be written to disk (and therefore never gets synced to cloud storage).
- Capturing directly to MongoDB does not retry failed writes to MongoDB. As a consequence, it is NOT guaranteed all data captured will be written to MongoDB.
  This can happen in cases such as MongoDB being inaccessible to `viam-server` or writes timing out.
- Capturing directly to MongoDB may reduce the maximum frequency that data capture can capture data due to the added latency of writing to MongoDB.
  If your use case needs to support very high capture rates, this feature may not be appropriate.

{{< /alert >}}
