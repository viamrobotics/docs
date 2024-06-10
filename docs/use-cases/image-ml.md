---
title: "How to collect and do useful things with images"
linkTitle: "Image data and vision"
weight: 20
type: "docs"
images: ["/services/ml/collect.svg"]
description: "Collect images and do interesting things with computer vision, ML, and webhooks."
---

You can use Viam's integrated tools to capture images from your cameras and use that image data with machine learning to do a variety of useful things.

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/use-cases/ml-vision-diagram.png)

For example, you can train a model to recognize your dog and detect whether they are sitting or standing.
Then, you can configure your machine to capture images only when your dog is in the camera frame so you don't capture hundreds of photos of an empty room.
You can configure filtering and webhooks to send you a picture of your dog when they are sitting.

You can do most of this using the [Viam app](https://app.viam.com) user interface.
You will not need to write any code unless you want to use webhooks.

<div style="border:1px solid; box-shadow:5px 5px 0 0;padding:1rem; margin:1rem; background-color:#f5f5f5">

**In this page:**

1. [Collect image data and sync it to the cloud](#collect-image-data-and-sync-it-to-the-cloud)
2. [Use filtering to collect and sync only certain images](#use-filtering-to-collect-and-sync-only-certain-images)
3. [Create a dataset and label data](#create-a-dataset-and-label-data)
4. [Train and test a machine learning (ML) model](#train-and-test-a-machine-learning-ml-model)
5. [Set up webhook alerts when certain things are identified in an image](#set-up-webhook-alerts-when-certain-things-are-identified-in-an-image)

</div>

## Collect image data and sync it to the cloud

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**1. Configure a camera [_(i)_](/components/camera/)**

First, [create a machine](/cloud/machines/#add-a-new-machine) if you haven't yet.

Configure a camera component, such as a [webcam](/components/camera/webcam/), on your machine.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**2. Enable the data management service [_(i)_](/services/data/)**

In your camera component configuration panel, find the **Data capture** section.
Click **Add method** and follow the prompt to **Create data management service**.
You can leave the default data manager settings.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**3. Capture data**

With the data management service configured on your machine, you can continue configuring how the camera component itself captures data.
In the **Data capture** panel of your camera's config, select **Read image** from the method selector, and set your desired capture frequency.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. View data in the Viam app**

Once you have synced images, you can [view those images in the Viam app](/services/data/view/) from the **DATA** tab in the top navigation bar.

You can also [export your data from the Viam app](/services/data/export/) to a deployed machine, or to any computer.

{{< /tablestep >}}
{{< /table >}}

## Use filtering to collect and sync only certain images

You can use filtering to selectively capture images, and you can also use filtering to sync only certain images.
In each case, you can filter based on an ML model, or you can create your own filtering logic.

Contributors have written several filtering {{< glossary_tooltip term_id="module" text="modules" >}} that you can use to filter image capture and sync.
The following steps use the [`filtered_camera`](https://github.com/erh/filtered_camera) module:

### Filter image capture with an ML model

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model to your machine [_(i)_](/services/ml/deploy/)**

Configure an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](/services/ml/deploy/tflite_cpu/).

From the **Model** dropdown, select the preexisting model you want to use, or click **Add new model** to upload your own.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**2. Add a vision service to use with the ML model [_(i)_](/services/vision/)**

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/modular-registry.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**3. Configure the filtered camera**

The `filtered-camera` {{< glossary_tooltip term_id="modular-resource" text="modular component" >}} pulls the stream of images from the camera you configured earlier, and applies the vision service to it.

Configure a `filtered-camera` component on your machine, following the [attribute guide in the README](https://github.com/erh/filtered_camera?tab=readme-ov-file#configure-your-filtered-camera) to specify the names of your webcam and vision service, and add classification and object detection filters.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. Configure data capture and sync on the filtered camera**

Configure data capture and sync just as you would for a webcam.
The filtered camera will only capture image data that passes the filters you configured in the previous step.

Turn off data capture on your webcam if you haven't already, so that you don't capture duplicate or unfiltered images.

{{< /tablestep >}}
{{< /table >}}

### Filter image sync with other filtering logic

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**Write your custom logic or find a module written by another user**

See [Trigger cloud sync conditionally](/services/data/trigger-sync/) for a documented example.

{{< /tablestep >}}
{{< /table >}}

## Create a dataset and label data

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**1. Collect images**

Start by collecting images from your cameras and syncing it to the [Viam app](https://app.viam.com).
See [Collect image data and sync it to the cloud](#collect-image-data-and-sync-it-to-the-cloud) above for instructions.

{{% alert title="Tip" color="tip" %}}
To keep your data organized, configure a tag in your data management service config panel.
This tag will be applied to all data synced from that machine.
If you apply the same tag to all data gathered from all machines that you want to use in your dataset, you can filter by that tag in the Viam app **DATA** tab to make the next steps easier.

This is not required, since you can use other filters like time or machine ID in the **DATA** tab to isolate your data.
{{% /alert %}}

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Label data">}}
**2. Label your images [_(i)_](/services/data/dataset/)**

Once you have enough images of the objects you'd like to classify, use the interface on the **DATA** tab to label your data.
If you want to train an image classifier, use image tags.
For an object detector, use bounding boxes.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/label.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Label data">}}
**2. Create a dataset [_(i)_](/services/data/dataset/)**

Use the interface on the **DATA** tab (or the [`viam data dataset add` command](/cli/#data)) to add all images you want to train the model on to a dataset.

{{< /tablestep >}}
{{< /table >}}

## Train and test a machine learning (ML) model

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**1. Train an ML model [_(i)_](/services/ml/train-model/)**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/services/data/datasets) and select the one you want to train on.
Click **Train model** and follow the prompts.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**2. Deploy your ML model [_(i)_](/services/ml/deploy/)**

To make use of ML models with your machine, configure the built-in ML model service on your machine to deploy and run the model.
Once you've added it, choose your newly-trained model from the dropdown menu.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure a service">}}
**3. Configure an <code>mlmodel</code> vision service [_(i)_](/services/vision/)**

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your model">}}
**4. Test your classifier [_(i)_](/services/vision/mlmodel/#test-your-detector-or-classifier)**

Test your mlmodel classifier with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud), [live camera footage,](/services/vision/mlmodel/#live-camera-footage) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

{{< /tablestep >}}
{{< /table >}}

## Set up webhook alerts when certain things are identified in an image

Not finished

## Next steps

See the following tutorials for examples of how to use the tools described on this page:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/verification-system/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
