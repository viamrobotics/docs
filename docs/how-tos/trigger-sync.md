---
title: "Trigger cloud sync conditionally"
linkTitle: "Trigger data sync conditionally"
description: "Trigger cloud sync to sync captured data when custom conditions are met."
type: "docs"
tags: ["data management", "cloud", "sync"]
images: ["/services/icons/data-cloud-sync.svg"]
icon: true
aliases:
  - /data/trigger-sync/
  - /services/data/trigger-sync/
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "registry"]
level: "Intermediate"
date: "2024-09-02"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You may want to sync data only when a certain logic condition is met, instead of at a regular time interval.
For example, if you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.
Or, you may want to trigger sync only when your machine detects an object of a certain color.
You can use the [trigger-sync-examples module](https://github.com/viam-labs/trigger-sync-examples-v2) if one of these examples is what you are looking for.

If you need different logic, this guide will show you the implementation of the [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time) module which triggers cloud sync based on a defined time interval.
You can use it as the basis of your own custom logic.

{{% alert title="In this page" color="tip" %}}

1. [Use the `CreateShouldSyncReading` function to enable sync](#use-the-createshouldsyncreading-function-to-enable-sync)
1. [Add and configure sensor to determine when to sync](#add-your-sensor-to-determine-when-to-sync)
1. [Configure the data manager to sync based on the sensor](#configure-the-data-manager-to-sync-based-on-sensor)
1. [Test your sync configuration](#test-your-sync-configuration)

{{% /alert %}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "Enable data capture and sync on your machine." >}}

Add the [data management service](/services/data/):

On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{< /expand >}}

{{% expand "Create a sensor module. Click to see instructions." %}}

Start by [creating a sensor module](/how-tos/sensor-module/).
Your sensor should have access to the information you need to determine if your machine should sync or not.
Based on that data, make the sensor return true when the machine should sync and false when it should not.
For example, if your want your machine to return data only during a specific time interval, your sensor needs to be able to access the time as well as be configured with the time interval during which you would like to sync data.
It can then return true during the specified sync time interval and false otherwise.

{{% /expand%}}

## Use the `CreateShouldSyncReading` function to enable sync

Regardless of the specifics of your trigger sync logic, to trigger sync your sensor needs to pass `true` to the [CreateShouldSyncReading function](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#CreateShouldSyncReading) within the definition of your modular sensor's `Readings` function.

The `sync-at-time` sensor does not sense time despite being named a time sensor.
It _senses_ whether the data manager should sync or not and determines this based on the time of day.
During the configured time of the day, the code will pass `true` to the [CreateShouldSyncReading function](https://pkg.go.dev/go.viam.com/rdk/services/datamanager#CreateShouldSyncReading) which will enable syncing:

```go {class="line-numbers linkable-line-numbers" data-line="7,12,28"}
func (s *timeSyncer) Readings(context.Context, map[string]interface{}) (map[string]interface{}, error) {
    currentTime := time.Now()
    var hStart, mStart, sStart, hEnd, mEnd, sEnd int
    n, err := fmt.Sscanf(s.start, "%d:%d:%d", &hStart, &mStart, &sStart)
    if err != nil || n != 3 {
        s.logger.Error("Start time is not in the format HH:MM:SS.")
        return datamanager.CreateShouldSyncReading(false), err
    }
    m, err := fmt.Sscanf(s.end, "%d:%d:%d", &hEnd, &mEnd, &sEnd)
    if err != nil || m != 3 {
        s.logger.Error("End time is not in the format HH:MM:SS.")
        return datamanager.CreateShouldSyncReading(false), err
    }

    zone, err := time.LoadLocation(s.zone)
    if err != nil {
        s.logger.Error("Time zone cannot be loaded: ", s.zone)
    }

    startTime := time.Date(currentTime.Year(), currentTime.Month(), currentTime.Day(),
        hStart, mStart, sStart, 0, zone)
    endTime := time.Date(currentTime.Year(), currentTime.Month(), currentTime.Day(),
        hEnd, mEnd, sEnd, 0, zone)

    // If it is between the start and end time, sync.
    if currentTime.After(startTime) && currentTime.Before(endTime) {
        s.logger.Info("Syncing")
        return datamanager.CreateShouldSyncReading(true), nil
    }

    // Otherwise, do not sync.
    return datamanager.CreateShouldSyncReading(false), nil
}
```

If you wish to see more context, see the entire [implementation of the sensor on GitHub](https://github.com/viam-labs/sync-at-time/blob/main/timesyncsensor/timesyncsensor.go).

For additional examples, see the `Readings` function of the [time-interval-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/time-interval-trigger/selective_sync/selective_sync.go) and the [color-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/color-trigger/selective_sync/selective_sync.go).

## Add your sensor to determine when to sync

Add your module to your machine and configure it.
In this example we will continue to use [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time).
You will need to follow the same steps with your module:

{{< table >}}
{{% tablestep %}}
**1. Add the sensor to your machine**

On your machine's **CONFIGURE** page, click the **+** button next to your machine part in the left menu.
Select **Component**, then search for and select the `sync-at-time:timesyncsensor` model provided by the [`sync-at-time` module](https://app.viam.com/module/naomi/sync-at-time).

Click **Add module**, then enter a name or use the suggested name for your sensor and click **Create**.

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep link="https://github.com/viam-labs/sync-at-time" %}}
**2. Configure your time frame**

Go to the new component panel and copy and paste the following attribute template into your sensor’s attributes field:

{{< tabs >}}
{{% tab name="Template" %}}

```json
{
  "start": "HH:MM:SS",
  "end": "HH:MM:SS",
  "zone": "<TIMEZONE>"
}
```

{{% /tab %}}
{{% tab name="Example" %}}

```json
{
  "start": "18:29:00",
  "end": "18:30:00",
  "zone": "CET"
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

</div>
<br>

In the next step you will configure the data manager to take the sensor into account when syncing.

## Configure the data manager to sync based on sensor

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
    "sync_interval_mins": 0.1,
    "capture_dir": "",
    "tags": []
  },
  "depends_on": ["timesensor"]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% expand "Click to view a full configuration example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="12-22,25-37,40-45"}
{
  "components": [
    {
      "name": "camera-1",
      "namespace": "rdk",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "0x114000005a39331"
      }
    },
    {
      "name": "timesensor",
      "namespace": "rdk",
      "type": "sensor",
      "model": "naomi:sync-at-time:timesyncsensor",
      "attributes": {
        "start": "18:29:00",
        "end": "18:30:00",
        "zone": "CET"
      }
    }
  ],
  "services": [
    {
      "name": "data_manager-1",
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": [],
        "selective_syncer_name": "timesensor",
        "sync_interval_mins": 0.1
      },
      "depends_on": ["timesensor"]
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "naomi_sync-at-time",
      "module_id": "naomi:sync-at-time",
      "version": "2.0.0"
    }
  ]
}
```

{{% /expand%}}

You have now configured sync to happen during a specific time slot.

## Test your sync configuration

To test your setup, [configure a webcam](/components/camera/webcam/) or another component and [enable data capture on the component](/services/data/#configuration).
Make sure to physically connect any hardware parts to the computer controlling your machine.
For a camera component, use the `ReadImage` method.
The data manager will now capture data.
Go to the [**CONTROL** tab](/fleet/control/).
You should see the sensor.
Click on `GetReadings`.

{{<imgproc src="/services/data/timesensor.png" resize="800x" declaredimensions=true alt="Control tab with sensor panel">}}

If you are in the time frame for sync, the time sync sensor will return true.

You can confirm that if data is currently syncing by going to the [**Data** tab](https://app.viam.com/data/view).
If you are not in the time frame for sync, adjust the configuration of your time sync sensor.
Then check again on the **CONTROL** and **Data** tab to confirm data is syncing.

## Next steps

You can now use custom logic to trigger sync conditionally.
For more information, see:

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{% card link="/how-tos/sensor-module/" %}}
{{% card link="/how-tos/create-module/" %}}
{{% manualcard link="https://github.com/viam-labs/trigger-sync-examples-v2" %}}

<h4>Sync Trigger Examples</h4>

Other example code for modules that trigger sync.

{{% /manualcard %}}
{{< /cards >}}
