---
linkTitle: "Create a dataset"
title: "Create a dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a dataset of images for training an ML model."
date: "2025-01-30"
aliases:
  - /build/train/create-a-dataset/
---

A dataset is a named collection of images at the organization level that you
label and use for training. Before training, your dataset must meet these
minimums:

| Requirement        | Minimum                |
| ------------------ | ---------------------- |
| Total images       | 15                     |
| Labeled images     | 80% of total           |
| Examples per label | 10                     |
| Label distribution | Roughly equal          |
| Image source       | Production environment |

For production use, aim for hundreds of images per label under varied
conditions.

## 1. Create a dataset

You can create a dataset from the web UI, the CLI, or programmatically.

**Web UI:**

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click the **DATASETS** subtab.
4. Click **+ Create dataset**.
5. Enter a descriptive name for your dataset. Use a name that reflects the task,
   such as `inspection-parts-v1` or `package-detection`. Dataset names must be
   unique within your organization.
6. Click **Create**.

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
`YOUR-ORGANIZATION-ID`) with your actual values. To find your organization ID,
click your organization name in the top navigation bar, then click **Settings**.
Your organization ID is displayed on the settings page with a copy button.

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

| Check                 | What to look for                                                              |
| --------------------- | ----------------------------------------------------------------------------- |
| Enough images         | At least 15 total. More is better.                                            |
| Labeling coverage     | At least 80% of images have tags or bounding boxes                            |
| Examples per label    | At least 10 images per label                                                  |
| Label balance         | No label should have more than 3x the images of any other label               |
| Production conditions | Images should represent real operating conditions, not staged or ideal setups |

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
