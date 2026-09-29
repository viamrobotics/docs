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
It names the part, the start and end times, and the components and methods to include, such as a camera's `GetImages` and an arm's `GetJointPositions`.
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

- **Images**, from the camera methods `ReadImage`, `GetImages`, and `CaptureAllFromCamera`. These are the only binary data a sequence accepts. Other binary data, such as point clouds, is rejected.
- **Readings** from any other capture method, such as sensor readings or joint positions, stored as tabular data.

Sequence tags label the sequence as a whole.
They are separate from the [tags on individual images and readings](/data/tag-data/), although the `capture-control` module sets both to the same values.

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

### From a machine

A machine records sequences through a [capture control sensor](/data/capture-sync/capture-on-demand/).
The data management service polls the sensor 10 times per second and reads a `sequences` list from its readings.
A sequence opens the first time its entry appears in the list, and closes when the entry disappears.
After it closes, the data manager uploads it on the next sync.

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

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO(python-sdk): The Python SDK doesn't support sequence create, get, update, delete, or list yet. Engineering confirmed it will before these docs ship. Replace this placeholder with a tested example and confirm the method and parameter names against the Python SDK reference. -->

```python
sequence_id = await data_client.create_sequence(
    part_id="<PART-ID>",
    resources=[{"resource_name": "my-camera", "method_name": "GetImages"}],
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

To copy a sequence's ID, click the **Sequence actions** menu on its row.

From code, `ListSequences` lists the sequences in an organization, `GetSequence` returns one by ID, and `GetSequenceBinaryData` returns the images inside it.
See the [data client API](/reference/apis/data-client/).

## Edit and delete sequences

The web UI can't edit or delete a sequence, and the CLI has no sequence commands.
Use the SDK:

- **Edit:** `UpdateSequence` changes a sequence's `resources`, `sequence_tags`, `start_time`, or `end_time`. Only the fields you list in its field mask change.
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
- **Editing and deleting need the SDK.** The web UI and CLI can't edit or delete a sequence.
- **Managed training doesn't accept sequence datasets.** Train on them with a [custom training script](/train/custom-training-scripts/).

## Next steps

- [Sequences tutorial](/data/sequences-tutorial/): record three sequences, collect them into a dataset, and export it.
- [Create a sequence dataset](/train/create-a-dataset/): collect sequences for training.
- [Capture on demand](/data/capture-sync/capture-on-demand/): start and stop capture, and record sequences, with the `capture-control` module.
- [Sequence dataset format](/train/sequence-dataset-format/): the Parquet files a training script receives.
