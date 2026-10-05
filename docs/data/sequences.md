---
title: "Sequences"
linkTitle: "Sequences"
description: "Mark a time window of a machine's captured images and readings as one sequence, then collect sequences into a dataset to train on."
capabilities: ["data-capture", "sequences"]
diataxis: how-to
type: "docs"
weight: 26
tags: ["data management", "sequences", "capture"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data"]
date: "2026-09-29"
---

A sequence marks a time window of data that one machine part captured, so you can train on that window as one example.
It names the part, the start and end times, and the components and methods to include, such as a camera's `GetImages` and an arm's `JointPositions`.
It also carries tags that describe the whole window, such as `pick-success` or `demo-3`.

Sequences exist to feed [sequence datasets](/train/create-a-dataset/), which you train on with a [custom training script](/train/custom-training-scripts/).
To follow the whole path from capture to exported training files, see the [sequences tutorial](/data/sequences-tutorial/).

## How a sequence works

A sequence is a saved filter over data you already captured, not a copy of it.
When you read a sequence, Viam returns the images and readings that match its part, resources, and time window.
This has three consequences:

- **Data must be captured during the window.** A sequence only selects data that [data capture](/data/capture-sync/capture-and-sync-data/) recorded and synced. If capture wasn't running on a resource while the sequence was open, the sequence has nothing from that resource.
- **Deleting data removes it from the sequence.** If you [delete](/data/delete-data/) images or readings inside the window, they no longer appear in the sequence.
- **Editing the window changes the contents.** If you change a sequence's start time, end time, or resources, it selects a different set of data.

A sequence can hold two kinds of data:

- **Images**, from the camera methods `ReadImage` and `GetImages`, or the vision service method `CaptureAllFromCamera`. These are the only binary data a sequence accepts. Other binary data, such as point clouds, is rejected. A sequence returns only JPEG and PNG images.
- **Readings** from any other capture method, such as sensor readings or joint positions, stored as tabular data.

Sequence tags label the sequence as a whole.
They are separate from the [tags on individual images and readings](/data/tag-data/).
The `capture-control` module's `start_capture` command sets both to the same values, and its `start_sequence` command sets only the sequence tags.

## Where sequences fit in data management

Sequences sit between captured data and training:

1. **Capture.** The data management service records images and readings from your machine's components. See [Capture and sync data](/data/capture-sync/capture-and-sync-data/).
2. **Mark sequences.** A capture control sensor on the machine opens and closes sequences while the machine runs. You can also create a sequence afterward, from code, over data you already have.
3. **Sync.** The data manager uploads captured data, and uploads each sequence after it closes.
4. **Collect.** You add sequences to a sequence dataset. See [Create a dataset](/train/create-a-dataset/).
5. **Export and train.** You export the dataset as Parquet files, or run a custom training script on it. See [Sequence dataset format](/train/sequence-dataset-format/).

## When to use a sequence

Use a sequence when a training example is a stretch of time, not a single image.
The meaning is in how the images and readings change over the window.
For example:

- **Learning from demonstrations.** Each sequence is one demonstration of a task, with the camera images and arm joint positions from start to finish.
- **Sequence classification.** Each sequence is one event, tagged with its outcome, such as a successful or failed grasp.

## Creating sequences

There are currently two ways to create sequences: either live readings from a machine, or from a set of existing data.

### From a running machine

A machine records sequences through a [capture control sensor](/data/capture-sync/capture-on-demand/).
The data management service polls the sensor 10 times per second and reads a `sequences` list from its readings.
A sequence opens the first time its entry appears in the list, and closes when the entry disappears.
Changing an open entry's tags or resources closes that sequence and opens a new one.
If the sensor's `Readings` call fails, every open sequence closes.
After a sequence closes, the data manager uploads it on the next sync.

You can use the `capture-control` module, which opens a sequence when you send it a command, or write your own sensor.
Start with the module.
Write your own sensor only if the machine should decide by itself when to record, or if you need more than one sequence open at a time.

To record sequences with the `capture-control` module:

1. Add the module's sensor to your machine, list the components and methods to record, and point the data management service at the sensor.
   See [Add the `capture-control` sensor](/data/capture-sync/capture-on-demand/#add-the-sensor) and [Point the data manager at the sensor](/data/capture-sync/capture-on-demand/#point-the-data-manager-at-the-sensor).
2. On the sensor's **Test** section, find **DoCommand**, and send:

   ```json
   { "start_capture": true, "frequency_hz": 2, "tags": ["demo-1"] }
   ```

   This starts capture on the listed components at 2 Hz and opens a sequence tagged `demo-1`.
   If capture is already running, send `{"start_sequence": true, "tags": ["demo-1"]}` instead, to open the sequence without changing capture.

3. When the event ends, send `{"stop_capture": true}` to stop capture and close the sequence, or `{"stop_sequence": true}` to close only the sequence.
4. Open the **DATA** tab and click **SEQUENCES**.
   The new sequence appears after the next sync.

You can send the same commands from code with `DoCommand`, or from a terminal with `viam machines part run`.
See the [sequences tutorial](/data/sequences-tutorial/#4-record-three-sequences) for both.

To record sequences from your own sensor, see [Write your own capture control sensor](/data/capture-sync/capture-on-demand/#write-your-own-sensor).
For every field the sensor can return, see the [capture control sensor readings reference](/data/reference/#capture-control-sensor-readings).

### From existing data

To mark a window of data you already captured, create the sequence from code.
Give it the machine part's ID, the resources and methods to include, and a start and end time.
Tags are optional.

1. Connect a data client.
   See [Set up a connection](/data/query-data-from-code/#set-up-a-connection) for the setup code and the API key it needs.
2. Find the part ID.
   At the top of the machine's page, click the **Live** or **Offline** status dropdown, then click **Part ID** to copy it.
3. Find when the data was captured.
   In the [**DATA** tab](https://app.viam.com/data/all), filter by the machine and the resource, and note the capture times of the first and last images or readings you want.
4. Create the sequence.
   The window includes data captured exactly at the start and end times.
   The examples give both times in UTC. If the times you noted are in another time zone, convert them or pass that time zone instead.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from datetime import datetime, timezone

from viam.proto.app.data import SequenceResourceFilter

sequence_id = await data_client.create_sequence(
    part_id="<PART-ID>",
    resources=[
        SequenceResourceFilter(resource_name="my-camera", method_name="GetImages")
    ],
    sequence_tags=["demo-1"],
    start_time=datetime(2026, 9, 29, 14, 0, 0, tzinfo=timezone.utc),
    end_time=datetime(2026, 9, 29, 14, 0, 30, tzinfo=timezone.utc),
)
```

{{% /tab %}}
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

## View sequences

1. Go to the [**DATA** tab](https://app.viam.com/data/all) and click **SEQUENCES**.
   The list shows each sequence's time range, machine part, resources, and tags.
2. Click a sequence to open it.
3. Pick a resource, shown as `<resource name> · <method>`, to see its images or readings during the window.

To copy a sequence's ID, click the **Sequence actions** menu on its row and select **Copy sequence ID**.

From code, `ListSequences` lists the sequences in an organization and `GetSequence` returns one by ID. The Python, TypeScript, and Go SDKs have these methods.
`GetSequenceBinaryData` returns the images inside a sequence, from Python or TypeScript.
There is no API for a sequence's readings. View them in the Viam app, or [export a sequence dataset](/train/create-a-dataset/#export-a-sequence-dataset).
See the [data client API](/reference/apis/data-client/).

## Edit and delete sequences

The Viam app can't edit or delete a sequence, and the CLI has no sequence commands.
Use the Python, TypeScript, or Go SDK.

- **Edit:** `UpdateSequence` changes a sequence's `resources`, `sequence_tags`, `start_time`, or `end_time`. Only the fields you list in its field mask change, and the field mask is required.
  The Python SDK's `update_sequence` builds the field mask for you from the arguments you pass, and raises an error if you pass none of them. Pass `sequence_tags=[]` to clear a sequence's tags.
- **Delete:** `DeleteSequence` deletes a sequence by its ID.

See the [data client API](/reference/apis/data-client/) for each method's parameters.

## Add sequences to a dataset

To train on sequences, collect them into a sequence dataset.
On a sequence's detail page, click **Add to dataset**, or call `AddSequencesToDataset` from code.
See [Create a dataset](/train/create-a-dataset/) to create the dataset, add sequences, and export it.

## Limitations {#limits}

- **Images are the only binary data.** See [How a sequence works](#how-a-sequence-works).
- **A sequence belongs to one machine part.** To combine data from several parts, record a sequence on each part and add them all to one dataset.
- **A crash loses the open sequence.** If `viam-server` stops uncleanly while a sequence is open, the data manager can't tell when the sequence ended. It moves the sequence to `failed/sequences/` in the capture directory and doesn't upload it. A normal shutdown closes open sequences so they upload on the next sync.
- **Editing and deleting need an SDK.** The Viam app and the CLI can't edit or delete a sequence.
- **Managed training doesn't accept sequence datasets.** Train on them with a [custom training script](/train/custom-training-scripts/).

## Next steps

- [Sequences tutorial](/data/sequences-tutorial/): record three sequences, collect them into a dataset, and export it.
- [Create a sequence dataset](/train/create-a-dataset/): collect sequences for training.
- [Capture on demand](/data/capture-sync/capture-on-demand/): start and stop capture, and record sequences, with the `capture-control` module.
- [Sequence dataset format](/train/sequence-dataset-format/): the Parquet files a training script receives.
