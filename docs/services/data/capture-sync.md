---
title: "Data Capture and Sync"
linkTitle: "Data Capture and Sync"
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
no_service: true
---

The data management service captures data from one or more {{< glossary_tooltip term_id="resource" text="resources" >}} locally, and syncs it to cloud storage when a connection to the cloud is available.
You can configure which data you want to capture, as well as the capture rate and the sync frequency.

Get started with a quickstart guide or keep reading for more details.

{{< cards >}}
{{< card link="/get-started/collect-data/" class="green">}}
{{< /cards >}}

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

The data is captured in the ESP32's flash memory until it is uploaded to the Viam cloud.

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

## Supported components and services

The following components and services support data capture, for the following methods:

{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/components/arm/)                         | `EndPosition`, `JointPositions` |
| [Board](/components/board/)                     | `Analogs`, `Gpios` |
| [Camera](/components/camera/)                   | `GetImages`, `ReadImage`, `NextPointCloud` |
| [Encoder](/components/encoder/)                 | `TicksCount` |
| [Gantry](/components/gantry/)                   | `Lengths`, `Position` |
| [Motor](/components/motor/)                     | `Position`, `IsPowered` |
| [Movement sensor](/components/movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position` |
| [Sensor](/components/sensor/)                   | `Readings` |
| [Servo](/components/servo/)                     | `Position` |
| [Vision service](/services/vision/)             | `CaptureAllFromCamera` |

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/components/movement-sensor/) | [`AngularVelocity`](/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/components/sensor/) | [`GetReadings`](/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}

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

When a machine loses its internet connection, it cannot resume cloud sync until it can reach the Viam cloud again.

To ensure that the machine can store all data captured while it has no connection, you need to provide enough local data storage.

{{< alert title="Warning" color="warning" >}}

If your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.

{{< /alert >}}

{{< expand "Automatic data deletion details" >}}

If cloud sync is enabled, the data management service deletes captured data once it has successfully synced to the cloud.

With `viam-server`, the data management service will also automatically delete local data in the event your machine's local storage fills up.
Local data is automatically deleted when _all_ of the following conditions are met:

- Data capture is enabled on the data manager service
- Local disk usage percentage is greater than or equal to 90%
- The Viam capture directory is at least 50% of the current local disk usage

If local disk usage is greater than or equal to 90%, but the Viam capture directory is not at least 50% of that usage, a warning log message will be emitted instead and no action will be taken.

Automatic file deletion only applies to files in the specified Viam capture directory, which is set to `~/.viam/capture` by default.
Data outside of this directory is not touched by automatic data deletion.

If your machine captures a large amount of data, or frequently goes offline for long periods of time while capturing data, consider moving the Viam capture directory to a larger, dedicated storage device on your machine if available.
You can change the capture directory using the `capture_dir` attribute.

You can also control how local data is deleted if your machine's local storage becomes full, using the `delete_every_nth_when_disk_full` attribute.

{{< /expand >}}

## Configure data capture and sync

{{< expand "Step 1: Configure the data management service" >}}

To capture data from one or more machines, you must first add the data management service:

{{< tabs >}}
{{% tab name="Config Builder" %}}

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
3. Select the `data management` type, then either use the suggested name or specify a name for your data management service.
4. Click **Create**.
5. On the panel that appears, configure data capture and sync attributes as applicable, then save your config.

![Data capture configuration](/tutorials/data-management/data-management-conf.png)

{{% /tab %}}
{{% tab name="JSON Example" %}}

If you prefer to write raw JSON, here is an example:

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

{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Note that even if capture is on for the whole part, but is not on for any individual {{< glossary_tooltip term_id="component" text="components" >}} (see Step 2), data is not being captured. <br> Default: `false` |
| `capture_dir`      | string | Optional | Path to the directory on your machine where you want to store captured data. If you change the directory for data capture, only new data is stored in the new directory. Existing data remains in the directory where it was stored. <br> Default: `~/.viam/capture` |
| `tags` | array of strings | Optional | Tags to apply to all images captured by this machine part. May include alphanumeric characters, underscores, and dashes. |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` |
| `additional_sync_paths` | string array | Optional | Paths to any other directories on your machine from which you want to sync data to the cloud. Once data is synced from a directory, it is automatically deleted from your machine. |
| `sync_interval_minutes` | float | Optional | Time interval in minutes between syncing to the cloud. Viam does not impose a minimum or maximum on the frequency of data syncing. However, in practice, your hardware or network speed may impose limits on the frequency of data syncing. <br> Default: `0.1`, meaning once every 6 seconds. |
| `delete_every_nth_when_disk_full` | int | Optional | How many files to delete when local storage meets the [fullness criteria](/services/data/capture-sync/#storage). The data management service will delete every Nth file that has been captured upon reaching this threshold. Use JSON mode to configure this attribute. <br> Default: `5`, meaning that every fifth captured file will be deleted. |
| `maximum_num_sync_threads` | int | Optional | Max number of CPU threads to use for syncing data to the Viam cloud. <br> Default: `1000` |

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Info" color="info" >}}
With `viam-micro-server`, the `capture_dir`, `tags`, and `additional_sync_paths`, and `delete_every_nth_when_disk_full` attributes are ignored and should not be configured.
{{< /alert >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Note that even if capture is on for the whole part, but is not on for any individual {{< glossary_tooltip term_id="component" text="components" >}} (see Step 2), data is not being captured. <br> Default: `false` |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` |
| `sync_interval_minutes` | float | Optional | Time interval in minutes between syncing to the cloud. Viam does not impose a minimum or maximum on the frequency of data syncing. However, in practice, your hardware or network speed may impose limits on the frequency of data syncing. <br> Default: `0.1`, meaning once every 6 seconds. |
| `cache_size_kb` | float | Optional | The maximum amount of storage bytes (in kilobytes) allocated to a data collector. <br> Default: `1` KB. |

{{% /tab %}}
{{< /tabs >}}

Now the data management service is enabled.
However, no data is being captured until you configure capture on one or more {{< glossary_tooltip term_id="resource" text="resources" >}}.

{{< /expand >}}
{{< expand "Step 2: Configure data capture for your resources" >}}

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

The following attributes are available for data capture configuration:

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description |
| ------------------ | ------ | --------- | ----------- |
| `capture_frequency_hz` | float   | **Required** | Frequency in hertz at which to capture data. For example, to capture a reading every 2 seconds, enter `0.5`. |
| `method` | string | **Required** | Depends on the type of component or service. See [Supported components and services](/services/data/capture-sync/#supported-components-and-services). |
| `additional_params` | depends | depends | Varies based on the method. For example, `ReadImage` requires a MIME type. |

Click the **Save** button in the top right corner of the page.

{{% /tab %}}
{{% tab name="Raw JSON example" %}}

{{< expand "Example for a camera component" >}}

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
            ]
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

{{< /expand >}}

{{< expand "Example for a vision service" >}}

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
      "model": "tflite_cpu",
      "attributes": {}
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

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

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}
{{< expand "Step 3: (Optional) Too much data? Capture only interesting data" >}}

See the [Use filtering to collect and sync only certain images](/how-tos/image-data/#use-filtering-to-collect-and-sync-only-certain-images) guide.

{{< /expand >}}
{{< expand "Step 4: (Optional) View captured data" >}}

To view all the captured data you have access to, go to the [**DATA** tab](https://app.viam.com/data/view) where you can also filter by location, type of data, and more.

Or, you can navigate to the **DATA** tab from an individual resource, part, or machine's configuration card to automatically apply relevant filters:

{{< tabs >}}
{{% tab name="One resource" %}}

To view captured data for a component or service, click on the menu in the top right of its card and select **View captured data**.

![Resource menu with the options Rename, Duplicate, View captured data, and Delete](/services/data/resource-menu.png)

{{% /tab %}}
{{% tab name="Machine part" %}}

To view captured data for a {{< glossary_tooltip term_id="part" text="machine part" >}}, click on the menu in the top right of its card or the menu in the machine resources list in the **Builder** menu and select **View captured data**.

{{<imgproc src="/services/data/part-menu.png" resize="220x" declaredimensions=true alt="Machine menu with the options Rename, Restart part, View captured data, View setup instructions, View history, View debug configuration, and Delete machine">}}

{{% /tab %}}
{{% tab name="Whole machine" %}}

To view captured data for a {{< glossary_tooltip term_id="machine" text="machine" >}} (including data from all parts of a multi-part machine), click on the data icon next to the **Save** button on the top right of the app.

{{<imgproc src="/services/data/data-icon.png" resize="200x" declaredimensions=true alt="Data icon">}}

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}
{{< expand "Step 5: (Optional) Pause sync" >}}

You can pause cloud sync at any time by navigating to your machine's **CONFIGURE** tab and disabling **Syncing** for your [data management service](../).

If you have captured data that you do not want to sync, delete the data on the machine before resuming cloud sync.
To delete the data locally, `ssh` into your machine and delete the data in the directory where you capture data.

{{< /expand >}}

## Sync data conditionally

You can use a {{< glossary_tooltip term_id="module" text="module" >}} to sync data only when a certain logic condition is met, instead of at a regular time interval.
For example, if you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.
To set up triggers for syncing see:

{{< cards >}}
{{% card link="/how-tos/trigger-sync/" %}}
{{< /cards >}}

## API

The data management service supports the following methods:

{{< readfile "/static/include/services/apis/generated/data_manager-table.md" >}}

The data client API supports a separate set of methods that allow you to upload and export data to and from the Viam app.
For information about that API, see [Data Client API](/appendix/apis/data-client/).

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a data management service, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for sample code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/data_manager.md" >}}

## Troubleshooting

### Images are dim on start up

If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.
Wait for a few seconds and you should see correctly colored images.

## Next steps

If you have synced data, such as [sensor](/components/sensor/) readings, you can [query that data with SQL or MQL](/how-tos/sensor-data-query-with-third-party-tools/) from the Viam app or a MQL-compatible client.
If you have synced images, you can use those images to [train machine learning models](/how-tos/deploy-ml/) within the Viam app.

Or check out the following guides and tutorials:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{% card link="/how-tos/performance-metrics/" %}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
