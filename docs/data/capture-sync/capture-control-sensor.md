---
title: "Control capture with a sensor"
linkTitle: "Control capture with a sensor"
description: "Change what a machine captures, and how often, based on a sensor's readings."
capabilities: ["data-capture"]
diataxis: how-to
type: "docs"
weight: 12
tags: ["data management", "capture", "sensor"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data"]
date: "2026-09-29"
---

A capture control sensor lets a sensor on your machine decide, while the machine runs, which resources the data management service captures from and how often.
Use one to capture only around events, to capture faster when something interesting happens, or to switch capture on for a resource that has no data capture configured.

This page shows how to write the sensor and connect it to the data management service.
To conditionally _sync_ data rather than control capture, see [Conditional sync](/data/capture-sync/conditional-sync/).

## Before you start

- A machine running `viam-server` with a [data management service](/data/capture-sync/capture-and-sync-data/) configured.
- A sensor you can change or write.
  The sensor can be any `sensor` component whose `Readings` method returns the keys described below.
  See [Write a module](/build-modules/write-a-driver-module/) to build one.

## How a capture control sensor works

The data management service polls the sensor's `Readings` method 10 times per second.
Each poll returns a list of overrides under a key you choose.
The service merges each override with the capture settings from the machine config and starts, changes, or stops collectors to match.

Overrides apply on top of the machine config and don't replace it.
When the sensor stops listing a resource, the service returns that resource to its configured capture settings.
If the resource has no configured capture, it stops capturing.

## Return an overrides list

In your sensor's `Readings` method, return a list under the key you choose.
Each entry in the list has these fields:

| Field                  | Type             | Required? | Description                                                                                                                                                                      |
| ---------------------- | ---------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_name`        | string           | Required  | Name of the resource to capture from, for example `my-camera`. Use the short name, without a remote part prefix.                                                                 |
| `method`               | string           | Required  | Capture method, for example `GetImages` or `Readings`.                                                                                                                           |
| `capture_frequency_hz` | float            | Optional  | Capture frequency for this resource and method. `0` disables capture. If you omit it, the resource keeps its configured frequency. Required to capture an unconfigured resource. |
| `tags`                 | array of strings | Optional  | Tags for data captured from this resource and method. Replaces the data management service's `tags` for this resource.                                                           |

The following `Readings` method returns an override that captures `my-camera` at 5 Hz while a `recording` flag is set.
The flag is a Python attribute on the sensor that your own code, such as a `DoCommand` handler, sets:

```python
    async def get_readings(self, *, extra=None, timeout=None, **kwargs):
        if not self.recording:
            return {"overrides": []}
        return {
            "overrides": [
                {
                    "resource_name": "my-camera",
                    "method": "GetImages",
                    "capture_frequency_hz": 5,
                    "tags": ["event"],
                }
            ]
        }
```

## Set the capture control sensor on the data manager

Tell the data management service which sensor to poll, and which key in its readings holds the overrides.

1. On your machine's **CONFIGURE** tab, find your data management service.
2. Switch to **JSON** mode, or open the service's attributes.
3. Add the `capture_control_sensor` attribute, with the sensor's name and the key it returns:

   ```json
   {
     "capture_control_sensor": {
       "name": "my-capture-sensor",
       "key": "overrides"
     }
   }
   ```

4. Add the sensor to the data management service's `depends_on` field so it starts first.
5. Click **Save**.

`name` is the sensor's resource name.
`key` is required, even if you only use the sensor to record [sequences](/data/sequences/).

Within a moment, the service starts applying the sensor's readings.
Check the machine's **LOGS** tab for messages that begin `capture control sensor enabling capture for`.

## Capture from resources the data manager doesn't list

An override can turn on capture for a resource that has no data capture configured.
The service finds the resource by name and starts a collector for the method you name.

For this to work:

- Set `capture_frequency_hz` to a value greater than `0`.
- Use a method that the resource supports for data capture.
  See [Supported resources](/data/capture-sync/capture-and-sync-data/#supported-resources).
- Don't name a method that needs extra parameters.
  The board methods `Analogs` and `Gpios` need parameters, so an override can't enable them.

If the service can't find the resource, or the method isn't capturable, it logs a warning and skips that entry.

## What happens when the sensor fails

If `Readings` returns an error, or its output can't be parsed, the service reverts every resource to its machine config.
It logs a warning and keeps polling, so capture picks up again as soon as the sensor returns valid readings.

If the sensor isn't found at startup, the service logs an error and the capture control sensor has no effect until you fix the config.

## Next steps

- [Group captured data into sequences](/data/sequences/): return a second key from the same sensor to record time windows of data.
- [Data management service reference](/data/reference/#capture-control-sensor-readings): all readings fields.
- [Conditional sync](/data/capture-sync/conditional-sync/): control when captured data uploads.
