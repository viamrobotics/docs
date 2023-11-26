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

## Novemeber 2023

### Changed: Model training from datasets

To make it easier to iterate while training machine learning models from image data, you now train models from [datasets](/data/dataset/).

## October 2023

### Added: Test an ML model in browser

After you upload and train a machine learning model, you can test its results in the **Data** tab.

This allows you to refine models by iteratively tagging more images for training based on observed performance.

For more information, see [Test classification models with existing images in the cloud](/ml/vision/classification/#existing-images-in-the-cloud).

To use this update, the classifier must have been trained or uploaded after September 19, 2023.
The current version of this feature exclusively supports classification models.

### Added: PLC support

The Viam platform now supports the [Revolution Pi line of PLCs](https://revolutionpi.com/) from KUNBUS in the form of a [module](https://app.viam.com/module/viam-labs/viam-revolution-pi).
This collaboration allows you to leverage the Raspberry Pi-based Revolution Pi, which runs on Linux and has a [specially designed I/O modules](https://www.raspberrypi.com/products/compute-module-4/?variant=raspberry-pi-cm4001000) for streamlined interaction with industrial controls, eliminating the need for additional components.

Read the [Viam PLC Support](https://www.viam.com/post/viam-plc-support-democratizing-access-to-smart-ot-and-ics) blog post for a step-by-step guide on using a PLC with Viam.

### Improved: SLAM map creation

The [Cartographer-module](/mobility/slam/cartographer/) now runs in Viam's cloud for creating or updating maps.
This enhancement allows you to:

- Generate larger maps without encountering session timeouts
- Provide IMU input to improve map quality
- Save maps to the **SLAM library** tab
- Create or update maps using previously captured LiDAR and IMU data
- Deploy maps to machines

## September 2023

### Added: Modular registry

The [Modular Registry](/registry/) enables you to use, create, and share custom modules, extending the capabilities of Viam beyond the components and services that are natively supported.

You can:

- Publish modules on the registry
- Add modules to any machine's configuration with a few clicks
- Select the desired module version for deployment, make changes at your convenience, and deploy the updates to a single machine or an entire fleet.

### Added: Mobile app

You can use a [mobile application](/fleet/#the-viam-mobile-app), available for download now in the [Apple](https://apps.apple.com/us/app/viam-robotics/id6451424162) and [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US) app stores, to connect to and control your Viam-powered machines directly from your mobile device.

### Added: Power sensor component

You now have the capability to use a [power sensor component](/build/configure/components/power-sensor/) to monitor the voltage, current, and power consumption within your machine's system.

### Added: Filter component's data before the cloud

Viam has written a module that allows you to filter data based on specific criteria before syncing it to [Viam's cloud](/data/cloud-sync/).
It equips machines to:

- Remove data that is not of interest
- Facilitate high-interval captures while saving data based on your defined metrics
- Prevent the upload of unnecessary data

To learn more, see [this tutorial](/tutorials/configure/pet-photographer/) on creating and configuring a data filtration module.

## August 2023

### Added: Configure a customlinux board

You can now use boards like the [Mediatek Genio 500 Pumpkin](https://ologicinc.com/portfolio/mediateki500/) that run Linux operating systems with the [`customlinux` board model](/build/configure/components/board/customlinux/).

### Added: Image inspection for ML training

This update enables you to get a closer examination of your image and streamline your image annotation experience by making it easier to add bounding boxes and labels in the **Data** tab.

With the latest improvements, you can now:

- Navigate between images using the arrow keys in the main image view
- Expand images for a more detailed inspection by clicking the expand button on the right image panel
- Move between full-screen images effortlessly with the <> arrow buttons or arrow keys
- Return to the standard view by using the escape key or collapse button

### Added: Duplicate component button

You now have the ability to duplicate any config component, service, module, remote, or process.

To use this feature:

- Click on the duplicate component icon at the top right of any resource
- Optionally, you can modify the component name to distinguish it
- Adjust any attributes, such as motor pin numbers

## July 2023

### Added: Apple SSO Authentication

Viam now supports sign-up/log-in through Apple Single Sign-On.

Note that currently, accounts from different SSO providers are treated separately, with no account merging functionality.

### Improved: Arm component API

Arm models now support the [`GetKinematics` method](/build/configure/components/arm/#getkinematics) in the arm API, allowing you to request and receive kinematic information.

## June 2023

### Added: View sensor data within Viam

You can now [view your sensor data](https://app.viam.com/data/view?view=sensors) directly in the Viam app to verify data creation and accuracy.
If you depend on sensor data to plan and control robot operations, this feature increases access to data and supports a more efficient workflow.

### Added: Session management in the Python SDK

The Python SDK now includes sessions, a safety feature that automatically cancels operations if the client loses connection to your robot.

[Session management](/build/program/apis/sessions/) helps you to ensure safer operation of your robot when dealing with actuating controls.
Sessions are enabled by default, with the option to [disable sessions](/build/program/apis/sessions/#disable-default-session-management).

### Added: Connect an ODrive motor controller as a Viam module

You can integrate and control ODrive motor controllers with Viam using a modular resource.

Visit the [GitHub repository](https://github.com/viamrobotics/odrive) to learn how to connect and use an ODrive motor controller with Viam, and view the sample configurations.

### Added: Implement custom robotic arms as Viam modules

When prototyping a robotic arm, you can now facilitate movement without creating your own motion planning.
This update enables you to implement custom models of an arm component as a [modular resource](/registry/) by coding three endpoints of the [Arm API](/build/configure/components/arm/#api):

- `getJointPositions`
- `movetoJointPositions`
- `GetKinematics`

Then, use the [motion planning service](/mobility/motion/) to specify poses, and Viam handles the rest.

For more information, see this [tutorial on creating a custom arm](/registry/examples/custom-arm/).

### Added: Apply a crop transform to camera views

You can now apply a [crop transform](/build/configure/components/camera/transform/) to the views of your connected cameras in the Viam app.

This feature enables you to focus on a specific area of your camera feed.

For example, crop a video stream of a busy street to just the sidewalk.

### Improved: Gantry component

To better control gantries with Viam, you can now:

- Specify speed values when calling the `MovetoPosition` method on [Gantry components](/build/configure/components/gantry/).
  This allows you to define the speed at which each axis moves to the desired position, providing enhanced precision and control over the gantry's movement.
- Set a home position for Gantry components to facilitate position resetting or maintain consistent starting points.

### Improved: Optimized Viam-trained object detection models

This update for object detection models [trained with the machine learning service](/ml/train-model/) brings significant improvements, including:

- 76% faster model inference for camera streams
- 64% quicker model training for object detection
- 46% reduction in compressed model size

## May 2023

### Added: TypeScript SDK beta release

The beta release of the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/) allows you to create a web interface to work with your robot, as well as create custom components and services.

### Added: Train object detection ML models

You now have the capability to directly [train object detection models](/ml/train-model/) in addition to image classification models from within the Viam app.

This update allows you to:

- Add labels by drawing bounding boxes around specific objects in your images or a single image.
- Create a curated subset of data for training by filtering images based on labels or tags.

### Added: Permissions for organizations in Viam

Now when you invite collaborators to join your organization, you can assign permissions to members by setting one of these roles:

- **Owner**: These members can see and edit [every tab on the robot page](/fleet/machines/#navigating-the-robot-page), as well as manage users in the app.
  This role is best for those on your team who are actively engineering and building robots.

- **Operator**: These members can only see and use the [remote control tab](/fleet/machines/#control).
  This role is best for those on your team who are teleoperating or remotely controlling robots.

For more information about assigning permissions and collaborating with others on Viam, see [Fleet Management](/fleet/).

### Improved: Control RoboClaw motor controllers with the driver

When using a RoboClaw motor controller without encoders connected to your motors, you now have more direct control over the RoboClaw’s functionality within Viam or through the motor API.

For example, in the Viam app, you can now set **Go For** values for these motors, utilizing a time-based estimation for the number of revolutions.

### Improved: Camera webcam names and setting framerates

The updates to the camera component have improved the process of connecting to and using cameras with your robots.

The latest updates enable you to:

- View readable webcam names in the **video path** of your camera component.
- Specify your preferred framerate by selecting the desired value in the newly added **framerate field** on the **Config** tab.

### Improved: Additions to code samples in the Viam app

The updated code samples now includes:

- Options for C++ and TypeScript
- The ability to hide or display your robots' [secrets](/build/program/apis/)

Access these samples in the **Code sample** tab on your robot's page to connect to your robot in various languages.

### Improved: Delete data in bulk in the Viam app

You can manage the data synced to Viam's cloud with the new capability for bulk data deletion on the **Data** tab.

## April 2023

### Changed: Vision service

{{% alert title="Important: Breaking Change" color="note" %}}

The [vision service](/ml/vision/) became more modular in RDK [v0.2.36](https://github.com/viamrobotics/rdk/releases/tag/v0.2.36), API [v0.1.118](https://github.com/viamrobotics/api/releases/tag/v0.1.118), and Python SDK [v0.2.18](https://github.com/viamrobotics/viam-python-sdk/releases/tag/v0.2.18).

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

You can replace existing color detectors by [configuring new ones in the UI](/ml/vision/detection/#configure-a-color_detector) or you can update the [Raw JSON configuration of your robots](/build/configure/#the-config-tab):

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

You can replace existing TFLite detectors by [configuring new ones in the UI](/ml/vision/detection/#configure-an-mlmodel-detector) or you can update the [Raw JSON configuration of your robots](/build/configure/#the-config-tab):

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

You can replace existing TFLite classifiers by [configuring new ones in the UI](/ml/vision/classification/#configure-an-mlmodel-classifier) or you can update the [Raw JSON configuration of your robots](/build/configure/#the-config-tab):

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

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/ml/vision/segmentation/#configure-an-obstacles_pointcloud-segmenter) or you can update the [Raw JSON configuration of your robots](/build/configure/#the-config-tab):

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

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/ml/vision/segmentation/#configure-a-detector_3d_segmenter) or you can update the [Raw JSON configuration of your robots](/build/configure/#the-config-tab):

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

You must add and remove models using the [robot config](/build/configure/).
You will no longer be able to add or remove models using the SDKs.

#### Add machine learning vision models to a vision service

The way to add machine learning vision models is changing.
You will need to first register the machine learning model file with the [ML model service](/ml/) and then add that registered model to a vision service.

## March 2023

### Added: Machine learning for image classification models

You can now [train](/ml/train-model/) and [deploy](/ml/deploy/#create-an-ml-model-service) image classification models with the [data management service](/data/) and use your robot's image data directly within Viaml
Additionally, you can [upload and use](/ml/upload-model/) existing machine learning models with your robots.
For more information on using data synced to the cloud to train machine learning models, read [Train a model](/ml/train-model/).

### Added: Motion planning with new `constraint` parameter

A new parameter, [`constraint`](/mobility/motion/constraints/), has been added to the [Motion service API](/mobility/motion/#api), allowing you to define restrictions on the robot's movement.
The constraint system also provides flexibility to specify that obstacles should only impact specific frames of a robot.

### Added: Fragments in robot configuration

You can now access {{< glossary_tooltip term_id="fragment" text="fragments" >}} in your robot setup.
The configurations you added will now show up automatically in the **Components** or **Services** subtabs in the **Builder** view.
This makes it easier to monitor what fragments you've added to your robot and how they're configured.

For more information, see [Fragments](/build/configure/#fragments).

### Improved: Sticky GPS keys

GPS keys you enter are now saved in your local storage.
This ensures that when you reload the page, your GPS keys remain accessible.

### Improved: More reliable camera streams

The camera component's streams are smoother and more reliable with recent improvements.

Additionally, camera streams automatically restart if you momentarily lose internet connection.

### UI updates to Logs and History

The latest UI updates enable you to:

- Load a previous configuration for reverting changes made in the past
- Search logs by filtering keywords or log levels such as _info_ or _error_ messages
- Change your timestamp format to **ISO** or **Local** depending on your preference.

## February 2023

### Added: Rover reuse in Try Viam

You now have the option to reuse a robot config from a previous Try Viam session.

### Added: Dynamic code samples

The Viam app **Code sample** tab now dynamically updates as you add resources to your robot's config.
The code samples instantiate each resource and include examples of how to call a `Get` method on it.

### Added: TypeScript SDK

Find more information in the [TypeScript SDK docs](https://ts.viam.dev/).

### Added: Frame system visualizer

When adding [frames](/mobility/frame-system/) to your robot's config in the Viam app, you can now use the **Frame System** subtab of the **Config** tab to more easily visualize the relative positions of frames.

### Added: Support for microcontrollers

Micro-RDK is a lightweight version of the RDK that can run on an ESP32.
Find more information in the [micro-RDK documentation](/get-started/installation/prepare/microcontrollers/).

## January 2023

### Added: Remote control power input

On your robot's **Control** tab on the [Viam app](https://app.viam.com/), you can now set the power of a [base](/build/configure/components/base/).
The base control UI previously always sent 100% power to the base's motors.

### Added: New encoder model: AMS AS5048

The [AMS AS5048](/build/configure/components/encoder/ams-as5048/) is now supported.

### Added: GetLinearAcceleration method

The movement sensor API now includes a [GetLinearAcceleration](/build/configure/components/movement-sensor/#getlinearacceleration) method.

### Added: Support for capsule geometry

The [motion service](/mobility/motion/) now supports capsule geometries.

The UR5 arm model has been improved using this new geometry type.

## December 2022

### Added: Modular resources

You can now implement your own custom {{< glossary_tooltip term_id="resource" text="resources" >}} as [_modular resources_](/registry/).

{{% alert title="Important: Breaking Change" color="note" %}}

All users need to update to the latest version of the RDK (V3.0.0) to access robots using the Viam app.

{{% /alert %}}

### Added: URDF kinematic file support

You can now supply kinematic information using URDF files when implementing your own arm models.

### Added: New movement sensor models

There are two new movement sensor {{< glossary_tooltip term_id="model" text="models" >}}:

- [ADXL345](/build/configure/components/movement-sensor/adxl345/): A 3-axis accelerometer
- [MPU-6050](/build/configure/components/movement-sensor/mpu6050/): A 6-axis accelerometer and gyroscope

### Improved: Camera performance and reliability

- Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
  **The default mime type for color cameras is now JPEG**, which improves the streaming rate across every SDK.
- Added discoverability when a camera reconnects without changing video paths.
  This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.

### Improved: Motion planning with remote components

The [motion service](/mobility/motion/) is now agnostic to the networking topology of a robot.

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

For information on configuring any camera model, see [Camera Component](/build/configure/components/camera/).

### Changed: App code sample tab name update

Changed the name of the **Connect** tab to **Code sample** based on user feedback.

### Added: New servo model

A new [servo model called `gpio`](/build/configure/components/servo/gpio/) supports servos connected to non-Raspberry Pi boards.

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

Removed `width` and `height` from the response of the [`GetImage`](/build/configure/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.
