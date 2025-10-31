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
date: "2025-10-11"
---

To train a machine learning model, you will need a dataset that meets the following conditions:

{{< readfile "/static/include/data/dataset-requirements.md" >}}

## Create a dataset

You can create a dataset using the web UI, the CLI, or one of the SDKs:

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Navigate to the **DATA** page and open the [**DATASETS** tab](https://app.viam.com/datasets).

1. Click the **+ Create dataset** button.

   {{< imgproc src="/services/data/create-dataset.png" alt="The **DATASETS** tab of the **DATA** page, showing the **+ Create dataset** button." resize="800x" style="width:500px" class="imgzoom shadow" >}}

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
{{< /tabs >}}

Now that you've created a dataset, you can add images to it.

## Capture images

You can either [capture individual images](#capture-individual-images) or [capture images periodically over time](#capture-images-over-time).

### Capture individual images

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset directly from a camera or vision component feed in the machine's **CONTROL** or **CONFIGURATION** tabs.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom shadow" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page, open the [**DATASETS** tab](https://app.viam.com/datasets), then select your dataset.

{{% /tab %}}
{{% tab name="Python" %}}

To capture an image and upload it to Viam, first get an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`data_client.binary_data_capture_upload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="42-55" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To capture an image and upload it to Viam, first get an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`DataClient.BinaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="55-82" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To capture an image and upload it to Viam, first get an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`dataClient.binaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="41-54" >}}

{{% /tab %}}
{{< /tabs >}}

Once you've captured enough images for training, you must [annotate](/data-ai/train/annotate-images/) the images before you can use them to train a model.

### Capture images over time

To capture a large number of images for training an ML model, use the data management service to [capture and sync image data](/data-ai/capture-data/capture-sync/) from your camera.

When you sync with data management, Viam stores the images in the cloud and you can access them on the [**DATA** page](https://app.viam.com/data/).
To use your captured images for training, [add the images to a dataset](#add-existing-images-to-a-dataset).

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}

## Add existing images to a dataset

If you have already uploaded images to Viam, you can [add selected images to a dataset](#add-selected-images-to-a-dataset) or [add filtered images to a dataset](#add-filtered-images-to-a-dataset).

### Add selected images to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. Filter the images with tags or other filters.

1. Select the images you would like to add to your dataset.

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

1. Use the dataset ID output by the dataset creation command or run the following command to get a list of dataset names and corresponding IDs:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset list
   ```

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with the specified tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Python" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
You can retrieve the binary data IDs from the [**DATA** tab](https://app.viam.com/data/view).
Click on an image and copy the binary data ID from the **DETAILS** section.

You can retrieve the dataset ID from the [**DATASETS** tab](https://app.viam.com/datasets/).
Click on the dataset.
On the dataset page, click the **...** menu next to the dataset name, then click **Copy dataset ID**.

Pass both IDs to [`data_client.add_binary_data_to_dataset_by_ids`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="30-33" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
You can retrieve the binary data IDs from the [**DATA** tab](https://app.viam.com/data/view).
Click on an image and copy the binary data ID from the **DETAILS** section.

You can retrieve the dataset ID from the [**DATASETS** tab](https://app.viam.com/datasets/).
Click on the dataset.
On the dataset page, click the **...** menu next to the dataset name, then click **Copy dataset ID**.

Pass both IDs to [`DataClient.AddBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="30-34" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
You can retrieve the binary data IDs from the [**DATA** tab](https://app.viam.com/data/view).
Click on an image and copy the binary data ID from the **DETAILS** section.

You can retrieve the dataset ID from the [**DATASETS** tab](https://app.viam.com/datasets/).
Click on the dataset.
On the dataset page, click the **...** menu next to the dataset name, then click **Copy dataset ID**.

Pass both IDs to [`dataClient.addBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

{{< read-code-snippet file="/static/include/examples-generated/add-to-dataset.snippet.add-to-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="26-29" >}}

{{% /tab %}}
{{< /tabs >}}

### Add filtered images to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. Use the filters side menu to select filters. For example, from the **Machine name** dropdown, select the name of a machine.
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
{{< /tabs >}}

## Use an existing dataset

If you have used the `viam dataset export` command to export a dataset or if you've been given a dataset from someone else, you can use the following script to import the dataset.
If you have a dataset that was not exported with Viam, you will need to make changes to this script.

{{< tabs >}}
{{% tab name="Python" %}}

{{% read-code-snippet file="/static/include/examples-generated/use-existing-dataset.snippet.use-existing-dataset.py" lang="python" class="line-numbers linkable-line-numbers" %}}

{{% /tab %}}
{{< /tabs >}}

{{% expand "Looking for test datasets?" %}}
We have two datasets you can use for testing, one with shapes and the other with a wooden figure:

{{< imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:400px" alt="The shapes dataset." class="imgzoom fill aligncenter shadow" >}}

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" style="width:400px" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" class="imgzoom fill aligncenter" resize="1400x" >}}

1. [Download the shapes dataset](https://storage.googleapis.com/docs-blog/dataset-shapes.zip) or [download the wooden figure dataset](https://storage.googleapis.com/docs-blog/dataset-figure.zip).
1. Unzip the download.
1. Use the above script.

{{% /expand %}}

## Merge datasets

You can combine two datasets to create a new dataset using the web UI:

1. Navigate to the **DATA** page and open the [**DATASETS** tab](https://app.viam.com/datasets).
1. Click the **...** menu on the dataset.
1. Select **Merge...** from the context menu.
1. Choose the dataset you want to merge with from the dropdown menu.
1. Enter a name for the new merged dataset.
1. Click **Merge datasets** to create the new combined dataset.
   The original datasets remain unchanged after merging.
   The merge operation creates a new dataset containing all the data from both source datasets.
