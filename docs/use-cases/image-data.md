---
title: "How to capture, filter, and sync image data"
linkTitle: "Capture and sync image data"
weight: 20
type: "docs"
tags: ["data management", "data", "services"]
images: ["/services/ml/collect.svg"]
description: "Capture images from a camera on your machine and selectively sync images to the cloud with filtering."
---

You can use Viam's built-in data management service to capture images from a camera on your machine and sync the images to the cloud.

If you want to capture only certain images, such as those containing a person, you can use a "filtering camera" to selectively capture images based on a computer vision model.

With your images synced to the cloud, you can view images from all your machines in one Viam app interface.
From there, you can use your image data to do things like [train ML models](/use-cases/deploy-ml/).

{{<imgproc src="/use-cases/ml-cycle.svg" declaredimensions=true alt="Cyclical diagram of a plant watering machine capturing images of plants, syncing those images to the cloud, a machine learning model being trained, and that model being used to recognize yellow leaves on plants and water them." style="max-width:350px" class="aligncenter">}}
<br>

{{< alert title="In this page" color="tip" >}}

1. [Collect image data and sync it to the cloud](#collect-image-data-and-sync-it-to-the-cloud)
2. [Use filtering to collect and sync only certain images](#use-filtering-to-collect-and-sync-only-certain-images)

{{< /alert >}}

In the next how-to guide you can use the images you collect here to [train computer vision models](/use-cases/deploy-ml/).

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Collect image data and sync it to the cloud

{{< table >}}
{{< tablestep link="/components/camera/">}}
{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**1. Configure a camera**

Configure a camera component, such as a [webcam](/components/camera/webcam/), on your machine.

{{< /tablestep >}}
{{< tablestep link="/services/data/">}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**2. Enable the data management service**

In your camera component configuration panel, find the **Data capture** section.
Click **Add method** and follow the prompt to **Create a data management service**.
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

You can use filtering to selectively capture images using a machine learning (ML) model, for example to only capture images with people in them.

Contributors have written several filtering {{< glossary_tooltip term_id="module" text="modules" >}} that you can use to filter image capture.
The following steps use the [`filtered_camera`](https://github.com/erh/filtered_camera) module:

{{< table >}}
{{< tablestep link="/services/ml/deploy/">}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model to your machine**

Configure an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](/services/ml/deploy/tflite_cpu/).

From the **Model** dropdown, select the preexisting model you want to use, or click **Add new model** to upload your own.

{{< /tablestep >}}
{{< tablestep link="/services/vision/">}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**2. Add a vision service to use with the ML model**

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
{{< tablestep >}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**5. (Optional) Trigger sync with custom logic**

By default, the captured data syncs at the regular interval you specified in the data capture config.
If you need to trigger sync in a different way, see [Trigger cloud sync conditionally](/services/data/trigger-sync/) for a documented example of syncing data only at certain times of day.

{{< /tablestep >}}
{{< /table >}}

## Next steps

Now that you have collected image data, you can [train new computer vision models](/use-cases/deploy-ml/) or [programmatically access your data](/services/data/export/):

{{< cards >}}
{{% card link="/use-cases/deploy-ml/" %}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{< /cards >}}

To see image data filtering in action, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/filtered-camera/" %}}
{{% card link="/tutorials/configure/pet-photographer.md" %}}
{{< /cards >}}
