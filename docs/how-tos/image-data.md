---
title: "Capture, filter, and sync image data"
linkTitle: "Capture and sync image data"
weight: 20
type: "docs"
tags: ["data management", "data", "services"]
images: ["/services/ml/collect.svg"]
description: "Capture images from a camera on your machine and selectively sync images to the cloud with filtering."
aliases:
  - /use-cases/image-data/
  - /tutorials/projects/filtered-camera
languages: []
viamresources: ["camera", "data_manager", "mlmodel", "vision"]
platformarea: ["ml", "data"]
level: "Intermediate"
date: "2024-08-26"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can use Viam's built-in data management service to capture images from a camera on your machine and sync the images to the cloud.

If you want to control the volume of data your machine writes and syncs, you can use a "filtering camera" and only capture images that contain a person or object detected by an ML model.
The filtering camera uses a computer vision model to detect objects in your camera feed and selectively stores and uploads only those images that are matched by your model.

With your images synced to the cloud, you can view images from all your machines in the Viam app interface.
From there, you can use your image data to do things like [train ML models](/how-tos/deploy-ml/).

![Data view](/services/data/delete_all.png)
<br>

{{< alert title="In this page" color="tip" >}}

1. [Collect image data and sync it to the cloud](#collect-image-data-and-sync-it-to-the-cloud)
1. [Stop data capture](#stop-data-capture).
1. [Use filtering to collect and sync only certain images](#use-filtering-to-collect-and-sync-only-certain-images)

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A configured camera. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a camera model](/components/camera/) that supports your camera.

If you are not sure what to use, start with a [webcam](/components/camera/webcam/) which supports most USB cameras and inbuilt laptop webcams.

{{% /expand%}}

## Collect image data and sync it to the cloud

Adding the data management service to your machine enables you to capture and sync data:

{{< gif webm_src="/how-tos/capture-images.webm" mp4_src="/how-tos/capture-images.mp4" alt="Configuring data management for a camera in the viam app" max-width="600px" class="aligncenter" >}}

{{< table >}}
{{% tablestep link="/services/data/" %}}
**1. Enable the data management service**

In the configuration pane for your configured camera component, find the **Data capture** section.
Click **Add method**.

When the **Create a data management service** prompt appears, click it to add the service to your machine.
You can leave the default data manager settings.

{{% /tablestep %}}
{{% tablestep %}}
**2. Capture data**

With the data management service configured on your machine, configure how the camera component itself captures data:

In the **Data capture** panel of your camera's configuration, select `ReadImage` from the method selector.

Set your desired capture frequency.
For example, set it to `0.05` to capture an image every 20 seconds.

Set the MIME type to your desired image format, for example `image/jpeg`.

{{% /tablestep %}}
{{% tablestep %}}
**3. Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. View data in the Viam app**

Click on the **...** menu of the camera component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/cam-capt-data.png)

If you do not see images from your camera, try waiting a minute and refreshing the page to allow time for the images to be captured and then synced to the app at the interval you configured.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs).

{{% /tablestep %}}
{{< /table >}}

{{% alert title="Tip" color="tip" %}}
To keep your data organized, you can configure a tag in your data management service config panel.
This tag will be applied to all data synced from that machine in the future.
If you apply the same tag to all data gathered from all machines that you want to use in your dataset, you can filter by that tag in the Viam app **DATA** tab, or when querying data.

This is not required, since you can use other filters like time or machine ID in the **DATA** tab to isolate your data.
{{% /alert %}}

You now know how to capture and sync image data.
For many use cases, you may not want to capture data unless it meets certain conditions.
Consider the example of a security camera that captures data every 5 seconds.
This setup would result in a large number of images, of which most wouldn't be interesting.

In the next part of this guide, you will learn how to filter the data before capturing and syncing it.

## Stop data capture

If this is a test project or if you are continuing this how to set up filtering, make sure you stop data capture to avoid [incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of test data.

In the **Data capture** section of your camera's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Use filtering to collect and sync only certain images

You can use filtering to selectively capture images using a machine learning (ML) model, for example to only capture images with people or specific objects in them.

Contributors have written several filtering {{< glossary_tooltip term_id="module" text="modules" >}} that you can use to filter image capture.
The following steps use the [`filtered_camera`](https://github.com/erh/filtered_camera) module:

{{< table >}}
{{% tablestep link="/services/ml/deploy/"%}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model service to your machine**

Add an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](/services/ml/deploy/tflite_cpu/).

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/icons/ml.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**2. Select a suitable ML model**

Click **Select model** on the ML model service configuration panel, then select an [existing model](https://app.viam.com/registry?type=ML+Model) you want to use, or click **Add new model** to upload your own.
If you're not sure which model to use, you can use [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO) from the **Registry**, which can detect people and animals, among other things.

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**3. Add a vision service to use with the ML model**

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Add and configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/modular-registry.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. Configure the filtered camera**

The `filtered-camera` {{< glossary_tooltip term_id="modular-resource" text="modular component" >}} pulls the stream of images from the camera you configured earlier, and applies the vision service to it.

Configure a `filtered-camera` component on your machine, following the [attribute guide in the README](https://github.com/erh/filtered_camera?tab=readme-ov-file#configure-your-filtered-camera).
Use the name of the camera you configured in the first part of this guide as the `"camera"` to pull images from, and select the name of the vision service you just configured as your `"vision"` service.
Then add all or some of the labels your ML model uses as classifications or detections in `"classifications"` or `"objects"`.

For example, if you are using the `EfficientDet-COCO` model, you could use a configuration like the following to only capture images when a person is detected with more than 60% confidence in your camera stream.

```json {class="line-numbers linkable-line-numbers"}
{
  "window_seconds": 0,
  "objects": {
    "Person": 0.8
  },
  "camera": "camera-1",
  "vision": "vision-1"
}
```

Additionally, you can also add a buffer window with `window_seconds` which controls the duration of a buffer of images captured prior to a successful match.
If you were to set `window_seconds` to `3`, the camera would also capture and sync images from the 3 seconds before a person appeared in the camera stream.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**5. Configure data capture and sync on the filtered camera**

Configure data capture and sync on the filtered camera just as you did before for the physical camera.
The filtered camera will only capture image data that passes the filters you configured in the previous step.

Turn off data capture on your original camera if you haven't already, so that you don't capture duplicate or unfiltered images.

{{% /tablestep %}}
{{% tablestep %}}
**6. Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

{{% /tablestep %}}
{{% tablestep %}}

{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**7. View filtered data in the Viam app**

Once you save your configuration, place something that is part of your trained ML model within view of your camera.

Images that pass your filter will be captured and will sync at the specified sync interval, which may mean you have to wait and then refresh the page for data to appear.
Your images will begin to appear under the **DATA** tab.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs) and ensure that the condition for filtering is met.
You can test the vision service from the [**CONTROL** tab](/cloud/machines/#control) to see its classifications and detections live.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**7. (Optional) Trigger sync with custom logic**

By default, the captured data syncs at the regular interval you specified in the data capture config.
If you need to trigger sync in a different way, see [Trigger cloud sync conditionally](/how-tos/trigger-sync/) for a documented example of syncing data only at certain times of day.

{{% /tablestep %}}
{{< /table >}}

## Stop data capture on the filtered camera

If this is a test project, make sure you stop data capture to avoid [incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of test data.

In the **Data capture** section of your filtered camera's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Next steps

Now that you have collected image data, you can [train new computer vision models](/how-tos/deploy-ml/) or [programmatically access your data](https://docs.viam.com/appendix/apis/data-client/):

{{< cards >}}
{{% card link="/how-tos/deploy-ml/" %}}
{{% card link="/appendix/apis/data-client/" %}}
{{< /cards >}}

To see image data filtering in action, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/configure/pet-photographer.md" %}}
{{< /cards >}}
