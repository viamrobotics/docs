---
linkTitle: "Create a training dataset"
title: "Create a training dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a dataset to train a machine learning model."
aliases:
  - /fleet/dataset/
  - /manage/data/label/
  - /manage/data/dataset/
  - /data/dataset/
  - /data-ai/ai/create-dataset/
---

To train a machine learning model, you will need a dataset.

You can create a dataset using the web UI, the CLI, or one of the SDKs:

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Navigate to the **DATA** page and open the [**DATASETS** tab](https://app.viam.com/data/datasets).

1. Click the **+ Create dataset** button.

   {{< imgproc src="/services/data/create-dataset.png" alt="The **DATASET** tab of the **DATA** page, showing the **+ Create dataset** button." resize="800x" style="width:500px" class="imgzoom" >}}

1. Enter a unique name for the dataset.

1. Click **Create dataset**.

{{% /tab %}}
{{% tab name="CLI" %}}

Run the following [Viam CLI](/dev/tools/cli/) command to create a dataset, replacing the `<org-id>` and `<name>` placeholders with your organization ID and a unique name for the dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
```

{{% /tab %}}
{{% tab name="Python" %}}

To create a dataset, pass a unique dataset name and organization ID to [`data_client.create_dataset`](/dev/reference/apis/data-client/#createdataset):

```python
viam_client = await connect()
data_client = viam_client.data_client

print("Creating dataset...")

try:
    dataset_id = await data_client.create_dataset(
        name="<dataset_name>",
        organization_id="<org_id>",
    )
    print(f"Created dataset: {dataset_id}")
except Exception as e:
    print("Error creating dataset. It may already exist.")
    print(f"Exception: {e}")
    raise
```

{{% /tab %}}
{{% tab name="Go" %}}

To create a dataset, pass a unique dataset name and organization ID to [`DataClient.CreateDataset`](/dev/reference/apis/data-client/#createdataset):

```go
ctx := context.Background()
viamClient, err := client.New(ctx, "<machine_address>", logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

dataClient := viamClient.DataClient()

fmt.Println("Creating dataset...")

datasetID, err := dataClient.CreateDataset(ctx, &datamanager.CreateDatasetRequest{
    Name:           "<dataset_name>",
    OrganizationID: "<org_id>",
})

if err != nil {
    fmt.Println("Error creating dataset. It may already exist.")
    fmt.Printf("Exception: %v\n", err)
    return
}

fmt.Printf("Created dataset: %s\n", datasetID)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

To create a dataset, pass a unique dataset name and organization ID to [`dataClient.createDataset`](/dev/reference/apis/data-client/#createdataset):

```typescript
const client = await createViamClient();
const dataClient = client.dataClient;

console.log("Creating dataset...");

try {
  const datasetId = await dataClient.createDataset({
    name: "<dataset_name>",
    organizationId: "<org_id>",
  });
  console.log(`Created dataset: ${datasetId}`);
} catch (error) {
  console.log("Error creating dataset. It may already exist.");
  console.log(`Exception: ${error}`);
  process.exit(1);
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

To create a dataset, pass a unique dataset name and organization ID to [`dataClient.createDataset`](/dev/reference/apis/data-client/#createdataset):

```dart
final viamClient = await ViamClient.connect();
final dataClient = viamClient.dataClient;

print("Creating dataset...");

try {
    final datasetId = await dataClient.createDataset(
        name: "<dataset_name>",
        organizationId: "<org_id>",
    );
    print("Created dataset: $datasetId");
} catch (e) {
    print("Error creating dataset. It may already exist.");
    print("Exception: $e");
    return;
}
```

{{% /tab %}}
{{< /tabs >}}

Finish creating a dataset by adding annotated images to it.
You can capture new images or add existing images:

{{< cards >}}
{{% card link="/data-ai/train/capture-images/" noimage="true" %}}
{{% card link="/data-ai/train/update-dataset/" noimage="true" %}}
{{% card link="/data-ai/train/annotate-images/" noimage="true" %}}
{{< /cards >}}
