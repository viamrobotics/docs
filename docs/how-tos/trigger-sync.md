---
title: "How to trigger cloud sync conditionally"
linkTitle: "Trigger data sync conditionally"
description: "Trigger cloud sync to sync captured data when custom conditions are met."
weight: 44
type: "docs"
tags: ["data management", "cloud", "sync"]
images: ["/services/icons/data-cloud-sync.svg"]
aliases:
  - /data/trigger-sync/
  - /services/data/trigger-sync/
no_service: true
---

You may want to sync data only when a certain logic condition is met, instead of at a regular time interval.
For example, if you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.
Or, you may want to trigger sync only when your machine detects an object of a certain color.
The code for both of these examples is provided by the [trigger-sync-examples module](https://github.com/viam-labs/trigger-sync-examples-v2), and you can [create your own module](/how-tos/create-module/) if you want to use different logic.

To set up conditional syncing you need to:

1. Create or use an existing module that implements a `sensor` component that uses your custom logic to determine when to enable and disable sync.
   While this sensor is not sensing the time it _senses_ whether the data manager should sync or not.
2. Change the configuration of the data manager to enable selective sync.

{{% alert title="Note: How sync is triggered" color="note" %}}

Regardless of the specifics of your trigger sync logic, to trigger sync you need to pass `true` to the [CreateShouldSyncReading function](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#CreateShouldSyncReading) within the definition of your modular sensor's `Readings` function.
See examples in the `Readings` function of the [time-interval-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/time-interval-trigger/selective_sync/selective_sync.go) and the [color-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/color-trigger/selective_sync/selective_sync.go).

{{% /alert %}}

This page covers how to use the `sync-at-time` module.
You can use this as an example if you use or create a similar module.

{{% alert title="In this page" color="tip" %}}

1. [Add the `sync-at-time` "sensor"](#add-sensor-to-determine-when-to-sync)
2. [Configure the data manager to sync based on the sensor](#configure-the-data-manager-to-sync-based-on-sensor)
3. [Test your sync configuration](#test-your-sync-configuration)

{{% /alert %}}

## Example: `sync-at-time`

In this example, you will configure sync to only trigger during a specific time frame of the day using an existing module [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time).
If you need to trigger sync based on a different condition, you need to create your own module and adjust the module logic accordingly.
Additional examples are available in this [GitHub Repo](https://github.com/viam-labs/trigger-sync-examples-v2).

### Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "Enable data capture and sync on your machine." >}}

Add the [data management](/services/data/) service:

On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{< /expand >}}

### Add sensor to determine when to sync

To use [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time):

{{< table >}}
{{% tablestep %}}
**1. Add the sensor to your machine**

On your machine's **CONFIGURE** page, click the **+** button next to your machine part in the left menu.
Select **Component**, then search for and select the `sync-at-time:timesyncsensor` model provided by the [`sync-at-time` module](https://app.viam.com/module/naomi/sync-at-time).

Click **Add module**, then enter a name or use the suggested name for your sensor and click **Create**.

{{% /tablestep %}}
{{% tablestep %}}
**2. Configure your time frame**

Go to the new component panel and copy and paste the following attribute template into your sensor’s attributes field:

{{< tabs >}}
{{% tab name="Config builder" %}}

```json
{
  "start": "HH:MM:SS",
  "end": "HH:MM:SS",
  "zone": "<TIMEZONE>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "name": "<SENSORNAME>",
  "model": "naomi:sync-at-time:timesyncsensor",
  "type": "sensor",
  "namespace": "rdk",
  "attributes": {
    "start": "HH:MM:SS",
    "end": "HH:MM:SS",
    "zone": "<TIMEZONE>"
  },
  "depends_on": []
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json
{
  "name": "timesensor",
  "model": "naomi:sync-at-time:timesyncsensor",
  "type": "sensor",
  "namespace": "rdk",
  "attributes": {
    "start": "18:29:00",
    "end": "18:30:00",
    "zone": "CET"
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the `naomi:sync-at-time:timesyncsensor` sensor:

<div class="td-content">

<!-- prettier-ignore -->
| Name    | Type   | Required? | Description |
| ------- | ------ | --------- | ----------- |
| `start` | string | **Required** | The start time for the time frame during which you want to sync. Example: `"14:10:00"`.  |
| `end`   | string | **Required** | The end of the sync time frame, for example: `"15:35:00"`. |
| `zone`  | string | **Required** | The time zone for the `start` and `end` time, for example: `"CET"`. |

{{< /tablestep >}}
{{< /table >}}

<div>
<br>

In the next step you will configure the data manager to take the sensor into account when syncing.

#### Configure the data manager to sync based on sensor

On your machine's **CONFIGURE** tab, switch to **JSON** mode and add a `selective_syncer_name` with the name for the sensor you configured and add the sensor to the `depends_on` field:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers" data-line="9,14"}
{
  "name": "data_manager-1",
  "type": "data_manager",
  "namespace": "rdk",
  "attributes": {
    "additional_sync_paths": [],
    "capture_dir": "",
    "capture_disabled": false,
    "selective_syncer_name": "<SENSOR-NAME>",
    "sync_disabled": false,
    "sync_interval_mins": 0.1,
    "tags": []
  },
  "depends_on": ["<SENSOR-NAME>"]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="7,12"}
{
  "name": "datamanager",
  "type": "data_manager",
  "namespace": "rdk",
  "attributes": {
    "additional_sync_paths": [],
    "selective_syncer_name": "timesensor",
    "sync_interval_mins": 0.2,
    "capture_dir": "",
    "tags": []
  },
  "depends_on": ["timesensor"]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% expand "Click to view a full configuration example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="29-40,43-55,80-85"}
{
  "components": [
    {
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "FDF90FEB-59E5-4FCF-AABD-DA03C4E19BFB"
      },
      "depends_on": [],
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 0.2,
                "method": "ReadImage",
                "additional_params": {
                  "mime_type": "image/jpeg"
                }
              }
            ]
          }
        }
      ],
      "name": "webcam",
      "model": "webcam"
    },
    {
      "attributes": {
        "start": "14:10:00",
        "end": "15:35:00",
        "zone": "CET"
      },
      "depends_on": [],
      "name": "timesensor",
      "model": "naomi:sync-at-time:timesyncsensor",
      "type": "sensor",
      "namespace": "rdk"
    }
  ],
  "services": [
    {
      "namespace": "rdk",
      "depends_on": ["timesensor"],
      "attributes": {
        "additional_sync_paths": [],
        "selective_syncer_name": "timesensor",
        "sync_interval_mins": 0.2,
        "capture_dir": "",
        "tags": []
      },
      "name": "datamanager",
      "type": "data_manager"
    }
  ],
  "agent": {
    "viam-server": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false
    },
    "agent-provisioning": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false
    },
    "viam-agent": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false
    }
  },
  "modules": [
    {
      "module_id": "naomi:sync-at-time",
      "version": "0.0.2",
      "type": "registry",
      "name": "naomi_sync-at-time"
    }
  ]
}
```

{{% /expand%}}

You have now configured sync to happen during a specific time slot.

### Test your sync configuration

To test your setup, [configure a webcam](/components/camera/webcam/) or another component and [enable data capture on the component](/services/data/capture/#configure-data-capture-for-individual-resources).
For a camera component, use the `ReadImage` method.
The data manager will now capture data.
Go to the [**CONTROL** tab](/fleet/control/).
You should see the sensor.
Click on `GetReadings`.

{{<imgproc src="/services/data/timesensor.png" resize="800x" declaredimensions=true alt="Control tab with sensor panel">}}

If you are in the time frame for sync, the time sync sensor will return true.
You can confirm that no data is currently syncing by going to the [**Data** tab](https://app.viam.com/data/view).
If you are not in the time frame for sync, adjust the configuration of your time sync sensor.
Then check again on the **CONTROL** and **Data** tab to confirm data is syncing.

## Next steps

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{% card link="/how-tos/create-module/" %}}
{{% manualcard link="https://github.com/viam-labs/trigger-sync-examples-v2" %}}

<h4>Sync Trigger Examples</h4>

Other example code for modules that trigger sync.

{{% /manualcard %}}
{{< /cards >}}
