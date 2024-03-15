---
title: "Selectively Capture Data using filtered-camera"
linkTitle: "Filtered Camera"
type: "docs"
description: "Use the filtered-camera module to selectively capture images."
images: ["/tutorials/filtered-camera-module/viam-figure-preview.png"]
imageAlt: "The wooden Viam figure being detected by a transform camera"
tags: ["camera", "vision", "detector", "mlmodel", "data"]
viamresources: ["camera", "vision", "mlmodel", "data_manager"]
languages: []
level: "Intermediate"
date: "2023-12-20"
# updated: ""
cost: "0"
---

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="The promotional Viam wooden figure we give out at events, being correctly detected with a 0.97 confidence threshold" resize="400x"  class="alignright" >}}

With the data management service, a Viam machine can capture data from a variety of components and sync that data to the Viam app.
However, if your machine captures a large volume of data, especially image data such as pictures, you may wish to control which specific images are captured or uploaded.

For example, imagine that you have positioned your machine's camera to view a busy city street.
Your machine will happily capture as many pictures as its configured capture rate dictates, resulting in potentially a large number of images captured over the course of a day.
If you wanted to see if any fancy sports cars might have driven by, you might have to search through many images to find out!

Instead, you can use the `filtered-camera` module to be able to selectively capture and sync only those images that meet the specific criteria you've outlined in a machine learning (ML) model.
For example, you could train an ML model that is focused on sports cars, and only capture images from the camera feed when a sports car is detected in the frame.

In this tutorial, you will learn how to use the `filtered-camera` module to selectively capture images only when a specific object is detected within the camera feed: the Viam wooden figure.
When this figure is not present in the camera frame, the `filtered-camera` module will stop capturing images until it detects the figure again.

You can train your own model to be able to identify any object you wish, or you can use a provided pre-trained model that is capable of identifying many common objects.
This tutorial will provide instructions on both approaches.

The `filtered-camera` module is available from the [Viam registry](https://app.viam.com/module/erh/filtered-camera), and you can [view the code on GitHub](https://github.com/erh/filtered_camera).

## Prerequisites

Before following this tutorial, you should:

1. [Create a new machine](/fleet/machines/#add-a-new-machine) in the Viam app.
1. [Install `viam-server`](/get-started/installation/) on your new machine.

## Add a camera and configure data capture

The `filtered-camera` module filters image data captured by a camera component, and so requires that your machine has a camera component and the data management service configured.

- A [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), allows your machine to see the world around it through an attached camera.
- The [data management service](/data/) enables your machine to capture images from an attached camera and sync them to the cloud.

### Add a camera component

Add a [camera](/components/camera/) component to your machine:

1. Navigate to your machine's page on the [Viam app](https://app.viam.com/robots) and select the **Config** tab.
1. Click the **Components** subtab and click **Create component** in the lower-left corner.
1. Select `camera` and then select `webcam`.
1. Give the camera a name, such as `my-webcam`, and click **Create**.
1. If your machine is online and connected to the Viam app, your camera's video path is automatically detected and configured.
   If your machine is not currently connected, you can manually select the video path for your camera, or bring your machine online to have this path automatically configured for you.
1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/filtered-camera-module/configure-webcam.png" alt="The camera component configuration pane in the Viam app showing a configured webcam with video path video0" resize="500x" >}}

### Add the data management service

Next, add the data management service to your machine to be able to capture and sync data:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Give the service a name, like `my-data-management`, then click **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   {{< imgproc src="/tutorials/filtered-camera-module/configure-data-management.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="700x" >}}

For more information, see [Add the data management service](/data/capture/#add-the-data-management-service).

### Configure data capture for a camera component

Once you have added the data management service, enable image data capture for your camera component:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. In the configuration pane for your configured camera component (named `my-webcam` in the above steps), find the **Data capture configuration** section, and click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg`.
   - Ensure that the toggle on the right-hand side is set to **On**.

     {{< imgproc src="/tutorials/filtered-camera-module/configure-webcam-data-capture.png" alt="The camera component configuration pane in the Viam app with data capture configured and enabled" resize="800x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.
1. In the [Viam app](https://app.viam.com), navigate to the [**Data**](/data/view/) tab, where you should see images captured by your camera component appearing steadily.
   If you see images appear here, proceed to the next step.
   If you do not see images appear after a short time, see the [troubleshooting](#troubleshooting) section for further guidance.

For more information see [Configure data capture](/data/capture/#configure-data-capture-for-individual-components) and [Configure cloud sync](/data/cloud-sync/).

## The machine learning (ML) model for filtering

The `filtered-camera` module that you will use in this tutorial supports two modes of filtering:

- [Detection](/ml/vision/#detections), where you use an ML model trained by drawing bounding boxes around distinct objects within captured images, which enables your machine to be able to detect those objects on its own.
- [Classification](/ml/vision/#classifications), where you use an ML model trained by tagging images with a class label that best describes it, which enables your machine to classify similar images on its own.

In this tutorial, you will use filtering with a _detection_ model to be able to detect certain objects in the camera feed and filter on the detected objects.
To create a detection model, you can train a machine learning (ML) model on images captured by your camera.

{{% alert title="Info" color="info" %}}
Alternatively, if you want to use a pre-trained model that is capable of identifying many basic objects, or if you already have a trained model that you want to use, skip to [Use an existing ML model](#use-an-existing-ml-model).
{{% /alert %}}

### Capture images and create a dataset

Position your machine to capture images of interesting objects that you want it to be able to identify on its own.
This tutorial will use images of a wooden Viam figure from multiple angles and positions.

{{< alert title="Tip" color="tip" >}}

For best results:

- Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your machine to be able to identify.
- Include a small number of images that do not contain any of the objects you wish to identify, but do not label these images.
  Unlabelled images must not comprise more than 20% of your dataset, so if you have 25 images in your dataset, at least 20 of those must be labelled.
- If your machine operates in various lighting conditions, such as changing sunlight, include images of each object under varying lighting conditions.

{{< /alert >}}

Once you have enough images captured and synced to the Viam app, add those images to a new dataset.
A [dataset](/data/dataset/) allows you to conveniently view, work with, and train an ML model on a collection of images.

1. In the [Viam app](https://app.viam.com), navigate to the [**Data**](/data/view/) tab to view your captured images.
1. Select an image you want to use in your ML model.
1. In the **Actions** pane on the right-hand side, enter a new dataset name under **Datasets**, then press return.
1. Repeat the steps above to add more images to your dataset, until you have enough to train an ML model on.

   {{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" resize="1400x" >}}

   For this tutorial, the dataset contains 20 images of the Viam wooden figure, and 5 images that _do not_ contain the Viam figure.
   This meets the ML model requirements of having at least 80% of the images in the dataset labelled with the target object to detect, while still including a small number of unlabelled images.

### Draw bounding boxes around matching objects

Once you have created a dataset containing the images you want to use, label and draw bounding boxes around the objects in those images you want your machine to be able to identify.

1. In the [Viam app](https://app.viam.com), navigate to the [**Datasets**](https://app.viam.com/data/datasets) subtab and select the dataset you created.
1. Select an image you want to use in your ML model.
1. In the **Actions** pane on the right-hand side, select the **Bounding box** mode, enter a new label that describes the object in the image you want to detect, then draw a bounding box over the image on the right-hand side.
   The example below shows adding the `viam-figure` label to an image, with a rectangular bounding box drawn around it.

   {{< imgproc src="/tutorials/filtered-camera-module/draw-bounding-box.png" alt="A selected image from the data tab, where the 'viam-figure' label has been added and a bounding box has been drawn around just the matching portion of the image " resize="400x" >}}

1. Repeat this process for the remaining images in your dataset.
   Once you have created a new label with your first image, you can select that label from the **Current label** dropdown for all future images in this dataset.
   Ensure that at least 80% of the images in your dataset are labelled, with the remaining images not containing objects to identify.
   If you want your machine to be able to identify multiple objects, you can add multiple labels per image as well.

### Train a new ML model

Once your dataset is ready, train a new ML model on that dataset.

1. Click the **Train model** button in the upper-left corner of the [**Datasets**](https://app.viam.com/data/datasets) subtab view for your dataset.
1. Select the **Object detection** model type, select the label or labels you added in the previous step, enter a name for your new ML model, and click **Train model**.

   {{< imgproc src="/tutorials/filtered-camera-module/train-a-new-model.png" alt="The models tab in the Viam app showing the configuration for training a new object detection model using the viam-figure dataset and viam-figure label" resize="1000x" >}}

   Your model will begin training on the images you have tagged, and should be ready after a short time.
   You can view your model's training progress from the **Models** subtab under the [**DATA** page](https://app.viam.com/data/view).

   {{< imgproc src="/tutorials/filtered-camera-module/train-model-training.png" alt="The models subtab under the data tab in the Viam app showing a model being actively trained" resize="800x" >}}

   Models that are still being trained appear under **Training**, while models that have completed training and are ready for use appear under **Models**.

   {{< imgproc src="/tutorials/filtered-camera-module/train-model-complete.png" alt="The models subtab under the data tab in the Viam app, showing a model that has completed training and is ready for use" resize="1200x" >}}

For more information, see [Train a model](/ml/train-model/).

### Use an existing ML model

You can either [use an existing model from the registry](#select-an-existing-model-from-the-registry) or [upload an ML model](#upload-an-existing-ml-model) trained outside the Viam platform.

#### Select an existing model from the Registry

The Viam registry hosts trained ML models that users have made public, which you can use to deploy classifiers or detectors for your use case onto your robot instead of training your own.
You can see all available ML models in the [Viam Registry](https://app.viam.com/registry).

Once you've decided on a model to use, continue to [Add the ML model service](#add-the-ml-model-service).

#### Upload an existing ML model

If you want to use a pre-trained model instead of training your own, or already have a model you want to use, you can upload an existing model instead.

{{% alert title="Info" color="info" %}}
If you trained your own model in the previous sections, skip to [Configure the ML model and vision services](#configure-the-ml-model-and-vision-services).
{{% /alert %}}

For example, you could use the object detection model we used for the [Turn on Lights with Object Detection tutorial](/tutorials/projects/light-up/), which was trained on many common objects, including animals, vehicles, household items, and sports gear.
You can download that model here:

- <file>[effdet0.tflite](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/effdet0.tflite)</file>: The TFLite model file containing the trained model.
- <file>[labels.txt](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/labels.txt)</file>: The corresponding labels file containing the labels to assign to matching detected objects.
  You can look through this file to see the full list of trained objects in the model.

To upload and use an existing ML model:

1. Navigate to the [**Models** page](https://app.viam.com/data/models) in the Viam app and click the **Upload model** button.
1. Select **New model** and configure visibility for your model: public models are available to all Viam users while private models are only available to users in your [organization](/fleet/organizations/).
1. If you haven't already, you will be prompted to select an [organization namespace](/fleet/organizations/#create-a-namespace-for-your-organization).
1. Then, in the resulting **Upload model** screen, enter a name for your model, select **Object detection**, and upload both the <file>effdet0.tflite</file> and <file>labels.txt</file> files.
   Add a brief description of your model, then click **Upload model**.

   {{< imgproc src="/tutorials/filtered-camera-module/upload-existing-model.png" alt="The models subtab under the data tab in the Viam app showing an existing model upload for an object detection model, including the effdet0.tflite model file and the labels.txt labels file" resize="800x" >}}

Your uploaded model is immediately available for use after upload.

{{< imgproc src="/tutorials/filtered-camera-module/upload-model-complete.png" alt="The models subtab under the data tab in the Viam app, showing a model that has been uploaded and is ready for use" resize="1200x" >}}

If you are designing your own model, see [`tflite_cpu` limitations](/ml/deploy/#tflite_cpu-limitations) for guidance on structuring your own model.

For more information, see [Upload an existing model](/ml/upload-model/).

## Configure the ML model and vision services

The `filtered-camera` module filters image data based on your ML model, and so requires that your machine has an ML model service and vision service configured.

- The [ML model service](/ml/deploy/) enables your machine to deploy a machine learning (ML) model to be used by other services.
- The [vision service](/ml/vision/) uses the deployed model together with your machine's camera to detect objects defined in the ML model on its own.

### Add the ML model service

Add the ML model service to your machine to be able to deploy and update ML models:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, select **ML model**, then select the built-in `TFLite CPU` model.
1. Give the service a name, like `my-mlmodel-service`, then click **Create**.
1. On the panel that appears, select the **Deploy model on robot** toggle, then select your model from the **Models** dropdown.
   If you don't see your model name appear here, ensure that your model appears under the [**Models** subtab](https://app.viam.com/data/models) of the **Data** tab in the Viam app.
   If you trained your own model, ensure that the model has finished training and appears under the **Models** section of that page, and not the **Training** section.
1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/filtered-camera-module/configure-mlmodel-service.png" alt="The ML model service configuration pane with deploy model on robot selected, and the my-viam-figure-model added" resize="600x" >}}

For more information, see [Create an ML model service](/ml/deploy/).

### Add the vision service

Add the vision service to your machine to be able to use the deployed ML model with your camera, and with the `filtered-camera` module.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, select **Vision**, then select the built-in `ML model` model.
1. Give the service a name, like `my-vision-service`, then click **Create**.
1. On the panel that appears, select your ML model from the **ML Model** dropdown.
1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/filtered-camera-module/configure-vision-service.png" alt="The vision service configuration pane with my-mlmodel-service selected as the ML model" resize="500x" >}}

For more information, see [Configure an `mlmodel` detector](/ml/vision/mlmodel/).

## Test your ML model with a transform camera

Before filtering your data, you can create a [transform camera](/components/camera/transform/) to test that the ML model is working as expected with your camera.
A transform camera will overlay a bounding box on your camera's live feed when it detects objects that match its ML model.
This step is optional, you can skip this step if you want to get right to filtering your data with the `filtered-camera` module.

### Add a transform camera

To add a transform camera to your machine:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create component** button at the bottom of the page, select **Camera**, then select the built-in `transform` model.
1. Give the transform camera a name, like `my-transform-camera`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
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

   {{< imgproc src="/tutorials/filtered-camera-module/configure-transform-camera.png" alt="The transform camera component configuration pane with required attributes configured" resize="800x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.

### Test your ML model on a live camera feed

Now that you've configured a transform camera, you can see your ML model in action from the **Control** tab:

1. On your machine's **Control** page in the [Viam app](https://app.viam.com), enable the toggle for both your camera component (`my-webcam`) and your transform camera (`my-transform-camera`).
   You can find these toggles under their respective component: click a control pane to expand it if it is collapsed.
   The screenshot below shows a machine with a configured `base` component, so the two toggles appear under the `base` control pane, but you can always find them under their own control pane as well.
1. The camera component displays the raw camera feed, but the transform camera will additionally overlay a bounding box on the same feed if a matching object is detected.
   Try placing an object your ML model can recognize in front of the camera.
   The transform camera should draw a bounding box around that object in the live camera feed, and indicate a confidence threshold for the match.

   {{< imgproc src="/tutorials/filtered-camera-module/transform-camera-overlay.png" alt="The control tab in the Viam app showing both a live camera feed and the live transform camera overlay, with the latter correctly detecting a viam figure with a confidence score of 0.97" resize="800x" >}}

1. When satisfied that your ML model is working well, you can disable both cameras.
   Alternatively, if the transform camera is not matching reliably, you will need to adjust your model.
   If you trained your model, consider adding and labelling more images in your dataset, or lowering the `confidence_threshold` of the transform camera.
   Ideally, you want your ML model to be able to identify objects with a high level of confidence, which usually is dependent on a robust source dataset.

## Add and configure the `filtered-camera` module

With all the prerequisites in place, you are ready to add the `filtered-camera` module to your machine.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create component** button at the bottom of the page, select **Camera**, then select the `filtered-camera` model.
   You can also search for `filtered-camera` directly.
1. Give the modular camera a name, like `my-filtered-camera`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "vision": "my-vision-service",
     "window_seconds": 10,
     "objects": {
       "viam-figure": 0.6
     },
     "camera": "my-webcam"
   }
   ```

   This example configures the `filter-camera` module to require a 60% confidence (`0.6`) threshold match for the label `viam-figure`, meaning that it must be at least 60% confident based on your ML model that the image contains the labelled object in order to capture it.
   Images that do not meet this threshold do not trigger a successful match.

   Additionally, the example configures a `window_seconds` value of `10` seconds, which controls the duration of a buffer of images captured _previous_ to a successful match.
   With this configuration, images captured up to `10` seconds before the successful match are included in the capture and sync process.

   If your model uses a different label, provide it here instead of `viam-figure`:

   - If you [trained your own model](#draw-bounding-boxes-around-matching-objects), you assigned one or more labels when you drew bounding boxes around matching objects in your uploaded images.
   - If you [uploaded our provided pre-trained model or are using your own](#upload-an-existing-ml-model), the labels can be found in the <file>labels.txt</file> file that you uploaded alongside your `.tflite` model file.

   If you used multiple labels in your ML model, you can specify them on multiple lines like so:

   ```json {class="line-numbers linkable-line-numbers"}
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

1. Next, in the **Data capture configuration** section on the `filtered-camera` module configuration pane, click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg`.
   - Ensure that the toggle on the right-hand side is set to **On**.

1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/filtered-camera-module/configure-filtered-camera.png" alt="The filtered-camera modular component configuration pane with required attributes configured and data capture enabled" resize="800x" >}}

### Test the `filtered-camera` module

With everything configured, the `filtered-camera` module is now ready to selectively capture only images that meet your ML model criteria.

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Find your camera component (`my-webcam`) and ensure that **Data capture** is _disabled_.

   {{< imgproc src="/tutorials/filtered-camera-module/data-capture-off.png" alt="The camera component configuration pane showing data capture disabled" resize="800x" >}}

   We want to use the `filtered-camera` module to capture data instead, so that it can selectively capture image based on your ML model.

1. Position your machine's camera so that no detectible objects are visible, then ensure that no new images are being synced to the Viam app by watching the [**Data** tab](https://app.viam.com/data/view) in the Viam app.
1. Then place an object that is part of your trained ML model within view of your camera, and watch images of that object begin to appear under the **Data** tab automatically.
1. Remove the object from view of the camera, and images should stop being captured and synced.

Congratulations, you now have a smart filtered camera on your machine, and can fine tune the kind of image capture it performs.

## Next steps

In this tutorial, you learned how to use the `filtered-camera` module to control the volume of data your machine writes and syncs, by using an ML model to detect objects in your camera feed and selectively capture and upload only those images that are matched by your model.

You could expand on this in many ways!
For example, you can:

- Train an ML model on familiar faces, so that your machine can capture and upload images of any new faces it encounters, but ignore familiar faces entirely.
- Train an ML model on various common forms of delivery packaging, so that your machine can send you an image of a new delivery, but not clutter your inbox with images of other things, such as cars driving by.
- Train an ML model on a variety of domestic farm animals, so that your machine can alert you if a different kind of animal is detected in the vicinity, without capturing images of every animal.

You can also refine your existing ML model by adding and labelling new images that help the ML model better identify matching objects, and then [upload the new version of your model](/ml/upload-model/#upload-a-new-model-or-new-version) using the ML model service.

If you trained a new model as part of this tutorial, try using the provided [pre-trained model files](#upload-an-existing-ml-model) instead, and then aiming your machine's camera at objects listed in the <file>labels.txt</file> file to see how accurately it is able to detect those objects.

In this tutorial, you learned how to use the `filtered-camera` module with [object detection](/ml/vision/#detections), but you can also use it to perform [object classification](/ml/vision/#classifications).
See the [`filtered-camera` module repository](https://github.com/erh/filtered_camera) for the attributes to use to configure object classification.

## Troubleshooting

### No images appearing in the Viam app

Ensure that the camera component (`my-webcam` in this tutorial) has data capture enabled under the **Components** subtab, and that the data management service (`my-data-management` in this tutorial) has both **Capturing** and **Syncing** enabled under the **Services** subtab.
Your machine can only sync images to the Viam app when it is online; if it is not presently online, it will sync captured images when next it connects to the internet.

### Cannot train ML model

In order to train an ML model on images, you must label at least 10 images, and your dataset must include at least 80% labeled images.
If you get an error on the Viam app [models page](https://app.viam.com/data/models) similar to `too few images` when you go to train a model, try adding more images to your dataset and labelling them until you have at least 10 labelled images, and a dataset where at least 80% of the images it contains are labelled.
