---
title: "Group captured data into sequences"
linkTitle: "Sequences"
description: "Record time windows of images and readings around events, and review them."
capabilities: ["data-capture", "sequences"]
diataxis: how-to
type: "docs"
weight: 26
tags: ["data management", "sequences", "capture"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data"]
date: "2026-09-29"
---

A sequence is a saved filter over data you already captured, not a copy of it.
It selects the data one machine part captured inside a time window, and it carries tags that apply to the whole window.
Each entry in the filter names a component or service and one of its methods, such as a camera's `GetImages` or an arm's `GetJointPositions`.

Use sequences to keep the images and readings from one event together, for example one demonstration of a task, or the seconds around an alarm.
You can then collect sequences into a [sequence dataset](/train/create-a-dataset/#sequence-datasets) and train on them with a custom training script.

To follow a complete example from capture to export, see the [sequences tutorial](/data/sequences-tutorial/).

## Record sequences from a machine

A machine records sequences through a [capture control sensor](/data/capture-sync/capture-control-sensor/).
The sensor returns a `sequences` list from its `Readings` method.
A sequence opens the first time its entry appears in the list, and closes when the entry disappears.

### 1. Make sure the data is captured

A sequence only selects data that data capture wrote down.
For the sequence to contain images and readings, capture must be running on those components while the sequence is open.
Either configure data capture on them, or let the capture control sensor turn capture on for the window.
The `capture-control` module's `start_capture` command does both.
See [Control capture with a sensor](/data/capture-sync/capture-control-sensor/).

### 2. Choose how the sensor opens sequences

The [`capture-control` module](/data/capture-sync/capture-control-sensor/#option-a-use-the-capture-control-module) opens and closes a sequence when you send it a command.
Send `{"start_capture": true, "tags": ["demo-1"]}` to start capture and open a sequence, and `{"stop_capture": true}` to end both.
If capture is already running, use `start_sequence` and `stop_sequence` to open and close only the sequence.
The module keeps one sequence open at a time.

To open sequences from your own logic, or to keep several open at once, write your own capture control sensor that returns a `sequences` list from its `Readings` method.
Each entry in the list has these fields:

| Field           | Type             | Required? | Description                                                                                                                                                      |
| --------------- | ---------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sequence_tags` | array of strings | Optional  | Tags for the whole sequence.                                                                                                                                     |
| `resources`     | array of objects | Required  | The components and services the sequence covers. Each has a `resource_name` and a `method`. Only image methods count as binary data. See [Limitations](#limits). |

The following `Readings` method opens one sequence while `self.recording` is `True`, and turns on capture for the same components:

```python
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

### 3. Point the data manager at the sensor

Set `capture_control_sensor` on the data management service, with the sensor's `name` and the `key` that holds the overrides:

```json
{
  "capture_control_sensor": {
    "name": "my-capture-sensor",
    "key": "overrides"
  }
}
```

`key` is required even if you only record sequences.
Also add the sensor to the service's `depends_on` list.
See [Control capture with a sensor](/data/capture-sync/capture-control-sensor/#2-point-the-data-manager-at-the-sensor).

### 4. Confirm the sequence uploaded

When a sequence closes, the data manager uploads it on the next sync.
Open the **DATA** tab, click **Sequences**, and look for a new row.
You can also call [`ListSequences`](/reference/apis/data-client/).

## View sequences

1. Go to the [**DATA** tab](https://app.viam.com/data/all) and click **Sequences**.
2. The list shows each sequence's time range, machine part, resources, and tags.
3. Click a sequence to open it.
   Pick a resource, shown as `<resource name> · <method>`, to see its images or its readings during the window.
4. To collect the sequence into a dataset, click **Add to dataset**.
   See [Create a sequence dataset](/train/create-a-dataset/#sequence-datasets).

To copy a sequence's ID, click the **Sequence actions** menu on its row.

## Create and edit sequences from code

You can also create a sequence after the fact, for example to label a window of data you already captured.
The TypeScript and Go data clients can create, get, update, delete, and list sequences.
You give `createSequence` the ID of the machine part, the components and methods to include, and a start and end time.
Tags are optional.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```typescript
const sequenceId = await dataClient.createSequence(
  "<PART-ID>",
  [{ resourceName: "my-camera", methodName: "GetImages" }],
  ["demo-1"],
  new Date("2026-09-29T14:00:00Z"),
  new Date("2026-09-29T14:00:30Z"),
);
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
sequenceID, err := dataClient.CreateSequence(
    ctx,
    "<PART-ID>",
    []app.SequenceResourceFilter{
        {ResourceName: "my-camera", MethodName: "GetImages"},
    },
    []string{"demo-1"},
    time.Date(2026, 9, 29, 14, 0, 0, 0, time.UTC),
    time.Date(2026, 9, 29, 14, 0, 30, 0, time.UTC),
)
```

{{% /tab %}}
{{< /tabs >}}

The Python SDK doesn't have create, get, update, delete, or list methods for sequences yet.
`updateSequence` changes only the fields you list in its field mask: `resources`, `sequence_tags`, `start_time`, and `end_time`.

For every method, see the [data client API](/reference/apis/data-client/).

## Limitations {#limits}

- **Images are the only binary data.** A sequence can include images from `ReadImage`, `GetImages`, and `CaptureAllFromCamera`. Any other method that produces binary data, such as point clouds, is rejected. Readings from all other methods count as tabular data.
- **A crash loses the open sequence.** If `viam-server` stops uncleanly while a sequence is open, the data manager can't tell when it ended. It moves the sequence to `failed/sequences/` in the capture directory and doesn't upload it. A normal shutdown closes open sequences so they upload on the next sync.
- **Deleted data drops out.** A sequence is a filter. If you delete the images or readings it points to, they no longer appear in it.
- **The web UI can't delete or edit a sequence.** Use the SDK.
- **Sequences belong to one machine part.**

## Next steps

- [Create a sequence dataset](/train/create-a-dataset/#sequence-datasets): collect sequences for training.
- [Control capture with a sensor](/data/capture-sync/capture-control-sensor/): the sensor that records sequences.
- [Data management service reference](/data/reference/#capture-control-sensor-readings): the `sequences` fields.
