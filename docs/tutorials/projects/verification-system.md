---
title: "A security system based on face identification"
linkTitle: "Security system"
type: "docs"
description: "Create an alarm system that can detect people and recognize faces, allowing it to intelligently trigger alarms."
videos:
  [
    "/tutorials/verification-system/demo.webm",
    "/tutorials/verification-system/demo.mp4",
  ]
videoAlt: "A person disarming the facial verification system."
images: ["/tutorials/verification-system/demo.gif"]
tags: ["mlmodel", "vision", "services", "security", "camera", "data management"]
authors: ["Sierra G."]
languages: []
viamresources: ["mlmodel", "vision", "camera"]
platformarea: ["ml"]
level: "Intermediate"
date: "2024-01-17"
updated: "2025-09-11"
cost: "0"
no_list: true
# SMEs: Bijan Haney
---

Security systems often include a human component, like a supervisor who monitors camera streams for suspicious activity.
In this tutorial, you will learn how to build a security system that detects people and intelligently decides whether to raise an alarm.
The system decides whether to raise an alarm based on whether it recognizes the face of the detected person using a machine learning model.

{{<video webm_src="/tutorials/verification-system/demo.webm" mp4_src="/tutorials/verification-system/demo.mp4" alt="Bijan interacting with the verification system" poster="/tutorials/verification-system/trigger_1.png" >}}

## Architecture

- The system uses a camera to obtain a live video stream.
- To detect people on the video stream, the system uses a people detection model, which can identify whether an object detected in your video stream is a person or not.
- You will need to obtain images of all the people whom the security system should know about.
  The face identification model uses the DeepFace library in conjunction with these photos to recognize people.
- The [`verification-system` module](https://app.viam.com/module/viam-labs/verification-system) provides a vision service that applies the two models to the camera stream.
  It also implements logic that starts a countdown when it detects a person in the camera stream and then decides whether to trigger an alarm based on whether it recognizes the person's face or not.

{{<imgproc src="/tutorials/verification-system/resource-diagram.png" resize="1200x" declaredimensions=true alt="Diagram of the components and services used in the verification system." class="imgzoom fill">}}

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Connect a camera to your machine.
This tutorial uses the [webcam](/operate/reference/components/camera/webcam/) model but you can also use other [camera components](/operate/reference/components/camera/).

{{% /expand %}}

## Configure the camera

Navigate to the **CONFIGURE** tab of your machine's page.

{{< table >}}
{{% tablestep start=1 %}}
**Configure the camera you want to use for your security system.**

Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `camera` type, then select the `webcam` model or another model if you are using a different camera.
Enter the name `my_webcam` for your camera and click **Create**.

{{% /tablestep %}}
{{% tablestep %}}

**Position your camera somewhere where it can detect people.**

{{<imgproc src="/tutorials/verification-system/camera.jpeg" resize="500x" declaredimensions=true alt="Camera hanging in office.">}}

{{% /tablestep %}}
{{% tablestep %}}
**Test the camera stream.**

Click on the camera's **TEST** panel to see the camera stream.

{{% /tablestep %}}
{{< /table >}}

## Configure the people detector

In order for your machine's camera to detect the presence of a person in its field of vision, we recommend using the [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO) model from the Viam Registry.
The model can detect a variety of objects, which you can see in the <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file, including people with the `person` label.

{{< alert title="Want to train your own model instead?" color="note" >}}
If you wish to train your own ML model, see [Train a TF or TFLite model](/data-ai/train/train-tf-tflite/).
{{< /alert >}}

To run the machine learning model on your machine, use the [ML model service](/data-ai/ai/deploy/):

1. On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
1. Select type `ML model`, then select model `TFLite CPU`.
1. Enter `persondetect` as the name for your ML model service, then click **Create**.
1. On the ML model service panel, select **Deploy model on machine** for the **Deployment** field.
1. Click **Select model**, then select the **EfficientDet-COCO** model by **viam-labs** from the **Registry** tab of the modal that appears.
1. Add the `vision / ML model` vision service to your machine and name it `person-detector`.
1. On the vision service panel, select `persondetect` as the **ML Model** and `my_webcam` as the **Default Camera**.

Now you are ready to configure the face identification model.

## Configure face identification

You now have a machine capable of detecting people in its camera feed.
To make it an intelligent security system, it also needs to identify _specific_ people in order to decide whether to trigger an alarm.

To do this, you can use the [`face-identification` module](https://app.viam.com/module/viam/face-identification), which uses Facebook's DeepFace library to perform face identification:

{{< table >}}
{{% tablestep start=1 %}}
**Add images of people that the system should recognize.**

Get a few pictures of each person that the system should be able to identify.
The pictures should clearly show the face of the person in good lighting, with all facial features visible.

In the finished system, any person who walks in front of your machine's camera and is _not_ identified will trigger an alarm!

Copy the images to your machine's filesystem and place them into a folder structure like this:

```treeview
path/
└── to/
    └── known_faces/
        └── john_doe/
        |   ├── john_1.jpeg
        |   └── john_2.jpeg
        └── jane_doe/
        |   ├── jane_1.png
        |   └── jane_2.jpeg
        └── admin_team/
            └── group_photo.png
```

For example, you can use the `scp` command to transfer an image to your machine like so:

```sh {class="command-line" data-prompt="$"}
scp -r /path/to/known_faces username@my-machine.local:/home/known_faces
```

You need the path to the <FILE>known_faces</FILE> folder when configuring the face identification service in the next steps.

{{% /tablestep %}}
{{% tablestep %}}
**Add the face identification vision service.**

On your machine's **CONFIGURE** tab, add the `vision / face-identification` vision service and name it `face-detect`.

On the panel that appears, enter the following configuration in the attributes field, making sure to update the `picture_directory` path to point to your <FILE>known_faces</FILE> folder.

```json {class="line-numbers linkable-line-numbers"}
{
  "camera_name": "my_webcam",
  "picture_directory": "/path/to/known_faces"
}
```

For more configuration options, see the [`viam-face-identification` module documentation](https://github.com/viam-modules/viam-face-identification?tab=readme-ov-file#attributes-description).

{{% /tablestep %}}
{{% tablestep %}}
**Test the face identification.**

Click on the `face-detect` vision service's **TEST** panel.
Whenever a known face is detected, you should see a bounding box with the person's name around the face.

{{% /tablestep %}}
{{< /table >}}

## Configure the security system

Now that you have configured both the people detector and the face identification service, you are ready to add the alarm logic that combines both.

The [`verification-system` module](https://app.viam.com/module/viam-labs/verification-system) contains the required logic.
It uses the camera stream, the people detector, and the face identification service to decide when to raise an alarm.

1. On your machine's **CONFIGURE** tab, add the `vision / verification-system` vision service and name it `verification-system`.

1. On the panel that appears, enter the following configuration into the attributes field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera_name": "my_webcam",
     "trigger_1_detector": "person-detector",
     "trigger_1_labels": ["Person"],
     "trigger_1_confidence": 0.35,
     "trigger_2_detector": "person-detector",
     "trigger_2_labels": ["Person"],
     "trigger_2_confidence": 0.5,
     "verification_detector": "face-detect",
     "verification_labels": ["john_doe", "jane_doe"],
     "disable_alarm": false,
     "disarmed_time_s": 10,
     "countdown_time_s": 10
   }
   ```

   The `verification-system` module uses distinct states.
   Its default state is called `TRIGGER_1`, which the system is in when there are low-confidence detections or no detections.

   If a person is detected in the camera stream with high confidence, the system will go into the `COUNTDOWN` state.
   During the countdown, it waits for a verified face to be identified by the configured `verification_detector`, which is the `face-detect` vision service.
   If the face identification service returns a label that is in the `verification_labels` array within the 10-second countdown, no alarm will be raised.
   Otherwise the system raises an alarm.

   For a more detailed overview on the states, see the [`verification-system` module documentation](https://github.com/viam-labs/verification-system).

1. If you used different names for your camera, model, or vision service, update them.
1. Also update the `verification_labels` to use the names of the people your system can detect - these are the folder names inside the <FILE>known_faces</FILE> folder.
1. For more configuration information, see the [`verification-system` module documentation](https://github.com/viam-labs/verification-system?tab=readme-ov-file#attributes).

## Test the system

At this point, your machine is fully capable of detecting people in its camera feed and identifying whether a specific detected person is "approved" (as specified under `"verification_labels"`) or not.
To see this in action, click on the `verification-system`'s **TEST** panel to see the camera stream.

The current state of the `verification-system` is visible as an overlay on the camera stream.
It should be `TRIGGER_1` if no people are visible.
Have one or more people walk in front of the camera and look directly at it.
Watch the state change to `COUNTDOWN` and then `DISARMED` when an approved person is detected, or to `ALARM` if no approved person appears within 10 seconds.

![Verification camera feed](/tutorials/verification-system/disarmed.png)

## Using the alarm state

The alarm state currently does not cause anything to happen besides appearing as an overlay on the camera stream.

To trigger an audio alarm or have your machine take an action based on the reported state, you can fork the [`verification-system` module](https://github.com/viam-labs/verification-system) to add logic when the system enters the [`ALARM` state](https://github.com/viam-labs/verification-system/blob/9f4bf41e878f6e15d9ffab661995f3556032f33d/src/verificationclassifier.py#L272).

## Next steps

Now that you have the verification aspect of your system working, you can use this as a launch point for customizing your own DIY home security system.
To dive deeper, we recommend looking at the [`verification-system` module logic](https://github.com/viam-labs/verification-system/blob/9f4bf41e878f6e15d9ffab661995f3556032f33d/src/verificationclassifier.py).
