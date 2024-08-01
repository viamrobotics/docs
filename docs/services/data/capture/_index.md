---
title: "Configure Data Capture"
linkTitle: "Data Capture"
description: "Configure data capture to save data from components remote parts."
weight: 10
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
images: ["/services/icons/data-capture.svg"]
no_list: true
aliases:
  - "/services/data/capture/"
  - "/data/capture/"
  - "/build/micro-rdk/data_management/"
# SME: Alexa Greenberg
no_service: true
---

The data management service captures data from one or more components.

Get started with a quickstart guide or keep reading for more details.

{{< cards >}}
{{< card link="/get-started/quickstarts/collect-data/" class="green">}}
{{< /cards >}}

{{< tabs >}}
{{% tab name="RDK" %}}

The data is captured locally on the machine's storage and, by default, stored in the `~/.viam/capture` directory.

If a machine restarts for any reason, capture automatically resumes and any data from already stored but not yet synced is synced.

The service can capture data from multiple components at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.

{{% /tab %}}
{{% tab name="micro-RDK" %}}
The data is captured in the ESP32's flash memory and periodically uploaded to the Viam cloud.

If the machine restarts before all data is synced, all unsynced data captured since the last sync point is lost.

The service can capture data from multiple components at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, high frequency data collection (> 100Hz) requires special considerations on the ESP32.

{{% /tab %}}
{{< /tabs >}}

You can change the frequency of data capture at any time for individual components.
If you use {{< glossary_tooltip term_id="fragment" text="fragments" >}}, you can change the frequency of data capture in real time for some or all machines in a fleet at the component or machine level.

For example, consider a tomato picking robot with a 3D camera and an arm.
When you configure the robot, you may set the camera to capture point cloud data at a frequency of 30Hz.
For the arm, you may want to capture joint positions at 1Hz.
If your requirements change and you want to capture data from both components at 10Hz, you can change the configurations at any time by changing the number.

Data capture is frequently used with [Cloud Sync](/services/data/cloud-sync/).
However, if you want to manage your machine's captured data yourself, you can enable only data capture without cloud sync.

## Add the data management service

To capture data from one or more machines, you must first add the [data management service](../):

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
3. Select the `data management` type, then either use the suggested name or specify a name for your data management service, for example `data-manager`.
4. Click **Create**.
5. On the panel that appears, you can manage the capturing and syncing functions.
   {{< tabs >}}
   {{% tab name="RDK" %}}
   Specify the **Directory**, the sync **Interval** and any **Tags** to apply to captured data.

If the sync **Interval** or the **Directory** is not specified, the data management service captures data at the default frequency every 0.1 minutes (after every 6 second interval) in the default `~/.viam/capture` directory.

{{< alert title="Info" color="info" >}}
If you change the directory for data capture only new data is stored in the new directory.
Existing data remains in the directory where it was stored.
{{< /alert >}}
{{% /tab %}}
{{% tab name="micro-RDK" %}}
Specify the sync **Interval**.

{{< alert title="Info" color="info" >}}
With micro-RDK, the `capture_dir`, `tags`, and `additional_sync_paths` attributes are ignored and should not be configured.
{{< /alert >}}
{{% /tab %}}
{{< /tabs >}}

{{%expand "Click to view the JSON configuration for the data management service" %}}
{{< tabs >}}
{{% tab name="RDK" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "name": "your-data-manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 1,
        "capture_dir": "",
        "tags": [],
        "capture_disabled": false,
        "sync_disabled": true,
        "delete_every_nth_when_disk_full": 5
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="micro-RDK" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "attributes": {
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": [],
        "sync_interval_mins": 3
      },
      "name": "my-data-manager",
      "namespace": "rdk",
      "type": "data_manager"
    }
  ]
}
```

{{< alert title="Info" color="info" >}}
With micro-RDK, the `capture_dir`, `tags`, and `additional_sync_paths` attributes are ignored and should not be configured.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

{{% /expand%}}

6. Click the **Save** button in the top right corner of the page.

![data capture configuration](/tutorials/data-management/data-management-conf.png)

When your machine is capturing data, there is a **Capturing** indication in your machine's status bar.

![data capture indicator on the machine's page](/tutorials/data-management/capturing.png)

## Configure data capture for individual components

Once you have added the data capture service, you can specify the data you want to capture at a component level.

### Supported components

The following components support data capture:

{{< tabs >}}
{{% tab name="RDK" %}}

- Arm
- Board
- Camera
- Encoder
- Gantry
- Motor
- Movement Sensor (includes GPS)
- Sensor
- Servo

{{% /tab %}}
{{% tab name="micro-RDK" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Sensor](/components/sensor/) | [`GetReadings`](/components/sensor/#getreadings) |
| [Movement Sensor](/components/movement-sensor/) | [`AngularVelocity`](/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/components/movement-sensor/#getlinearvelocity) |

{{% /tab %}}
{{< /tabs >}}

To add data capture for a component, navigate to the **CONFIGURE** tab of your machine's page in the Viam app.

For each component you can capture data for, there is a `Data capture` section in its panel.
Click `Add Method` and then select the **Method** type and the capture **Frequency**.

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

{{< /alert >}}

Click the **Save** button in the top right corner of the page.

Now, using the RDK, your data will be saved locally on your machine to the directory specified in the data management service.
If you are using the micro-RDK, data will be captured at the configured capture frequency and saved in flash memory and synced to Viam app at the selected interval.

For example, a camera has the options `ReadImage` and `NextPointCloud` and a motor has the options `Position` and `IsPowered`.

![component config example](/services/data/data-service-component-config.png)

{{%expand "Click to view an example JSON configuration" %}}

{{< tabs >}}
{{% tab name="RDK" %}}

This example configuration captures data from the ReadImage method of a camera:

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
{{% tab name="micro-RDK" %}}

This example configuration captures data from the GetReadings method of a temperature sensor and wifi signal sensor:

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
                "capture_frequency_hz": 0.1
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

{{% /expand%}}

You may capture data from one or more component methods:

- To enable or disable data capture for a configured component or method, use the `on/off` toggle on the component's configuration pane in the Viam app.
- To change the frequency of data capture for a method, enter the number of measurements you wish to capture per second in the frequency field on the component's configuration pane in the Viam app.

After adding configuration for the methods, click the **Save** button in the top right corner of the page.

If you want to remove a capture method from the configuration, click the `delete` icon.

## Configure data capture for remote parts

Viam supports data capture from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.
For example, if you use a {{< glossary_tooltip term_id="part" text="part" >}} that does not have a Linux operating system or that does not have enough storage or processing power, you can still process and capture the data from that part's components by adding it as a remote part.

Currently, you can only configure data capture from remote components in your JSON configuration.
To add them to your JSON configuration you must explicitly add the remote component's `type`, `model`, `name`, and `additional_params` to the `data_manager` service configuration in the `remotes` configuration:

<!-- prettier-ignore -->
| Key | Description |
| --- | ----------- |
| `type` | The type tells your machine what the component is. For example, a board. |
| `model` | The model is a {{< glossary_tooltip term_id="model-namespace-triplet" text="colon-delimited-triplet" >}} that specifies the namespace, the type of the part, and the part itself. |
| `name` | The name specifies the fully qualified name of the part. |
| `additional_params` | The additional parameters specify the data sources when you are using a board. |

{{%expand "Click to view example JSON configuration for an ESP32 board" %}}

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
                "capture_frequency_hz": 10
              },
              {
                "method": "Analogs",
                "additional_params": {
                  "reader_name": "A2"
                },
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

{{% /expand%}}

{{%expand "Click to view the JSON configuration for capturing data from two analog readers and a pin of the board's GPIO" %}}

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
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A1" },
                "disabled": false
             },
             {
                "method": "Analogs",
                "capture_frequency_hz": 1,
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A2" },
                "disabled": false
              },
              // Captures data from pin 27 of the board's GPIO
              {
                "method": "Gpios",
                "capture_frequency_hz": 1,
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

{{% /expand%}}

{{%expand "Click to view the JSON configuration for capturing data from a camera" %}}

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

{{% /expand%}}

## Capture data selectively with filtering

See the [Use filtering to collect and sync only certain images](/use-cases/image-data/#use-filtering-to-collect-and-sync-only-certain-images) guide.

## Automatic data deletion

If [cloud sync](/services/data/cloud-sync/) is enabled, the data management service deletes captured data once it has successfully synced to the cloud.

With the RDK, the data management service will also automatically delete local data in the event your machine's local storage fills up.
Local data is automatically deleted when _all_ of the following conditions are met:

- Data capture is enabled on the data manager service
- Local disk usage percentage is greater than or equal to 90%
- The Viam capture directory is at least 50% of the current local disk usage

If local disk usage is greater than or equal to 90%, but the Viam capture directory is not at least 50% of that usage, a warning log message will be emitted instead and no action will be taken.

Automatic file deletion only applies to files in the specified Viam capture directory, which is set to `~/.viam/capture` by default.
Data outside of this directory is not touched by automatic data deletion.

If your machine captures a large amount of data, or frequently goes offline for long periods of time while capturing data, consider moving the Viam capture directory to a larger, dedicated storage device on your machine if available. You can change the capture directory using the `capture_dir` attribute.

You can also control how local data is deleted if your machine's local storage becomes full, using the `delete_every_nth_when_disk_full` attribute:

- The `delete_every_nth_when_disk_full` attribute controls how many files to delete when local storage meets the above fullness criteria.
  The data management service will delete every Nth file that has been captured upon reaching this threshold.
  The default value is `5`, meaning that every fifth captured file will be deleted.
  This value should be suitable for most cases.

## View captured data

To view captured data for a machine, click on the data icon next to the **Save** button on the top right of the app.

{{<imgproc src="/services/data/data-icon.png" resize="300x" declaredimensions=true alt="Data icon">}}

To view captured data for a {{< glossary_tooltip term_id="part" text="machine part" >}}, click on the menu in the top right of its card or the menu in the machine resources list in the **Builder** menu and select **View captured data**.

{{<imgproc src="/services/data/part-menu.png" resize="300x" declaredimensions=true alt="Machine menu with the options Rename, Restart part, View captured data, View setup instructions, View history, View debug configuration, and Delete machine">}}

To view captured data for a component or service, click on the menu in the top right of its card and select **View captured data**.

![Resource menu with the options Rename, Duplicate, View captured data, and Delete](/services/data/resource-menu.png)

To view all the captured data you have access to, see [View Data](/services/data/view/).

## Troubleshooting

### Images are dim on start up

If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.
Wait for a few seconds and you should see correctly colored images.

## Next steps

To sync your captured data with the cloud, [configure cloud sync](/services/data/cloud-sync/).

If you have synced data, such as [sensor](/components/sensor/) readings, you can [query that data with SQL or MQL](/use-cases/sensor-data-query/) from the Viam app or a MQL-compatible client.
If you have synced images, you can use those images to [train machine learning models](/services/ml/train-model/) within the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).

To learn how to capture Performance Metrics for machines, see [Performance Monitoring Data Capture](/services/data/capture/performance-metrics/).

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{% card link="/services/data/capture/performance-metrics/" %}}
{{% card link="/tutorials/projects/filtered-camera/" %}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
