---
linkTitle: "Create a dataset"
title: "Create a dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a dataset of images or sequences for training an ML model."
capabilities: ["datasets", "sequences"]
diataxis: how-to
date: "2025-01-30"
aliases:
  - /build/train/create-a-dataset/
  - /data-ai/train/create-dataset/
---

A dataset is a named collection of data at the organization level that you use for training.
Datasets come in two types, and you choose the type when you create the dataset.
You can't change it later.

## Choose a dataset type

|                  | Image dataset                                              | Sequence dataset                                                                                         |
| ---------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Holds            | Individual images. The app calls this type **Binary Data** | [Sequences](/data/sequences/): time windows of images and readings from one machine part                 |
| Use it to        | Classify an image or detect objects in it                  | Learn from something that unfolds over time, such as sequence classification or a robot's demonstrations |
| Labeling         | You tag images or draw bounding boxes                      | Sequence tags, set when the sequence is recorded                                                         |
| Managed training | Yes                                                        | No. Use a [custom training script](/train/custom-training-scripts/)                                      |
| Export           | Images plus a `dataset.jsonl` file                         | Three Parquet files plus images                                                                          |

If you want a model that looks at one image at a time, use an image dataset.
If the meaning is in how images and readings change over a window of time, use a sequence dataset.
The steps below are for image datasets, up to [Sequence datasets](#sequence-datasets).

## Platform requirements

Viam rejects a training job if the dataset does not meet these minimums:

| Requirement        | Minimum                                                             |
| ------------------ | ------------------------------------------------------------------- |
| Labeled images     | 80% of the dataset                                                  |
| Examples per label | 10 images (classification) or 10 bounding boxes (object detection)  |
| Total images       | 15 (object detection only; classification has no total-image floor) |

## Recommendations for quality

Platform minimums get a training job accepted; they do not guarantee a good
model. For production use:

- Aim for hundreds of examples per label under varied conditions.
- Keep label counts roughly balanced -- no label should have more than 3x the
  images of any other.
- Capture images from the deployment environment, meaning the real lighting,
  backgrounds, camera angles, and distances your machine uses. Stock datasets
  and stylized marketing images do not generalize.

## 1. Create a dataset

You can create a dataset from the web UI, the CLI, or programmatically.

**Web UI:**

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click the **DATASETS** subtab.
4. In the **Dataset Name** field, enter a descriptive name for your dataset.
   Use a name that reflects the task, such as `inspection-parts-v1` or
   `package-detection`. Dataset names must be unique within your organization.
5. Leave **Data type** set to **Binary Data**, the type for image datasets.
6. Click **Create dataset**.

Your empty dataset now appears in the list.

**CLI:**

If you have the Viam CLI installed, create a dataset from the command line:

```bash
viam dataset create --org-id=YOUR-ORG-ID --name=my-inspection-dataset
```

The command returns the dataset ID, which you will need for subsequent CLI and
SDK operations.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient


API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def connect() -> ViamClient:
    dial_options = DialOptions.with_api_key(API_KEY, API_KEY_ID)
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    dataset_id = await data_client.create_dataset(
        name="my-inspection-dataset",
        organization_id=ORG_ID,
    )
    print(f"Created dataset: {dataset_id}")

    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

func main() {
    apiKey := "YOUR-API-KEY"
    apiKeyID := "YOUR-API-KEY-ID"
    orgID := "YOUR-ORGANIZATION-ID"

    ctx := context.Background()
    logger := logging.NewDebugLogger("create-dataset")

    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, apiKey, apiKeyID, logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    datasetID, err := dataClient.CreateDataset(
        ctx, "my-inspection-dataset", orgID)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Created dataset: %s\n", datasetID)
}
```

{{% /tab %}}
{{< /tabs >}}

Replace all placeholder values (`YOUR-API-KEY`, `YOUR-API-KEY-ID`,
`YOUR-ORGANIZATION-ID`) with your actual values. The API key must be
organization-scoped -- machine-scoped and location-scoped keys cannot
create datasets. To fetch or create these values from the CLI:

```bash
viam organizations list
viam organizations api-key create --org-id=YOUR-ORGANIZATION-ID --name=training
```

You can also find your organization ID by clicking your organization name in
the top navigation bar and then clicking **Settings**.

## 2. Add images to the dataset

With a dataset created, you need to populate it with images.

**Web UI:**

1. Click the **DATA** tab in the top navigation.
2. Use the filters to find the images you want. Filter by machine, component,
   time range, or tags.
3. Select individual images by clicking their checkboxes, or use **Select all**
   to select all visible images.
4. Click **Add to dataset** in the action bar that appears.
5. Select your dataset from the dropdown.
6. Click **Add**.

The selected images are now part of your dataset.

**CLI:**

Add images to a dataset using filter criteria:

```bash
viam dataset data add filter \
  --dataset-id=YOUR-DATASET-ID \
  --location-id=YOUR-LOCATION-ID \
  --tags=label1,label2
```

This adds all images matching the filter to the dataset. You can filter by
location, machine, component, tags, or time range.

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=["binary-data-id-1", "binary-data-id-2"],
        dataset_id="YOUR-DATASET-ID",
    )
    print("Images added to dataset.")

    viam_client.close()
```

You can get binary data IDs by querying for images first using the data client's
`binary_data_by_filter` method, which returns objects that include the binary ID.

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = dataClient.AddBinaryDataToDatasetByIDs(
    ctx,
    []string{"binary-data-id-1", "binary-data-id-2"},
    "YOUR-DATASET-ID",
)
if err != nil {
    logger.Fatal(err)
}
fmt.Println("Images added to dataset.")
```

{{% /tab %}}
{{< /tabs >}}

## 3. Annotate your images

Before training, you need to label every image in your dataset with tags
(for classification) or bounding boxes (for object detection).

See [Annotate images](/train/annotate-images/) for step-by-step instructions
on manual labeling, or [Automate annotation](/train/automate-annotation/) to
use an existing ML model to speed up the process.

## 4. Verify dataset quality

Before you train a model, check that your dataset meets the requirements.

**In the web UI:**

1. Go to the **DATA** tab and click the **DATASETS** subtab.
2. Click your dataset to open it.
3. Review the dataset summary, which shows:
   - Total number of images
   - Number of labeled images
   - Labels used and their counts
4. Check each requirement:

| Check                 | What to look for                                                                                     |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| Enough images         | Object detection: at least 15 total. Classification: at least 10 per label (the binding constraint). |
| Labeling coverage     | At least 80% of images have tags or bounding boxes                                                   |
| Examples per label    | At least 10 images per label                                                                         |
| Label balance         | No label should have more than 3x the images of any other label                                      |
| Production conditions | Images should represent real operating conditions, not staged or ideal setups                        |

**Common issues to fix before training:**

- **Too few images in one class:** Capture more images of the underrepresented
  class, or remove the class and merge it with a related one.
- **Unlabeled images:** Either label them or remove them from the dataset.
  Unlabeled images do not help training and can confuse the summary statistics.
- **Non-representative images:** If your model will run on a factory floor but
  your training images were taken on a clean desk, the model will not generalize.
  Capture images under production conditions -- with the actual lighting,
  background, camera angle, and distance your machine uses.

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    datasets = await data_client.list_datasets_by_organization_id(
        organization_id=ORG_ID,
    )
    for ds in datasets:
        print(f"Dataset: {ds.name}, ID: {ds.id}")

    viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
datasets, err := dataClient.ListDatasetsByOrganizationID(ctx, orgID)
if err != nil {
    logger.Fatal(err)
}
for _, ds := range datasets {
    fmt.Printf("Dataset: %s, ID: %s\n", ds.Name, ds.ID)
}
```

{{% /tab %}}
{{< /tabs >}}

## Download a dataset (optional)

To download a copy of a dataset, for example to inspect it locally or train
outside Viam:

1. Go to the **DATA** tab and click the **DATASETS** subtab.
2. Click your dataset to open it.
3. Click the **...** (dataset actions) menu next to the dataset name and click
   **Download**. The option appears only when the dataset contains images.
4. Click **Download images**. Your browser saves a `<dataset-name>.tar.gz`
   archive of the dataset's image files.

The browser builds the whole archive in memory, so a very large dataset can
exhaust the browser's memory. Images that fail to download are left out of the
archive without a warning. For a large dataset, or when you need a complete
copy, use the CLI export below instead.

The browser download includes image files only, not labels, tags, or
bounding boxes. To export the images together with their annotations, use the
[Viam CLI](/cli/):

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<output-directory> --dataset-id=<dataset-id>
```

For an image dataset, this writes the images and a `dataset.jsonl` manifest
containing their annotations to the destination directory.

## Sequence datasets

A sequence dataset holds [sequences](/data/sequences/) instead of images.
There is no image selection or annotation step.
You add sequences, export the dataset as Parquet files, and train on it with a custom training script.

Before you start, record one or more sequences.
See [Group captured data into sequences](/data/sequences/).

### Create a sequence dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to the [**DATA** tab](https://app.viam.com/data/all) and click **DATASETS**.
2. In the **Dataset Name** field, enter a name.
3. Set **Data type** to **Sequence Data**.
4. Click **Create dataset**.

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

The TypeScript and Go SDKs and `viam dataset create` can't set a dataset's type yet, so create sequence datasets in the web UI or with Python.

### Add sequences

{{< tabs >}}
{{% tab name="Web UI" %}}

To add a sequence from its detail page:

1. Open the sequence from **DATA** > **SEQUENCES**.
2. Click **Add to dataset**.
3. Select the dataset, or enter a new name to create one, and confirm.

To add from the dataset page:

1. Open the dataset from the **DATASETS** tab.
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

### Export a sequence dataset {#export-a-sequence-dataset}

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

### Sequence dataset limitations

- A sequence dataset holds sequences only.
  You can't add images to it, and you can't [merge](/cli/datasets-and-training/#merge-datasets) sequence datasets.
- Managed [training](/train/train-a-model/) doesn't accept sequence datasets.
  Train with a custom training script.
- Sequence exports run queries against your organization's data, and tabular queries count toward your data query usage.

## Troubleshooting

{{< expand "Dataset creation fails" >}}

- **Name already exists.** Dataset names must be unique within your organization.
  Choose a different name or delete the existing dataset if it is no longer
  needed.
- **Permission denied.** Verify that your API key has organization-level access.
  API keys scoped to a single machine or location cannot create datasets.

{{< /expand >}}

{{< expand "Images not appearing in the dataset" >}}

- **Sync delay.** Images must sync from the machine to the cloud before they
  are available to add to a dataset. Wait a minute and check the **DATA** tab
  to confirm images have arrived.
- **Wrong filter.** If using the CLI `add filter` command, double-check your
  filter criteria. A typo in a tag name or location ID will match zero images
  without an error.
- **Binary ID mismatch.** If adding images programmatically by ID, verify that
  the binary IDs are correct. You can retrieve valid IDs using the
  `binary_data_by_filter` method.

{{< /expand >}}

{{< expand "Label imbalance warnings" >}}

- **Collect more data for underrepresented labels.** The most effective fix is
  to capture more images of the minority class under varied conditions.
- **Do not duplicate images.** Adding copies of the same image inflates the
  count without adding information. The model needs diverse examples.
- **Consider merging labels.** If two labels are very similar and one has few
  examples, merge them into a single label.

{{< /expand >}}

## What's next

- [Annotate images](/train/annotate-images/) -- label your images with tags
  or bounding boxes for training.
- [Automate annotation](/train/automate-annotation/) -- use an existing ML
  model to auto-label images instead of doing it by hand.
- [Train a model](/train/train-a-model/) -- use your labeled dataset to
  train a classification or object detection model.
- [Sequence dataset format](/train/sequence-dataset-format/) -- the columns in
  a sequence export, and how to train a custom script on it.
