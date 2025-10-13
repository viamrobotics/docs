---
linkTitle: "Annotate images"
title: "Annotate images for training"
weight: 20
layout: "docs"
type: "docs"
description: "Annotate images to train a machine learning model."
date: "2025-10-11"
aliases:
  - /data-ai/train/capture-annotate-images/
---

To train a machine learning model, you must have a set of annotated images to train on.

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand%}}

{{< alert title="Tip" color="tip" >}}

For the best results, use the same camera for both capturing training data and production deployment.

{{< /alert >}}

## Annotate images

You must annotate images in order to train an ML model on them.
Viam supports two annotations for images:

- [Tags for whole images (classification)](#add-tags-to-an-image)
- [Bounding boxes around objects within images (object detection)](#label-objects-within-an-image)

### Add tags to an image

Use tags to add metadata about an entire image, for example whether the quality of a manufacturing output is `good` or `bad`.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

You can tag your data automatically with an existing ML model, if you have one, or manually:

{{< tabs >}}
{{% tab name="Automatic" %}}

To use auto-predictions, you must first [add your images to a dataset](/data-ai/train/create-dataset/).

1. Navigate to your [dataset's](https://app.viam.com/datasets/) page.
1. Click on **Get auto-predictions**.
1. **Select** a classification model to generate predictions with.
1. Set the **confidence threshold** above which to create a label prediction.
1. Click **Get predictions**.
1. Once predictions have finished generating, click on **Review predictions**.
1. For each image, **Accept (A)** or **Reject (R)** each prediction.

   {{<imgproc src="/data-ai/review-ui.png" resize="1200x" class="imgzoom shadow" declaredimensions=true alt="UI for reviewing predictions">}}

{{% /tab %}}
{{% tab name="Manual" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-star.webm" mp4_src="/services/data/tag-star.mp4" alt="Tag image with a full label">}}

1. Repeat these steps for all images in the dataset.

{{% /tab %}}
{{< /tabs >}}

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

Once you've annotated your dataset, you can [train](/data-ai/train/train-tf-tflite/) an ML model to make inferences.

### Label objects within an image

Use labels to add metadata about objects within an image, for example by drawing bounding boxes around each bicycle in a street scene and adding the bicycle label.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

You can label your data automatically with an existing ML model, if you have one, or manually:

{{< tabs >}}
{{% tab name="Automatic" %}}

To use auto-predictions, you must first [add your images to a dataset](/data-ai/train/create-dataset/).

1. Navigate to your [dataset's](https://app.viam.com/datasets/) page.
1. Click on **Get auto-predictions**.
1. **Select** a object detection model to generate predictions with.
1. Set the **confidence threshold** above which to create a label prediction.
1. Click **Get predictions**.
1. Once predictions have finished generating, click on **Review predictions**.
1. For each image, **Accept (A)** or **Reject (R)** each prediction.

   {{<imgproc src="/data-ai/review-ui-detection.png" resize="1200x" class="imgzoom shadow" declaredimensions=true alt="UI for reviewing predictions">}}

{{% /tab %}}
{{% tab name="Manual" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-figure.webm" mp4_src="/services/data/label-figure.mp4" alt="Add a bounding box around the viam figure in an image">}}

1. Repeat these steps for all images in the dataset.

{{< alert title="Tip" color="tip" >}}
Once created, you can move, resize, or delete the bounding box.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

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

Once you've annotated your dataset, you can [train](/data-ai/train/train-tf-tflite/) an ML model to make inferences.

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
