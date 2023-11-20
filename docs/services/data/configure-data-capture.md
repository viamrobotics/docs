---
title: "Configure Data Capture"
linkTitle: "Configure Data Capture"
description: "Configure data capture to save data from components remote parts."
weight: 30
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Devin Hilly
---

## Add the data management service

To capture data from one or more machines, you must first add the [data management service](../):

1. From your robot's **Config** tab, navigate to the **Services** subtab.
2. Click **Create service** in the lower-left corner of the page.
   Choose `Data Management` as the type and specify a name for your data management service, for example `data-manager`.
3. Click **Create**.
4. On the panel that appears, you can manage the capturing and syncing functions and specify the **directory**, the sync **interval** and any **tags** to apply to captured data.

   If the sync **interval** or the **directory** is not specified, the data management service captures data at the default frequency every 0.1 minutes (after every 6 second interval) in the default `~/.viam/capture` directory.

   {{< alert title="Info" color="info" >}}
   If you change the directory for data capture only new data is stored in the new directory.
   Existing data remains in the directory where it was stored.
   {{< /alert >}}

5. Click **Save Config**.

![data capture configuration](/tutorials/data-management/data-management-conf.png)

{{%expand "Click to view the JSON configuration for the data management service" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 1,
        "capture_dir": "",
        "tags": []
      }
    }
  ]
}
```

{{% /expand%}}

## Configure Data Capture for Individual Components

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

To add data capture for a component, navigate to the **Config** tab of your robot's page in the Viam app.

For each component you can capture data for, there is a `Data Capture Configuration` section in its panel.
Click `Add Method` and then select the method type and the capture frequency.

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

{{< /alert >}}

Click **Save Config** at the bottom of the window.

Now your data will be saved locally on your machine to the directory specified in the data management service.

For example, a camera has the options `ReadImage` and `NextPointCloud` and a motor has the options `Position` and `IsPowered`.

![component config example](/services/data/data-service-component-config.png)

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

After adding configuration for the methods, click **Save Config**.

If you want to remove a capture method from the configuration, click the `delete` icon.

## Configure Data Capture for Remote Parts

Viam supports data capture from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote" text="remote" >}} parts.
For example, if you use a {{< glossary_tooltip term_id="part" text="part" >}} that does not have a Linux operating system or that does not have enough storage or processing power, you can still process and capture the data from that part's components by adding it as a remote part.

Currently, you can only configure data capture from remote components in your raw JSON configuration.
To add them to your JSON configuration you must explicitly add the remote component's `type`, `model`, `name`, and `additional_params` to the `data_manager` service configuration in the `remotes` configuration:

<!-- prettier-ignore -->
| Key | Description |
| --- | ----------- |
| `type` | The type tells your machine what the component is. For example, a board. |
| `model` | The model is a {{< glossary_tooltip term_id="model-namespace-triplet" text="colon-delimited-triplet" >}} that specifies the namespace, the type of the part, and the part itself. |
| `name` | The name specifies the fully qualified name of the part. |
| `additional_params` | The additional parameters specify the data sources when you are using a board. |

{{%expand "Click to view example JSON configuration for an ESP32 board" %}}

The following example shows the configuration of the remote part, in this case an [ESP32 board](/micro-rdk/board/esp32/).
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

## Next Steps

To sync your captured data with the cloud, [configure cloud sync](../configure-cloud-sync/).

You can [query](../query/) tabular data that you have synced to the cloud, and can use images you have synced to [train machine learning models](../../ml/train-model/) within the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
