---
title: "Trigger Cloud Sync Conditionally"
linkTitle: "Trigger Sync"
description: "Trigger cloud sync to sync captured data conditionally."
weight: 20
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Alexa Greenberg
---

You can use a {{< glossary_tooltip term_id="module" text="module" >}} to sync data only when a certain logic condition is met, instead of at a regular time interval.
For example, if you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.
Or, you may want to trigger sync only when your machine detects an object of a certain color.
The code for both of these examples is provided by the [trigger-sync-examples module](https://github.com/viam-labs/trigger-sync-examples-v2), and you can [create your own module](/registry/create/) if you want to use different logic.

{{% alert title="Note: How sync is triggered" color="note" %}}

Regardless of the specifics of your trigger sync logic, to trigger sync you need to pass `true` to the [CreateShouldSyncReading function](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#CreateShouldSyncReading) within the definition of your modular sensor's `Readings` function.
See examples in the `Readings` function of the [time-interval-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/time-interval-trigger/selective_sync/selective_sync.go) and the [color-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/color-trigger/selective_sync/selective_sync.go).

{{% /alert %}}

## Example: `sync-at-time`

This module allows you to configure cloud sync to occur only at a specific time frame by implementing a sensor, `naomi:sync-at-time:timesyncsensor`, that enables sync within a specified time frame and disables sync outside that time frame.

To set up conditional syncing you need to:

1. Create or use an existing module that implements a `sensor` component that uses your custom logic to determine when to enable and disable sync.
   While this sensor is not sensing the time it _senses_ whether the data manager should sync or not.
2. Change the configuration of the data manager to enable selective sync.

### Requirements

Before configuring your sensor, you must [create a machine](https://docs.viam.com/fleet/machines/#add-a-new-machine) and you also need to:

1. Enable [data capture](https://docs.viam.com/data/capture/).
2. Enable [cloud sync](https://docs.viam.com/data/cloud-sync/).

### Add sensor to determine when to sync

In this example, you will configure sync to only trigger during a specific time frame of the day using an existing module [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time).
If you need to trigger sync based on a different condition, you need to create your own module and adjust the module logic accordingly.
Additional examples are available in this [GitHub Repo](https://github.com/viam-labs/trigger-sync-examples-v2).

To use [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time):

1. Go to your machine's **CONFIGURE** page and click **Create component**.
2. Then select the `sync-at-time:timesyncsensor` model from the [`sync-at-time` module](https://app.viam.com/module/naomi/sync-at-time).
3. Click **Add module**, then enter a name or use the automatically suggested name for your sensor and click **Create**.
   The sensor will return true and enable sync when in a specified time frame.
4. To configure your time frame, go to the new component panel and copy and paste the following attribute template into your sensor’s **Attributes** box:

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

<!-- prettier-ignore -->
| Name    | Type   | Inclusion    | Description |
| ------- | ------ | ------------ | ----------- |
| `start` | string | **Required** | The start time for the time frame during which you want to sync. Example: `"14:10:00"`.  |
| `end`   | string | **Required** | The end of the sync time frame, for example: `"15:35:00"`. |
| `zone`  | string | **Required** | The time zone for the `start` and `end` time, for example: `"CET"`. |

In the next step you will configure the data manager to take the sensor into account when syncing.

#### Configure data manager to sync based on sensor

On your machine's **CONFIGURE** tab, switch to **JSON** mode and add a `selective_syncer_name` with the name for the sensor you configured and add the sensor to the `depends_on` field:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers" data-line="9,14"}
{
  "name": "Data-Management-Service",
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
  "agent_config": {
    "subsystems": {
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

To test your setup, [configure a webcam](https://docs.viam.com/components/camera/webcam/) or another component and [enable data capture on the component](https://docs.viam.com/data/capture/#configure-data-capture-for-individual-components).
For a camera component, use the `ReadImage` method.
The data manager will now capture data.
Go to the [**CONTROL** tab](https://docs.viam.com/fleet/machines/#control).
You should see the sensor.
Click on `GetReadings`.

{{<imgproc src="/data/timesensor.png" resize="800x" declaredimensions=true alt="Control tab with sensor panel">}}

If you are in the time frame for sync, the time sync sensor will return true.
You can confirm that no data is currently syncing by going to the [**Data** tab](https://app.viam.com/data/view).
If you are not in the time frame for sync, adjust the configuration of your time sync sensor.
Then check again on the **CONTROL** and **Data** tab to confirm data is syncing.

## Next steps

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{% card link="/registry/create" %}}
{{% manualcard link="https://github.com/viam-labs/trigger-sync-examples-v2" %}}

<h4>Sync Trigger Examples</h4>

Other example code for modules that trigger sync.

{{% /manualcard %}}
{{< /cards >}}
