---
title: "Conditional sync"
linkTitle: "Conditional sync"
description: "Control when captured data syncs to the cloud using a sensor that decides whether to sync."
type: "docs"
weight: 7
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

By default, the data management service syncs all captured data at a regular interval. Conditional sync lets you add custom logic that controls _whether_ sync proceeds at each interval, so data accumulates locally until your conditions are met. Use this to sync only during off-peak hours, when connected to WiFi, or after a specific event.

## Concepts

### The selective syncer mechanism

Conditional sync works through the [sensor API](/reference/components/sensor/).
You configure a sensor component whose `Readings()` method returns `"should_sync": true` or `"should_sync": false`.
At each sync interval, the data manager calls `Readings()` on this sensor before uploading.
If the result includes `"should_sync": true`, sync proceeds.
If `"should_sync": false`, the cycle is skipped and data continues to accumulate locally.

The sensor is the only mechanism for conditional sync. There is no built-in rules engine or config-only option.
Any logic you need (time-of-day windows, network status, sensor thresholds, external APIs) goes in your sensor's `Readings()` implementation.
You wire it up by setting `selective_syncer_name` in the data management service config.

{{< alert title="Important" color="caution" >}}
If `selective_syncer_name` is configured but the sensor cannot be found, **scheduled sync is disabled** until the sensor becomes available.
Make sure the sensor is correctly configured and added to the data manager's `depends_on` field.
{{< /alert >}}

## Example: sync during a time window

This example uses the [`sync-at-time:timesyncsensor`](https://app.viam.com/module/naomi/sync-at-time) module to sync data only during a configured time window.
You can substitute any sensor that returns `should_sync`. The data manager configuration is the same.

### Add the sync sensor

1. On your machine's **CONFIGURE** tab, click **+** next to your machine part and select **Component or service**.
2. Search for and select the `sync-at-time:timesyncsensor` model.
   Click **Add module**, enter a name (for example, `timesensor`), and click **Create**.
3. Configure the time window in the sensor's attributes:

   ```json
   {
     "start": "18:29:00",
     "end": "18:30:00",
     "zone": "CET"
   }
   ```

   | Name    | Type   | Required | Description                                                                   |
   | ------- | ------ | -------- | ----------------------------------------------------------------------------- |
   | `start` | string | **Yes**  | Start of the sync window in `HH:MM:SS` format.                                |
   | `end`   | string | **Yes**  | End of the sync window in `HH:MM:SS` format.                                  |
   | `zone`  | string | **Yes**  | Time zone for `start` and `end` (for example, `"CET"`, `"America/New_York"`). |

4. Click **Save**.

### Configure the data manager

Switch to **JSON** mode on your machine's **CONFIGURE** tab.
In the data management service config, set `selective_syncer_name` to your sensor's name and add the sensor to `depends_on`:

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

## Build a custom sync sensor

If no existing module fits your use case, you can build a custom module that implements the [sensor API](/reference/components/sensor/) (`rdk:component:sensor`).
The data manager calls `Readings()` on the sensor and looks for a `"should_sync"` key with a boolean value.
The sensor can return additional readings alongside `should_sync`.

The RDK provides a helper function for building sync sensors: `datamanager.CreateShouldSyncReading(bool)` returns a properly formatted readings map.

1. Follow the [module development guide](/build-modules/write-a-driver-module/) to create a sensor module.
2. Implement `Readings()` to return `"should_sync": true` when sync should proceed and `"should_sync": false` otherwise.
3. Deploy the module and [configure the data manager](#configure-the-data-manager) with your sensor's name.

For a reference implementation, see the [sync-at-time source code](https://github.com/viam-labs/sync-at-time/blob/main/module.go).
