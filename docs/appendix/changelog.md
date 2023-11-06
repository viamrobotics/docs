---
title: "Changelog"
linkTitle: "Changelog"
weight: 110
draft: false
type: "docs"
description: "A lot of added features, improvements, and changes over time."
aliases:
  - "/appendix/release-notes/"
# SME:
---

## April 2023

### Changed: Vision service

{{% alert title="Important: Breaking Change" color="note" %}}

The [vision service](/services/vision/) became more modular in RDK [v0.2.36](https://github.com/viamrobotics/rdk/releases/tag/v0.2.36), API [v0.1.118](https://github.com/viamrobotics/api/releases/tag/v0.1.118), and Python SDK [v0.2.18](https://github.com/viamrobotics/viam-python-sdk/releases/tag/v0.2.18).

Find more information on each of the changes below.

{{% /alert %}}

#### Use individual vision service instances

You need to create **an individual vision service instance** for each detector, classifier, and segmenter model.
You can no longer be able to create one vision service and register all of your detectors, classifiers, and segmenters within it.

{{%expand "Click for details on how to migrate your code." %}}

#### API calls

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

{{< tabs >}}
{{% tab name="New Way" %}}

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

```python {class="line-numbers linkable-line-numbers"}
my_object_detector = VisionClient.from_robot(robot, "find_objects")
img = await cam.get_image()
detections = await my_object_detector.get_detections(img)
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```python {class="line-numbers linkable-line-numbers"}
vision = VisionServiceClient.from_robot(robot)
img = await cam.get_image()
detections = await vision.get_detections(img, "find_objects")
```

{{% /tab %}}
{{< /tabs >}}

#### Color Detector configurations

You can replace existing color detectors by [configuring new ones in the UI](/services/vision/detection/#configure-a-color_detector) or you can update the [Raw JSON configuration of your robots](/manage/configuration/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "blue_square",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 100,
            "detect_color": "#1C4599",
            "hue_tolerance_pct": 0.07,
            "value_cutoff_pct": 0.15
        }
    },
    {
        "name": "green_triangle",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 200,
            "detect_color": "#62963F",
            "hue_tolerance_pct": 0.05,
            "value_cutoff_pct": 0.20
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "segment_size_px": 100,
                    "detect_color": "#1C4599",
                    "hue_tolerance_pct": 0.07,
                    "value_cutoff_pct": 0.15
                },
                "name": "blue_square",
                "type": "color_detector"
            },
            {
                "parameters": {
                    "segment_size_px": 200,
                    "detect_color": "#62963F",
                    "hue_tolerance_pct": 0.05,
                    "value_cutoff_pct": 0.20
                },
                "name": "green_triangle",
                "type": "color_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite Detector configurations

You can replace existing TFLite detectors by [configuring new ones in the UI](/services/vision/detection/#configure-an-mlmodel-detector) or you can update the [Raw JSON configuration of your robots](/manage/configuration/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "person_detector",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/file.tflite",
            "label_path": "/path/to/labels.tflite",
            "num_threads": 1
        }
    },
    {
        "name": "person_detector",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "person_detector"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/file.tflite",
                    "label_path": "/path/to/labels.tflite",
                    "num_threads": 1
                },
                "name": "person_detector",
                "type": "tflite_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite Classifier configurations

You can replace existing TFLite classifiers by [configuring new ones in the UI](/services/vision/classification/#configure-an-mlmodel-classifier) or you can update the [Raw JSON configuration of your robots](/manage/configuration/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "fruit_classifier",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/classifier_file.tflite",
            "label_path": "/path/to/classifier_labels.txt",
            "num_threads": 1
        }
    },
    {
        "name": "fruit_classifier",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "fruit_classifier"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/classifier_file.tflite",
                    "label_path": "/path/to/classifier_labels.txt",
                    "num_threads": 1
                },
                "name": "fruit_classifier",
                "type": "tflite_classifier"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Radius Clustering 3D Segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/services/vision/segmentation/#configure-an-obstacles_pointcloud-segmenter) or you can update the [Raw JSON configuration of your robots](/manage/configuration/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "rc_segmenter",
        "type": "vision",
        "model": "obstacles_pointcloud"
        "attributes": {
            "min_points_in_plane": 1000,
            "min_points_in_segment": 50,
            "clustering_radius_mm": 3.2,
            "mean_k_filtering": 10
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "min_points_in_plane": 1000,
                    "min_points_in_segment": 50,
                    "clustering_radius_mm": 3.2,
                    "mean_k_filtering": 10
                },
                "name": "rc_segmenter",
                "type": "radius_clustering_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Detector to 3D Segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/services/vision/segmentation/#configure-a-detector_3d_segmenter) or you can update the [Raw JSON configuration of your robots](/manage/configuration/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "my_segmenter",
        "type": "vision",
        "model": "detector_3d_segmenter"
        "attributes": {
            "detector_name": "my_detector",
            "confidence_threshold_pct": 0.5,
            "mean_k": 50,
            "sigma": 2.0
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "detector_name": "my_detector",
                    "confidence_threshold_pct": 0.5,
                    "mean_k": 50,
                    "sigma": 2.0
                },
                "name": "my_segmenter",
                "type": "detector_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand%}}

#### Add and remove models using the robot config

You must add and remove models using the [robot config](/manage/configuration/).
You will no longer be able to add or remove models using the SDKs.

#### Add machine learning vision models to a vision service

The way to add machine learning vision models is changing.
You will need to first register the machine learning model file with the [ML model service](/services/ml/) and then add that registered model to a vision service.

## February 2023

### Added: Rover reuse in Try Viam

You now have the option to reuse a robot config from a previous Try Viam session.

### Added: Dynamic code samples

The Viam app **Code sample** tab now dynamically updates as you add resources to your robot's config.
The code samples instantiate each resource and include examples of how to call a `Get` method on it.

### Added: TypeScript SDK

Find more information in the [TypeScript SDK docs](https://ts.viam.dev/).

### Added: Frame system visualizer

When adding [frames](/services/frame-system/) to your robot's config in the Viam app, you can now use the **Frame System** subtab of the **Config** tab to more easily visualize the relative positions of frames.

### Added: Support for microcontrollers

Micro-RDK is a lightweight version of the RDK that can run on an ESP32.
Find more information in the [micro-RDK documentation](/installation/prepare/microcontrollers/).

## January 2023

### Added: Remote control power input

On your robot's **Control** tab on the [Viam app](https://app.viam.com/), you can now set the power of a [base](/components/base/).
The base control UI previously always sent 100% power to the base's motors.

### Added: New encoder model: AMS AS5048

The [AMS AS5048](/components/encoder/ams-as5048/) is now supported.

### Added: GetLinearAcceleration method

The movement sensor API now includes a [GetLinearAcceleration](/components/movement-sensor/#getlinearacceleration) method.

### Added: Support for capsule geometry

The [motion service](/services/motion/) now supports capsule geometries.

The UR5 arm model has been improved using this new geometry type.

## December 2022

### Added: Modular resources

You can now implement your own custom {{< glossary_tooltip term_id="resource" text="resources" >}} as [_modular resources_](/registry/).

The [old method](/registry/advanced/custom-components-remotes/) of using a separate server to implement a custom resource is still supported, but implementation as a modular resource reduces network requests and is strongly recommended.

{{% alert title="Important: Breaking Change" color="note" %}}

All users need to update to the latest version of the RDK (V3.0.0) to access robots using the Viam app.

{{% /alert %}}

### Added: URDF kinematic file support

You can now supply kinematic information using URDF files when implementing your own arm models.

### Added: New movement sensor models

There are two new movement sensor {{< glossary_tooltip term_id="model" text="models" >}}:

- [ADXL345](/components/movement-sensor/adxl345/): A 3-axis accelerometer
- [MPU-6050](/components/movement-sensor/mpu6050/): A 6-axis accelerometer and gyroscope

### Improved: Camera performance and reliability

- Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
  **The default mime type for color cameras is now JPEG**, which improves the streaming rate across every SDK.
- Added discoverability when a camera reconnects without changing video paths.
  This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.

### Improved: Motion planning with remote components

The [motion service](/services/motion/) is now agnostic to the networking topology of a robot.

- Kinematic information is now transferred over the robot API.
  This means that the motion service is able to get kinematic information for every component on the robot, regardless of whether it is on a main or remote viam-server.
- Arms are now an input to the motion service.
  This means that the motion service can plan for a robot that has an arm component regardless of whether the arm is connected to a main or {{< glossary_tooltip term_id="remote" text="remote" >}} instance of `viam-server`.

### Improved: Motion planning path smoothing

- RRT\* paths now undergo rudimentary smoothing, resulting in improvements to path quality with negligible change to planning performance.
- Plan manager now performs direct interpolation for any solution within some factor of the best score, instead of only in the case where the best inverse kinematics solution could be interpolated.

### Improved: Data synchronization reliability

Previously, data synchronization used bidirectional streaming.
Now is uses a simpler unary approach that is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.

## November 2022

### Changed: Camera configuration

**Changed** the configuration schemes for the following camera models:

- Webcam
- FFmpeg
- Transform
- Join pointclouds

For information on configuring any camera model, see [Camera Component](/components/camera/).

### Changed: App code sample tab name update

Changed the name of the **Connect** tab to **Code sample** based on user feedback.

### Added: New servo model

A new [servo model called `gpio`](/components/servo/gpio/) supports servos connected to non-Raspberry Pi boards.

### Added: RTT indicator in the app

A badge in the Viam app now displays RTT (round trip time) of a request from your client to the robot.
Find this indicator of the time to complete one request/response cycle on your robot's **Control** tab, in the **Operations & Sessions** card.

### Added: Python 3.8 support

The Python SDK now supports Python 3.8, in addition to 3.9 and 3.10.

### Added: New parameter: `extra`

A new API method parameter, `extra`, allows you to extend {{< glossary_tooltip term_id="modular-resource" text="modular-resource" >}} functionality by implementing the new field according to whatever logic you choose.
`extra` has been added to the following APIs: arm, data management, gripper, input controller, motion, movement sensor, navigation, pose tracker, sensor, SLAM, vision.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

Users of the Go SDK _must_ update code to specify `extra` in the arguments that pass into each request.

`extra` is an optional parameter in the Python SDK.

{{% /alert %}}

### Added: Service dependencies

`viam-server` now initializes and configures resources in the correct order.
For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the SLAM service.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

If you are using the SLAM service, you now need to specify sensors used by the SLAM service in the `depends_on` field of the SLAM configuration.
Other service configurations are not affected.

{{% /alert %}}

### Removed: width and height fields from camera API

Removed `width` and `height` from the response of the [`GetImage`](/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.
