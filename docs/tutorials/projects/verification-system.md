---
title: "Create a Facial Verification System"
linkTitle: "Verification System"
type: "docs"
description: "Create an alarm system that can detect people and can recognize faces, allowing it to smartly trigger alarms."
videos:
  [
    "/tutorials/verification-system/demo.webm",
    "/tutorials/verification-system/demo.mp4",
  ]
videoAlt: "Bijan disarming the facial verification system."
images: ["/tutorials/verification-system/demo.gif"]
tags: ["mlmodel", "vision", "services", "security", "camera", "data management"]
authors: ["Sierra G."]
languages: []
viamresources: ["mlmodel", "vision", "camera"]
level: "Intermediate"
date: "2024-01-17"
cost: "0"
no_list: true
# SMEs: Bijan Haney
---

With the machine learning (ML) service, a Viam machine can use an ML model together with its vision service to detect the presence of certain objects or patterns in the world around it.
In this tutorial, you will learn how to build a facial verification system using Viam which can detect when a person appears in view of a camera, and either enter an alarm state if the detected person is not a valid approved person, or enter a disarm state if the detected person is approved.
While the verification system itself is a classifier vision service, to accomplish this you configure it with dependencies on a variety of resources:

![Diagram of the components and services used in the verification system.](/tutorials/verification-system/resource-diagram.png)

You will use two vision detectors, each powered by its own ML model:

1. A `people-detect` ML model detector, which can identify whether an object detected in your camera feed is a person or not.
   You will train this model by capturing images of a variety of people using your camera and the data management service, and classifying matching pictures with labels when a person is present in the frame.
2. A `face-detect` ML model detector, which can identify the face of a specific person.
   You will use a pre-existing facial recognition model that uses the DeepFace library, and provide photos of each person you want your security system to recognize.

Layering these two detectors, your verification system will trigger a countdown when it detects a person in its feed and disarm the alarm if it detects an approved face within the countdown period.

{{<video webm_src="/tutorials/verification-system/demo.webm" mp4_src="/tutorials/verification-system/demo.mp4" alt="Bijan interacting with the verification system" poster="/tutorials/verification-system/trigger_1.png">}}

Here you can see the detector waiting in `TRIGGER_1` state, its default state, until a person appears in front of the camera.
As soon as the person is detected, the detector transitions to the `COUNTDOWN` state, where a countdown of 10 seconds begins.
After a few seconds, the detector recognizes the person's face, and enters the `DISARMED` state.

Had the person's face not matched an approved face, the detector would instead have transitioned to the `ALARM` state.
For more information on the various states used by the verification system, see [Configure a verification system](#configure-a-verification-system).

To keep this tutorial simple, you will use a transform camera to overlay the current state of the verification system on your live camera feed.
If you wanted to take this tutorial further, you could use these state transitions to power other services or functions of your machine, such as emitting an audio warning on `ALARM` state, or updating an LED display during `COUNTDOWN` with the remaining time until alarm.

## Prerequisites

Before following this tutorial, you should:

1. [Create a new machine](/fleet/machines/#add-a-new-machine) in the Viam app.
1. [Install `viam-server`](/get-started/installation/) on your new machine.

Your machine must have a [camera](/components/camera/) component, such as a [webcam](/components/camera/webcam/).

## Configure a camera

Navigate to the **Config** tab of your machine's page on the [Viam app](https://app.viam.com).
Configure the camera you want to use for your security system.

We configured ours as a `webcam`, but you can use whatever model of camera you'd like.
Reference [these supported models](/components/camera/#supported-models).

1. To configure a `webcam`, navigate to the **Config** tab of your Machine's page in [the Viam app](https://app.viam.com).
2. Click on the **Components** subtab and click **Create component**.
3. Select the `camera` type, then select the `webcam` model.
4. Enter the name `my_webcam` for your camera and click **Create**.
5. If your machine is online and connected to the Viam app, your camera’s video path is automatically detected and configured.
   If your machine is not currently connected, you can manually select the video path for your camera, or bring your machine online to have this path automatically configured for you.

Position your camera somewhere where it can easily see the people it will be configured to detect.

{{<imgproc src="/tutorials/verification-system/camera.jpeg" resize="500x" declaredimensions=true alt="Camera hanging up in office.">}}

Next, configure the person detector, or, the coarser layer of the security system that verifies that there's a person moving.

## Configure an `mlmodel` person detector

In order for your machine's camera to be able to detect the presence of a person in its field of vision, you can either use an existing ML Model from the registry capable of detecting people or train your own.

### Use an existing ML model

The [ML model service](/ml/) allows you to deploy a machine learning model to your robot.
For your machine to be able to detect people, you will use a Machine Learning model from the Viam registry called [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO).
The model can detect a variety of things which you can see in <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file including `person`s.

1. Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/Machines).
2. Click **Create service** in the lower-left corner of the page.
3. Select type `ML Model`, then select model `TFLite CPU`.
4. Enter `persondetect` as the name for your ML model service, then click **Create**.
5. Select the **Deploy model on robot** for the **Deployment** field.
6. Then select the `viam-labs:EfficientDet-COCO` model from the **Models** dropdown.

Finally, configure an `mlmodel` detector vision service to use your new `"persondetect"` ML model:

1. Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/Machines).
2. Click the **Services** subtab and click **Create service** in the lower-left corner.
3. Select the `Vision` type, then select the `ML Model` model.
4. Give the detector the name `people-detect` and click **Create**.
5. In your vision service's panel, fill in the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "mlmodel_name": "persondetect"
   }
   ```

6. Click **Save config**.

For more information, see [Configure an `mlmodel` detector](/ml/vision/mlmodel/)

Continue to [Configure a facial detector](#configure-a-facial-detector).

### Train your own model

To train your own model, you will need to capture images of a variety of people using your camera, and upload them to the Viam app using the [data management service](/data/).

To add the [data management service](/data/) and configure data capture:

1. Navigate to your machine’s page on the [Viam app](https://app.viam.com/robots) and select the **Config** tab.
2. Click the **Services** subtab and click **Create service** in the lower-left corner.
3. Choose `Data Management` as the type and then either use the suggested name or specify a name for your data management service, such as `data-manager`.
   Click **Create**.
4. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.
5. Navigate to the **Components** subtab.
   Scroll to the panel of the camera you just configured.
   Find the **Data Capture Configuration** section.
   Click **Add Method**.
   If you're using a webcam, select the method **Type** [`ReadImage()`](/components/camera/#getimage).
   Set the **Frequency** to `0.333`.
   This will capture an image from the camera roughly once every 3 seconds.
   Click **Save config.**
6. Toggle the **Data capture configuration** on.
   Now, your camera is taking pictures.
   Walk in front of it a number of times, perhaps with a friend or two, letting the camera capture many images of you.
   For best results, try capturing a variety of angles and use different lighting.
7. Select the [**DATA** page](https://app.viam.com/data/view) from the top of the screen.
   Here you can view the images captured so far from the camera on your machine.
   You should see new images appearing steadily as cloud sync uploads them from your machine.

For more information, see [configure data capture for individual components](/data/capture/#configure-data-capture-for-individual-components).

{{% alert title="Tip" color="tip" %}}
If you are using a different model of camera, you may need to use a different **Type** of method in your data capture configuration.
For instance, depth camera modules on the [Viam Registry](https://app.viam.com/registry) such as the [Intel Realsense](https://app.viam.com/module/viam/realsense/) and the [Luxonis OAK](https://app.viam.com/module/viam/oak) use [`GetImages()`](/components/camera/#getimages).
{{% /alert %}}

Next, position your camera to capture a variety of images of people.
Consider the lighting conditions, and angle of vision of the position where you intend to place your camera when you deploy it for actual use.
For example, if you will be using your facial detection machine to look out your front window at your entrance way, you will want to be sure to include many images of people at about window-height, and perhaps in different lighting conditions or different stages of walking or standing at the door.

{{< alert title="Tip" color="tip" >}}

For best results:

- Provide at least 10 images that include people, ideally taken from multiple different angles.
- Include a small number of images that do not contain any of the objects you wish to identify, but do not label these images.
  Unlabelled images must not comprise more than 20% of your dataset, so if you have 25 images in your dataset, at least 20 of those must be labelled.
- If your subject might appear under various lighting conditions, such as changing sunlight or light fixtures that might not always be on, include images under those varying lighting conditions as well.

{{< /alert >}}

Then, create a new dataset using your uploaded images and train a new model using that model:

1. [Create a new dataset and add the images you captured](/data/dataset/#create-a-dataset-and-add-data).
   Remember that you must add at least 10 images that contain people, as well as a few (but no more than 20% of the total images) that _do not_ contain people.
2. Label the images that contain people with [bounding boxes](/data/dataset/#bounding-boxes), and add the label `person`. You only want this model to be able to distinguish between what is and isn't a person, so you can conduct this training step with anyone, not necessarily the specific people you intend to approve later.
3. [Train a model on your dataset](/ml/train-model/).
   Give it the name `"persondetect"`, and select **Object Detection** as the **Model Type**.
4. [Deploy the model](/ml/deploy/) to your machine so it can be used by other services, such as the vision service.

Finally, configure an `mlmodel` detector to use your new `"persondetect"` ML model:

1. Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/Machines).
2. Click the **Services** subtab and click **Create service** in the lower-left corner.
3. Select the `Vision` type, then select the `ML Model` model.
4. Give the detector the name `people-detect` and click **Create**.
5. In your vision service's panel, fill in the **Attributes** field:

```json {class="line-numbers linkable-line-numbers"}
{
  "mlmodel_name": "persondetect"
}
```

6. Click **Save config**.

For more information, see [Configure an `mlmodel` detector](/ml/vision/mlmodel/)

Now you are ready to configure the more fine-grained layer: the facial recognition detector.

## Configure a facial detector

We now have a machine capable of detecting people in its camera feed, but we also want to be able to identify _specific_ people in order to decide to either trigger an alarm if the specific person is not an approved person, or to disarm entirely if the detected person is allowed.
First, select a profile picture of at least one face that you want your detector to be able to identify.
A good profile picture clearly shows the face of the person in good lighting, with all facial features visible.
Continue this process for each additional person you want your detector to be able to identify.
Remember that a person who walks in front of your machine's camera who is _not_ able to be identified will trigger the `ALARM` state!

Once you have one or more pictures selected, copy them to your machine's filesystem in your preferred fashion.
For example, you could use the `scp` command to transfer an image to your machine like so:

```sh { class="command-line"}
scp /path/to/my-photo.jpg username@my-machine.local:/home/me/my-photo.jpg
```

After you have copied at least one image of a person to your machine, you are ready to configure the second detection layer: the facial recognition detector.
For this tutorial, you will use Viam Labs's `facial-detector` module, available from the [Viam registry](https://app.viam.com/module/viam-labs/facial-detector).
The `facial-detector` module provides a [modular](/registry/) vision service that uses Facebook's DeepFace library to perform facial detections.

To add the `facial-detector` module to your machine:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, select `vision`, then select the `detector:facial-detector` model.
   You can also search for `facial-detector` directly.
1. Name your modular vision service `face-detect`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "face_labels": {
       "my_name": "/home/me/my-photo.jpg"
     },
     "recognition_model": "ArcFace",
     "detection_framework": "ssd"
   }
   ```

   Edit the attributes as applicable according to the configuration information on [GitHub](https://github.com/viam-labs/facial-detection):

   - `"face_labels"`: Label a photo of the face of each person you want your security system to recognize with the name you want for the label paired with the image path on your machine running `viam-server`.
     You can [use `scp` to transfer your pictures](https://www.warp.dev/terminus/scp-from-remote-to-local) from your development machine to that machine.
   - `"recognition_model"`: The model to use for facial recognition.
     `"ArcFace"` is chosen as the default for a good balance of speed and accuracy.
   - `"detection_framework"`: The detection framework to use for facial detection.
     `"ssd"` is chosen as the default for a good balance of speed and accuracy.

See the [`facial-detector` module documentation](https://github.com/viam-labs/facial-detection) for more information on the available attributes.

## Configure a verification system

Now that you have configured both the coarser `people-detect` object detector and the more fine-grained `face-detect` facial detector, you are ready to add the alarm logic that uses these detectors to either trigger an alarm or disarm, based on the detected person.
For this, add and configure the `verification-system` module from the Viam registry following the steps below:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create services** button at the bottom of the page, select `vision`, then select the `classifier:verification-system` model.
   You can also search for `verification-system` directly.
1. Name your modular vision service `security`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "trigger_1_confidence": 0.35,
     "verification_detector": "face-detect",
     "camera_name": "my-webcam",
     "trigger_2_confidence": 0.5,
     "trigger_1_labels": ["Person"],
     "trigger_2_labels": ["Person"],
     "disable_alarm": false,
     "trigger_2_detector": "people-detect",
     "verification_labels": ["my_name"],
     "trigger_1_detector": "people-detect",
     "disarmed_time_s": 10,
     "countdown_time_s": 10
   }
   ```

   In the configuration above:

   - `"trigger_1_detector"` and `"trigger_2_detector"` both use the `people-detect` ML model you created to determine if a person is present in the camera frame.
     For this tutorial, you are configuring both of these triggers identically to use the person detection ML model.
   - `"trigger_1_labels"` and `"trigger_2_labels"` similarly both use the `"person"` label you added to images when training the `people-detect` model.
     For this tutorial, you are configuring both of these labels identically to use the person detection ML model.
   - `"verification_detector"` uses the `face-detect` ML model you configured when you added images of faces to approved and labelled them in the configuration.
   - `"verification_labels"` contains an array of approved names that match each name you assigned to an image in the `facial-detector` modules' `"face_labels"` configuration attribute.
   - `"camera_name"` is the name of the camera to use to detect people and faces.
     If you used a different name for your camera, update this parameter with your camera's name.
   - Edit the other attributes to reflect your desired confidence thresholds and times between states.

See the [`verification-system` module documentation](https://github.com/viam-labs/verification-system) for more information about the trigger states and their various configuration options.

## Configure a transform camera

At this point, your machine is fully capable of detecting people in its camera feed, and of identifying whether a specific detected person is "approved" (defined under `"face_labels"`) or not.
To easily see this in action, you can add a [transform camera](/components/camera/transform/) to your machine to overlay the current state of the on top of the camera feed.

To add a transform camera to your machine:

1. On your machine's **Config** page in the [Viam app](https://app.viam.com), navigate to the **Components** tab.
1. Click the **Create component** button at the bottom of the page, select `camera`, then select the built-in `transform` model.
1. Give the transform camera a name, like `my-transform-camera`, then click **Create**.
1. On the panel that appears, enter the following configuration into the **Attributes** field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "pipeline": [
       {
         "attributes": {
           "classifier_name": "security",
           "confidence_threshold": 0.5
         },
         "type": "classification"
       }
     ],
     "source": "my-webcam"
   }
   ```

   If you used different names for the vision service or the camera component, update this configuration with those names.
   You can adjust the `confidence_threshold` to suit your needs.
   A value of `0.5` is a relatively loose match, representing 50% confidence.

1. Click **Save Config** at the bottom of the window to save your changes.

## View your verification system in action

{{% alert title="Note" color="note" %}}
The various states do not cause anything to happen on their own besides appearing as overlays on the transform cam.
To trigger an audio alarm or otherwise have your machine take an action based on the reported state, you can write your own logic using one of the [Viam SDKs](https://docs.viam.com/build/program/) to [poll the classifications](/ml/vision/#getclassificationsfromcamera).

See [2D Image Classification](/ml/vision/#classifications) for information about working with classifiers in Viam, and [Vision API](/ml/vision/#api) for usage of the Computer Vision API this module implements.
{{% /alert %}}

With everything configured, you are now ready to see your facial recognition machine in action by watching the transform camera as a person passes in front of the camera.

To view your machine's transform camera overlay:

1. On your machine's **Control** page in the [Viam app](https://app.viam.com), select the transform camera pane, which is listed by the name you gave it in the previous session, such as `my-transform-camera`.
2. Enable the view toggle to see a live camera feed from your camera, overlayed by the current state of the `verification-system` module, which should be `TRIGGER_1` if no people are present in-frame.
3. Have one or more people walk in front of the camera and look directly into it.
   Watch the state change to `COUNTDOWN` and then `DISARMED` when an approved person is detected, or to `ALARM` if no approved person appears within 10 seconds!

   ![Verification camera feed](/tutorials/verification-system/disarmed.png)

## Next steps

Now that you've got the verification aspect of your system working, you can use this as a launch point for customizing your own DIY home security system.
For example:

- Write a program using one of the [Viam SDK](/sdks/) to poll the `facial-verification` module for its current state, and take action when a particular state is reached.
  For example, you could use [`GetClassificationsFromCamera()`](/ml/vision/#getclassificationsfromcamera) to capture when a transition into the `ALARM` state occurs, and then send you an Email with the captured image of the trespasser!
- Try changing the type of [detectors](/ml/vision/#detections), using different detectors for the `TRIGGER_1` and `TRIGGER_2` states.
- Add the [filtered camera module](/tutorials/projects/filtered-camera/) to your machine, and use it as the source camera in your verification system in order to save images to the Viam cloud only when the system enters into specific states.
  This way, you could limit the images captured and synced to only those you are interested in reviewing later, for example.
- If you don't want the `ALARM` capabilities, and would like to just use it as a notification system when a detector gets triggered, set `disable_alarm: true` in the config, which prevents `TRIGGER_2` from entering into the `COUNTDOWN` state, meaning the system will only cycle between the states of `TRIGGER_1` and `TRIGGER_2`.
- Use entering into the state `TRIGGER_2` as a way to send notifications.
