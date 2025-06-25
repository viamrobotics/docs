---
linkTitle: "Create training dataset"
title: "Create training dataset"
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

To create a dataset:

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Navigate to the **DATA** page and open the [**DATASETS** tab](https://app.viam.com/data/datasets).

1. Click the **+ Create dataset** button.

   {{< imgproc src="/services/data/create-dataset.png" alt="The **DATASET** tab of the **DATA** page, showing the **+ Create dataset** button." resize="800x" style="width:500px" class="imgzoom" >}}

1. Enter a unique name for the dataset.

1. Click **Create dataset** to create the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

1. First, install the Viam CLI and authenticate:

   {{< readfile "/static/include/how-to/install-cli.md" >}}

1. [Log in to the CLI](/dev/tools/cli/#authenticate).

1. Run the following command to create a dataset, replacing the `<org-id>` and `<name>` placeholders with your organization ID and a unique name for the dataset:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset create --org-id=<org-id> --name=<name>
   ```

{{% /tab %}}
{{% tab name="SDK" %}}

{{< tabs >}}
{{% tab name="Python" %}}

To create a dataset, pass a unique dataset name and organization ID to `data_client.create_dataset`:

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
    return 1
```

{{% /tab %}}
{{% tab name="Go" %}}

To create a dataset, pass a unique dataset name and organization ID to `dataClient.CreateDataset`:

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

To create a dataset, pass a unique dataset name and organization ID to `dataClient.createDataset`:

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

To create a dataset, pass a unique dataset name and organization ID to `dataClient.createDataset`:

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

{{% /tab %}}
{{< /tabs >}}

Once you create a dataset, [capture](/data-ai/train/capture-images/) images, [add](/data-ai/train/update-dataset/) the images to your dataset, and [annotate](/data-ai/train/annotate-images/) the images with training metadata to train your own ML model.
