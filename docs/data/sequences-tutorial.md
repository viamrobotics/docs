---
linkTitle: "Sequences tutorial"
title: "Record and export sequences tutorial"
weight: 3
layout: "docs"
type: "docs"
description: "Record three sequences of camera images and sensor readings, collect them into a sequence dataset, and export the dataset for training."
capabilities: ["data-capture", "sequences", "datasets"]
diataxis: how-to
date: "2026-09-29"
---

In this tutorial, you will record time windows of data from a machine as sequences, review them in the Viam app, collect them into a sequence dataset, and export the dataset as Parquet files.
By the end, you will have followed the whole path that a training script starts from: from capture on the machine to files you can train on.

**Time:** ~20 minutes

**What you need:**

- A machine connected to the Viam app (if you don't have one yet, follow [Set up a machine](/set-up-a-machine/))
- The [Viam CLI](/cli/overview/), installed and logged in
- Python 3 on your laptop or desktop, for the final step

We will use a fake camera and a fake sensor, so this tutorial works without physical hardware.

## 1. Add a fake camera and a fake sensor

We need components that produce data.

1. Go to your machine's page in the Viam app.
2. Click the **+** button in the left sidebar and select **Blocks**.
3. Search for **camera/fake** and select the result.
4. Name it `test-camera` and click **Add to machine**.
5. Repeat to add **sensor/fake**, and name it `test-sensor`.
6. Click **Save** in the upper right.

Expand the **Test** section on each component card to confirm the camera shows an image and the sensor returns readings.

Don't configure data capture on either component.
In the next steps, a capture control sensor will turn capture on only while you record.

## 2. Add the capture control sensor

A sequence starts and stops when a [capture control sensor](/data/capture-sync/capture-control-sensor/) says so.
We will use the `capture-control` module, which you switch on and off by hand.

1. On the **CONFIGURE** tab, click **+** and select **Blocks**.
2. Search for **capture-control** and select the sensor from the `viam` namespace.
3. Name it `my-capture-sensor` and click **Add to machine**.
4. In its attributes, list the two components to control and the capture frequency:

   ```json
   {
     "resources": [
       { "resource_name": "test-camera", "method": "GetImages" },
       { "resource_name": "test-sensor", "method": "Readings" }
     ],
     "default_capture_frequency_hz": 2
   }
   ```

5. Click **Save**.

## 3. Connect the sensor to the data manager

1. On the **CONFIGURE** tab, click **+**, select **Blocks**, and add a **data management** service named `data-manager` if your machine doesn't have one.
2. Switch to **JSON** mode.
3. Find the `data-manager` service and add the sensor to its attributes and its `depends_on` list:

   ```json
   {
     "name": "data-manager",
     "api": "rdk:service:data_manager",
     "model": "rdk:builtin:builtin",
     "attributes": {
       "sync_interval_mins": 0.1,
       "capture_control_sensor": {
         "name": "my-capture-sensor",
         "key": "overrides"
       }
     },
     "depends_on": ["my-capture-sensor"]
   }
   ```

4. Click **Save**.

Nothing is captured yet, because the sensor isn't recording.

## 4. Record three sequences

Now we will record three demonstrations, 10 seconds each.

1. Expand the **Test** section of `my-capture-sensor`, find **DoCommand**, and send:

   ```json
   { "start_capture": true, "tags": ["demo-1"] }
   ```

2. Wait 10 seconds.
3. Send `{"stop_capture": true}`.
4. Repeat with the tags `demo-2` and `demo-3`.

The data manager watches the sensor's readings.
Each `start_capture` began capture and opened a sequence, and each `stop_capture` ended capture and closed the sequence.
The data manager uploads each finished sequence on the next sync.

## 5. Review the sequences

Wait about 30 seconds, then:

1. Click the **DATA** tab in the Viam app.
2. Click **SEQUENCES**.
3. You should see three rows, each with a 10-second time range, your machine part, and the tag `demo-1`, `demo-2`, or `demo-3`.
4. Click a sequence.
   Pick `test-camera · GetImages` to see its images, and `test-sensor · Readings` to see its readings.

{{< alert title="What just happened?" color="info" >}}

Behind the scenes:

1. The data manager polled `my-capture-sensor` 10 times per second.
2. After `start_capture`, the sensor returned an overrides list, so the data manager began capturing `test-camera` and `test-sensor` at 2 Hz, even though neither has capture configured.
3. The `sequences` entry opened a sequence.
4. After `stop_capture`, the entry disappeared, so the sequence closed and its start and end times were saved.
5. Sync uploaded the captured data and the sequence.

The sequence doesn't contain the data.
It is a saved filter: one machine part, a time window, and two components.

{{< /alert >}}

## 6. Collect the sequences into a dataset

1. On the **DATA** tab, click **DATASETS**.
2. In the **Dataset Name** field, enter `demos`.
3. Set **Data type** to **Sequence Data**, and click **Create dataset**.
4. Open the dataset and click **Add sequences**.
5. Select all three sequences and click **Add**.

The dataset's sidebar now shows 3 sequences.
See [Sequence datasets](/train/create-a-dataset/#sequence-datasets).

## 7. Export the dataset

Copy the dataset's ID from the dataset page, then run:

```bash
viam dataset export --dataset-id=<dataset-id> --destination=./demos
```

The CLI starts an export job, waits for it, and downloads the result.
When it finishes, `./demos` contains `<dataset-id>.zip` and a `binary_data/` folder with the camera images.

To look inside, install `pandas` and `pyarrow` (`pip install pandas pyarrow`), then save this as `inspect_export.py`:

```python
import sys
import zipfile
import pandas as pd

zip_path = sys.argv[1]
with zipfile.ZipFile(zip_path) as z:
    z.extractall("demos/parquet")

sequences = pd.read_parquet("demos/parquet/sequences.parquet")
binary = pd.read_parquet("demos/parquet/binary_data.parquet")
tabular = pd.read_parquet("demos/parquet/tabular_data.parquet")

print(sequences[["sequence_id", "tags", "start_at", "end_at"]])
print("images per sequence:")
print(binary.groupby("sequence_id").size())
print("readings per sequence:")
print(tabular.groupby("sequence_id").size())
```

Run it:

```bash
python inspect_export.py demos/<dataset-id>.zip
```

You should see three sequences, each with roughly 20 images and 20 readings.
The rows in the two data files link to a sequence through `sequence_id`.
See [Sequence dataset format](/train/sequence-dataset-format/) for every column.

## 8. Clean up

1. Send `{"stop_capture": true}` to `my-capture-sensor` if a sequence is still open.
2. On the **CONFIGURE** tab, remove `capture_control_sensor` and `depends_on` from the data manager, and click **Save**.
3. To remove the test components, delete `test-camera`, `test-sensor`, and `my-capture-sensor`, and click **Save**.

Data and sequences already synced stay in the cloud.

## What you learned

You built the whole path from capture to training data:

- **Capture control**: a sensor turned capture on for two components only while it was recording.
- **Sequences**: the same sensor opened and closed a sequence around each recording, so each demonstration is one item.
- **Dataset**: you collected sequences into a sequence dataset instead of picking individual images.
- **Export**: you downloaded the dataset as Parquet files, the input for a custom training script.

## What's next

- [Control capture with a sensor](/data/capture-sync/capture-control-sensor/): the full reference for overrides.
- [Group captured data into sequences](/data/sequences/): recording, viewing, and creating sequences from code.
- [Sequence dataset format](/train/sequence-dataset-format/): the columns in each Parquet file.
- [Custom training scripts](/train/custom-training-scripts/): train a model on the exported data.
