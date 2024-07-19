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

If you'd like to follow a more detailed tutorial, see [Selectively Capture Data Using filtered-camera](/tutorials/projects/filtered-camera/).

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Collect image data and sync it to the cloud

{{< table >}}
{{% tablestep link="/components/camera/"%}}
{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**1. Configure a camera**

On your [machine's page](#prerequisites), configure any camera component.
If you are not sure what to use, start with a [webcam](/components/camera/webcam/).

{{% /tablestep %}}
{{% tablestep link="/services/data/"%}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**2. Enable the data management service**

In your camera component configuration panel, find the **Data capture** section.
Click **Add method**.

When the **Create a data management service** prompt appears, click it to add the service to your machine.
You can leave the default data manager settings.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**3. Capture data**

With the data management service configured on your machine, you can continue configuring how the camera component itself captures data.

In the **Data capture** panel of your camera's config, select **Read image** from the method selector.

Set your desired capture frequency.
For example, set it to `0.05` to capture an image every 20 seconds.

Set the MIME type to your desired image format, for example `image/jpeg`.

Click save to start capturing data.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. View data in the Viam app**

{{< alert title="Wait until data appears" color="note" >}}
Once you have saved your configuration changes, your data will sync at the specified sync interval, which may mean you have to wait and then refresh the page for data to appear.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs).
{{< /alert >}}

Once you have synced images, you can [view those images in the Viam app](/services/data/view/) from the **DATA** tab in the top navigation bar.

You can also [export your data from the Viam app](/services/data/export/) to a deployed machine, or to any computer.

{{% /tablestep %}}
{{< /table >}}

You now know how to capture and sync image data.

{{< alert title="Avoid fees by disabling data capture" color="note" >}}
If this is not a production machine and you have confirmed that your machine is capturing and syncing data, disable data capture in the camera configuration to avoid [incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of test data.
{{< /alert >}}

For many use cases, you may not want to capture data unless it meets certain conditions.
Consider the example of a security camera that captures data every 5 seconds.
This setup would result in a large number of images, of which most wouldn't be interesting.
In the next part of this guide, you will learn how to filter the data before capturing and syncing it.

## Use filtering to collect and sync only certain images

You can use filtering to selectively capture images using a machine learning (ML) model, for example to only capture images with people in them.

Contributors have written several filtering {{< glossary_tooltip term_id="module" text="modules" >}} that you can use to filter image capture.
The following steps use the [`filtered_camera`](https://github.com/erh/filtered_camera) module:

{{< table >}}
{{% tablestep link="/services/ml/deploy/"%}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model to your machine**

Configure an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](/services/ml/deploy/tflite_cpu/).

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model to your machine**

From the **Model** dropdown, select an [existing model](https://app.viam.com/registry?type=ML+Model) you want to use, or click **Add new model** to upload your own.
If you're not sure which model to add, you can add [`EfficientNet-ImageNet2012`](https://app.viam.com/ml-model/viam/EfficientNet-ImageNet2012) which can detect people and animals, among other things.

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**3. Add a vision service to use with the ML model**

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/modular-registry.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. Configure the filtered camera**

The `filtered-camera` {{< glossary_tooltip term_id="modular-resource" text="modular component" >}} pulls the stream of images from the camera you configured earlier, and applies the vision service to it.

Configure a `filtered-camera` component on your machine, following the [attribute guide in the README](https://github.com/erh/filtered_camera?tab=readme-ov-file#configure-your-filtered-camera) to specify the names of your camera and vision service, and add classification and object detection filters.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**5. Configure data capture and sync on the filtered camera**

Configure data capture and sync just as you did before.
The filtered camera will only capture image data that passes the filters you configured in the previous step.

Turn off data capture on your camera if you haven't already, so that you don't capture duplicate or unfiltered images.

{{% /tablestep %}}
{{% tablestep %}}

{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**6. View filtered data in the Viam app**

Once you save your configuration, your filtered images will sync and you can [view those images in the Viam app](/services/data/view/) from the **DATA** tab.

{{< alert title="Wait until data appears" color="note" >}}
Your data will sync at the specified sync interval, which may mean you have to wait for data to appear.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs) and ensure that the condition for filtering is met.
You can add a [`transform` camera](/components/camera/transform/) to see detections or classifications live from the [**CONTROL** tab](/cloud/machines/#control).
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**7. (Optional) Trigger sync with custom logic**

By default, the captured data syncs at the regular interval you specified in the data capture config.
If you need to trigger sync in a different way, see [Trigger cloud sync conditionally](/services/data/trigger-sync/) for a documented example of syncing data only at certain times of day.

{{% /tablestep %}}
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
