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

## 1. Add the `capture-control` sensor {#add-the-sensor}

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

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On your machine's **CONFIGURE** tab, click **+**, select **Blocks**, and search for **capture-control**. Select the `viam:capture-control:capture-control-sensor` model.
2. Name it `my-capture-sensor` and click **Add to machine**.
3. In the sensor's attributes, paste the JSON above.
4. Click **Save**.

{{% /tab %}}
{{% tab name="CLI and SDK" %}}

The CLI can't add a registry module to a machine.
`viam machines part add-resource` adds the sensor's entry but not the `viam:capture-control` module entry, so `viam-server` can't build the sensor.
Use the [Viam MCP server](/reference/mcp/) instead, which adds the module for you.
Ask your MCP client something like:

> On my machine `<machine-name>`, add a sensor named `my-capture-sensor` with the model `viam:capture-control:capture-control-sensor` and the attributes shown above.

The client calls the `add_machine_config_item` tool.
If the module wasn't already on the machine, its result includes a `module_added` entry for `viam:capture-control`.

{{% /tab %}}
{{< /tabs >}}

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

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On your machine's **CONFIGURE** tab, find your data management service.
2. Switch to **JSON** mode.
3. Add `capture_control_sensor` to the service's `attributes`, as shown above.
4. Click **Save**.

{{% /tab %}}
{{% tab name="CLI and SDK" %}}

If your machine has no data management service yet, add one.
Its API is `rdk:service:data_manager`, which `--resource-subtype` doesn't accept, so pass `--api`:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource --part=$VIAM_PART_ID \
  --name=data-manager --api=rdk:service:data_manager --model-name=builtin
```

Then set the attribute.
`--config` replaces all of the service's existing attributes, so include any you already have:

```sh {class="command-line" data-prompt="$"}
viam resource update --part=$VIAM_PART_ID --resource-name=data-manager \
  --config '{"capture_control_sensor": {"name": "my-capture-sensor", "key": "overrides"}}'
```

{{% /tab %}}
{{< /tabs >}}

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

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **CONFIGURE** tab, expand the **Test** section of `my-capture-sensor` and find **DoCommand**.
2. Send `{"start_capture": true, "frequency_hz": 2, "tags": ["run-1"]}`.
3. Wait for the moment you want to record to pass.
4. Send `{"stop_capture": true}`.

{{% /tab %}}
{{% tab name="CLI and SDK" %}}

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=$VIAM_PART_ID \
  --component=my-capture-sensor --method=DoCommand \
  --data='{"command": {"start_capture": true, "frequency_hz": 2, "tags": ["run-1"]}}'
```

After the moment you want to record has passed:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=$VIAM_PART_ID \
  --component=my-capture-sensor --method=DoCommand \
  --data='{"command": {"stop_capture": true}}'
```

To send the commands from code, call `do_command` on the sensor with the same dictionary.

{{% /tab %}}
{{< /tabs >}}

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

While this sensor isn't recording, it returns an empty overrides list, so every component returns to its own capture settings.
Unlike the `capture-control` module, it doesn't turn off capture you configured on the components.
To turn capture off between recordings, return the same overrides with `capture_frequency_hz` set to `0`.

Use each resource's short name, without a remote part prefix.

<!-- TODO(eng): confirm that a bare name resolves for a resource on a remote part. The lookup map is keyed by ShortName(), which keeps the remote: prefix (rdk services/datamanager/builtin/builtin.go). -->

Deploy the sensor as a module and add it to your machine with `viam module reload-local`.
By default, the command adds no resources. Pass `--model-name` with your sensor's model triple to add the sensor to your machine's configuration, and `--resource-name` to name it:

```sh {class="command-line" data-prompt="$"}
viam module reload-local --model-name=<namespace>:<module>:<model> --resource-name=my-capture-sensor
```

See [Test locally](/build-modules/write-a-driver-module/#3-test-locally) and [Write a module](/build-modules/write-a-driver-module/).
Then [point the data manager at the sensor](#point-the-data-manager-at-the-sensor), setting `key` to the key your sensor returns its overrides under.

## Next steps

- [Sequences](/data/sequences/): what a sequence is, and how to view, edit, and train on the sequences you record.
- [Sequences tutorial](/data/sequences-tutorial/): record sequences with the `capture-control` module, then build and export a sequence dataset.
- [Conditional sync](/data/capture-sync/conditional-sync/): control when captured data uploads.
