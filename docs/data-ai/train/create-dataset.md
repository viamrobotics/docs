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

To train a machine learning model, you will need a dataset that meets the following conditions:

{{< readfile "/static/include/data/dataset-requirements.md" >}}

## Create a dataset

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

{{< read-code-snippet file="/static/include/examples-generated/create-dataset.snippet.create-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="31-34" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To create a dataset, pass a unique dataset name and organization ID to [`DataClient.CreateDataset`](/dev/reference/apis/data-client/#createdataset):

{{< read-code-snippet file="/static/include/examples-generated/create-dataset.snippet.create-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="30" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To create a dataset, pass a unique dataset name and organization ID to [`dataClient.createDataset`](/dev/reference/apis/data-client/#createdataset):

{{< read-code-snippet file="/static/include/examples-generated/create-dataset.snippet.create-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="27-30" >}}

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

You can now add images to your dataset.

## Add to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. Click to select the images you would like to add to your dataset.

1. Click the **Add to dataset** button in the top right.

1. From the **Dataset** dropdown, select the name of your dataset.

1. Click **Add \<n\> images** to add the selected images to the dataset.

{{< alert title="Tip" color="tip" >}}

To select a range of images, select one image, then hold **Ctrl/Cmd** while clicking another image.
This will select both images as well as the entire range of images between those images.

{{< /alert >}}

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, [create a dataset](/data-ai/train/create-dataset/), if you haven't already.

1. If you just created a dataset, use the dataset ID output by the creation command.
   If your dataset already exists, run the following command to get a list of dataset names and corresponding IDs:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset list
   ```

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with a subset of tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID output by the command in the previous step:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Python" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`data_client.add_binary_data_to_dataset_by_ids`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="31-34" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`DataClient.AddBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="30-34" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`dataClient.addBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="26-29" >}}

{{% /tab %}}
{{< /tabs >}}

## Add all images captured by a specific machine to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. From the **Machine name** dropdown, select the name of a machine.
1. Click the **Apply** button at the bottom of the left sidebar.
1. Click to select the images you would like to add to your dataset.
1. Click the **Add to dataset** button in the top right.
1. From the **Dataset** dropdown, select the name of your dataset.
1. Click **Add \<n\> images** to add the selected images to the dataset.

{{< alert title="Tip" color="tip" >}}

To select a range of images, select one image, then hold **Ctrl/Cmd** while clicking another image.
This will select both images as well as the entire range of images between those images.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Python" %}}

The following script adds all images captured from a certain machine to a new dataset:

{{< read-code-snippet file="/static/include/examples-generated/add-machine-images-to-dataset.snippet.add-machine-images-to-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="56-61" >}}

{{% /tab %}}
{{% tab name="Go" %}}

The following script adds all images captured from a certain machine to a new dataset:

{{< read-code-snippet file="/static/include/examples-generated/add-machine-images-to-dataset.snippet.add-machine-images-to-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="88-92" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

The following script adds all images captured from a certain machine to a new dataset:

{{< read-code-snippet file="/static/include/examples-generated/add-machine-images-to-dataset.snippet.add-machine-images-to-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="61-64" >}}

{{% /tab %}}
{{% tab name="Flutter" %}}

The following script adds all images captured from a certain machine to a new dataset:

```dart
import 'package:viam_sdk/viam_sdk.dart';

// Configuration constants - replace with your actual values
const String datasetName = ""; // a unique, new name for the dataset you want to create
const String orgId = ""; // your organization ID, find in your organization settings
const String partId = ""; // ID of machine that captured target images, find in machine config
const String apiKey = ""; // API key, find or create in your organization settings
const String apiKeyId = ""; // API key ID, find or create in your organization settings
const int maxMatches = 500;

Future<ViamClient> connect() async {
  return await ViamClient.withApiKey(
    apiKey: apiKey,
    apiKeyId: apiKeyId,
  );
}

Future<List<BinaryData>> fetchBinaryDataIds(
    DataClient dataClient, String partId) async {
  final filter = Filter(partId: partId);
  final List<BinaryData> allMatches = [];
  String? last;

  print("Getting data for part...");

  while (allMatches.length < maxMatches) {
    print("Fetching more data...");

    final response = await dataClient.binaryDataByFilter(
      filter: filter,
      limit: 50,
      last: last,
      includeBinaryData: false,
    );

    if (response.data.isEmpty) {
      break;
    }

    allMatches.addAll(response.data);
    last = response.last;
  }

  return allMatches;
}

Future<int> main() async {
  final viamClient = await connect();
  final dataClient = viamClient.dataClient;

  final matchingData = await fetchBinaryDataIds(dataClient, partId);

  print("Creating dataset...");

  try {
    final datasetId = await dataClient.createDataset(
      name: datasetName,
      organizationId: orgId,
    );
    print("Created dataset: $datasetId");

    print("Adding data to dataset...");

    final binaryIds = matchingData
        .map((obj) => obj.metadata.binaryDataId)
        .toList();

    await dataClient.addBinaryDataToDatasetByIds(
      binaryIds: binaryIds,
      datasetId: datasetId,
    );

    print("Added files to dataset.");
    print("See dataset: https://app.viam.com/data/datasets?id=$datasetId");

    viamClient.close();
    return 0;

  } catch (error) {
    print("Error creating dataset. It may already exist.");
    print("See: https://app.viam.com/data/datasets");
    print("Exception: $error");
    viamClient.close();
    return 1;
  }
}
```

{{% /tab %}}
{{< /tabs >}}

## Use an existing dataset

If you have used the `viam dataset export` command to export a dataset or if you've been given a dataset from someone else you can use the following script to import the dataset.
If you have a dataset that was not exported with Viam, you will need to make changes to this script.

{{% read-code-snippet file="/static/include/examples-generated/use-existing-dataset.snippet.use-existing-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line=" " %}}

{{% expand "Looking for test datasets?" %}}
We have two datasets you can use for testing, one with shapes and the other with a wooden figure:

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:400px" alt="The shapes dataset." class="imgzoom fill aligncenter shadow" >}}

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" style="width:400px" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" class="imgzoom fill aligncenter" resize="1400x" >}}

1. [Download the shapes dataset](https://storage.googleapis.com/docs-blog/dataset-shapes.zip) or [download the wooden figure dataset](https://storage.googleapis.com/docs-blog/dataset-figure.zip).
1. Unzip the download.
1. Use the above script.

{{% /expand%}}
