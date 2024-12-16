---
title: "Data Management Service"
linkTitle: "Data Management Service"
description: "Configure the data management service to capture data from your components and services and sync it to the cloud."
weight: 10
type: "docs"
tags: ["data management", "cloud", "sync", "capture"]
icon: true
images: ["/services/icons/data-capture.svg"]
no_list: true
aliases:
  - /services/data/capture/
  - /data/capture/
  - /build/micro-rdk/data_management/
  - /services/data/capture/
  - /services/data/cloud-sync/
  - /data/cloud-sync/
  - /services/data/capture-sync/
no_service: true
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The data management service captures data from one or more {{< glossary_tooltip term_id="resource" text="resources" >}} locally, and syncs it to cloud storage when a connection to the cloud is available.
You can configure which data you want to capture, as well as the capture rate and the sync frequency.

{{< tabs >}}
{{% tab name="viam-server" %}}

The data is captured locally on the machine's storage and, by default, stored in the `~/.viam/capture` directory.

If a machine restarts for any reason, capture automatically resumes and any data from already stored but not yet synced is synced.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.
Avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

Data capture is frequently used with cloud sync.
However, if you want to manage your machine's captured data yourself, you can enable only data capture without cloud sync.

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

The data is captured in the ESP32's flash memory until it is uploaded to the Viam Cloud.

If the machine restarts before all data is synced, all unsynced data captured since the last sync point is lost.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, high frequency data collection (> 100Hz) requires special considerations on the ESP32.

{{% /tab %}}
{{< /tabs >}}

{{< expand "Click for an example." >}}
Consider a tomato picking robot with a 3D camera and an arm.
When you configure the robot, you might set the camera to capture point cloud data at a frequency of 30Hz.
For the arm, you might capture joint positions at 1Hz.

If your requirements change and you want to capture data from both components at 10Hz, you can change the capture rate at any time in each component's data capture configuration.
{{< /expand >}}

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## Security

The data management service uses {{< glossary_tooltip term_id="grpc" text="gRPC" >}} calls to send and receive data, so your data is encrypted while in flight.
When data is stored in the cloud, it is encrypted at rest by the cloud storage provider.

## Data Integrity

Viam's data management service is designed to safeguard against data loss, data duplication and otherwise compromised data.

If the internet becomes unavailable or the machine needs to restart during the sync process, the sync is interrupted.
If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval in between tries is at one hour, at which point the service retries the sync every hour.
When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.
If the interruption happens mid-file, sync resumes from the beginning of that file.

To avoid syncing files that are still being written to, the data management service only syncs files that haven't been modified in the previous 10 seconds.

## Storage

Data that is successfully synced to the cloud is automatically deleted from local storage.

When a machine loses its internet connection, it cannot resume cloud sync until it can reach the Viam Cloud again.

{{<imgproc src="/services/data/data_management.png" resize="x1100" declaredimensions=true alt="Data is captured on the machine, uploaded to the cloud, and then deleted off local storage." class="imgzoom" >}}

To ensure that the machine can store all data captured while it has no connection, you need to provide enough local data storage.

{{< alert title="Warning" color="warning" >}}

If your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.

{{< /alert >}}

{{< expand "Automatic data deletion details" >}}

If cloud sync is enabled, the data management service deletes captured data once it has successfully synced to the cloud.

With `viam-server`, the data management service will also automatically delete local data in the event your machine's local storage fills up.
Local data is automatically deleted when _all_ of the following conditions are met:

- Data capture is enabled on the data management service
- Local disk usage percentage is greater than or equal to 90%
- The Viam capture directory is at least 50% of the current local disk usage

If local disk usage is greater than or equal to 90%, but the Viam capture directory is not at least 50% of that usage, a warning log message will be emitted instead and no action will be taken.

Automatic file deletion only applies to files in the specified Viam capture directory, which is set to `~/.viam/capture` by default.
Data outside of this directory is not touched by automatic data deletion.

If your machine captures a large amount of data, or frequently goes offline for long periods of time while capturing data, consider moving the Viam capture directory to a larger, dedicated storage device on your machine if available.
You can change the capture directory using the `capture_dir` attribute.

You can also control how local data is deleted if your machine's local storage becomes full, using the `delete_every_nth_when_disk_full` attribute.

{{< /expand >}}

{{< expand "Capture directly to MongoDB" >}}

Data capture supports capturing tabular data directly to MongoDB in addition to capturing to disk.

This feature is intended to support use cases like offline dashboards which don't require strong data delivery or consistency guarantees.

Here is a sample configuration that will capture fake sensor readings both to the configured MongoDB URI as well as to the `~/.viam/capture` directory on disk:

```json
{
  "components": [
    {
      "name": "sensor-1",
      "namespace": "rdk",
      "type": "sensor",
      "model": "fake",
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
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "mongo_capture_config": {
          "uri": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
        }
      }
    }
  ]
}
```

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

{{< /expand >}}

## Configuration

To capture data from one or more machines, you must first [configure the data management service](#data-management-service-configuration).
Then [configure data management](#resource-data-capture-configuration) on each {{< glossary_tooltip term_id="resource" text="resource" >}} that you want to capture data from.

### Data management service configuration

{{< tabs >}}
{{% tab name="Config Builder" %}}

From your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), add the `data management` service.
On the panel that appears, configure data capture and sync attributes as applicable, then save your config.

![Data capture configuration](/tutorials/data-management/data-management-conf.png)

{{% /tab %}}
{{% tab name="JSON Example" %}}

{{< tabs >}}
{{% tab name="viam-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "name": "my-data-manager",
      "namespace": "rdk",
      "type": "data_manager",
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
      "namespace": "rdk",
      "type": "data_manager",
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

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the data management service:

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description | `viam-micro-server` Support |
| ------------------ | ------ | --------- | ----------- | ------------------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Note that even if capture is on for the whole part, but is not on for any individual {{< glossary_tooltip term_id="component" text="components" >}} (see Step 2), data is not being captured. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `capture_dir`      | string | Optional | Path to the directory on your machine where you want to store captured data. If you change the directory for data capture, only new data is stored in the new directory. Existing data remains in the directory where it was stored. <br> Default: `~/.viam/capture` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `tags` | array of strings | Optional | Tags to apply to all images captured by this machine part. May include alphanumeric characters, underscores, and dashes. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `additional_sync_paths` | string array | Optional | Paths to any other directories on your machine from which you want to sync data to the cloud. Once data is synced from a directory, it is automatically deleted from your machine. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `sync_interval_mins` | float | Optional | Time interval in minutes between syncing to the cloud. Viam does not impose a minimum or maximum on the frequency of data syncing. However, in practice, your hardware or network speed may impose limits on the frequency of data syncing. <br> Default: `0.1`, meaning once every 6 seconds. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_data_on_part_deletion` | bool | Optional | Whether deleting this {{< glossary_tooltip term_id="machine" text="machine" >}} or {{< glossary_tooltip term_id="part" text="machine part" >}} should result in deleting all the data captured by that machine part. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_every_nth_when_disk_full` | int | Optional | How many files to delete when local storage meets the [fullness criteria](/services/data/#storage). The data management service will delete every Nth file that has been captured upon reaching this threshold. Use JSON mode to configure this attribute. <br> Default: `5`, meaning that every fifth captured file will be deleted. |  <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `maximum_num_sync_threads` | int | Optional | Max number of CPU threads to use for syncing data to the Viam Cloud. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2 so half the number of logical CPUs available to viam-server |  <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `mongo_capture_config.uri` | string | Optional | The [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) data capture will attempt to write tabular data to after it is enqueued to be written to disk. When non-empty, data capture will capture tabular data to the configured MongoDB database and collection at that URI.<br>See  `mongo_capture_config.database` and  `mongo_capture_config.collection` below for database and collection defaults.<br>See [Data capture directly to MongoDB](/services/data/#capture-directly-to-mongodb) for an example config.|  <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `mongo_capture_config.database` | string | Optional | When `mongo_capture_config.uri` is non empty, changes the database data capture will write tabular data to. <br> Default: `"sensorData"`   |  <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `mongo_capture_config.collection` | string | Optional | When `mongo_capture_config.uri` is non empty, changes the collection data capture will write tabular data to.<br> Default: `"readings"`   |  <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `cache_size_kb` | float | Optional | `viam-micro-server` only. The maximum amount of storage bytes (in kilobytes) allocated to a data collector. <br> Default: `1` KB. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |

### Resource data capture configuration

You can capture data for any {{< glossary_tooltip term_id="resource" text="resource" >}} that supports it, including resources on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.

{{< tabs >}}

{{% tab name="Regular" %}}

Once you have added the data capture service, you can specify the data you want to capture at a resource level.

{{< tabs >}}
{{% tab name="Config builder" %}}

For each resource you can capture data for, there is a **Data capture** section in its panel.
Select a **Method** and specify a capture **Frequency** in hertz.
You can add multiple methods with different capture frequencies.
Some methods will prompt you to add additional parameters.

The available methods, and corresponding additional parameters, will depend on the component or service type.
For example, a camera has the options `ReadImage` and `NextPointCloud`.
Keep in mind that some models do not support all options, for example webcams do not capture point clouds, and choose the method accordingly.

![component config example](/services/data/data-service-component-config.png)

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

{{< /alert >}}

{{% /tab %}}
{{% tab name="JSON example" %}}

{{< tabs >}}
{{% tab name="viam-server" %}}

This example configuration captures data from the `ReadImage` method of a camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    ...
    ,
    {
      "name": "data_manager",
      "type": "data_manager",
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
                "method": "ReadImage",
                "additional_params": {
                  "reader_name": "cam1",
                  "mime_type": "image/jpeg"
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
      "type": "camera",
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

This example configuration captures data from the `GetReadings` method of a temperature sensor and wifi signal sensor:

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
      "namespace": "rdk",
      "type": "data_manager"
    }
  ],
  "components": [
    {
      "type": "sensor",
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
      "name": "tmp36",
      "namespace": "rdk"
    },
    {
      "type": "sensor",
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
      "name": "my-wifi-sensor",
      "namespace": "rdk"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Example for a vision service:

{{< tabs >}}
{{% tab name="viam-server" %}}

This example configuration captures data from the `CaptureAllFromCamera` method of the vision service:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "camera-1",
      "namespace": "rdk",
      "type": "camera",
      "model": "webcam",
      "attributes": {}
    }
  ],
  "services": [
    {
      "name": "vision-1",
      "namespace": "rdk",
      "type": "vision",
      "model": "mlmodel",
      "attributes": {},
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
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": []
      }
    },
    {
      "name": "mlmodel-1",
      "namespace": "rdk",
      "type": "mlmodel",
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

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Remote parts" %}}

Viam supports data capture from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.
For example, if you use a {{< glossary_tooltip term_id="part" text="part" >}} that does not have a Linux operating system or that does not have enough storage or processing power, you can still process and capture the data from that part's resources by adding it as a remote part.

Currently, you can only configure data capture from remote resources in your JSON configuration.
To add them to your JSON configuration you must explicitly add the remote resource's `type`, `model`, `name`, and `additional_params` to the `data_manager` service configuration in the `remotes` configuration:

<!-- prettier-ignore -->
| Key | Description |
| --- | ----------- |
| `type` | The type tells your machine what the resource is. For example, a board. |
| `model` | The model is a {{< glossary_tooltip term_id="model-namespace-triplet" text="colon-delimited-triplet" >}} that specifies the namespace, the type of the part, and the part itself. |
| `name` | The name specifies the fully qualified name of the part. |
| `additional_params` | The additional parameters specify the data sources when you are using a board. |

{{< expand "Click to view example JSON configuration for an ESP32 board" >}}

The following example shows the configuration of the remote part, in this case an [ESP32 board](/components/board/esp32/).
This config is just like that of a non-remote part; the remote connection is established by the main part (in the next expandable example).

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-esp32",
      "model": "esp32",
      "type": "board",
      "namespace": "rdk",
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

The following example captures data from two analog readers that provide a voltage reading and from pin 27 of the board's GPIO:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": ["tag1", "tag2"]
      },
      "name": "data_manager",
      "type": "data_manager"
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
                  "pin_name": “27”
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

The following example captures data from the `ReadImage` method of a camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": []
      },
      "name": "data_manager",
      "type": "data_manager"
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
                "method": "ReadImage",
                "additional_params": {
                  "mime_type": "image/jpeg",
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

The following attributes are available for data capture configuration:

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_frequency_hz` | float   | **Required** | Frequency in hertz at which to capture data. For example, to capture a reading every 2 seconds, enter `0.5`. |
| `method` | string | **Required** | Depends on the type of component or service. See [Supported components and services](/services/data/#supported-components-and-services). |
| `retention_policy` | object | Optional | Option to configure how long data collected by this component or service should remain stored in the Viam Cloud. You must set this in JSON mode. See the JSON example for a camera component. <br> **Options:** `"days": <int>`, `"binary_limit_gb": <int>`, `"tabular_limit_gb": <int>`. <br> Days are in UTC time. Setting a retention policy of 1 day means that data stored now will be deleted the following day **in UTC time**. You can set either or both of the size limit options and size is in gigabytes. |
| `additional_params` | depends | depends | Varies based on the method. For example, `ReadImage` requires a MIME type. |

### Supported components and services

The following components and services support data capture, for the following methods:

{{< readfile "/static/include/data/capture-supported.md" >}}

## View captured data

To view all the captured data you have access to, go to the [**DATA** tab](https://app.viam.com/data/view) where you can filter by location, type of data, and more.

You can also access data from a resource, machine part, or machine menu.

## Considerations

- **Capturing too much data**: You can [use filtering to collect and sync only certain images](/how-tos/image-data/#use-filtering-to-collect-and-sync-only-certain-images) to capture data selectively.
- **Rentention policy**: Set a `retention_policy` attribute in your [data capture configuration](#resource-data-capture-configuration) to avoid keeping data stored in the Viam Cloud longer than a specified number of days.
- **Pausing sync**: You can pause cloud sync at any time by navigating to your machine's **CONFIGURE** tab and disabling **Syncing** for your [data management service](../).

  If you have captured data that you do not want to sync, delete the data on the machine before resuming cloud sync.
  To delete the data locally, `ssh` into your machine and delete the data in the directory where you capture data.

- **Sync data conditionally**: You can use a {{< glossary_tooltip term_id="module" text="module" >}} to sync data only when a certain logic condition is met, instead of at a regular time interval.
  For example, if you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.
  To set up triggers for syncing see [Conditional cloud sync](/how-tos/conditional-sync/).

## API

The [data management service API](/dev/reference/apis/services/data/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/data_manager-table.md" >}}

The data client API supports a separate set of methods that allow you to upload and export data to and from the Viam app.
For information about that API, see [Data Client API](/dev/reference/apis/data-client/).

## Troubleshooting

### Images are dim on start up

If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.
Wait for a few seconds and you should see correctly colored images.

## Next steps

If you have synced data, such as [sensor](/components/sensor/) readings, you can [query that data with SQL or MQL](/how-tos/sensor-data-query-with-third-party-tools/) from the Viam app or a MQL-compatible client.
If you have synced images, you can use those images to [train machine learning models](/how-tos/train-deploy-ml/) within the Viam app.

Or check out the following guides and tutorials:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/how-tos/performance-metrics/" %}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
