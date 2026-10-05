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
- The [Viam CLI](/cli/overview/), installed and authenticated on your computer
- Python 3 installed on your computer

We will use a fake camera and a fake sensor, so this tutorial works without physical hardware.

You can follow each step in the Viam app or from a terminal.
The **CLI and Python** tabs let you script the whole tutorial, or hand it to an AI coding agent to run for you.
If you use those tabs, expand **Set up for the CLI and Python path** and finish it first.

{{% expand "Set up for the CLI and Python path" %}}

1. Find your organization ID, your machine's ID, and the ID of its main part:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations list
   viam machines list --organization=<org-id> --all
   viam machines part list --machine=<machine-id>
   ```

2. Create an API key for the SDK scripts:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations api-key create --org-id=<org-id> --name=sequences-tutorial
   ```

3. Export the IDs and the key as environment variables. The commands and scripts in the following steps read them:

   ```sh {class="command-line" data-prompt="$"}
   export VIAM_ORG_ID=<org-id>
   export VIAM_PART_ID=<part-id>
   export VIAM_API_KEY_ID=<api-key-id>
   export VIAM_API_KEY=<api-key>
   ```

4. Make a working directory and install the Python SDK in it:

   <!-- TODO(python-sdk): pin the minimum viam-sdk version that includes list_sequences, for example "viam-sdk>=X.Y.Z", once the release ships. -->

   ```sh {class="command-line" data-prompt="$"}
   mkdir sequences-tutorial && cd sequences-tutorial
   python3 -m venv .venv && source .venv/bin/activate
   pip install viam-sdk pandas pyarrow
   ```

{{% /expand %}}

## 1. Add a fake camera and a fake sensor

We need components that produce data.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Go to your machine's page in the Viam app.
2. Click the **+** button in the left sidebar and select **Blocks**.
3. Search for **camera/fake** and select the result.
4. Name it `test-camera` and click **Add to machine**.
5. Repeat to add **sensor/fake**, and name it `test-sensor`.
6. Click **Save** in the upper right.

Expand the **Test** section on each component card to confirm the camera shows an image and the sensor returns readings.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource --part=$VIAM_PART_ID \
  --name=test-camera --model-name=fake --resource-subtype=camera
viam machines part add-resource --part=$VIAM_PART_ID \
  --name=test-sensor --model-name=fake --resource-subtype=sensor
```

Wait a few seconds for the machine to pick up the change, then confirm the sensor returns readings:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=$VIAM_PART_ID \
  --component=test-sensor --method=GetReadings
```

{{% /tab %}}
{{< /tabs >}}

Don't configure data capture on either component.
In the next steps, a capture control sensor will turn capture on only while you record.

## 2. Add the capture control sensor

A sequence starts and stops when a [capture control sensor](/data/capture-sync/capture-on-demand/) says so.
We will use the `capture-control` module, which you switch on and off by hand.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **CONFIGURE** tab, click **+** and select **Blocks**.
2. Search for **capture-control** and select **capture-control/capture-control-sensor**.
3. Name it `my-capture-sensor` and click **Add to machine**.
4. In its attributes, list the two components to control:

   ```json
   {
     "resources": [
       { "resource_name": "test-camera", "method": "GetImages" },
       { "resource_name": "test-sensor", "method": "Readings" }
     ]
   }
   ```

5. Click **Save**.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

The CLI can't add a registry module to a machine.
`viam machines part add-resource` adds the sensor's entry but not the `viam:capture-control` module entry, so `viam-server` can't build the sensor.
You can follow the Viam app instructions, or use the [Viam MCP server](/reference/mcp/) instead, which adds the module for you.
Ask your MCP client something like:

> On my machine `<machine-name>`, add a sensor named `my-capture-sensor` with the model `viam:capture-control:capture-control-sensor` and these attributes:
>
> ```json
> {
>   "resources": [
>     { "resource_name": "test-camera", "method": "GetImages" },
>     { "resource_name": "test-sensor", "method": "Readings" }
>   ]
> }
> ```

The client calls the `add_machine_config_item` tool.
Its result includes a `module_added` entry for `viam:capture-control`.

{{% /tab %}}
{{< /tabs >}}

## 3. Connect the sensor to the data manager

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **CONFIGURE** tab, click **+**, select **Blocks**, and search for **data_manager**. Choose the **data_manager/builtin** service and name it `data-manager`.
2. Switch to **JSON** mode.
3. Find the `data-manager` service and add the sensor to its attributes:

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
     }
   }
   ```

4. Click **Save**.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

Add the data management service, then set its attributes.
The service's API is `rdk:service:data_manager`, which `--resource-subtype` doesn't accept, so pass `--api`:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource --part=$VIAM_PART_ID \
  --name=data-manager --api=rdk:service:data_manager --model-name=builtin
viam resource update --part=$VIAM_PART_ID --resource-name=data-manager \
  --config '{"sync_interval_mins": 0.1, "capture_control_sensor": {"name": "my-capture-sensor", "key": "overrides"}}'
```

If your machine already has a data management service under another name, remove it first.
A machine can have only one.

{{% /tab %}}
{{< /tabs >}}

Nothing is captured yet, because the sensor isn't recording.

## 4. Record three sequences

Now we will record three demonstrations, 10 seconds each.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Expand the **Test** section of `my-capture-sensor`, find **DoCommand**, and send:

   ```json
   { "start_capture": true, "frequency_hz": 2, "tags": ["demo-1"] }
   ```

2. Wait 10 seconds.
3. Send `{"stop_capture": true}`.
4. Repeat with the tags `demo-2` and `demo-3`.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

```sh
for tag in demo-1 demo-2 demo-3; do
  viam machines part run --part=$VIAM_PART_ID \
    --component=my-capture-sensor --method=DoCommand \
    --data="{\"command\": {\"start_capture\": true, \"frequency_hz\": 2, \"tags\": [\"$tag\"]}}"
  sleep 10
  viam machines part run --part=$VIAM_PART_ID \
    --component=my-capture-sensor --method=DoCommand \
    --data='{"command": {"stop_capture": true}}'
  sleep 2
done
```

{{% /tab %}}
{{< /tabs >}}

The data manager watches the sensor's readings.
Each `start_capture` began capture at 2 Hz and opened a sequence, and each `stop_capture` ended capture and closed the sequence.
The data manager uploads each finished sequence on the next sync.

## 5. Review the sequences

Wait about 30 seconds, then:

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Click the **DATA** tab in the Viam app.
2. Click **SEQUENCES**.
3. You should see three rows, the time range for each sequence, your machine part, the fake camera and sensor resources, and the tag `demo-1`, `demo-2`, or `demo-3`.
4. Click a sequence. You should see both the recorded images from `test-camera`, and the readings from `test-sensor`.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

The CLI can't list sequences yet, so this step uses the Python SDK.
Save this as `list_sequences.py`.
It prints each matching sequence's details, then its ID on standard output:

```python
import asyncio
import os
import sys

from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions

TAGS = {"demo-1", "demo-2", "demo-3"}


async def main():
    client = await ViamClient.create_from_dial_options(
        DialOptions.with_api_key(
            os.environ["VIAM_API_KEY"], os.environ["VIAM_API_KEY_ID"]
        )
    )
    data = client.data_client

    page_token = None
    while True:
        sequences, next_page_token = await data.list_sequences(
            organization_id=os.environ["VIAM_ORG_ID"], page_token=page_token
        )
        for s in sequences:
            if s.part_id != os.environ["VIAM_PART_ID"]:
                continue
            if not TAGS.intersection(s.sequence_tags):
                continue
            resources = ", ".join(
                f"{r.resource_name} · {r.method_name}" for r in s.resources
            )
            print(
                ",".join(s.sequence_tags),
                s.start_time.ToDatetime().isoformat(),
                s.end_time.ToDatetime().isoformat(),
                resources,
                file=sys.stderr,
            )
            print(s.id)
        if not next_page_token:
            break
        page_token = next_page_token

    client.close()


asyncio.run(main())
```

Run it and keep the IDs for the next step:

```sh {class="command-line" data-prompt="$"}
SEQUENCE_IDS=$(python list_sequences.py)
echo $SEQUENCE_IDS
```

You should see three sequences, one for each tag, each 10 to 15 seconds long, with `test-camera · GetImages` and `test-sensor · Readings` as resources.
The script matches on tags, so if you run the tutorial again, it also lists the sequences from earlier runs.

{{% /tab %}}
{{< /tabs >}}

{{< alert title="What just happened?" color="info" >}}

Behind the scenes:

1. The data manager polled `my-capture-sensor` 10 times per second.
2. The sensor returns an overrides list on every poll, at 0 Hz while it isn't recording. After `start_capture`, the frequency in that list changed to 2 Hz, so the data manager began capturing `test-camera` and `test-sensor`, even though neither has capture configured.
3. The `sequences` entry opened a sequence.
4. After `stop_capture`, the entry disappeared, so the sequence closed and its start and end times were saved.
5. Sync uploaded the captured data and the sequence.

The sequence doesn't contain the data.
It is a saved filter: one machine part, a time window, and two components.

{{< /alert >}}

## 6. Collect the sequences into a dataset

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **DATA** tab, click **DATASETS**.
2. Click **Create dataset**.
3. In the **Dataset Name** field, enter `demos`.
4. Set **Data type** to **Sequence Data**, and click **Create dataset** again.
5. Open the dataset and click **Add Data**.
6. Select all three sequences and click **Add**.

The dataset's sidebar now shows 3 sequences.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

`viam dataset create` can't set a dataset's type yet, so this step uses the Python SDK.
Save this as `create_dataset.py`.
It creates a sequence dataset, adds the sequences you pass it, and prints the dataset's ID.
The dataset is named `demos` unless you set `DATASET_NAME`:

```python
import asyncio
import os
import sys

from viam.app.viam_client import ViamClient
from viam.proto.app.dataset import DatasetType
from viam.rpc.dial import DialOptions


async def main():
    # Split the arguments too, because zsh passes $SEQUENCE_IDS as one argument.
    sequence_ids = " ".join(sys.argv[1:]).split()
    client = await ViamClient.create_from_dial_options(
        DialOptions.with_api_key(
            os.environ["VIAM_API_KEY"], os.environ["VIAM_API_KEY_ID"]
        )
    )
    data = client.data_client
    dataset_id = await data.create_dataset(
        name=os.environ.get("DATASET_NAME", "demos"),
        organization_id=os.environ["VIAM_ORG_ID"],
        type=DatasetType.DATASET_TYPE_SEQUENCE_DATA,
    )
    await data.add_sequences_to_dataset(
        dataset_id=dataset_id, sequence_ids=sequence_ids
    )
    print(dataset_id)
    client.close()


asyncio.run(main())
```

Run it with the IDs from step 5:

```sh {class="command-line" data-prompt="$"}
DATASET_ID=$(python create_dataset.py $SEQUENCE_IDS)
echo $DATASET_ID
```

Dataset names must be unique in your organization.
If `demos` already exists, pick another name, for example `export DATASET_NAME=demos-2`, and run the script again.

{{% /tab %}}
{{< /tabs >}}

See [Create a dataset](/train/create-a-dataset/).

## 7. Export the dataset

Copy the dataset's ID from the dataset page, or use `$DATASET_ID` from the **CLI and Python** tab, then run:

```sh {class="command-line" data-prompt="$"}
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

```sh {class="command-line" data-prompt="$"}
python inspect_export.py demos/<dataset-id>.zip
```

You should see three sequences, each with 20 to 30 images and about as many readings, two per second of recording.
The rows in the two data files link to a sequence through `sequence_id`.
See [Sequence dataset format](/train/sequence-dataset-format/) for every column.

## What you learned

You built the whole path from capture to training data:

- **Capture control**: a sensor turned capture on for two components only while it was recording.
- **Sequences**: the same sensor opened and closed a sequence around each recording, so each demonstration is one item.
- **Dataset**: you collected sequences into a sequence dataset instead of picking individual images.
- **Export**: you downloaded the dataset as Parquet files, the input for a custom training script.

## What's next

- [Capture on demand](/data/capture-sync/capture-on-demand/): all of the `capture-control` module's commands, and how to write your own capture control sensor.
- [Sequences](/data/sequences/): recording, viewing, and creating sequences from code.
- [Sequence dataset format](/train/sequence-dataset-format/): the columns in each Parquet file.
- [Custom training scripts](/train/custom-training-scripts/): train a model on the exported data.
