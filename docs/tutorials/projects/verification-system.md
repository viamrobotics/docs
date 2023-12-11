---
title: "Create a Facial Verification System"
linkTitle: "Verification System"
type: "docs"
description: "Configure a verification system module to implement a facial verification security system on your smart machine."
image: "/tutorials/verification-system/disarmed.png"
imageAlt: "Bijan disarming the facial verification system."
images: ["/tutorials/verification-system/disarmed.png"]
tags: ["mlmodel", "vision", "services", "security", "camera"]
authors: ["Sierra G."]
languages: []
viamresources: ["mlmodel", "vision", "camera"]
level: "Intermediate"
date: "28 November 2023"
cost: "0"
no_list: true
# SMEs: Bijan Haney
---


Follow this tutorial to create a simple security system with visual people detection to alarm, and facial recognition to disarm.
In this project, you will create a security system with facial recognition to "verify" whether intruders present are recognized by your system and can disable your alarm.
To accomplish this on your machine, you will configure an [`mlmodel` person detector](#configure-an-mlmodel-person-detector) and [facial detector](#configure-a-facial-detector) together in the [`verification-system` module](https://app.viam.com/module/viam-labs/verification-system).

The verification system module itself is a model of [vision service classifier](/ml/vision/classification/), a type of vision service that returns labels for a given image, but it works because of these layered [vision service detectors](/ml/vision/detection/), object detectors which return bounding boxes drawn around the identified objects.
With the combination of detectors you configure on your machine, your verification system will trigger a countdown when it detects people and disarm the alarm if it detects your face with the facial detector within the countdown period.

For example:

{{<video webm_src="/tutorials/verification-system/demo.webm" mp4_src="/tutorials/verification-system/demo.mp4" alt="Bijan interacting with the verification system" poster="/tutorials/verification-system/trigger_1.png">}}

## Requirements

- A [camera](/components/camera/)
- A computer running `viam-server` that the camera can connect to, like a [single-board computer (SBC)](/components/board/)

Before configuring your camera, you must [create a robot](/fleet/machines/#add-a-new-robot).

1. On the locations page of the [Viam app](https://app.viam.com), add a new robot by providing a name in the **New Robot** field and clicking **Add robot**.
2. Click on that robot's name to go to its page.

## Configure a camera

Navigate to the **Config** tab of your machine's page on the [Viam app](https://app.viam.com).
Configure the camera you want to use for your security system.

We configured ours as a webcam named `"my-webcam"`.
Follow [these instructions](/components/camera/webcam/) to do so.

Connect your camera to your machine running `viam-server`, and hang it up somewhere where it can see people in your home:

{{<imgproc src="/tutorials/verification-system/camera.jpeg" resize="500x" declaredimensions=true alt="Camera hanging up in office.">}}

Next, configure the person detector, or, the "coarser" layer of the security system that verifies that there's a person moving.

## Configure an `mlmodel` person detector

Create a detector to detect when people are in your verification system camera's field of vision:

1. [Capture images from your camera](/data/capture/#configure-data-capture-for-individual-components) with Viam's data management service, then [create a dataset](/data/dataset/#create-a-dataset-and-add-data).
2. Label your data with [bounding boxes](/data/dataset/#bounding-boxes) labeled as `Person` where a person is present to create an object detection model for people. You only want this model to be able to distinguish between what is and isn't a person, so you can conduct this training step with anyone.
3. [Train a model on your dataset](/ml/train-model/). Select **Model Type** as **Object Detection**.
4. [Deploy the model](/ml/deploy/) to your machine so you can use it.

Now that you've trained and deployed the model itself, [configure an `mlmodel` detector model](/ml/vision/detection/#configure-an-mlmodel-detector) with the name of the ML model service you deployed your model as.
Name this detector `"people-detect"`.

For example, we configured a person detector as follows:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.persondetect0tflite}/persondetect0.tflite",
      "label_path": "${packages.persondetect0tflite}/persondetectlabels.txt",
      "num_threads": 1
    },
    "name": "persondetect"
  },
  {
    "name": "people-detect",
    "type": "vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "persondetect"
    }
  }
]
```

Now, move on to configuring the "finer" layer of the detectors-- the facial recognition detector.

## Configure a facial detector

To create a detector that can recognize individual faces, use Viam Lab's `facial-detector` module, available in the [registry](https://app.viam.com/module/viam-labs/facial-detector).
This is a modular vision service that uses the DeepFace library to perform facial detections.

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Services** subtab and click **Create service**.
Select the `vision` type, then select the `detector:facial-detector` model. Enter a name for your vision service, `"face-detect"` and click **Create**.

Edit the attributes as applicable according to the configuration information on [GitHub](https://github.com/viam-labs/facial-detection):

- `"face_labels"`: Label a photo of the face of each person you want your security system to recognize with the name you want for the label paired with the image path.
- `"recognition_model"`: The model to use for facial recognition. `"ArcFace"` is chosen as the default for a good balance of speed and accuracy. See [GitHub](https://github.com/viam-labs/facial-detection) for more options.
- `"detection_framework"`: The detection framework to use for facial detection. `"ssd"` is chosen as the default for a good balance of speed and accuracy.

```json {class="line-numbers linkable-line-numbers"}
{
  "face_labels": {
    "my_name": "/home/me/my-photo.jpg"
  },
  "recognition_model": "ArcFace",
  "detection_framework": "ssd"
}
```

Make sure to name this detector `"face-detect"`.

## Configure a verification system

Now that you've configured your camera, a rough `"people-detect"` detector and a more fine-tuned `"face-detect"` facial detector, you can set up your facial verification system module.

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/). Click on the **Services** subtab and click **Create service**. Select the `vision` type, then select the `classifier:verification-system` model. Enter a name for your vision service and click **Create**.

To use the facial detector as the verification detector and the people detector as the first two layers of detectors, with **Builder** mode selected copy and paste the following attributes configuration into your service's **Attributes** box:

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

Name your service `"security"`.

- As the `"people-detect"` detector serves as both trigger detector 1 and 2, set `"trigger_1_labels"` and `"trigger_2_labels"` to `"Person"` to match the bounding box label of `"Person"` you assigned to images in your dataset when training the object detection model behind this detector.
- As the verification detector is your facial detector `"face-detect"`, set `"verification_labels"` to match each name you assigned to an image in the facial detector modules' `"face_labels"` configuration attribute.
- Note that `"camera_name": "my_webcam"` matches the name we configured for our source camera.
  If you used a different name for your camera, change the name in the JSON.
- Edit the other attributes to reflect your desired confidence thresholds and times between states.

The following attributes are available for the `viam-labs:classifier:verification-system` model:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `camera_name` | string | **Required** | The name of the camera component to use for source images. |
| `trigger_1_detector` | string | Optional | The name of the [vision service detector](/ml/vision/detection/) that will be used as the first stage to trigger the system to enter verification mode. If left blank, the system will immediately transition to state `TRIGGER_2`. |
| `trigger_1_labels` | array | Optional | The class names from `trigger_1_detector` that count as valid. Required if `trigger_1_detector` is specified. |
| `trigger_1_confidence` | float | Optional | The detection confidence needed in order to move into the `TRIGGER_2` state. <br> Default: `0.2` |
| `trigger_2_detector` | string | **Required** | The name of the vision service detector that will detect the thing that needs to be verified. |
| `trigger_2_labels` | array | **Required** | The class names from `trigger_2_detector` that count as valid. |
| `trigger_2_confidence` | float | Optional | The detection confidence needed in order to move into the `COUNTDOWN` state. <br> Default: `0.5` |
| `verification_detector` | string | **Required** | The name of the vision service detector that you want to use to verify the object. |
| `verification_labels` | array | **Required** | The class names from `verification_detector` that count as valid. |
| `verification_confidence` | float | Optional | The detection confidence needed in order to move into the `DISARMED` state. <br> Default: `0.8` |
| `countdown_time_s` | int | Optional | The time in seconds the system will remain in state `COUNTDOWN` before transitioning to state `ALARM`. <br> Default: `20` |
| `alarm_time_s` | int | Optional | The time in seconds the system will remain in  state `ALARM` before transitioning to state `TRIGGER_1`. <br> Default: `10` |
| `disarmed_time_s` | int | Optional | The time in seconds the system will remain in  state `DISARMED` before transitioning to state `TRIGGER_1`. <br> Default: `10` |
| `disable_alarm` | bool | Optional | Disables the `COUNTDOWN` and `ALARM` states. The system will always remain the `TRIGGER_1` and `TRIGGER_2` states. <br> Default: `false` |

## Configure a transform camera

To view the classifications that your verification system makes, configure a transform camera.

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**. Select the `camera` type, then select the `transform` model. Enter a name for your camera and click **Create**.

With **Builder** mode selected, copy and paste the following attributes JSON into your camera's **Attributes** box:

```json {class="line-numbers linkable-line-numbers"}
{
  "pipeline": [
    {
      "type": "classifications",
      "attributes": {
        "classifier_name": "security",
        "confidence_threshold": 0.5
      }
    }
  ],
  "source": "my-webcam"
}
```

Note that the camera name in `"source"` and the `"classifier_name"` match the names that we configured for our source camera and verification system service, respectively.
If you used different names, edit as applicable.
View these [instructions to configure a transform camera](/components/camera/transform/) for reference.
Save your config.

## View your verification system in action

Navigate to the **Control** tab.
Expand the card matching the name of the transform camera you configured to view an image stream with the system's notifications overlaid.

## How the verification system works

The module sets up a state machine with 5 states:

1. `TRIGGER_1`: The module begins in this state.
   It is meant to be attached to a coarse, fast detector, like a simple motion detector.
   This state runs the `trigger_1_detector` on every frame, looking for detections with any label from `trigger_1_labels` with at least `trigger_1_confidence`.
   If the detector triggers, then the state moves to `TRIGGER_2`.
   If no `TRIGGER_1` detector was specified in the config, the module moves immediately to state `TRIGGER_2`.
2. `TRIGGER_2`: This state runs the `trigger_2_detector` on every frame, looking for detections with any label from `trigger_2_labels` with at least `trigger_2_confidence`.
   If the detector triggers, then the state moves to `COUNTDOWN`.
   If it doesn't trigger in 10 frames, it returns to state `TRIGGER_1`.
3. `COUNTDOWN`: This state runs the `verification_detector` on every frame, looking for detections with any label from `verification_labels` with at least `verification_confidence`.
   If the detector triggers, then the state moves to `DISARMED`.
   If it doesn't trigger in the time specified by `countdown_time_s`, it moves to state `ALARM`.
4. `ALARM`: The alarm state.
   The module will emit the `ALARM` classification for the amount of time specified in `alarm_time_s`.
   After that amount of time elapses, the module will return to state `TRIGGER_1`.
5. `DISARMED`: The disarmed state.
   The module will emit the `DISARMED` classification for the amount of time specified in `disarmed_time_s`.
   After that amount of time elapses, the module will return to state `TRIGGER_1`.

If you do not want the `ALARM` capabilities, and would like to just use it as a notification system when a detector gets triggered, you can set `disable_alarm: true` in the config, which will prevent `TRIGGER_2` from entering into the `COUNTDOWN` state.
This means the system will only cycle between the states of `TRIGGER_1` and `TRIGGER_2`.

You can use entering into the state `TRIGGER_2` as a way to send notifications.

## Next Steps

- Try changing the type of [detectors](/ml/vision/detection/), using different detectors for the `TRIGGER_1` and `TRIGGER_2` states.
- Configure the [filtered camera module](https://app.viam.com/module/erh/filtered-camera) and use it as the source camera in your verification system to save images to the Viam cloud when the system enters into specific states.
