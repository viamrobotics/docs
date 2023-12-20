---
title: "Use the Filtered Camera Module to selectively capture images"
linkTitle: "Filtered Camera"
weight: 6
type: "docs"
description: "Make a functional guardian with a servo motor, some LEDs, a camera, and the ML Model and vision service to detect people and pets."
webmSrc: "/tutorials/guardian/preview.webm"
mp4Src: "/tutorials/guardian/preview.mp4"
videoAlt: "A guardian detecting a person or pet."
images: ["/tutorials/guardian/preview.gif"]
tags: ["camera", "vision", "detector", "python"]
no_list: true
authors: ["Naomi Pentrel"]
languages: ["python"]
viamresources: ["camera", "vision", "servo", "mlmodel"]
level: "Intermediate"
date: "2023-12-20"
# updated: ""
---

If your smart machine [captures](/data/capture/) a lot of data, you might want to filter captured data to selectively store only the data you are interested in.
For example, you might want to use your smart machine's camera to capture images based on specific criteria, such as the presence of a certain color, and omit captured images that don't meet that criteria.

## Prerequisites

Before following this tutorial, ensure you:

1. [Create a new machine](/fleet/machines/#add-a-new-robot) in the Viam app.
1. [Install `viam-server`](/get-started/installation/) on your new machine.

## Add a camera and configure data capture

The `filter_camera` module filters image data captured by a camera component, and so requires that your machine has a camera component and data management service configured.

- A [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), allows your machine to see the world around it through an attached camera.
- The [data management service](/data/) enables your machine to capture images from an attached camera and sync them to the cloud.

### Add a camera component

Add a [camera](/components/camera/) component to your machine:

1. Navigate to your robot's page on the [Viam app](https://app.viam.com/robots) and select the **Config** tab.
1. Click the **Components** subtab and click **Create component** in the lower-left corner.
1. Select `camera` and then select `webcam`.
1. Give your camera a name, such as `my-webcam`, and click **Create**.
1. If your machine is online and connected to the Viam app, your camera's video path is automatically detected and configured.
   If your machine is not currently connected, you can manually select the video path for your camera, or bring your machine online to have this path automatically configured for you.
1. Click **Save Config** at the bottom of the window to save your changes.

### Add the data management service

Next, add the data management service to your smart machine to be able capture and sync data:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Give the service a name, like `my-data-management`, then click **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   {{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="600x" >}}

For more information, see [Add the data management service](/data/capture/#add-the-data-management-service).

### Configure data capture for a camera component

Once you have added the data management service, enable image data capture for your camera component:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. In the configuration pane for your configured camera component (named `my-webcam` in the above steps), find the **Data capture configuration** section, and click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg` to configure image data capture.
   - Ensure that the toggle on the right-hand side is set to **On**.

     {{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="The camera component configuration pane with data capture configuration enabled using type ReadImage and a capture frequency of 0.333" resize="600x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.
1. In the [Viam app](https://app.viam.com), navigate to the [**Data**](/data/view/) tab, where you should see images captured by your camera component appear roughly every 6 seconds.
   If you see images appear here, proceed to the next step.
   If you do not see images appear after a short time, see the [troubleshooting](#troubleshooting) section for further guidance.

For more information see [Configure data capture](/data/capture/#configure-data-capture-for-individual-components) and [Configure cloud sync](/data/cloud-sync/).

## Label images and train a machine learning (ML) model

Now that your camera component is steadily capturing images to the Viam app, you can train a machine learning (ML) model on those images to be able to detect certain objects in the camera feed.

The `filtered_camera` module supports two modes of filtering:

- [Detection](/ml/vision/detection/), where you train an ML model by drawing bounding boxes around distinct objects within captured images, to enable your machine to be able to detect those objects on its own.
- [Classification](/ml/vision/classification/), where you train an ML model by tagging images with a class label that best describes it, to enable your machine to be able to classify similar images on its own.

This tutorial demonstrates configuring a *detection* model.

### Capture images and create a dataset

Position your machine to capture images of interesting objects that you want it to be able to identify on its own.
This tutorial will use images of a wooden Viam figure from multiple angles and positions.

{{< alert title="Tip" color="tip" >}}

For best results:

- Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your smart machine to be able to identify.
- Include a small number of images that do not contain any of the objects you wish to identify, but do not label these images.
  Unlabelled images must not comprise more than 20% of your dataset, so if you have 20 images in your dataset, at least 16 of those must be labelled.
- If your machine operates in various lighting conditions, such as changing sunlight, include images of each object under varying lighting conditions.

{{< /alert >}}

Once you have enough images captured and synced to the Viam app, add those images to a new dataset.
A [dataset](/data/dataset/) allows you to conveniently view, work with, and train an ML model on a collection of images.

1. In the [Viam app](https://app.viam.com), navigate to the [**Data**](/data/view/) tab to view your captured images.
1. Select an image you want to use in your ML model.
1. In the **Actions** pane on the right-hand side, enter a new dataset name under **Datasets**, then press return.
1. Repeat the steps above to add more images to your dataset, until you have enough to train an ML model on.

### Draw bounding boxes around matching objects

Once you have created a dataset containing the images you want to use, draw bounding boxes around the objects in those images you want your machine to be able to identify.

1. In the [Viam app](https://app.viam.com), navigate to the [**Datasets**](https://app.viam.com/data/datasets) subtab and select the dataset you created.
1. Select an image you want to use in your ML model.
1. In the **Actions** pane on the right-hand side, select the **Bounding box** mode, enter a new label that describes the object in the image you want to detect, then draw a bounding box over the image on the right-hand side.
1. Repeat this process for the remaining images in your dataset.
   Ensure that at least 80% of the images in your dataset are labelled, with the remaining images not containing objects to identify.
   If you want your machine to be able to identify multiple objects, you can add multiple labels per image as well.

### Train an ML model

Once your dataset is ready, train a new ML model on that dataset.

1. Click the **Train model** button in the upper-left cover of the [**Datasets**](https://app.viam.com/data/datasets) subtab view for your dataset.
1. Select the **Object detection** model type, select the label or labels you added in the previous step, enter a name for your new ML model, and click **Train model**.

Your model will begin training on the images and labels you have provided.

If you already have a model you want to use, you can [upload an existing model](/ml/upload-model/) instead and skip this step.

## Configure ML model and vision services

The `filter_camera` module filters image data based on your trained ML model, and so requires that your machine has the ML model service and vision service configured.

- The [ML model service](/ml/) enables your machine to deploy a machine learning (ML) model to be used by other services.
- The [vision service](/ml/vision/) enables your machine's camera to detect objects defined in the ML model on its own.

### Add the ML model service

Add the ML model service to your smart machine to be able to deploy and update ML models:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, select **ML model**, then select the built-in `TFLite CPU` model.
1. Give the service a name, like `my-mlmodel-service`, then click **Create**.
1. On the panel that appears, select the **Deploy model on robot** toggle, then select your trained model from the **Models** dropdown.
   If you don't see your model name appear here, ensure that your model has finished training under the [**Models** subtab](https://app.viam.com/data/models) of the **Data** tab in the Viam app.
1. Click **Save Config** at the bottom of the window to save your changes.

For more information, see [Create an ML model service](/ml/deploy/#create-an-ml-model-service).

### Add the vision service

Add the vision service to your smart machine to be able to use the deployed ML model with your camera, and with the `filtered_camera` module.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, select **Vision**, then select the built-in `ML model` model.
1. Give the service a name, like `my-vision-service`, then click **Create**.
1. On the panel that appears, select your trained ML model from the **ML Model** dropdown.
1. Click **Save Config** at the bottom of the window to save your changes.

For more information, see [Configure an `mlmodel` detector](/ml/vision/detection/#configure-an-mlmodel-detector).

## Test your ML model with a transform camera

Before adding the `filtered_camera` module, you can create a transform camera to test that the ML model is working as expected with your camera.
A transform camera will overlay a bounding box on your camera's live feed when it detects objects that match its ML model.
This step is optional, you can skip this step if you want to get right to using the `filtered_camera` module.

### Add a transform camera

To add a transform camera to your machine:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create component** button at the bottom of the page, select **Camera**, then select the built-in `transform` model.
1. Give the service a name, like `my-transform-camera`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json
   {
     "pipeline": [
       {
         "attributes": {
           "detector_name": "my-vision-service",
           "confidence_threshold": 0.5
         },
         "type": "detections"
       }
     ],
     "source": "my-webcam"
   }
   ```

   If you used different names for the vision service or the camera component, update this configuration with those names.
   You can adjust the `confidence_threshold` to suit your needs.
   A value of `0.5` is a relatively loose match, representing 50% confidence.
   To require that your machine match with more confidence, you can raise this value to something like `0.8`, representing 80% confidence.

1. Click **Save Config** at the bottom of the window to save your changes.

### Test your ML model on a live camera feed

Now that you've configured a transform camera, you can see your ML model in action from the **Control** tab:

1. On your machine's **Control** page in the [Viam app](https://app.viam.com), enable the toggle for both your camera component (`my-webcam`) and your transform camera (`my-transform-camera`).
   You can find these toggles under their respective component: click a control pane to expand it if it is collapsed.
   The screenshot below shows a machine with a configured `base` component, so the two toggles appear under the `base` control pane, but you can always find them under their own control pane as well.
1. The camera component displays the raw camera feed, but the transform camera will additionally overlay a bounding box on the same feed if a matching object is detected.
   Try placing an object you trained your ML model on in front of the camera.
   The transform camera should draw a bounding box around that object in the live camera feed, and indicate a confidence threshold for the match.
1. When satisfied that your ML model is working well, you can disable both cameras.
   Alternatively, if the transform camera is not matching reliably, or at all, consider adding and labelling more images in your dataset, or lowering the `confidence_threshold` of the transform camera.
   Ideally, you want your ML model to be able to identify objects with a high level of confidence, which usually is dependent on a robust source dataset.

## Add and configure the `filtered_camera` module

With all the prerequisites in place, you are ready to add the `filtered_camera` module to your machine.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create component** button at the bottom of the page, select **Camera**, then select the `filtered-camera` model.
   You can also search for `filtered-camera` directly.
1. Give the module a name, like `my-filtered-camera`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json
   {
     "vision": "my-vision-service",
     "window_seconds": 10,
     "objects": {
       "viam-figure": 0.6
     },
     "camera": "my-webcam"
   }
   ```

   If you used a different label when drawing your bounding boxes and training your ML model, supply it here instead of `viam-figure`.
   If you used multiple labels, specify them on multiple lines like so:

   ```json
   {
     "vision": "my-vision-service",
     "window_seconds": 10,
     "objects": {
       "apple": 0.6,
       "orange": 0.6,
       "pear": 0.6
     },
     "camera": "my-webcam"
   }
   ```

1. Next, in the **Data capture configuration** section on the `filtered_camera` module configuration pane, click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to ``0.333``.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg` to configure image data capture.
   - Ensure that the toggle on the right-hand side is set to **On**.

1. Click **Save Config** at the bottom of the window to save your changes.

### Test the `filtered-camera` module

With everything configured, the `filtered-camera` module is now ready to selectively capture only images that meet your ML model criteria.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Find your camera component (`my-webcam`) and ensure that **Data capture** is *disabled*.
   We want to use the `filtered-camera` module to capture data instead, so that it can selectively capture image based on your ML model.
1. Position your machine's camera so that no detectible objects are visible, then ensure that no new images are being synced to the Viam app by watching the [**Data** tab](https://app.viam.com/data/view) in the Viam app.
1. Then place an object that is part of your trained ML model within view of your camera, and watch images of that object begin to appear under the **Data** tab automatically!

## Next steps

You can use the `filtered-camera` module to control the volume of data your machine writes and syncs, focusing only only image data that meets your ML model-specified match criteria.
You could use this in many ways, such as:

- Train an ML model on familiar faces, so that your machine can capture and upload images of any new faces it encounters, but ignore familiar faces entirely.
- Train an ML model on various common forms of delivery packaging, so that your machine can send you an image of a new delivery, but not clutter your inbox with images of other things, such as cars driving by.
- Train an ML model on a variety of domestic farm animals, so that your machine can alert you if a different kind of animal is detected in the vicinity, without capturing images of every animal.

This tutorial demonstrated using the `filtered-camera` module with [object detection](/ml/vision/detection/), but you can also use it to perform [object classification](/ml/vision/classification/).

## Troubleshooting

### No images appearing in the Viam app

Ensure that the camera component (`my-webcam` in this tutorial) has data capture enabled under the **Components** subtab, and that the data management service (`my-data-management` in this tutorial) has both **Capturing** and **Syncing** enabled under the **Services** subtab.

### Cannot train ML model

In order to train an ML model on images, you must label at least 10 images, and your dataset must include at least 80% labeled images.
If you get an error on the Viam app [models page](https://app.viam.com/data/models) similar to `too few images` when you go to train a model, try adding more images to your dataset and labelling them until you have at least 10 labelled images, and a dataset where at least 80% of the images it contains are labelled.
