---
title: "Configure Data capture and sync"
linkTitle: "Data Capture"
weight: 30
type: "docs"
description: "Configure data capture and sync in the micro-RDK to save data from components."
images: ["/services/icons/data-capture.svg"]
icon: true
tags: ["data management", "cloud", "sync"]
no_list: true
no_service: true
# SMEs: Gautham V.
---

The micro-RDK data management service captures data from one or more components in the ESP32's flash memory.
The service periodically uploads data to Viam cloud.
If the machine restarts before all data is synced, all unsynced data captured since the last sync point is lost.

The micro-RDK data management service can capture data from multiple components at the same or different frequencies.
The micro-RDK does not impose an upper limit on the frequency of data collection.
However, in practice, high frequency data collection (> 100Hz) requires special considerations on the ESP32.

## Add the data management service

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
3. Select the `data management` type, then either use the suggested name or specify a name for your data management service, for example `data-manager`.
4. Click **Create**.
5. On the panel that appears, you can manage the capturing and syncing functions and specify the sync **Interval**.
   {{< alert title="Info" color="info" >}}
   With micro-RDK, the `capture_dir`, `tags`, and `additional_sync_paths` attributes are ignored and should not be configured.
   {{< /alert >}}
6. Click the **Save** button in the top right corner of the page.

![data capture configuration](/tutorials/data-management/data-management-conf.png)

{{%expand "Click to view the JSON configuration for the data management service" %}}

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

{{% /expand%}}

## Configure data capture for individual components

Once you have added the data management service, you can specify the data you want to capture at a component level.

### Supported components

Only the following components types are currently supported with data capture:
| Type | Method |
| ----- | ----------- |
| [Sensor](/build/micro-rdk/sensor/) | [`GetReadings`](/components/sensor/#getreadings) |
| [Movement Sensor](/build/micro-rdk/movement-sensor/) | [`AngularVelocity`](/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/components/movement-sensor/#getlinearvelocity) |

To add data capture for a component, navigate to the **CONFIGURE** tab of your machine's page in the Viam app.

For each component you can capture data for, find the `Data capture` section in its panel.
Click `Add Method` and then select the **Method** type and the capture **Frequency**.

{{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this can lead to performance degradation.

{{< /alert >}}

Click the **Save** button in the top right corner of the page.

Now your data will be captured at the configured capture frequency and synced to Viam app at the selected interval.

{{%expand "Click to view an example JSON configuration capturing data from the GetReadings method of a temperature sensor and wifi signal sensor" %}}

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

{{% /expand%}}

- To enable or disable data capture for a configured component or method, use the `on/off` toggle on the component's configuration pane in the Viam app.
- To change the frequency of data capture for a method, enter the number of measurements you wish to capture per second in the frequency field on the component's configuration pane in the Viam app.

After adding the configuration for the methods, click the **Save** button in the top right corner of the page.

If you want to remove a capture method from the configuration, click the `delete` icon.

## View captured data

To view captured data for a machine, click on the data icon next to the **Save** button on the top right of the Viam app.

{{<imgproc src="/services/data/data-icon.png" resize="300x" declaredimensions=true alt="Data icon">}}

To view captured data for a {{< glossary_tooltip term_id="part" text="machine part" >}}, click on the **...** menu in the top right of its card, or the menu in the machine resources list in the **Builder** menu, and select **View captured data**.

{{<imgproc src="/services/data/part-menu.png" resize="300x" declaredimensions=true alt="Machine menu with the options Rename, Restart part, View captured data, View setup instructions, View history, View debug configuration, and Delete machine">}}

To view captured data for a {{< glossary_tooltip term_id="part" text="machine part" >}}, click on the **...** menu in the top right of its card, or the menu in the machine resources list in the **Builder** menu, and select **View captured data**.

![Resource menu with the options Rename, Duplicate, View captured data, and Delete](/services/data/resource-menu.png)

To view all the captured data you have access to, see [View Data](/services/data/view/).
