---
linkTitle: "Filter data"
title: "Filter data before sync"
weight: 10
layout: "docs"
type: "docs"
description: "Use filtering to collect and sync only certain images."
---

You can use filtering to selectively capture images using a machine learning (ML) model, for example to only capture images with people or specific objects in them.

Contributors have written several filtering {{< glossary_tooltip term_id="module" text="modules" >}} that you can use to filter image capture.
The following steps use the [`filtered_camera`](https://github.com/erh/filtered_camera) module:

{{< table >}}
{{% tablestep link="/services/ml/"%}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
**1. Add an ML model service to your machine**

Add an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](https://github.com/viam-modules/mlmodel-tflite).

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/icons/ml.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
**2. Select a suitable ML model**

Click **Select model** on the ML model service configuration panel, then select an [existing model](https://app.viam.com/registry?type=ML+Model) you want to use, or click **Upload a new model** to upload your own.
If you're not sure which model to use, you can use [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO) from the **Registry**, which can detect people and animals, among other things.

{{% /tablestep %}}
{{% tablestep link="/services/vision/"%}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
**3. Add a vision service to use with the ML model**

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Add and configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/modular-registry.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
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
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
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

{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
**7. View filtered data in the Viam app**

Once you save your configuration, place something that is part of your trained ML model within view of your camera.

Images that pass your filter will be captured and will sync at the specified sync interval, which may mean you have to wait and then refresh the page for data to appear.
Your images will begin to appear under the **DATA** tab.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs) and ensure that the condition for filtering is met.
You can test the vision service from the [**CONTROL** tab](/cloud/machines/#control) to see its classifications and detections live.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="width: 150px"  declaredimensions=true alt="Train models">}}
**7. (Optional) Trigger sync with custom logic**

By default, the captured data syncs at the regular interval you specified in the data capture config.
If you need to trigger sync in a different way, see [Conditional cloud sync](/how-tos/conditional-sync/) for a documented example of syncing data only at certain times of day.

{{% /tablestep %}}
{{< /table >}}

## Stop data capture on the filtered camera

If this is a test project, make sure you stop data capture to avoid [incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of test data.

In the **Data capture** section of your filtered camera's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.
