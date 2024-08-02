---
title: "Capture Data and Train a Model"
linkTitle: "Capture Data and Train a Model"
weight: 4
type: "docs"
description: "Configure data capture and cloud sync, filter and tag captured data, and train an ML model."
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/services/ml/training.png"]
aliases:
  - "/tutorials/data-management-tutorial/"
  - "/tutorials/data-management/"
  - "/data-management/data-management-tutorial/"
  - "/tutorials/services/data-management-tutorial/"
tags: ["data management", "data", "mlmodel", "vision", "services", "try viam"]
authors: []
languages: []
viamresources: ["data_manager", "mlmodel", "vision", "camera"]
level: "Beginner"
date: "2023-02-08"
cost: "0"
no_list: true
# SMEs: Natalia Jacobowitz
---

<!-- LEARNING GOALS
After following this tutorial, you will understand how to use the data management service to capture and sync image data from your machine to the Viam app, and how to train a machine learning model on that data. You will be able to use the mlmodel service together with the vision service to be able to overlay successful matches directly over your camera feed in the Viam app.

Notes:
- Consider whether we should add/replace some of this content in this with some of Selectively Capture Data using filtered-camera  that capture captrue & train as well. -->

In this tutorial, you will use three Viam services together to enable your machine to recognize specific objects in the world around it:

- The [data management service](#the-data-management-service), to capture images from a camera on your machine and sync them to the cloud.
- The [ML model service](#the-ml-model-service), to manage and deploy a machine learning (ML) model based on these images, once you have added tags to the images matching the objects you want to detect.
- The [vision service](/services/vision/), to enable your machine's camera to detect objects defined in the ML model on its own.

With all three services working together, your machine will be able to analyze its camera feed for the presence of specific shapes, such as a red star or blue circle.
When it detects a likely match, it will overlay a confidence score onto the camera feed alongside the name of the detected shape, indicating how closely the shape in the camera frame matches a shape it has seen before.

{{< alert title="Tip" color="tip" >}}
To get started without any hardware, you can rent a rover through [Try Viam](https://app.viam.com/try), which is pre-configured with everything you need to begin this tutorial.
Rover rentals are 10 minutes in length, but you can [extend your session](/appendix/try-viam/faq/#can-i-extend-my-time) as needed, or [re-use a configuration from a previous session](/appendix/try-viam/faq/#how-can-i-reuse-my-rented-rover) if your time expires and you want to start a new session.

You can also use your own Viam machine as long as you have followed the [prerequisite steps](#prerequisites).
{{< /alert >}}

## Prerequisites

Before following this tutorial, ensure you have:

- A machine running `viam-server`, the software that runs your machine and connects it to the Viam app.

  - If you are using your own machine:
    {{% snippet "setup.md" %}}
  - If you are using a Viam Rover through [Try Viam](https://app.viam.com/try), no further action is needed.

- A configured camera component.

  - If you are using your own machine, add a [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), to your machine.
  - If you are using a Viam Rover through [Try Viam](https://app.viam.com/try), a camera is already configured for you.

## The data management service

You can manage how your machine works with data files and images by using the _data management service_.

The [data management](/services/data/) service has two parts: [data capture](/services/data/capture/) and [cloud sync](/services/data/cloud-sync/).

- **Data capture** allows you to capture data locally from specific components on your machine running Viam.
  You can choose the components, corresponding methods, and the frequency of the data capture from the [Viam app](https://app.viam.com/).

- **Cloud sync** runs in the background and uploads your machine's captured data to the Viam app at a defined frequency.
  Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your machine has low network bandwidth.
  With cloud sync enabled for a component, data captured locally to your machine is automatically deleted after a successful sync.
  Data synced between your machine and the Viam app is encrypted in transit (over the wire) and when stored in the cloud (at rest).

Data capture and data sync are frequently used together, and are both enabled by default when you add the data management service to your machine.
However, if you want to manage your machine's captured data yourself, you can enable data capture but disable data sync.
If you are capturing data to a device with limited storage, or intend to capture a large amount of data, see [automatic data deletion](/services/data/capture/#automatic-data-deletion).

To capture data from your machine and sync to the Viam app, add the data management service and configure data capture for at least one component.

### Add the data management service

First, add the data management service to your machine to be able capture and sync data:

1. On your machine's **CONFIGURE** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Use the suggested name for your service or give it a name, like `viam-data-manager`, then click **Create Service**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data locally to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   {{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="900x" >}}

For more information, see [Add the data management service](/services/data/capture/#add-the-data-management-service).

### Configure data capture for a component

Once you have added the data management service, you can configure data capture for specific components on your machine.
For this tutorial, you will configure data capture for images from a [camera](/components/camera/) component, but other data types such as sensor data or SLAM map data from other types of [components](/components/) can be captured as well.

To enable image data capture for a camera component:

1. Navigate to your machine's **CONFIGURE** page in the [Viam app](https://app.viam.com).

1. In the configuration pane for your [configured camera component](#prerequisites), find the **Data capture** section, and click the **Add method** button to configure data capture for this camera.

   - Set the **Method** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **MIME type** to `image/jpeg` to configure image data capture.

     {{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="The camera component configuration pane with data capture configuration enabled using type ReadImage and a capture frequency of 0.333" resize="600x" >}}

   - Make sure the **On/Off** toggle is switched to **On**.

1. Click **Save** at the top right of the window to save your changes.

For more information see [Configure data capture](/services/data/capture/#configure-data-capture-for-individual-components) and [Configure cloud sync](/services/data/cloud-sync/).

### View and filter captured data

Now that you have configured data capture on your camera component, you can view the resulting data files in the Viam app.

Click on the menu icon on the camera configuration pane and select **View captured data**.

{{<imgproc src="/services/data/capture-data-menu.png" resize="500x" declaredimensions=true alt="Resource menu with the options Rename, Duplicate, View captured data, and Delete" class="aligncenter">}}

Here you can view the images captured so far from the camera on your machine.
New images should appear roughly every six seconds as cloud sync uploads them from your machine.

You can use the filters on the left side of the screen to filter your images by machine, component, date range, and more.

If you have a lot of images, filter them by limiting the displayed images to a specific date and time range:

{{< imgproc src="/tutorials/data-management/filter-date-range.png" alt="The data tab displaying images filtered by date and time range" resize="1200x" >}}

For more information see [View and filter data](/services/data/view/).

## The ML model service

Once your machine is capturing and syncing images to the Viam app, you are ready to train a machine learning (ML) model using those images.
You can use an ML model to help your machine adapt its behavior to the world around it.

For this tutorial, you will train an ML model to be able to recognize specific shapes (for example, red and blue stars), and then deploy that model to your machine using the _ML (machine learning) model service_.
With a model deployed to your machine, you can use the [ML model](/services/ml/) service together with the [vision](/services/vision/) service to analyze newly-detected objects for a possible match to a known shape.

To train a model from your captured data, first tag your images with appropriate labels and add them to a dataset.
Then train a model based on your dataset and labels and deploy the model to your machine.

### Tag images and create a dataset

1. From the [**DATA** page](https://app.viam.com/data/view) in the Viam app, select an image captured from your machine that you would like to tag and add to your dataset.
1. In the **Tags** field on the right-hand side, enter a new tag describing the object in the image that you want your machine to be able to identify, then click **Add as new tag**.
   Tag names support alphanumeric characters, underscores, and hyphens.

   For this tutorial, you will use the objects shown in the [Try Viam](https://app.viam.com/try) test octagon, which include shapes like a red star and an orange triangle.
   The image below shows the `red_star` tag being added to an image:

   {{< imgproc src="/tutorials/data-management/add-tag-red-star.png" alt="The tags and labels configuration pane of a selected image, with the text red_star entered as the tag" resize="350x" >}}

   If you are not using a Try Viam rover, you can choose objects in your machine's surroundings instead.

   Then use the Datasets dropdown to create a new dataset and assign the image to it.
   We called our dataset `shapes`.

   {{<gif webm_src="/tutorials/data-mlmodel/add-to-dataset.webm" mp4_src="/tutorials/data-mlmodel/add-to-dataset.mp4" alt="Add image to dataset" max-width="600px">}}

1. Repeat this process for other images that contain objects you want your model to be able to identify.
   Once you have added a tag to an image and created a dataset, you can select the tag from the **Tags** dropdown menu and the dataset from the **Datasets** dropdown for other images.

   {{< alert title="Tip" color="tip" >}}

   For best results:

   - Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your machine to be able to identify.
   - Include some images that do not contain any of the objects you wish to identify, but do not tag these images.
   - If your machine operates in various lighting conditions, such as changing sunlight, include images of each object from varying lighting conditions.
   - You can tag a single image with multiple tags if needed, but be sure to use `Multi label classification` when training your model later in this tutorial.

   {{< /alert >}}

Feel free to return to your machine's **Control** tab to position your camera (and rover) to capture additional images from a variety of different angles, or with different lighting or background compositions.
Generally, the more different perspectives of a given object you tag, the more likely your model will be able to identify it, even under differing conditions.
The following is an example of a good selection of images containing the `blue_star` tag, taken from a variety of angles:

{{< imgproc src="/tutorials/data-management/filter-by-blue-star.png" alt="The data tab showing images that contain blue stars from various angles, with a search filter for blue_star applied to only show images tagged with that label" resize="1200x" >}}

If you want to remove a tag, click the **X** icon to the right of the tag name below the **Tags** field.

### View your dataset

Upon completion of tagging your data set, you can view the data in your dataset by clicking on your dataset's name on the image sidebar or on the [**DATASETS** subtab](https://app.viam.com/data/datasets).

![The shapes dataset.](/tutorials/data-management/shapes-dataset.png)

### Train a model on a dataset

To train a model:

1. From the dataset view, click on **Train model**.
1. Give your model a name, like `my-classifier-model`, and select the **Model type**:
   - Use `Single label classification` if you only added one tag per image.
   - Use `Multi label classification` if you added more than one tag for some images.
1. Select the tags you want to train your model on from the **Labels for training** dropdown, then click **Train model**.
   Unselected tags will be ignored, and will not be part of the resulting model.
   If you do not see a tag you expected to see in the **Labels for training** dropdown, ensure your filtered images contain images with the tag.

   {{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane with five tags filtered" resize="1200x" >}}

Your model will begin training on the images you have tagged, and should be ready after a short time.
You can view your model's training progress from the **Models** subtab under the [**DATA** page](https://app.viam.com/data/view).

{{< imgproc src="/tutorials/data-management/model-training-progress.png" alt="The models tab on the data page showing a model named my-classifier-model being trained" resize="600x" >}}

Models that are still being trained appear under **Training**, while models that have completed training and are ready for use appear under **Models**.

{{< imgproc src="/tutorials/data-management/trained-model.png" alt="The models tab on the data page showing a completed model named my-classifier-model ready for deployment" resize="800x" >}}

For more information, see [Train a model](/services/ml/train-model/).

### Deploy a model

Once your model has finished training, add the [ML model](/services/ml/) service and deploy your model to your machine to be able to use it to classify newly-captured images.

To deploy a model to your machine:

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
1. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
1. Select the `ML model` type, then select the `TFLite CPU` model.
1. Enter a name or use the suggested name, like `my-mlmodel-service`, for your service and click **Create**.
1. In the resulting ML Model service configuration pane, select **Deploy model on machine**, then select the model you just trained from the **Select model** dropdown menu.

   {{< imgproc src="/tutorials/data-management/mlmodel-service-conf.png" alt="The ML model service configuration pane showing the required settings to deploy the my-classifier-model." resize="600x" >}}

1. Click **Save** at the top right of the window to save your changes.

## The vision service

Now that you have deployed an ML model to your machine using the ML model service, you are ready to configure a _vision service_ which can detect the objects you've tagged in images from a camera feed.

1. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
1. Select the `vision` type, then select the `ML model` model.
1. Enter a name, like `my-vision-service`, or use the suggested name for your service and click **Create**.
1. In the resulting vision service configuration pane, select the ML model service you just added from the **ML Model** dropdown menu.

   {{< imgproc src="/tutorials/data-management/vision-service-conf.png" alt="The vision service configuration pane showing the ML model service my-mlmodel-service added" resize="500x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.

### Test object detection

Your machine is now ready to detect the objects you've tagged.

You can test your detector by clicking on the **Test** area of the vision service's configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream will show detections with bounding boxes around the detections, so try moving an object your model should recognize in front of the camera.
If you are using a Viam Rover, use the `viam_base` panel to move your rover, then click on the vision panel to check for detections.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="600x" >}}

{{< imgproc src="/tutorials/data-management/red-star.png" alt="Detected red star" resize="600x" >}}

That's it! Your machine is now smarter and better able to understand the world around it.

## Use your model with code

Once you know your model is working, you can write code to change your machine's behavior based on what it detects.
For an example see the following tutorial:

{{< cards >}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}

## Troubleshooting

If you are using [Try Viam](https://app.viam.com/try) and your session expires, you can [re-use a configuration from a previous session](/appendix/try-viam/faq/#how-can-i-reuse-my-rented-rover) to keep your configuration changes.
You can also [extend your existing session](/appendix/try-viam/faq/#can-i-extend-my-time) while it's still running, if it hasn't expired yet.

If your machine isn't capturing data and syncing it to the Viam app, ensure that both the data management service (named `viam-data-manager` in this tutorial) and the **Data capture** configuration for your camera (`cam` on the Try Viam rover) are enabled.

If your transform camera is not matching objects you have tagged, try lowering the `confidence_threshold`, or adding and tagging more images.

## Next steps

In this tutorial, you learned:

- how to use the [data management](/services/data/) service to capture images from your machine's camera and sync them to the Viam app
- how to filter and tag your synced images according to the objects you wanted to detect
- how to use the [ML model](/services/ml/) service to train an ML model based on those images and deploy that model to your machine
- how to use the [vision service](/services/vision/) to detect objects defined in an ML model from a live camera feed

From here, you could do anything! Try one of the following:

- Capture images of your hand making specific gestures, and train a model on that data to teach your machine to recognize certain hand gestures, and respond accordingly.
  For example, you might train it to stop or start based on your hand gesture, to turn in a specific direction, or adjust its speed.
- Teach your machine to [recognize specific pets](/tutorials/projects/pet-treat-dispenser/), and dispense treats appropriately.
- Teach your machine to [recognize specific toys](/tutorials/projects/bedtime-songs-bot/), and to sing a specific song about each.
- Try creating an [object detection model](/services/vision/#detections) to be able to identify parts of an image specifically with a bounding box.

For more ideas, check out our other [tutorials](/tutorials/).

{{< snippet "social.md" >}}
