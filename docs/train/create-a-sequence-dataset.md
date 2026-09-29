---
linkTitle: "Create a sequence dataset"
title: "Create a sequence dataset"
weight: 12
layout: "docs"
type: "docs"
description: "Collect sequences into a dataset, and export it for training."
capabilities: ["datasets", "sequences"]
diataxis: how-to
date: "2026-09-29"
---

A sequence dataset is a named, organization-level collection of [sequences](/data/sequences/).
Unlike an image dataset, it holds time windows of images and readings, and it has no image selection or annotation step.
You collect sequences into it, export it as Parquet files, and train on it with a [custom training script](/train/custom-training-scripts/).

## Before you start

- One or more sequences in your organization.
  See [Group captured data into sequences](/data/sequences/).
- The [Viam CLI](/cli/overview/) installed, if you want to export from the command line.

## 1. Create the dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to the [**DATA** tab](https://app.viam.com/data/all) and click **Datasets**.
2. Click **Create dataset**.
3. Enter a name, and under **Data type**, select **Sequence Data**.
4. Click **Create**.

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.proto.app.dataset import DatasetType

dataset_id = await data_client.create_dataset(
    name="my-sequence-dataset",
    organization_id="<ORG-ID>",
    type=DatasetType.DATASET_TYPE_SEQUENCE_DATA,
)
```

{{% /tab %}}
{{< /tabs >}}

The type is set when you create the dataset and can't change later.
The TypeScript and Go SDKs and `viam dataset create` can't set a dataset's type yet, so create sequence datasets in the web UI or with Python.

## 2. Add sequences

{{< tabs >}}
{{% tab name="Web UI" %}}

To add a sequence from its detail page:

1. Open the sequence from **DATA** > **Sequences**.
2. Click **Add to dataset**.
3. Select the dataset, or enter a new name to create one, and confirm.

To add from the dataset page:

1. Open the dataset from the **Datasets** tab.
2. Click **Add sequences**.
3. In the **All sequences** dialog, select the sequences you want and click **Add**.

{{% /tab %}}
{{% tab name="Python" %}}

```python
await data_client.add_sequences_to_dataset(
    dataset_id="<DATASET-ID>",
    sequence_ids=["<SEQUENCE-ID>"],
)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```typescript
await dataClient.addSequencesToDataset(["<SEQUENCE-ID>"], "<DATASET-ID>");
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err := dataClient.AddSequencesToDataset(ctx, "<DATASET-ID>", []string{"<SEQUENCE-ID>"})
```

{{% /tab %}}
{{< /tabs >}}

The dataset's sidebar shows how many sequences it holds.

To remove sequences, call `remove_sequences_from_dataset` (Python), `removeSequencesFromDataset` (TypeScript), or `RemoveSequencesFromDataset` (Go).
See the [data client API](/reference/apis/data-client/).

## 3. Export the dataset

The `viam dataset export` command detects a sequence dataset, starts an export job on the server, waits for it, and downloads the result:

```sh {class="command-line" data-prompt="$"}
viam dataset export \
  --dataset-id=<dataset-id> \
  --destination=./my-sequence-dataset
```

The destination then contains:

- `<dataset-id>.zip`: three Parquet files, `binary_data.parquet`, `tabular_data.parquet`, and `sequences.parquet`.
  See [Sequence dataset format](/train/sequence-dataset-format/).
- `binary_data/`: the image files, named `<binary-data-id><extension>`.

To skip the image files and download only the zip, add `--only-parquet`.
To change how often the CLI checks the job, or how long it waits, use `--poll-interval` (default `5s`) and `--max-wait` (default `30m`).

From code, call `start_sequence_dataset_export` to get a job ID, poll `get_sequence_dataset_export` until its status is `COMPLETED`, then download the zip from `download_url`.
The URL is short-lived, so download it right away.
The Python and TypeScript SDKs have these methods.
The Go SDK doesn't.

## Limitations

- A sequence dataset holds sequences only.
  You can't add images to it, and you can't [merge](/cli/datasets-and-training/#merge-datasets) sequence datasets.
- Managed [training](/train/train-a-model/) doesn't accept sequence datasets.
  Train with a custom training script.
- Sequence exports run queries against your organization's data, and tabular queries count toward your data query usage.

## Next steps

- [Sequence dataset format](/train/sequence-dataset-format/): the columns in each Parquet file.
- [Custom training scripts](/train/custom-training-scripts/): train on the exported data.
