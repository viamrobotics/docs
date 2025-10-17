---
title: "Conditional cloud sync"
linkTitle: "Conditional sync"
description: "Trigger cloud sync to sync captured data when custom conditions are met."
type: "docs"
weight: 20
tags: ["data management", "cloud", "sync"]
images: ["/services/icons/data-cloud-sync.svg"]
icon: true
aliases:
  - /data/trigger-sync/
  - /how-tos/trigger-sync/
  - /services/data/trigger-sync/
  - /how-tos/conditional-sync/
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "registry"]
date: "2024-12-04"
updated: "2025-09-05"
---

By default, `viam-server` checks for new data to sync at the configured interval (`sync_interval_mins`).
You can additionally configure sync to only happen when certain conditions are met.
For example:

- Only sync when on WiFi
- Sync when conditions are met or events are detected
- Sync during certain time windows

To sync only when certain conditions are met you must provide the data manager a sensor that returns `"should_sync": true` when sync should happen and `"should_sync": false` otherwise.

This page will show you the implementation of a sensor which only allows sync during a defined time interval.
You can use it as the basis of your own custom logic.

You can also view [trigger-sync-examples module](https://github.com/viam-labs/trigger-sync-examples-v2) for more examples.

## Prerequisites

{{% expand "A running machine connected to Viam. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "Enable data capture and sync on your machine." >}}

Add the [data management service](/data-ai/capture-data/capture-sync/#configure-data-capture-and-sync-for-individual-resources):

On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{< /expand >}}

{{% expand "Create a sensor module. Click to see instructions." %}}

Start by [creating a sensor module](/operate/modules/support-hardware/).

Your sensor should have access to the information you need to determine if your machine should sync or not.
Based on that data, make the sensor return true when the machine should sync and false when it should not.

For example, if your want your machine to return data only during a specific time interval, your sensor needs to be able to access the time as well as be configured with the time interval during which you would like to sync data.
It can then return true during the specified sync time interval and false otherwise.

{{% /expand%}}

## Return `should_sync` as a reading from a sensor

The following example implementation of the `Readings()` method returns `"should_sync": true` if the current time is in a specified time window, and `"should_sync": false` otherwise.

```go {class="line-numbers linkable-line-numbers" data-line="26,31,32,37"}
func (s *timeSyncer) Readings(context.Context, map[string]interface{}) (map[string]interface{}, error) {
    currentTime := time.Now()
    var hStart, mStart, sStart, hEnd, mEnd, sEnd int
    n, err := fmt.Sscanf(s.start, "%d:%d:%d", &hStart, &mStart, &sStart)

    if err != nil || n != 3 {
        s.logger.Error("Start time is not in the format HH:MM:SS.")
        return nil, err
    }
    m, err := fmt.Sscanf(s.end, "%d:%d:%d", &hEnd, &mEnd, &sEnd)
    if err != nil || m != 3 {
        s.logger.Error("End time is not in the format HH:MM:SS.")
        return nil, err
    }

    zone, err := time.LoadLocation(s.zone)
    if err != nil {
        s.logger.Error("Time zone cannot be loaded: ", s.zone)
    }

    startTime := time.Date(currentTime.Year(), currentTime.Month(), currentTime.Day(),
        hStart, mStart, sStart, 0, zone)
    endTime := time.Date(currentTime.Year(), currentTime.Month(), currentTime.Day(),
        hEnd, mEnd, sEnd, 0, zone)

    readings := map[string]interface{}{"should_sync": false}
    readings["time"] = currentTime.String()
    // If it is between the start and end time, sync.
    if currentTime.After(startTime) && currentTime.Before(endTime) {
        s.logger.Debug("Syncing")
        readings["should_sync"] = true
        return readings, nil
    }

    // Otherwise, do not sync.
    s.logger.Debug("Not syncing. Current time not in sync window: " + currentTime.String())
    return readings, nil
}
```

{{< alert title="Note" color="note" >}}
You can return other readings alongside the `should_sync` value.
{{< /alert >}}

You must also update the `Config` and resource struct to include the required attributes and update the `init()` and `Validate()` functions appropriately.
Check the [implementation of the sensor on GitHub](https://github.com/viam-labs/sync-at-time/blob/main/module.go) for more detailed information.

For additional examples, see the `Readings` function of the [time-interval-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/time-interval-trigger/selective_sync/selective_sync.go) and the [color-trigger code](https://github.com/viam-labs/trigger-sync-examples-v2/blob/main/color-trigger/selective_sync/selective_sync.go).

## Add your sensor to determine when to sync

Add your module to your machine and configure it.
In this example we will continue to use [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time).
You will need to follow the same steps with your module:

{{< table >}}
{{% tablestep start=1 %}}
**Add the sensor to your machine**

On your machine's **CONFIGURE** page, click the **+** button next to your machine part in the left menu.
Select **Component or service**, then search for and select the `sync-at-time:timesyncsensor` model provided by the [`sync-at-time` module](https://app.viam.com/module/naomi/sync-at-time).

Click **Add module**, then enter a name or use the suggested name for your sensor and click **Create**.

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep %}}
**Configure your time frame**

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
  "api": "rdk:service:data_manager",
  "model": "rdk:builtin:builtin",
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
  "api": "rdk:service:data_manager",
  "model": "rdk:builtin:builtin",
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

```json {class="line-numbers linkable-line-numbers" data-line="12-21,25-37,40-45"}
{
  "components": [
    {
      "name": "camera-1",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {
        "video_path": "0x114000005a39331"
      }
    },
    {
      "name": "timesensor",
      "api": "rdk:component:sensor",
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
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
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
      "version": "3.0.3"
    }
  ]
}
```

{{% /expand%}}

You have now configured sync to happen during a specific time slot.

## Test your sync configuration

To test your setup, [configure a webcam](/operate/reference/components/camera/webcam/) or another component and [enable data capture on the component](/data-ai/capture-data/capture-sync/#configure-data-capture-and-sync-for-individual-resources).
Make sure to physically connect any hardware parts to the computer controlling your machine.
For a camera component, use the `ReadImage` method.
The data manager will now capture data.
Go to the [**CONTROL** tab](/manage/troubleshoot/teleoperate/default-interface/#web-ui).
You should see the sensor.
Click on `GetReadings`.

{{<imgproc src="/services/data/timesensor.png" resize="800x" declaredimensions=true alt="Control tab with sensor panel" style="width: 500px" class="imgzoom shadow" >}}

If you are in the time frame for sync, the time sync sensor will return true.

If data is currently syncing, go to the [**Data** tab](https://app.viam.com/data/view) to see your data.
If you are not in the time frame for sync, adjust the configuration of your time sync sensor.
Then check again on the **CONTROL** and **Data** tab to confirm data is syncing.
