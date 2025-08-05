---
linkTitle: "Capture and annotate images"
title: "Capture and annotate images for training"
weight: 20
layout: "docs"
type: "docs"
description: "Capture images that you can use to train a machine learning model."
---

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand%}}

{{< alert title="Tip" color="tip" >}}

For the best results, use the same camera for both training data capture and production deployment.

{{< /alert >}}

## Capture images

### Capture individual images

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset directly from a camera or vision component feed in the machine's **CONTROL** or **CONFIGURATION** tabs.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page, open the [**DATASETS** tab](https://app.viam.com/data/datasets), then select your dataset.

{{% /tab %}}
{{% tab name="Python" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`data_client.binary_data_capture_upload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="44-55" >}}

{{% /tab %}}
{{% tab name="Go" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`DataClient.BinaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="56-75" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`dataClient.binaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

{{< read-code-snippet file="/static/include/examples-generated/capture-images.snippet.capture-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="45-53" >}}

{{% /tab %}}
{{< /tabs >}}

Once you've captured [enough images for training](/data-ai/train/train-tflite/), you must [annotate](#annotate-images) the images before you can use them to train a model.

### Capture images over time

To capture a large number of images for training an ML model, use the data management service to [capture and sync image data](/data-ai/capture-data/capture-sync/) from your camera.

When you sync with data management, Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
To use your captured images for training, [add the images to a dataset](/data-ai/train/create-dataset/#add-to-a-dataset) and [annotate them](#annotate-images), so you can use them to train a model.

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}

You can either manually add annotations through the Viam web UI, or add annotations with an existing ML model.

## Annotate images

You must annotate images in order to train an ML model on them.
Viam supports two ways to annotate an image:

- [Add tags to whole images (classification)](#add-tags-to-an-image)
- [Label bounding boxes around objects within images (object detection)](#label-objects-within-an-image)

### Add tags to an image

Use tags to add metadata about an entire image, for example if the quality of a manufacturing output is `good` or `bad`.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Python" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`data_client.add_tags_to_binary_data_by_ids`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`DataClient.AddTagsToBinaryDataByIDs`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`dataClient.addTagsToBinaryDataByIds`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.

### Label objects within an image

Use labels to add metadata about objects within an image, for example by drawing bounding boxes around each bicycle in a street scene and adding the bicycle label.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-magnemite.webm" mp4_src="/services/data/label-magnemite.mp4" alt="Add a bounding box around the magnemite pokemon in an image">}}

{{< alert title="Tip" color="tip" >}}

Once created, you can move, resize, or delete the bounding box.

{{< /alert >}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Python" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`data_client.add_bounding_box_to_image_by_id`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`DataClient.AddBoundingBoxToImageByID`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`dataClient.addBoundingBoxToImageById`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.

## Capture, annotate, and add images to a dataset in a single script

The following example demonstrates how you can capture an image, use an ML model to generate annotations, and then add the image to a dataset.
You can use this logic to expand and improve your datasets continuously over time.
Check the annotation accuracy in the **DATA** tab, then re-train your ML model on the improved dataset to improve the ML model.

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}
