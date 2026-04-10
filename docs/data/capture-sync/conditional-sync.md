---
title: "Conditional sync"
linkTitle: "Conditional sync"
description: "Control when captured data syncs to the cloud using a sensor that decides whether to sync."
type: "docs"
weight: 10
tags: ["data management", "cloud", "sync"]
images: ["/services/icons/data-cloud-sync.svg"]
icon: true
aliases:
  - /data/conditional-sync/
  - /data-ai/capture-data/conditional-sync/
  - /data/trigger-sync/
  - /how-tos/trigger-sync/
  - /services/data/trigger-sync/
  - /how-tos/conditional-sync/
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "registry"]
date: "2024-12-04"
updated: "2025-12-04"
---

By default, the data management service syncs all captured data at a regular interval. Conditional sync lets you control _when_ sync happens, so data accumulates locally until your conditions are met: sync only during off-peak hours, when connected to WiFi, after a sensor reading crosses a threshold, or based on any other logic you define.

## How conditional sync works

Conditional sync uses a sensor component as a gate. You configure a sensor whose `Readings()` method returns `"should_sync": true` or `"should_sync": false`. At each sync interval, the data manager calls `Readings()` on this sensor before uploading. If the result is `true`, sync proceeds. If `false`, the cycle is skipped and data continues to accumulate locally.

The sensor is the only mechanism for conditional sync. There is no built-in rules engine or config-only option. Any logic you need goes in the sensor's `Readings()` implementation. You can use an existing sensor module from the registry or write your own.

{{< alert title="Important" color="caution" >}}
If `selective_syncer_name` is configured but the sensor cannot be found, **scheduled sync is disabled** until the sensor becomes available. Make sure the sensor is correctly configured and added to the data manager's `depends_on` field.
{{< /alert >}}

## Configure conditional sync

This example uses the [`sync-at-time/timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time) sensor module to sync data only during a configured time window. You can substitute any sensor that returns `should_sync`.

### 1. Add the sync sensor

1. On your machine's **CONFIGURE** tab, click **+** next to your machine part and select **Component or service**.
2. Search for **sync-at-time/timesyncsensor** and select the result.
3. Click **Add module**, enter a name (for example, `timesensor`), and click **Create**.
4. Configure the time window in the sensor's attributes:

   ```json
   {
     "start": "18:00:00",
     "end": "06:00:00",
     "zone": "America/New_York"
   }
   ```

   | Field   | Type   | Required | Description                                             |
   | ------- | ------ | -------- | ------------------------------------------------------- |
   | `start` | string | Yes      | Start of the sync window in `HH:MM:SS` format.          |
   | `end`   | string | Yes      | End of the sync window in `HH:MM:SS` format.            |
   | `zone`  | string | Yes      | Time zone (for example, `"CET"`, `"America/New_York"`). |

5. Click **Save**.

### 2. Point the data manager at the sensor

The `selective_syncer_name` field is not available in the UI. Switch to **JSON** mode on the **CONFIGURE** tab.

Find the data management service in your config and add two fields:

- `selective_syncer_name`: the name of your sync sensor
- `depends_on`: include the sensor name so the data manager waits for it to be available

```json {class="line-numbers linkable-line-numbers" data-line="7,12"}
{
  "name": "data_manager-1",
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

Click **Save**.

### 3. Verify conditional sync is working

1. Confirm data capture is running: check the machine's **LOGS** for capture activity.
2. If you are outside the sync window, data should accumulate locally but not appear in the **DATA** tab.
3. When the sync window opens, check the **DATA** tab. Captured data should begin appearing.
4. If data appears immediately regardless of the window, check that `selective_syncer_name` matches the sensor name exactly and that the sensor is in `depends_on`.

## Build a custom sync sensor

If no existing module fits your use case, you can write a sensor module that implements whatever sync logic you need: check network connectivity, compare sensor readings to a threshold, query an external API, or combine multiple conditions.

The sensor must implement the [sensor API](/reference/components/sensor/) and return a `"should_sync"` key with a boolean value from `Readings()`. The data manager checks this key at each sync interval. The sensor can return additional readings alongside `should_sync`.

The RDK provides a helper: `datamanager.CreateShouldSyncReading(bool)` returns a properly formatted readings map.

1. Follow the [module development guide](/build-modules/write-a-driver-module/) to create a sensor module.
2. Implement `Readings()` to return `"should_sync": true` when sync should proceed and `"should_sync": false` otherwise.
3. Deploy the module and [configure the data manager](#2-point-the-data-manager-at-the-sensor) with your sensor's name.
