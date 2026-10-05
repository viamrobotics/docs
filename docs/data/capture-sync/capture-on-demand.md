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

- Record [sequences](/data/sequences/), time windows of data that you train on as one example. To create a sequence over data you already captured, see [Sequences](/data/sequences/#from-existing-data).
- Capture from several components together, only while something is happening.
- Turn on capture for a component that has no data capture configured.

To keep only camera frames where an ML model detects something, use a [filtered camera](/data/filter-at-the-edge/#use-a-filtered-camera-with-ml) instead.
To control when captured data uploads, rather than what is captured, see [Conditional sync](/data/capture-sync/conditional-sync/).

## Before you start

- A machine running `viam-server` v0.130.0 or later, with a data management service, such as `data_manager/builtin`, configured.
  Capture control sensors need v0.116.0, sequences need v0.127.0, and capturing components that have no data capture configured needs v0.130.0.
- The components you want to record, such as a camera and an arm, configured on the machine.

## How capture on demand works

The data management service can read capture settings from a sensor on the machine, called a capture control sensor.
It polls the sensor's `Readings` method 10 times per second and applies what the sensor returns: which components to capture, how often, with which tags, and which sequences are open.

The `capture-control` module is a ready-made capture control sensor.
You list the components it controls in its configuration, then send it `DoCommand` calls to start and stop recording.

While the sensor lists a component, the frequency and tags it sets temporarily override that component's capture settings.
Your component configuration is left unchanged.
When the sensor stops listing a component, the component returns to its own capture settings.
If it has none, it stops capturing.
If the data management service has `capture_disabled` set to `true`, it ignores the sensor.

## 1. Add the `capture-control` sensor to your machine {#add-the-sensor}

The sensor is the model `viam:capture-control:capture-control-sensor`.
Configure it with the components and methods to record:

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

{{< alert title="The module turns capture off between recordings" color="caution" >}}
While the module isn't recording, it tells the data management service to capture the components in `resources` at 0 Hz.
If you want to capture data all the time, set `default_capture_frequency_hz` above `0`. The module then captures at that frequency from startup, and after any configuration change, until you send `stop_capture`.
Either way, while the module runs, its setting overrides any capture you configured on the listed components, so they capture only while you record or at the set `default_capture_frequency_hz`.
{{< /alert >}}

## 2. Point the data manager at the sensor {#point-the-data-manager-at-the-sensor}

Tell the data management service which sensor to poll, and which key in its readings holds the capture settings.
The `capture-control` module uses the key `overrides`.

Set `capture_control_sensor` on the data management service, with the sensor's name and key.
`key` is required, even if you only use the sensor to record [sequences](/data/sequences/).

```json
{
  "name": "data-manager",
  "api": "rdk:service:data_manager",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "capture_control_sensor": {
      "name": "my-capture-sensor",
      "key": "overrides"
    }
  }
}
```

Within a moment, the service starts applying the sensor's readings.

## 3. Start and stop recording {#start-and-stop-recording}

Send the sensor `DoCommand` calls.
Each command is a key set to `true`, with optional arguments beside it:

| Command                                                         | What it does                                                                                                   |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `{"start_capture": true, "frequency_hz": 2, "tags": ["run-1"]}` | Starts capture at the frequency, tagged, and opens a [sequence](/data/sequences/) with the same tags.          |
| `{"stop_capture": true}`                                        | Stops capture and closes the sequence.                                                                         |
| `{"start_sequence": true, "tags": ["run-1"]}`                   | Opens a sequence without changing capture. Use it when capture is already running. Doesn't use `default_tags`. |
| `{"stop_sequence": true}`                                       | Closes the sequence and leaves capture unchanged.                                                              |

`frequency_hz` and `tags` are optional on `start_capture`.
If you leave out `frequency_hz` and `default_capture_frequency_hz` is `0`, the sequence opens but nothing is captured.
Send one command per call. A call with more than one command key set to `true` returns an error.

Sending `start_capture` or `start_sequence` again with different tags closes the open sequence and opens a new one.
Sending it again with the same tags continues the same sequence.

The sensor forgets its state when its configuration changes.
Changing its configuration, or restarting the module or `viam-server`, ends any recording in progress.

To check that recording started, look for log messages that begin `capture control sensor enabling capture for`, and for `sequence started`.
If `default_capture_frequency_hz` is above `0`, the capture message begins `capture control sensor changing capture_frequency_hz for` instead.
Find them on the machine's **LOGS** tab, or with `viam machines part logs --part=$VIAM_PART_ID`.
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

If the sensor's `Readings` returns an error, or its output can't be parsed, the service reverts every component to its own capture settings and closes any open sequences.
An error in the middle of a recording therefore splits it into two sequences.
If the readings don't contain the key set in `capture_control_sensor`, the service also reverts every component, without logging a warning.
It logs a warning and keeps polling, so capture picks up again as soon as the sensor returns valid readings.

If the service can't find the sensor, or `key` is missing, it logs an error and ignores the sensor.
The service picks up a sensor that becomes available later, such as one from a module that starts slowly.

## Advanced: write your own capture control sensor {#write-your-own-sensor}

The `capture-control` module covers most uses: something outside the machine, such as a person, a script, or a workflow step, decides when to record.

Write your own sensor only when you need one of these:

- **The machine decides by itself**, from another sensor's readings, a vision detection, or a schedule, without a separate process sending commands.
- **Different settings per component**, such as a camera at 10 Hz and a sensor at 1 Hz, or different tags on each.
- **More than one sequence open at the same time.**

Your sensor's `Readings` method returns two lists:

- Under a key you choose, a list of capture overrides. Each entry names a `resource_name` and `method`, and can set `capture_frequency_hz` and `tags`.
- Under the fixed key `sequences`, a list of open sequences. Each entry has a `resources` list and optional `sequence_tags`. A sequence opens the first time its entry appears, and closes when the entry disappears.

For every field, see [Capture control sensor readings](/data/reference/#capture-control-sensor-readings).

For more, see [Build and deploy modules](/build-modules/overview/).

## Next steps

- [Sequences](/data/sequences/): what a sequence is, and how to view, edit, and train on the sequences you record.
- [Sequences tutorial](/data/sequences-tutorial/): record sequences with the `capture-control` module, then build and export a sequence dataset.
- [Conditional sync](/data/capture-sync/conditional-sync/): control when captured data uploads.
