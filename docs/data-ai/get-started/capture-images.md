---
linkTitle: "Capture"
title: "Capture"
weight: 20
layout: "docs"
type: "docs"
description: "Capture images for a training dataset"
---

{{< tabs >}}
{{% tab name="One image" %}}

You can add images to a dataset directly from a camera or vision component feed in the **CONTROL** or **CONFIGURATION** tabs of the Viam app.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page's [**DATASETS** tab](https://app.viam.com/data/datasets) in the Viam app and select your dataset.

{{% /tab %}}
{{% tab name="Many images" %}}

To capture a large number of images for training an ML model, [Capture and sync image data](/data-ai/edge/capture-sync/) using the data management service with your camera.

Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
We recommend you tag the images first and then use the CLI to [add the tagged images to a dataset](/data-ai/g//#add-tagged-images-to-a-dataset).

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}
{{% /tab %}}
{{< /tabs >}}

Once you've captured enough images for training, you must annotate them to train a model.
