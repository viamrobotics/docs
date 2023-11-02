---
title: "Capture Data and Train a Model"
linkTitle: "Capture Data and Train a Model"
weight: 60
type: "docs"
description: "Configure data capture and cloud sync, filter and tag captured data, and train a new ML model."
image: "/tutorials/data-management/data-captured-images.png"
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/tutorials/data-management/data-captured-images.png"]
aliases:
  - "/tutorials/data-management-tutorial/"
  - "/tutorials/data-management/"
  - "/manage/data-management/data-management-tutorial/"
  - "/tutorials/services/data-management-tutorial/"
tags: ["data management", "data", "mlmodel", "vision", "services", "try viam"]
authors: []
languages: []
viamresources: ["data_manager", "mlmodel", "vision", "camera"]
level: "Beginner"
date: "8 February 2023"
cost: "0"
no_list: true
# SMEs: Alexa Greenberg, Natalia Jacobowitz
---

In this tutorial, you will use three Viam services together to enable a smart machine to recognize specific objects in the world around it:

- The [data management](#the-data-management-service) service, to capture images from a camera on your smart machine and sync them to the cloud.
- The [ML model](#the-ml-model-service) service, to manage and deploy a machine learning (ML) model based on these images, once you added tags to the images matching the objects you want to detect.
- THe [vision](/services/vision/) service, to enable your smart machine's camera to detect objects defined in the ML model on its own.

Working together, these services enable your smart machine to recognize the world around it and make intelligent decisions about the world it sees.

{{< alert title="Tip" color="tip" >}}
To get started easily, you can rent a rover through [Try Viam](https://app.viam.com/try), which is pre-configured with everything you need to begin this tutorial.
Rover rentals are 10 minutes in length, but you can [extend your session](/try-viam/faq/#can-i-extend-my-time) as needed, or [re-use a configuration from a previous session](/try-viam/faq/#how-can-i-reuse-my-rented-rover) if your time expires and you want to start a new session.
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

The [data management](/manage/data/) service has two parts: [data capture](/services/data/#data-capture) and [cloud sync](/services/data/#cloud-sync)

- **Data capture** allows you to capture data from specific components on your smart machine running Viam.
  You can choose the components, corresponding methods, and the frequency of the data capture from the [Viam app](https://app.viam.com/).

- **Cloud sync** runs in the background and uploads your smart machine's captured data to the Viam app at a defined frequency.
  Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your smart machine has low network bandwidth.
  With cloud sync enabled for a component, data captured locally to your smart machine is automatically deleted after a successful sync.
  Data synced between your smart machine and the Viam app is encrypted in transit (over the wire) and when stored in the cloud (at rest).

Data capture and data sync are frequently used together, and are both enabled by default when you add the data management service to your smart machine.
However, if you want to manage your smart machine's captured data yourself, you can enable data capture but disable data sync.

To capture data from your smart machine and sync to the Viam app, add the data management service and configure data capture for at least one component.

### Add the data management service

First, add the data management service to your smart machine to be able capture and sync data:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Give the service a name, like `viam-data-manager`, then click **Create Service**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   {{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="600x" >}}

For more information, see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).

### Configure data capture for a component

Once you have added the data management service, you can configure data capture for specific components on your smart machine.
For this tutorial, you will configure data capture for images from a [camera](/components/camera/) component, but other data types such as sensor data or SLAM map data from other types of [components](/components/) can be captured as well.

To enable image data capture for a camera component:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. If you have not already, add a [camera component](/components/camera/), such as a [webcam](/components/camera/webcam/), to your smart machine.
   If you are using a Viam Rover, the camera is pre-configured, and named `cam`.

1. In your camera component configuration pane, find the **Data capture configuration** section, and click the **Add method** button to enable data capture for this camera.

   - Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **Mime type** to `image/jpeg` to configure image data capture.

     {{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="The camera component configuration pane with data capture configuration enabled using type ReadImage and a capture frequency of 0.333" resize="600x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.

For more information see [Configure data capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components) and [Configure cloud sync](/services/data/configure-cloud-sync/).

### View and filter captured data

Now that you have configured data capture on your camera component, you can view the resulting data files in the Viam app, and can apply filters to limit the files returned by specific criteria, such as by robot or date range.

1. First, in the [Viam app](https://app.viam.com), browse to your robot's **Control** tab and enable the camera to verify that a live stream is returned.
   If you do not see a functioning camera stream, verify that you have configured your [camera](/components/camera/) correctly.

1. Then, select the [**DATA** page](https://app.viam.com/data/view) from the top of the screen.

   {{< imgproc src="/tutorials/data-management/data-captured-images.png" alt="The data page showing a variety of captured images with search options presented on the left" resize="1200x" >}}

   Here you can see the images captured so far from the camera on your smart machine.
   New images should appear roughly every six seconds as cloud sync uploads them from your smart machine.

You can use the filters on the left side of the screen to filter your images by robot, component, date range, and more.
You can also use the **Copy export command** button to use the Viam CLI to [export captured data](/manage/cli/#data), if desired.

For more information see [View and filter data](/manage/data/view/).

## The ML model service

Once your smart machine is capturing and syncing images to the Viam app, you are ready to train a new machine learning (ML) model using those image.
You can use an ML model to help your smart recognize and adapt its behavior to the world around it.

For this tutorial, you will train an ML model to be able to recognize specific objects, and then deploy that model to your smart machine using the _ML (machine learning) model service_.
With a model deployed to your smart machine, the [ML model](/services/ml/) service can be used together with the [vision](/services/vision/) service to analyze newly-detected objects for a possible match to a known object.

To train a new model from your captured data, first tag your images with appropriate labels, train a new model based on those labels, then deploy the model to your smart machine.

### Tag images

1. From the [**DATA** page](https://app.viam.com/data/view) in the Viam app, select an image captured from your smart machine that you would like to tag.
1. In the **Tags** field on the right-hand side, enter a new tag describing the object in the image that you want your smart machine to be able to identify, then click **Add as new tag**.
   Tag names support alphanumeric characters, underscores, and hyphens.

   For this tutorial, will use the objects shown in the [Try Viam](https://app.viam.com/try) test octagon, which include shapes like a red star and an orange triangle.
   The image below shows adding the `red_star` tag to an image:

   {{< imgproc src="/tutorials/data-management/add-tag-red-star.png" alt="The tags and labels configuration pane of a selected image, with the text red_star entered as the tag" resize="350x" >}}

1. Repeat this process for other images that contain objects you want your model to be able to identify.
   Once you have added a tag to an image, you can select that tag from the **Tags** drop down menu for other images that also feature the tagged object.

   {{< alert title="Tip" color="tip" >}}

   For best results:

   - Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your smart machine to be able to identify.
   - Include some images that do not contain any of the objects you wish to identify, but do not tag these images.
   - If your smart machine operates in various lighting conditions, such as changing sunlight, include images of each object from varying lightning conditions.
   - You can tag a single image with multiple tags if needed, but be sure to use `Multi label classification` when training your model later in this tutorial.

   {{< /alert >}}

Feel free to return to your smart machine's **Control** tab to position your camera to capture additional images from a variety of different angles, or with different lighting or background compositions.
Generally, the more different perspectives of a given object you tag, the more likely your model will be able to identify it, even under differing conditions.
The following is an example of a good selection of images containing the `blue_star` tag, taken from a variety of angles:

{{< imgproc src="/tutorials/data-management/filter-by-blue-star.png" alt="The data tab showing images that contain blue stars from various angles, with a search filter for blue_star applied to only show images tagged with that label" resize="1200x" >}}

If you want to remove a tag, click the **X** icon to the right of the tag name below the **Tags** field.

For more information, see [Train a model](/manage/ml/train-model/).

### Filter images using tags

Once you have tagged your images, you can use those tags to filter your images to control which images to run your model on.

To filter images by tag, use the **Tags** drop down filter on the left-hand side to select the tag you want to filter by, then click the **Search** button to limit displayed images to only those matching the provided tag.

For example, the following shows an images data set filtered to only show images tagged with the `red_star` tag:

{{< imgproc src="/tutorials/data-management/filter-by-red-star.png" alt="The filtering pane on the left of the data page with the tag red_star checked and the search button shown" resize="250x" >}}

You can search for multiple tags at once, which will display images that match any of the included tags.
To reset a filter, and return to viewing all captured images, click the **Reset filters** button on the left, then click **Search** again.

### Train a new model based on a filter

Filtering images using tags also constrains the model you train to only those images you want to inform your model.
This is especially useful when you may have captured a large number of images of a variety of objects, but only want to train a model to identify a few of them.

To train a new model:

1. First, ensure that you have filtered your images by adding each tag you would like to use in your model using the **Tags** drop down filter on the left-hand side, then click **Search**.
1. When you are happy with the images shown, click the **Train model** button in the upper-right.
1. Give your model a name, like `my-object-detector`, and select the **Model type**:
   - Use `Single label classification` if you only added one tag per image.
   - Use `Multi label classification` if you added more than one tag for some images.
1. Select the tags you want to train your model on from the **Labels for training** drop down, then click **Train model**.
   Unselected tags will be ignored, and will not be part of the resulting model.
   If you do not see a tag you expected to see in the **Labels for training** drop down, ensure you have included that tag in the [search filter](#filter-images-using-tags) on the left.

   {{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane with four tags filtered" resize="1200x" >}}

Your new model will begin training on the images you have tagged, and should be ready after a short time.
You can view your model's training progress from the **Models** subtab under the [**DATA** page](https://app.viam.com/data/view).

{{< imgproc src="/tutorials/data-management/model-training-progress.png" alt="The models tab on the data page showing a model named my-classifier-model being trained" resize="600x" >}}

Models that are still being trained appear under **Training**, while models that have completed training and are ready for use appear under **Models**.

{{< imgproc src="/tutorials/data-management/trained-model.png" alt="The models tab on the data page showing a completed model named my-classifier-model ready for deployment" resize="800x" >}}

### Deploy a model

Once your new model has finished training, add the [ML model](/services/ml/) service and deploy your model to your smart machine to be able to use it to classify newly-captured images.

To deploy a new model to your smart machine:

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **ML Model**, then select **TFLite CPU**.
1. Give the service a name, like `my-mlmodel-service`, then click **Create**.
1. In the resulting ML Model service configuration pane, select **Deploy model on robot**, then select the model you just trained from the **Models** dropdown menu.
1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/data-management/mlmodel-service-conf.png" alt="The ML model service configuration pane showing the required settings to deploy the my-classifier-model." resize="600x" >}}

## The vision service

Now that you have deployed a new ML model to your smart machine using the ML model service, you are ready to configure your camera to detect the objects you've tagged by using the _vision service_.
The [vision](/services/vision/) service enables a camera to, among other things, make use of deployed ML models to intelligently identify objects in in a camera feed.

To enable your smart machine's camera to identify the objects you've tagged, first add the vision service, then add a transform camera to be able to use your ML model as a classifier.

### Add the vision service

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Vision**, then select **ML Model**.
1. Give the service a name, like `my-vision-service`, then click **Create**.
1. In the resulting vision service configuration pane, select the ML model service you just added from the **ML Model** dropdown menu.
1. Click **Save Config** at the bottom of the window to save your changes.

   {{< imgproc src="/tutorials/data-management/vision-service-conf.png" alt="The vision service configuration pane showing the ML model service my-mlmodel-service added" resize="500x" >}}

### Add a transform camera

1. On your robot's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create components** button at the bottom of the page, and select **Camera**, then select **Transform camera**.
1. Give the camera a name, like ``, then click **Create**.
1. In the resulting camera components configuration pane, enter the following into the **Attributes** section for the transform camera:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "pipeline": [
       {
         "type": "classifications",
         "attributes": {
           "classifier_name": "my-vision-service",
           "confidence_threshold": 0.6
         }
       }
     ],
     "source": "cam"
   }
   ```

   If you are not using a Try Viam rover, replace `cam` with the name of the configured camera on your smart machine.
   The `confidence_threshold` controls how confident the model must be in order to present a matching object tag, on a scale of `0.0` - `1.0`, with `1.0` representing a 100% match requirement.
   The more and varied images you have captured and tagged, the more confidently your model can identify the objects you have tagged.

   {{< imgproc src="/tutorials/data-management/transform-cam-conf.png" alt="The transform camera component configuration pane showing the required attributes entered" resize="500x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.

## Test object detection

Your smart machine is now ready to detect the objects you've tagged.

1. On your robot's **Control** page in the [Viam app](https://app.viam.com), find your configured camera component.
   If you are using a Viam Rover, use the `viam_base` base instead, which presents both the camera and the transform camera together.
1. Enable both the camera and the transform camera, to show both on the right-hand side.
   On the Viam Rover, and using the transform camera name from earlier in this tutorial, these are `cam` and `my-transform-cam`.
1. Move your smart machine to a position where your camera can see an object that you have tagged in your ML model, and watch your smart machine identify it!

   {{< imgproc src="/tutorials/data-management/transform-blue-star.png" alt="The control tab for a rover showing a live camera feed with the transform camera overlay indicating an object match for the blue_star tag" resize="600x" >}}

   {{< imgproc src="/tutorials/data-management/transform-red-star.png" alt="The control tab for a rover showing a live camera feed with the transform camera overlay indicating an object match for the red_star tag" resize="600x" >}}

That's it! Your smart machine is now smarter and better able to understand the world around it.

## Troubleshooting

If you are using [Try Viam](https://app.viam.com/try) and your session expires, you can [re-use a configuration from a previous session](/try-viam/faq/#how-can-i-reuse-my-rented-rover) to keep your configuration changes.
You can also [extend your existing session](/try-viam/faq/#can-i-extend-my-time) while it's still running, if it hasn't expired yet.

If your smart machine isn't capturing data and syncing it to the Viam app, ensure that both the data management service (named `viam-data-manager` in this tutorial) and the **Data capture configuration** for your camera (`cam` on the Try Viam rover) are enabled.

If your transform camera is not matching objects you have tagged, try lowering the `confidence_threshold`, or adding and tagging more images.

## Next steps

In this tutorial, you learned:

- how to use the [data management](/manage/data/) service to capture images from your smart machine's camera and sync them to the Viam app
- how to filter and tag your synced images according to the objects you wanted to detect
- how to use the [ML model](/services/ml/) service to train a new ML model based on those images and deploy that model to your smart machine
- how to use the [vision service](/services/vision/) to detect objects defined in an ML model from a live camera feed

From here, you could do anything! Try one of the following:

- Capture images of your hand making specific gestures, and train a model on that data to teach your smart machine to recognize certain hand gestures, and respond accordingly.
  For example, you might train it to stop or start based on your hand gesture, to turn in a specific direction, or adjust its speed.
- Teach your smart machine to [recognize specific pets](/tutorials/projects/pet-treat-dispenser/), and dispense treats appropriately.
- Teach your smart machine to [recognize specific toys](/tutorials/projects/bedtime-songs-bot/), and to sing a specific song about each.
- Try creating an [object detection model](/services/vision/detection/) to be able to identify parts of an image specifically with a bounding box.

For more ideas, check out our other [tutorials](/tutorials/).

{{< snippet "social.md" >}}
