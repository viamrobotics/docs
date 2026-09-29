---
title: "Start and stop capture on demand"
linkTitle: "Capture on demand"
description: "Start and stop capture on several components at once while the machine runs, and record sequences, with the capture-control module."
capabilities: ["data-capture", "sequences"]
diataxis: how-to
type: "docs"
weight: 7
tags: ["data management", "capture", "sensor"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data"]
date: "2026-09-29"
---

Record data only during the moments you care about, such as a demonstration, a test run, or a production cycle, instead of capturing all the time.
You start and stop recording with a command, and every component you list starts and stops together.

Use capture on demand to:

- Record [sequences](/data/sequences/), time windows of data that you train on as one example. This is the only way to record sequences from a running machine.
- Capture from several components together, only while something is happening.
- Turn on capture for a component that has no data capture configured.

To keep only camera frames where an ML model detects something, use a [filtered camera](/data/filter-at-the-edge/#use-a-filtered-camera-with-ml) instead.
To control when captured data uploads, rather than what is captured, see [Conditional sync](/data/capture-sync/conditional-sync/).

## Before you start

- A machine running `viam-server` with a data management service, such as `data_manager/builtin`, configured.
- The components you want to record, such as a camera and an arm, configured on the machine.

## How capture on demand works

The data management service can read capture settings from a sensor on the machine, called a capture control sensor.
It polls the sensor's `Readings` method 10 times per second and applies what the sensor returns: which components to capture, how often, with which tags, and which sequences are open.

The `capture-control` module is a ready-made capture control sensor.
You list the components it controls in its configuration, then send it `DoCommand` calls to start and stop recording.

The sensor's settings apply on top of the capture settings you configured on each component, and don't replace them.
When the sensor stops listing a component, the component returns to its own capture settings.
If it has none, it stops capturing.

## 1. Add the `capture-control` sensor {#add-the-sensor}

1. On your machine's **CONFIGURE** tab, click **+**, select **Blocks**, search for **capture-control**, and select the sensor from the `viam` namespace.
2. Name it `my-capture-sensor` and click **Add to machine**.
3. In the sensor's attributes, list the components and methods to record:

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

The module is experimental, so its commands might change.

{{< alert title="The module turns capture off between recordings" color="caution" >}}
While the module isn't recording, it tells the data management service to capture the components in `resources` at 0 Hz.
The exception is `default_capture_frequency_hz`: if you set it above `0`, the module captures at that frequency from startup, and after any configuration change, until you send `stop_capture`.
This overrides any capture you configured on those components, so they capture only while you record.
{{< /alert >}}

## 2. Point the data manager at the sensor {#point-the-data-manager-at-the-sensor}

Tell the data management service which sensor to poll, and which key in its readings holds the capture settings.
The `capture-control` module uses the key `overrides`.

1. On your machine's **CONFIGURE** tab, find your data management service.
2. Switch to **JSON** mode.
3. In the service's `attributes`, add `capture_control_sensor` with the sensor's name and key:

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

## 3. Start and stop recording {#start-and-stop-recording}

Send the sensor `DoCommand` calls from its **Test** section on the **CONFIGURE** tab, or from code.
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

To send the same commands from code or from a terminal, see the [sequences tutorial](/data/sequences-tutorial/#4-record-three-sequences).

To check that recording started, open the machine's **LOGS** tab and look for messages that begin `capture control sensor enabling capture for`.
After the next sync, the data appears on the **DATA** tab, and any sequences appear under **SEQUENCES**.

## Capture components that have no data capture configured

You can list a component in `resources` even if it has no data capture configured.
The data management service finds the component by name and starts capturing the method you name.

For this to work:

- Record at a frequency above `0`, from `frequency_hz` or `default_capture_frequency_hz`. The component has no configured frequency to fall back on.
- Use a method that the component supports for data capture.
  See [Supported resources](/data/capture-sync/capture-and-sync-data/#supported-resources).
- Don't name a method that needs extra parameters.
  The board methods `Analogs` and `Gpios` need parameters, so a capture control sensor can't enable them.

If the service can't find the component, or the method isn't capturable, it logs a warning and skips that entry.

## What happens when the sensor fails

If the sensor's `Readings` returns an error, or its output can't be parsed, the service reverts every component to its own capture settings.
It logs a warning and keeps polling, so capture picks up again as soon as the sensor returns valid readings.

If the sensor isn't found at startup, the service logs an error, and the sensor has no effect until you fix the config.

## Advanced: write your own capture control sensor {#write-your-own-sensor}

The `capture-control` module covers most uses: something outside the machine, such as a person, a script, or a workflow step, decides when to record.
If a script can watch for your condition and send `start_capture` and `stop_capture`, use the module and do that instead.

Write your own sensor only when you need one of these:

- **The machine decides by itself**, from another sensor's readings, a vision detection, or a schedule, without a separate process sending commands.
- **Different settings per component**, such as a camera at 10 Hz and a sensor at 1 Hz, or different tags on each.
- **More than one sequence open at the same time.**

Your sensor's `Readings` method returns two lists:

- Under a key you choose, a list of capture overrides. Each entry names a `resource_name` and `method`, and can set `capture_frequency_hz` and `tags`.
- Under the fixed key `sequences`, a list of open sequences. Each entry has a `resources` list and optional `sequence_tags`. A sequence opens the first time its entry appears, and closes when the entry disappears.

For every field, see [Capture control sensor readings](/data/reference/#capture-control-sensor-readings).

A sequence only selects data that was captured, so turn on capture for the same resources while a sequence is open.
The following sensor records `my-camera` and `my-sensor` at 5 Hz in one sequence while it is recording.
You turn recording on and off by sending it a `start` or `stop` command with `DoCommand`.
In your own sensor, replace that with whatever logic should decide:

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
            return {"overrides": [], "sequences": []}
        resources = [
            {"resource_name": "my-camera", "method": "GetImages"},
            {"resource_name": "my-sensor", "method": "Readings"},
        ]
        return {
            "overrides": [{**r, "capture_frequency_hz": 5} for r in resources],
            "sequences": [
                {"sequence_tags": ["demo-1"], "resources": resources},
            ],
        }
```

Use each resource's short name, without a remote part prefix.

Deploy the sensor as a module and add it to your machine with `viam module reload-local`.
The command adds the sensor to your machine's configuration, using the resource name you pass in `--resource-name`.
See [Test locally](/build-modules/write-a-driver-module/#3-test-locally) and [Write a module](/build-modules/write-a-driver-module/).
Then [point the data manager at the sensor](#point-the-data-manager-at-the-sensor), setting `key` to the key your sensor returns its overrides under.

## Next steps

- [Sequences](/data/sequences/): what a sequence is, and how to view, edit, and train on the sequences you record.
- [Sequences tutorial](/data/sequences-tutorial/): record sequences with the `capture-control` module, then build and export a sequence dataset.
- [Conditional sync](/data/capture-sync/conditional-sync/): control when captured data uploads.
