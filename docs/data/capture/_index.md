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
# SME: Alexa Greenberg
---

The data management service captures data from one or more components locally on the machine's storage.
The process runs in the background and, by default, stores data in the `~/.viam/capture` directory.

If a machine restarts for any reason, capture automatically resumes.

The service can capture data from multiple components at the same or different frequencies.
Viam does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.

You can change the frequency of data capture at any time for individual components.
If you use {{< glossary_tooltip term_id="fragment" text="fragments" >}}, you can change the frequency of data capture in real time for some or all machines in a fleet at the component or machine level.

For example, consider a tomato picking robot with a 3D camera and an arm.
When you configure the robot, you may set the camera to capture point cloud data at a frequency of 30Hz.
For the arm, you may want to capture joint positions at 1Hz.
If your requirements change and you want to capture data from both components at 10Hz, you can change the configurations at any time by changing the number.

Data capture is frequently used with [Cloud Sync](/data/cloud-sync/).
However, if you want to manage your machine's captured data yourself, you can enable only data capture without cloud sync.

## Add the data management service

To capture data from one or more machines, you must first add the [data management service](../):

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
3. Select the `data management` type, then either use the suggested name or specify a name for your data management service, for example `data-manager`.
4. Click **Create**.
5. On the panel that appears, you can manage the capturing and syncing functions and specify the **Directory**, the sync **Interval** and any **Tags** to apply to captured data.

   If the sync **Interval** or the **Directory** is not specified, the data management service captures data at the default frequency every 0.1 minutes (after every 6 second interval) in the default `~/.viam/capture` directory.

   {{< alert title="Info" color="info" >}}
   If you change the directory for data capture only new data is stored in the new directory.
   Existing data remains in the directory where it was stored.
   {{< /alert >}}

6. Click the **Save** button in the top right corner of the page.

![data capture configuration](/tutorials/data-management/data-management-conf.png)

{{%expand "Click to view the JSON configuration for the data management service" %}}

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
        "sync_disabled": true
      }
    }
  ]
}
```

{{% /expand%}}

## Configure data capture for individual components

Once you have added the data capture service, you can specify the data you want to capture at a component level.
The following components support data capture:

- Arm
- Board
- Camera
- Encoder
- Gantry
- Motor
- Movement Sensor (includes GPS)
- Sensor
- Servo

To add data capture for a component, navigate to the **CONFIGURE** tab of your machine's page in the Viam app.

For each component you can capture data for, there is a `Data capture` section in its panel.
Click `Add Method` and then select the **Method** type and the capture **Frequency**.

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

{{< /alert >}}

Click the **Save** button in the top right corner of the page.

Now your data will be saved locally on your machine to the directory specified in the data management service.

For example, a camera has the options `ReadImage` and `NextPointCloud` and a motor has the options `Position` and `IsPowered`.

![component config example](/data/data-service-component-config.png)

{{%expand "Click to view an example JSON configuration capturing data from the ReadImage method of a camera" %}}

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

{{% /expand%}}

You may capture data from one or more component methods:

- To enable or disable data capture for a configured component or method, use the `on/off` toggle.
- To change the frequency of data capture for a method, enter the number of measurements you wish to capture per second in the frequency field.

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

The following example shows the configuration of the remote part, in this case an [ESP32 board](/build/micro-rdk/board/esp32/).
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
                "additional_params": {
                  "A2": "",
                  "A1": ""
                },
                "disabled": false
              },
              // Captures data from pin 27 of the board's GPIO
              {
                "method": "Gpio",
                "capture_frequency_hz": 1,
                "name": "rdk:component:board/my-esp32",
                "additional_params": {
                  "27": ""
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

## Troubleshooting

### Images are dim on start up

If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.

## Next steps

To sync your captured data with the cloud, [configure cloud sync](/data/cloud-sync/).

If you have synced tabular data, such as [sensor](/components/sensor/) readings, you can [query that data with SQL or MQL](/data/query/) from the Viam app or a MQL-compatible client.
If you have synced images, you can use those images to [train machine learning models](/ml/train-model/) within the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).

To learn how to capture Performance Metrics for machines, see [Performance Monitoring Data Capture](/data/capture/performance-metrics/).

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{% card link="/data/capture/performance-metrics/" %}}
{{% card link="/tutorials/projects/filtered-camera/" %}}
{{< /cards >}}
