---
linkTitle: "Create a dataset"
title: "Create a dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a binary or sequence dataset for training an ML model."
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

Both types are created the same way.
They differ in how you add data and in what you can do with the dataset afterward.

|                   | Binary dataset                            | Sequence dataset                                                                                         |
| ----------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Holds             | Individual files, usually images          | [Sequences](/data/sequences/): time windows of images, tabular data, or both, from one machine part      |
| Use it to         | Classify an image or detect objects in it | Learn from something that unfolds over time, such as sequence classification or a robot's demonstrations |
| Create with       | Viam app, CLI, Python, TypeScript, Go     | Viam app, Python                                                                                         |
| Labeling          | You tag images or draw bounding boxes     | Sequence tags, such as the task a demonstration shows                                                    |
| Built-in training | Yes                                       | No. Use a [custom training script](/train/custom-training-scripts/)                                      |
| Merge datasets    | Yes                                       | No                                                                                                       |
| Export            | Files plus a `dataset.jsonl` file         | Three Parquet files plus images                                                                          |

## Create a dataset

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Go to the [**DATA** tab](https://app.viam.com/data/all) and click **DATASETS**.
2. Click **Create dataset**.
3. In the **Dataset Name** field, enter a descriptive name for your dataset.
   Use a name that reflects the task, such as `inspection-parts-v1` or
   `package-detection`. Dataset names must be unique within your organization.
4. Set **Data type**:
   - **Binary Data** for a binary dataset. This is the default.
   - **Sequence Data** for a sequence dataset.
5. Click **Create dataset** again.

Your empty dataset now appears in the list.

{{% /tab %}}
{{% tab name="CLI" %}}

This creates a binary dataset. Binary datasets don't support sequences.
The CLI can't create sequence datasets.

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=YOUR-ORG-ID --name=my-inspection-dataset
```

The command returns the dataset ID, which you need for subsequent CLI and
SDK operations.

{{% /tab %}}
{{% tab name="Python" %}}

This creates a binary dataset and a sequence dataset. Python supports both types.

```python
import asyncio
from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient
from viam.proto.app.dataset import DatasetType


API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def connect() -> ViamClient:
    dial_options = DialOptions.with_api_key(API_KEY, API_KEY_ID)
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    # Binary dataset (the default type). Holds binary files such as images, no sequences.
    dataset_id = await data_client.create_dataset(
        name="my-inspection-dataset",
        organization_id=ORG_ID,
    )
    print(f"Created dataset: {dataset_id}")

    # Sequence dataset. Holds sequences only, no individual images.
    sequence_dataset_id = await data_client.create_dataset(
        name="my-sequence-dataset",
        organization_id=ORG_ID,
        type=DatasetType.DATASET_TYPE_SEQUENCE_DATA,
    )
    print(f"Created dataset: {sequence_dataset_id}")

    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

This creates a binary dataset. Binary datasets don't support sequences.
The Go SDK can't create sequence datasets.

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

    // Binary dataset (the default type). Holds binary files such as images, no sequences.
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

The TypeScript and Go SDKs and `viam dataset create` can't set a dataset's type yet, so create sequence datasets in the web UI or with Python.

For the CLI and SDKs, replace all placeholder values (`YOUR-API-KEY`, `YOUR-API-KEY-ID`,
`YOUR-ORGANIZATION-ID`) with your actual values. The API key must be
organization-scoped -- machine-scoped and location-scoped keys cannot
create datasets. To fetch or create these values from the CLI:

```bash
viam organizations list
viam organizations api-key create --org-id=YOUR-ORGANIZATION-ID --name=training
```

You can also find your organization ID by clicking your organization name in
the top navigation bar and then clicking **Settings**.

## Add data

How you add data depends on the dataset type.
A binary dataset holds binary files, usually images, and a sequence dataset holds sequences only.

- **Images** must sync from the machine to the cloud before you can add them to a dataset.
- **Sequences** must be recorded first. See [Sequences](/data/sequences/), or follow the [sequences tutorial](/data/sequences-tutorial/) to go from recording to export in one pass.

{{< tabs >}}
{{% tab name="Viam app" %}}

The Viam app can add data to both dataset types.

**Binary dataset:**

1. Click the **DATA** tab in the top navigation.
2. Use the filters to find the images you want. Filter by machine, component,
   time range, or tags.
3. Select individual images by clicking their checkboxes, or use **Select all**
   to select all visible images.
4. Click **Add to dataset** in the action bar that appears.
5. Select your dataset from the dropdown.
6. Click **Add**.

**Sequence dataset**, from a sequence's detail page:

1. Open the sequence from **DATA** > **SEQUENCES**.
2. Click **Add to dataset**.
3. Select the dataset, or enter a new name to create one, and confirm.

**Sequence dataset**, from the dataset page:

1. Open the dataset from the **DATASETS** tab.
2. Click **Add Data**. If the dataset already holds sequences, the button is **Add sequences**.
3. In the **All sequences** dialog, select the sequences you want and click **Add**.

The dataset's sidebar shows how many sequences it holds.

{{% /tab %}}
{{% tab name="CLI" %}}

The CLI can add images to a binary dataset.
It has no sequence commands, so use the Viam app or an SDK for sequence datasets.

Add images to a dataset using filter criteria:

```bash
viam dataset data add filter \
  --dataset-id=YOUR-DATASET-ID \
  --location-id=YOUR-LOCATION-ID \
  --tags=label1,label2
```

This adds all images matching the filter to the dataset. You can filter by
location, machine, component, tags, or time range.
To add images by ID instead, see [Datasets and training](/cli/datasets-and-training/).

To remove images, use `viam dataset data remove`.

{{% /tab %}}
{{% tab name="Python" %}}

The Python SDK can add data to both dataset types.

**Binary dataset:**

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
To remove images, call `remove_binary_data_from_dataset_by_ids`.

**Sequence dataset:**

```python
await data_client.add_sequences_to_dataset(
    dataset_id="YOUR-DATASET-ID",
    sequence_ids=["YOUR-SEQUENCE-ID"],
)
```

To remove sequences, call `remove_sequences_from_dataset`.

{{% /tab %}}
{{% tab name="TypeScript" %}}

The TypeScript SDK can add data to both dataset types.

**Binary dataset:**

```typescript
await dataClient.addBinaryDataToDatasetByIds(
  ["binary-data-id-1", "binary-data-id-2"],
  "YOUR-DATASET-ID",
);
```

To remove images, call `removeBinaryDataFromDatasetByIds`.

**Sequence dataset:**

```typescript
await dataClient.addSequencesToDataset(["YOUR-SEQUENCE-ID"], "YOUR-DATASET-ID");
```

To remove sequences, call `removeSequencesFromDataset`.

{{% /tab %}}
{{% tab name="Go" %}}

The Go SDK can add data to both dataset types.

**Binary dataset:**

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

To remove images, call `RemoveBinaryDataFromDatasetByIDs`.

**Sequence dataset:**

```go
err = dataClient.AddSequencesToDataset(ctx, "YOUR-DATASET-ID", []string{"YOUR-SEQUENCE-ID"})
```

To remove sequences, call `RemoveSequencesFromDataset`.

{{% /tab %}}
{{< /tabs >}}

Removing data from a dataset doesn't delete the underlying images or sequences.
See the [data client API](/reference/apis/data-client/) for each method's parameters.

## Prepare a dataset for training

Whichever way you train, the model can only learn what your dataset shows it.
Label the data and check it against the recommendations below.
For built-in training, the dataset must also meet the minimums in its [prerequisites](/train/train-a-model/#prerequisites).
A custom training script skips those checks, so your script decides what it needs.

### Label your data

**Binary dataset:** label every image with tags (for classification) or bounding
boxes (for object detection).
See [Annotate data](/train/annotate-data/) for step-by-step instructions
on manual labeling, or [Automate annotation](/train/automate-annotation/) to
use an existing ML model to speed up the process.

**Sequence dataset:** tag each sequence with its task.
You usually set tags while recording.
If you didn't, see [Tag sequences](/train/annotate-data/#tag-sequences) to add them from code.

### Recommendations for quality

These apply to every dataset, whether you use built-in training or a custom training script.
Meeting the built-in training minimums gets a job accepted; it doesn't guarantee a good model.

- **Collect data in the deployment environment.** Use the real lighting,
  backgrounds, camera angles, and distances your machine uses. Stock datasets,
  staged setups, and stylized marketing images do not generalize.
- **Cover the variation the model will see.** Vary conditions such as time of day, object position, and operator.
  Adding copies of the same image or demonstration inflates the count without adding information.
- **Keep labels roughly balanced.** No label should have more than 3x the
  examples of any other.
- **Label everything consistently.** Use one spelling for each label, and remove or label any data that has no label.

For a binary dataset, aim for hundreds of examples per label.
For a sequence dataset, make each sequence one complete demonstration of one task, recorded from the same set of resources, and tag every sequence with its task.

### Verify dataset quality

Check the dataset's labels and counts before you train.

1. Go to the **DATA** tab and click the **DATASETS** subtab.
2. Click your dataset to open it.
3. For a binary dataset, review the dataset summary, which shows:
   - Total number of files, including any non-image files
   - Number of labeled images
   - Labels used and their counts

For a sequence dataset, the sidebar shows how many sequences the dataset holds.

You can also pull a dataset's contents to check them in your own script.
For a binary dataset, `viam dataset export --only-jsonl` downloads a `dataset.jsonl` file with every image's labels, or call `binary_data_by_filter` with the dataset ID in its filter.
For a sequence dataset, call `sequences_by_dataset_id` to list its sequences and their tags.

**Common issues to fix before training:**

- **Too few examples of one label:** Capture more data for the underrepresented
  label under varied conditions, or remove the label and merge it with a related one.
- **Unlabeled data:** Either label it or remove it from the dataset.
  Unlabeled images do not help training and can confuse the summary statistics.
- **Non-representative data:** If your model will run on a factory floor but
  your training images were taken on a clean desk, the model will not generalize.
  Capture data under production conditions -- with the actual lighting,
  background, camera angle, and distance your machine uses.

## Export a dataset

Export a dataset to inspect it locally or to train outside Viam.
What you get depends on the dataset type and the interface.

{{< tabs >}}
{{% tab name="CLI" %}}

`viam dataset export` writes the full dataset to a local directory, for both dataset types.

**Binary dataset:**

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<output-directory> --dataset-id=<dataset-id>
```

This writes the files and a `dataset.jsonl` manifest containing their
annotations to the destination directory.

<span id="export-a-sequence-dataset"></span>**Sequence dataset:** the command detects a sequence dataset, starts an export job on the server, waits for it, and downloads the result:

```sh {class="command-line" data-prompt="$"}
viam dataset export \
  --dataset-id=<dataset-id> \
  --destination=./my-sequence-dataset
```

The destination then contains:

- `<dataset-id>.zip`: three Parquet files, `binary_data.parquet`, `tabular_data.parquet`, and `sequences.parquet`.
  See [Sequence dataset format](/train/sequence-dataset-format/).
- `binary_data/`: the image files, named `<binary-data-id><extension>`.
  Binary data IDs contain slashes, so the files sit in nested folders.

To skip the image files and download only the zip, add `--only-parquet`.
To change how often the CLI checks the job, or how long it waits, use `--poll-interval` (default `5s`) and `--max-wait` (default `30m`).

{{% /tab %}}
{{% tab name="Viam app" %}}

The Viam app can download a binary dataset's files, without annotations.
It can't export a sequence dataset.

1. Go to the **DATA** tab and click the **DATASETS** subtab.
2. Click your dataset to open it.
3. Click the **...** (dataset actions) menu next to the dataset name and click
   **Download**. The option appears only when the dataset contains files.
4. Click **Download files**. Your browser saves a `<dataset-name>.tar.gz`
   archive of the dataset's files, including non-image files such as video
   or audio.

The browser download includes the files only, not tags, bounding boxes, or
other annotations. The browser builds the whole archive in memory, so it
refuses a dataset larger than 500 MB. Files that fail to download are left
out of the archive, and a warning says how many. For a large dataset, or when
you need a complete copy, use the CLI export instead.

{{% /tab %}}
{{% tab name="Python and TypeScript" %}}

The SDKs can export a sequence dataset.
To export a binary dataset with its annotations, use the CLI.

Call `start_sequence_dataset_export` (Python) or `startSequenceDatasetExport` (TypeScript) to get a job ID, poll `get_sequence_dataset_export` or `getSequenceDatasetExport` until its status is `COMPLETED`, then download the zip from `download_url`.
The URL expires after one hour, so download it right away.

{{% /tab %}}
{{% tab name="Go" %}}

The Go SDK has no dataset export.
Use the CLI.

{{% /tab %}}
{{< /tabs >}}

## Sequence dataset limitations

- A sequence dataset holds sequences only.
  You can't add images to it, and you can't [merge](/cli/datasets-and-training/#merge-datasets) sequence datasets.
- [Built-in training](/train/train-a-model/) doesn't accept sequence datasets.
  Train with a custom training script.
- Sequence exports query your organization's tabular data, and those queries count toward your organization's usage.
  See [Billing](/organization/billing/).

## Troubleshooting

{{< expand "Dataset creation fails" >}}

- **Name already exists.** Dataset names must be unique within your organization.
  Choose a different name or delete the existing dataset if it is no longer
  needed.
- **Permission denied.** Verify that your API key has organization-level access.
  API keys scoped to a single machine or location cannot create datasets.
- **Can't create a sequence dataset.** The CLI and the Go and TypeScript SDKs
  can't set a dataset's type. Use the web UI or the Python SDK.

{{< /expand >}}

{{< expand "Images not appearing in a binary dataset" >}}

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

{{< expand "Label imbalance warnings in a binary dataset" >}}

- **Collect more data for underrepresented labels.** The most effective fix is
  to capture more images of the minority class under varied conditions.
- **Do not duplicate images.** Adding copies of the same image inflates the
  count without adding information. The model needs diverse examples.
- **Consider merging labels.** If two labels are very similar and one has few
  examples, merge them into a single label.

{{< /expand >}}

## What's next

**Binary datasets:**

- [Annotate data](/train/annotate-data/) -- label your images with tags
  or bounding boxes for training.
- [Automate annotation](/train/automate-annotation/) -- use an existing ML
  model to auto-label images instead of doing it by hand.
- [Train a model](/train/train-a-model/) -- use your labeled dataset to
  train a classification or object detection model.

**Sequence datasets:**

- [Sequence dataset format](/train/sequence-dataset-format/) -- the columns in
  a sequence export, and how to train a custom script on it.
- [Custom training scripts](/train/custom-training-scripts/) -- write and
  submit your own training script.
