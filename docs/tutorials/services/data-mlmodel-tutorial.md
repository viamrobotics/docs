---
title: "Capture Data and Train a Model"
linkTitle: "Capture Data and Train a Model"
weight: 60
type: "docs"
description: "Configure data capture and cloud sync, filter and tag captured data, and train a new ML model."
image: "/tutorials/data-management/image1.png"
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/tutorials/data-management/image1.png"]
aliases:
    - "/tutorials/data-management-tutorial/"
    - "/tutorials/data-management/"
    - "/manage/data-management/data-management-tutorial/"
    - "/tutorials/services/data-management-tutorial/"
tags: ["data management", "data", "mlmodel", "services", "try viam"]
authors: []
languages: []
viamresources: [ "data_manager", "mlmodel", "camera" ]
level: "Beginner"
date: "8 February 2023"
cost: "0"
no_list: true
# SMEs: Alexa Greenberg, Natalia Jacobowitz
---

In this tutorial, you will learn how to use two Viam services together:

- The [data management](#the-data-management-service) service, which you will use to capture images from a camera on your smart machine and sync them to the cloud.
- The [ML model](#the-ml-model-service) service, which you will use to tag and filter these images by shape, and to train a machine learning model based on these images.

Working together, these two services enable to you train and continually refine an ML model that your smart machine can use to make intelligent decisions about the world around it.

{{< alert title="Tip" color="tip" >}}
To get started easily, you can rent a rover through [Try Viam](https://app.viam.com/try), which is pre-configured with everything you need to begin this tutorial.
You can also use your own Viam smart machine as long as you have followed the [prerequisite steps](#prerequisites).
{{< /alert >}}

## Prerequisites

Before following this tutorial, ensure you have:

- A smart machine running Viam.

  - If you are using your own smart machine, make sure you have [installed `viam-server`](/installation/).
  - If you are using a Viam Rover through [Try Viam](https://app.viam.com/try), no further action is needed.

- A configured camera component.

  - If you are using your own smart machine, add a [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), to your smart machine.
  - If you are using a Viam Rover through [Try Viam](https://app.viam.com/try), a camera is already configured for you.

## The data management service

You can manage how your smart machine works with data files and images by using the _data management service_.

The [data management](/manage/data/) service helps you to manage data on your smart machine every step of the way, from capturing data locally, to syncing and managing your data securely in the cloud.

Viam's data management service has two distinct parts: [data capture](/manage/data/#data-capture) and [cloud sync](/manage/data/#cloud-sync)

- **Data capture** allows you to capture data from specific components on your smart machine running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture from the [Viam app](https://app.viam.com/).

- **Cloud sync** runs in the background and uploads your smart machine's captured data to the Viam app at a defined frequency.
Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your smart machine has low network bandwidth.
With cloud sync enabled for a component, data captured locally to your smart machine is automatically deleted after a successful sync.
Data synced between your smart machine and the Viam app is encrypted in transit (over the wire) and when stored in the cloud (at rest).

Data capture and data sync are frequently used together, and are both enabled by default when you add the data management service to your smart machine.
However, if you want to manage your smart machine's captured data yourself, you can enable data capture but disable data sync.

To capture data from your smart machine and sync to the Viam app, you must add the data management service and configure data capture for at least one component.

### Add the data management service

First, add the data management service to your smart machine to be able capture and sync data:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Enter `viam-data-manager` as the name for your instance of the data management service, then click **Create Service**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   ![Data Management configuration pane](/tutorials/data-management/data-management-conf.png)

For more information, see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).

### Configure data capture for a component

Once you have added the data management service, you can configure data capture for specific components on your smart machine.
For this tutorial we will configure data capture for a camera component, capturing images and syncing them to the Viam app, but you can use the data management service with most [components](/components/).
This allows you to capture not just image data, but also sensor data, state data, SLAM mapping data, and many other types.

To enable image data capture for a camera component:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. If you have not already, add a [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), to your smart machine.
   If you are using a Viam Rover, the camera is pre-configured, and named `cam`.

1. In your camera component configuration pane, find the **Data capture configuration** section, and click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg` to configure image data capture for this tutorial.

   ![Screenshot from the Viam app showing the data capture settings used for this tutorial.](/tutorials/data-management/camera-data-capture.png)

1. Click **Save Config** at the bottom of the window to save your changes.

For more information see [Configure data capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components) and [Configure cloud sync](/services/data/configure-cloud-sync/).

### View and filter captured data

Now that you have configured data capture on your camera component, you can view the resulting data files in the Viam app, and can apply filters to limit the files returned by specific criteria, such as by robot or date range.

1. First, in the [Viam app](https://app.viam.com), browse to your robot's **Control** tab and enable the camera to verify that a live stream is returned.
   If you do not see a functioning camera stream, verify that you have configured your [camera](/components/camera/) correctly.

1. Then, select the [**DATA** page](https://app.viam.com/data/view) from the top of the screen.

   ![The data page of the Viam app showing a gallery of the images captured from the Viam Rover.](/tutorials/data-management/image1.png)

   Here you can see the images captured thus far from the camera on your smart machine.
   New images should appear roughly every six seconds as cloud sync uploads them from your smart machine.

You can use the filters on the left side of the screen to filter your images by robot, component, date range, and more.
You can also use the **Copy export command** button to use the Viam CLI to [export captured data](/manage/cli/#data), if desired.

For more information see [View and filter data](/manage/data/view/).

## The ML model service

With a suitable selection of images uploaded to the Viam app, you can now train a new model from your images data set, by using the _ML (machine learning) model service_.

The [ML model](/services/ml/) service uses machine learning to analyze a data set and train an ML model, which a smart machine can later use to adjust its behavior based on insights gathered from that data.

Training a model involves tagging each image you want your model to be aware of with specific keywords (called "tags"), and then deploying that model to your smart machine.
Models can also be refined later by adding and tagging new images to improve their accuracy, and then deploying the updated model to your smart machine.

With a trained model deployed, your smart machine will be able to identify matching shapes in newly-captured images on its own.

### Tag images

1. From the [**DATA** page](https://app.viam.com/data/view) in the Viam app, select an image captured from your smart machine that you would like to tag.
1. In the **Tags** field on the right-hand side, enter a new tag describing the object in the image that you want your smart machine to be able to identify, then click **Add as new tag**.
   Tag names support alphanumeric characters, underscores, and hyphens.
   For this tutorial, we are using the shapes shown in the [Try Viam](https://app.viam.com/try) test octagon, which include shapes like a black triangle and a yellow circle.
   The image below shows adding the `black_triangle` tag to an eligible image (though the thumbnail on the left doesn't show the rest of the picture that contains the shape):

   ![The data page of the Viam app showing a gallery of images filtered to show images matching any configured tag](/tutorials/data-management/tag-image.png)

   {{< alert title="Tip" color="tip" >}}
   For best results, provide several images of the same object from different perspectives, and repeat this approach for each object you intend to tag.
   Feel free to return to your smart machine's **Control** tab to position your camera to capture additional images from a variety of different angles, or with different lighting or background compositions.
   Generally, the more different perspectives of a given object you tag, the more likely your model will be able to identify it, even under differing conditions.
   {{< /alert >}}

1. Repeat this process for other images that contain objects you want your model to be able to identify.
   Once you have added a tag to an image, you can select that tag from the **Tags** drop down menu for other images that also feature the tagged object.
   To be able to train a model using a given tag, you must have tagged at least 10 images with that tag.

You can skip any images that don't contain an object that you want your smart machine to be able to identify.
If you want to remove a tag, click the **X** icon to the right of the tag name below the **Tags** field.

For more information, see [Train a model](/manage/ml/train-model/).

### Filter images using tags

You can use your tags to filter your images, and only display matching images based on their tag.

To filter images by tag, use the **Tags** drop down filter on the left-hand side to select the tag you want to filter by, then click the **Search** button to limit displayed images to only those matching the provided tag.

For example, the following shows an images data set filtered to only show images tagged with the `black_triangle` tag:

![The data page of the Viam app showing a gallery of images filtered to show only images tagged with the black_triangle tag](/tutorials/data-management/filter-specific-tag.png)

You can search for multiple tags at once, which will display images that match any of the included tags.
To reset a filter, and return to viewing all captured images, click the **Reset filters** button on the left, then click **Search** again.

### Train a new model based on a filter

Filtering images using tags also constrains the model you train to only those images you want to inform your model.
This is especially useful when you may have captured a large number of images of a variety of objects, but only want to train a model to identify a few of them.

To train a new model:

1. First, ensure that you have filtered your images by adding each tag you would like to use in your model using the **Tags** drop down filter on the left-hand side, then clicking **Search**.
   For this tutorial, we are filtering by all tags, to include every image we have tagged with a shape, since we want our ML model to be able to identify each of these shapes:

   ![The data page of the Viam app showing a gallery of images filtered to show images matching any configured tag](/tutorials/data-management/filter-all-tags.png)

1. When you are happy with the images shown, click the **Train model** button in the upper-right.
1. Give your model a name, and select the **Model type**:
   - Use `Single label classification` if you only added one tag per image.
   - Use `Multi label classification` if you added more than one tag for some images.
1. Select the tags you want to train your model on from the **Labels for training** drop down, then click **Train model**.
   Unselected tags will be ignored, and will not be part of the resulting model.
   For this tutorial, we are using `Single label classification` and selecting all tags:
  ![The data page of the Viam app showing a gallery of images filtered to show images matching any configured tag](/tutorials/data-management/train-model.png)

Your new model will begin training on the images you have tagged, and should be ready after a short time.
You can view your model's training progress from the **Models** subtab under the [**DATA** page](https://app.viam.com/data/view).
Models that are still being trained appear under **Training**, while models that have completed training and are ready for use appear under **Models**.

### Deploy and use your model

Once your new model has finished training, add the [ML model](/services/ml/) service and deploy your model to your smart machine to be able to use it to classify newly-captured images.

To deploy a new model to your smart machine:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **ML Model**, then select **TFLite CPU**.
1. Give the service a name, then click **Create**.
1. In the resulting ML Model configuration pane, select **Deploy model on robot**, then select the model you just trained from the **Models** dropdown menu.
1. Click **Save Config** at the bottom of the window to save your changes.

## Next steps

In this tutorial, you learned how to use the [data management](/manage/data/) service to capture images from your smart machine's camera and sync them to the Viam app where you filtered and tags images according to the objects you wanted to detect.
You also learned how to use the [ML model](/services/ml/) service to train a new ML model based on those images, and to deploy that model to your smart machine.

From here, you could do anything! Try one of the following:

- Capture images of your hand making specific gestures, and train a model on that data to teach your smart machine to recognize certain hand gestures, and respond accordingly.
  For example, you might train it to stop or start based on your hand sign, to turn in a specific direction, or adjust its speed.
- Teach your smart machine to [recognize specific pets](/tutorials/projects/pet-treat-dispenser/), and dispense treats appropriately.
- Teach your smart machine to [recognize specific toys](/tutorials/projects/bedtime-songs-bot/), and to sing a specific song about each.
- Try creating an [object detection model](/services/vision/detection/) to be able to identify parts of an image specifically with a bounding box.

For more ideas, check out our [tutorials](/tutorials/).

{{< snippet "social.md" >}}
