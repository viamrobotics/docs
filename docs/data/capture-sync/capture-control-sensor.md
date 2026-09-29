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

## How a capture control sensor works

The data management service polls the sensor's `Readings` method 10 times per second.
Each poll returns a list of overrides under a key you choose.
The service merges each override with the capture settings you configured on the component, and starts, changes, or stops capture to match.

Overrides apply on top of your configured capture settings and don't replace them.
When the sensor stops listing a resource, that resource returns to its configured capture settings.
If it has none, it stops capturing.

## 1. Choose a capture control sensor

You can use the `capture-control` module, or write a sensor of your own.

|            | `capture-control` module                                                                                      | Your own sensor                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Best when  | Something outside the machine decides when to record: a button, a script, a workflow step, or you in the app. | The machine decides by itself, for example from another sensor's readings, a vision detection, or a schedule. |
| Trigger    | You send `DoCommand` calls.                                                                                   | Any logic in `Readings`.                                                                                      |
| Components | A fixed list in the config, all with one frequency and one set of tags.                                       | Any list, changing at any time, each with its own frequency and tags.                                         |
| Sequences  | One sequence at a time.                                                                                       | As many as you return.                                                                                        |
| Effort     | Configuration only.                                                                                           | You write and deploy a [module](/build-modules/write-a-driver-module/).                                       |

Start with the module unless you need one of the right-hand column's abilities.
The module is experimental, so its commands might change.

### Option A: use the `capture-control` module

1. On your machine's **CONFIGURE** tab, click **+**, select **Blocks**, search for **capture-control**, and select the sensor from the `viam` namespace.
2. Name it `my-capture-sensor` and click **Add to machine**.
3. In the sensor's attributes, list the components and methods to control:

   ```json
   {
     "resources": [
       { "resource_name": "my-camera", "method": "GetImages" },
       { "resource_name": "my-sensor", "method": "Readings" }
     ],
     "default_tags": ["event"]
   }
   ```

   | Attribute                      | Required? | Description                                                                                                                                                                                                                   |
   | ------------------------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `resources`                    | Required  | The components and methods to control. At least one.                                                                                                                                                                          |
   | `default_capture_frequency_hz` | Optional  | Frequency the sensor sends from startup until the first `start_capture`, and when `start_capture` doesn't give one. Default `0`, which captures nothing. Any other value captures continuously until you send `stop_capture`. |
   | `default_tags`                 | Optional  | Tags used when `start_capture` doesn't give any.                                                                                                                                                                              |

4. Click **Save**.

{{< alert title="The module turns capture off between recordings" color="caution" >}}
While the module isn't recording, it tells the data management service to capture the components in `resources` at 0 Hz.
The exception is `default_capture_frequency_hz`: if you set it above `0`, the module captures at that frequency from startup, and after any configuration change, until you send `stop_capture`.
This overrides any capture you configured on those components, so they capture only while you record.
{{< /alert >}}

Control the module with `DoCommand`, from the sensor's **Test** section or from code.
Each command is a key set to `true`, with optional arguments beside it:

| Command                                                         | What it does                                                                                          |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `{"start_capture": true, "frequency_hz": 2, "tags": ["run-1"]}` | Starts capture at the frequency, tagged, and opens a [sequence](/data/sequences/) with the same tags. |
| `{"stop_capture": true}`                                        | Stops capture and closes the sequence.                                                                |
| `{"start_sequence": true, "tags": ["run-1"]}`                   | Opens a sequence without changing capture. Use it when capture is already running.                    |
| `{"stop_sequence": true}`                                       | Closes the sequence and leaves capture unchanged.                                                     |

`frequency_hz` and `tags` are optional on `start_capture`.
If you leave out `frequency_hz` and `default_capture_frequency_hz` is `0`, the sequence opens but nothing is captured.
Sending `start_capture` again with different tags closes the open sequence and opens a new one.
The sensor forgets its state when its configuration changes.

### Option B: write your own sensor

In your sensor's `Readings` method, return a list under a key you choose.
Each entry in the list has these fields:

| Field                  | Type             | Required? | Description                                                                                                                                                                                                                                  |
| ---------------------- | ---------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_name`        | string           | Required  | Name of the component or service to capture from, for example `my-camera`. Use the short name, without a remote part prefix.                                                                                                                 |
| `method`               | string           | Required  | Capture method, for example `GetImages` or `Readings`.                                                                                                                                                                                       |
| `capture_frequency_hz` | float            | Optional  | Capture frequency for this resource and method. `0` disables capture. If you omit it, capture uses the frequency you set in the resource's own **Data capture** section. A resource with no capture configured has none, so you must set it. |
| `tags`                 | array of strings | Optional  | Tags for data captured from this resource and method. Replaces the data management service's `tags` for this resource.                                                                                                                       |

The following sensor captures `my-camera` at 5 Hz while it is recording.
You turn recording on and off by sending the sensor a `start` or `stop` command with `DoCommand`:

```python
    recording = False

    async def do_command(self, command, *, timeout=None, **kwargs):
        if command.get("command") == "start":
            self.recording = True
        elif command.get("command") == "stop":
            self.recording = False
        return {"recording": self.recording}

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

Deploy the sensor as a module and add it to your machine with `viam module reload-local`.
The command adds the sensor to your machine's configuration, using the resource name you pass in `--resource-name`.
See [Test locally](/build-modules/write-a-driver-module/#3-test-locally) and [Write a module](/build-modules/write-a-driver-module/).

## 2. Point the data manager at the sensor

The sensor must already be on your machine.
Tell the data management service which sensor to poll, and which key in its readings holds the overrides.
The `capture-control` module uses the key `overrides`.

1. On your machine's **CONFIGURE** tab, find your data management service.
2. Switch to **JSON** mode.
3. In the service's `attributes`, add `capture_control_sensor` with the sensor's name and the key it returns:

   ```json
   "attributes": {
     "capture_control_sensor": {
       "name": "my-capture-sensor",
       "key": "overrides"
     }
   }
   ```

   `key` is required, even if you only use the sensor to record [sequences](/data/sequences/).

4. Next to `attributes`, in the service's own config, add the sensor's name to `depends_on`:

   ```json
   "depends_on": ["my-capture-sensor"]
   ```

   `depends_on` lists other resources that must be running before this one starts.
   With it, `viam-server` starts the sensor before the data management service.

5. Click **Save**.

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
