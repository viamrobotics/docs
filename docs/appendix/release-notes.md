---
title: "Release Notes"
linkTitle: "Release Notes"
weight: 110
draft: true
type: "docs"
description: "Release Notes for Viam."
# SME: Naomi
---

## 25 April 2023

{{< tabs >}}
{{% tab name="Breaking Changes" %}}

## Vision Service

The [vision service](/services/vision/) is becoming more modular in RDK [v0.2.36](https://github.com/viamrobotics/rdk/releases/tag/v0.2.36), API [v0.1.118](https://github.com/viamrobotics/api/releases/tag/v0.1.118), and Python SDK [v0.2.18](https://github.com/viamrobotics/viam-python-sdk/releases/tag/v0.2.18).

The following **breaking changes** will take effect:

- [Use individual vision service instances](#use-individual-vision-service-instances)
- [Add and remove models using the robot config](#add-and-remove-models-using-the-robot-config)
- [Add machine learning vision models to a vision service](#add-machine-learning-vision-models-to-a-vision-service)

### Use individual vision service instances

You will need to create **an individual vision service instance** for each detector, classifier, and segmenter model.
You will no longer be able to create one vision service and register all of your detectors, classifiers, and segmenters within it.

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

### Add and remove models using the robot config

You must add and remove models using the [robot config](../../manage/configuration/).
You will no longer be able to add or remove models using the SDKs.

### Add machine learning vision models to a vision service

The way to add machine learning vision models is changing.
You will need to first register the machine learning model file with the [ML model service](/services/ml/) and then add that registered model to a vision service.

{{% /tab %}}
{{< /tabs >}}

## 28 February 2023

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions

- rdk - **v0.2.18**
- api - **v0.1.83**
- slam - **v0.1.22**
- viam-python-sdk - **v0.2.10**
- goutils - **v0.1.13**
- rust-utils - **v0.0.10**

(**Bold=updated version**)

{{% /tab %}}

{{% tab name="New Features" %}}

## New Features

### Reuse rovers in Try Viam

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                Users of Try Viam now have the option to reuse a robot config if they want to continue working on a project that they started in a prior session.
{{<gif webm_src="/appendix/reuse-rovers.webm" mp4_src="/appendix/reuse-rovers.mp4" alt="Select a rover to reuse in the UI">}}
</td>
        </tr>
    <tbody>
</table>

### Dynamic Code Samples Tab

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                The code sample included for each SDK dynamically updates as resources are added to the config.
                We instantiate each resource and provide an example of how to call a simple <code>Get</code> method so that users can start coding right away without needing to import and provide the name of all of the components and services in their config.
{{<gif webm_src="/appendix/dynamic-code-sample.webm" mp4_src="/appendix/dynamic-code-sample.mp4" alt="Example of the python code sample generated for the Viam Rover fragment">}}
{{<gif webm_src="/appendix/example-output-try-viam.webm" mp4_src="/appendix/example-output-try-viam.mp4" alt="Example output from running the example code used in the Try Viam experience">}}
</td>
        </tr>
    <tbody>
</table>

### TypeScript SDK

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                Users that want to create web interfaces to control their robots can use the new TypeScript SDK as a client.
                Currently only web browser apps are supported due to how networking is handled.
                The RDK server running on the robot is able to detect if a given SDK client session has lost communication because it tries to maintain a configurable heartbeat, by default once every 2 seconds.
                Users can choose to opt-out of this session management.
                <ul>
                <li>
                    <a href="https://ts.viam.dev/">TypeScript SDK Docs</a>
                </li>
                <li>
                    <a href="https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples">Teleop Example from Github page</a>
{{<gif webm_src="/appendix/teleop-example.webm" mp4_src="/appendix/teleop-example.mp4" alt="Example of the python code sample generated for the Viam Rover fragment">}}
</li>
                </ul>
            </td>
        </tr>
    <tbody>
</table>

### Frame System Visualizer

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                Users can now set up a frame system on their robot using a 3D visualizer located in the **Frame System** tab on the config UI.
                Setting up the frame system hierarchy of a robot enables the RDK to transform poses between different component reference frames.
                Users can also give individual components a geometry so that the RDK’s builtin motion planner can avoid obstacles while path planning.
                <ul>
                <li>
{{<gif webm_src="/appendix/frame-system-visualizer.webm" mp4_src="/appendix/frame-system-visualizer.mp4" alt="Example of configuring a frame system for a Viam Rover that has a camera and a lidar">}}
</li>
                </ul>
            </td>
        </tr>
    <tbody>
</table>

### Viam for Microcontrollers

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                Micro-RDK is a lightweight version of the RDK that is capable of running on an ESP32.  Examples & detailed set up instructions can be found in the <a href="https://github.com/viamrobotics/micro-rdk">Micro-RDK GitHub repo.</a>
            </td>
        </tr>
    <tbody>
</table>

{{% /tab %}}

{{% tab name="Improvements" %}}

## Improvements

### Base control card UI

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                We have improved the UI of the base control card to make it easier to view multiple camera streams while remotely controlling a base.
                When a robots config contains SLAM, we also now provide a view of the SLAM Map with a dot to indicate where the robot is currently localized within that map.
                <br>
{{<imgproc src="/appendix/base-control-card-ui.png" resize="600x" declaredimensions=true alt="Base component card UI">}}
</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}

#### Viam Server goes into restart loop instead of using cached config

When restarting a <code>viam-server</code> that was previously connected to the internet and cached the config - it went into a restart loop when it does not have access to the internet.

#### Never have long-lived I2CHandle objects

Creating an <code>I2CHandle</code> locks the I2C bus that spawned it, and closing the handle unlocks the bus again. That way, only one device can talk over the bus at a time, and you don’t get race conditions. However, if a component creates a handle in its constructor, it locks the bus forever, which means no other component can use that bus.

We have changed components that stored an <code>I2CHandle</code>, so that they instead just store a pointer to the board <code>board.I2C</code> bus itself, create a new handle when they want to send a command, and close it again as soon as they're done.

#### Sensor does not show GPS readings

We changed `sensor.Readings ["position"]` field to return the values of the `*geo.Point` being accessed.

#### Add implicit dependencies to servo implementation

All component drivers can now declare dependencies, which are used to infer the order or instantiation.

{{% /tab %}}
{{< /tabs >}}

## 31 January 2023

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions

- rdk - **v0.2.14**
- api - **v0.1.63**
- slam - **v0.1.17**
- viam-python-sdk - **v0.2.8**
- goutils - **v0.1.9**
- rust-utils - **v0.0.9**

(**Bold=updated version**)

{{% /tab %}}

{{% tab name="New Features" %}}

## New Features

### Add Power Input to Remote Control

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>Users can now set the power of the base from the remote control UI. This sets the power percentage being sent to the motors that are driving the base which determines its overall speed.<br>
{{<imgproc src="/appendix/base-power-control.png" alt="Base power control in the UI" resize="400x" >}}
</td>
        </tr>
    <tbody>
</table>

### New Drivers in the RDK: AMS AS5048 Encoder

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>RDK now natively supports the AMS AS5048 encoder. This is the encoder that is included in the SCUTTLE robot.
            </td>
        </tr>
    <tbody>
</table>

{{% /tab %}}

{{% tab name="Improvements" %}}

## Improvements

### Linear Acceleration

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                We added a <code>GetLinearAcceleration</code> method to the movement sensor API.
                This allows us to represent IMUs that are commonly used by hobbyists using the movement sensor interface.
            </td>
        </tr>
    <tbody>
</table>

### Capsule Support & Improved UR5 Kinematics

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                We have added support for capsule geometries to our motion planning service.
                Using this new geometry type, we have also improved our representation of the kinematics of a UR5 arm.
            </td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>
                Assertion Error
            </strong></td>
            <td>We were previously not able to send error messages over webRTC to the python SDK.
            This meant that users would see an unhelpful error "Assertion Error" message.
            Now, we are able to surface those errors so that users have more feedback as they program in Python.</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{< /tabs >}}

## 28 December 2022

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions

- rdk - **v0.2.9**
- api - **v0.1.31**
- slam - **v0.1.13**
- viam-python-sdk - **v0.2.6**
- goutils - **v0.1.6**
- rust-utils - **v0.0.6**

(**Bold=updated version**)

{{% /tab %}}

{{% tab name="New Features" %}}

## New Features

### Custom Modular Resources

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>This new feature allows users to implement their own custom components or component models using our Go SDK.
            We are now working to add support in each of our SDKs so that users can create custom resources in a variety of programming languages.
            Previously, the only way for users to implement custom resources was to use an SDK as a server.
            This meant that a user needed to run a <code>viam-server</code> for their custom component and add it to their main part as a remote.
            With custom modular resources, users no longer need to run separate server instances for each custom resource which saves additional network requests.<br/>

{{< alert title="Important" color="note" >}}
This is a breaking change.
This breaking change affects ALL users who are using the Viam app to configure their robot.
You will need to update to at the latest version of the RDK (V3.0.0) to access your robot using the remote control page.
{{< /alert >}}

</td>
        </tr>
    <tbody>
</table>

### URDF Support

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>Users that are implementing their own arms are now able to supply kinematic information using URDF files.
            This is a convenience for our users since URDF files are readily available for common hardware. </td>
        </tr>
    <tbody>
</table>

### New Movement Sensors

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We added support for two new movement sensors.
            Refer to the <a href="/components/movement-sensor/">Movement Sensor</a> topic for more information.
            <ul>
                <li>ADXL345: A 3 axis accelerometer</li>
                <li>MPU6050: 6 axis accelerometer + gyroscope</li>
            </ul>
            <td>
        </tr>
    <tbody>
</table>
{{% /tab %}}

{{% tab name="Improvements" %}}

## Improvements

### Improved Camera Performance/Reliability

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>
                <ol>
                    <li>Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
                    <strong>The default mime type for color cameras is now JPEG</strong>, which improves the streaming rate across every SDK. </li>
                    <li>Added discoverability when a camera reconnects without changing video paths.
                    This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.</li>
                </ol>
            </td>
        </tr>
    <tbody>
</table>

### Motion Planning with Remote Components

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We made several improvements to the motion service that make it agnostic to the networking topology of a users robot.</td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td>
                <ol>
                    <li>Kinematic information is now transferred over the robot API.
                    This means that the motion service is able to get kinematic information for every component on the robot, regardless of whether it is on a main or remote <code>viam-server</code>.</li>
                    <li>Arms are now an input to the motion service.
                    This means that the motion service can plan for a robot that has an arm component regardless of whether the arm is on a main or remote <code>viam-server</code>.</li>
                </ol>
            </td>
        </tr>
    <tbody>
</table>

### Motion Planning Path Smoothing

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Various small improvements to follow the last major development.</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td><ol><li>Implementation of rudimentary smoothing for RRT* paths, resulting in improvements to path quality, with negligible change to planning performance".</li>
        <li>Changes to plan manager behavior to perform direct interpolation for any solution within some factor of the best score, instead of only in the case where the best IK solution could be interpolated.</li></ol></td>
    </tr>
<tbody>
</table>

### Improved Data Synchronization Reliability

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We updated how captured data is uploaded from robots to app.viam.com</td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td>We previously used bidirectional streaming, with the robot streaming sensor readings to the app and the app streaming acknowledgements of progress back to the robot.
            We switched to a simpler unary approach which is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.<br>

{{< alert title="Important" color="note" >}}
This breaking change will NOT affect most users.
If you have previously captured data on your robot that has not yet been synced, enable syncing to get that data into app.viam before using the new release.
{{< /alert >}}

</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>RDK Shutdown Failure</strong></td>
            <td>Fixed a bug where RDK shutdown requests sometimes failed when connected to serial components. </td>
        </tr>
        <tr>
            <td><strong>Python Documentation</strong></td>
            <td>Fixed issues around documentation rendering improperly in some browsers.</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{< /tabs >}}

## 28 November 2022

{{< tabs >}}
{{% tab name="Versions" %}}

### Release Versions

- rdk - **v0.2.3**
- api - **v0.1.12**
- slam - **v0.1.9**
- viam-python-sdk - v0.2.0
- goutils - v0.1.4
- rust-utils - v0.0.5

(**Bold=updated version**)

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}

### Camera Reconnection Issue

<table style="margin-bottom:18px">
  <tbody style="vertical-align:top;">
      <tr>
          <td width="120px"><strong>What is it?</strong></td>
          <td>When a camera loses connection, it now automatically closes the connection to its video path.
          Previously, when users supplied a video path in their camera configuration, they encountered issues if the camera tried to reconnect because the supplied video path was already being used for the old connection. </td>
      </tr>
      <tr>
          <td><strong>What does it affect?</strong></td>
          <td>On losing their video path connection, cameras now automatically close the video path connection.</td>
      </tr>
  <tbody>
</table>

{{% /tab %}}
{{% tab name="Improvements" %}}

### Improvements

#### Camera Configuration Changes

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We updated the underlying configuration schemes for the following camera models.
            We are also migrating  existing camera configurations to align with the new schemas.
            To learn more about the changes, please refer to our <a href="/components/camera/">camera documentation</a>.
            <ul>
                <li>Webcam</li>
                <li>FFmpeg</li>
                <li>Transform</li>
                <li>Join Pointclouds</li>
            </ul>
    </tbody>
</table>

#### Robot Details Page

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>Based on user feedback, we changed the name of the <strong>CONNECT</strong> tab to <strong>CODE SAMPLE</strong>.</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% /tabs %}}

## 15 November 2022

{{< tabs >}}
{{% tab name="Versions" %}}

### Release Versions

- rdk - v0.2.0
- api - v0.1.7
- slam - v0.1.7
- viam-python-sdk - v0.2.0
- goutils - v0.1.4
- rust-utils - v0.0.5

{{% /tab %}}
{{% tab name="New Features" %}}

### New Features

#### New servo model

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We added a new servo model called <code>GPIO</code>. This represents <emphasis>any</emphasis> servo that is connected directly to <emphasis>any</emphasis> board using GPIO pins. We created this component in response to the common practice of connecting servos to separate hats, such as the <code>PCA9685</code>, rather than connecting directly to the board. Our previous implementation required a direct connection from the servo to the Raspberry Pi.</td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td>While Viam continues to support the <code>pi</code> model of servo, we encourage users to begin using the <code>GPIO</code> model in <emphasis>all<emphasis> of their robots moving forward because it is board-agnostic.</td>
        </tr>
    <tbody>
</table>

#### Added RTT to remote control page

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We added a new badge in the <code>Current Operations</code> card of the remote control page of the Viam app. This badge lists the RTT (round trip time) of a request from your client to the robot (the time to complete one request/response cycle).</td>
        </tr>
    <tbody>
</table>

#### Python 3.8 Support

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>Our Python SDK now supports Python 3.8, in addition to 3.9 and 3.10. You will need to update the Python SDK to access the new feature.</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% tab name="Improvements" %}}

### Improvements

#### New Parameter: extra

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We added a new API method parameter named, <code>extra</code>, that gives users the option of extending existing resource functionality by implementing the new field according to whatever logic they chose.
                <code>extra</code> is available to requests for all methods in the following APIs:<br><br>
                <table style="margin-bottom: 12px;">
                    <tr><td><li>Arm</li>
                    <li>Data Manager</li>
                    <li>Gripper</li>
                    <li>Input Controller</li></td><td><li>Motion</li>
                    <li>Movement Sensor</li>
                    <li>Navigation</li>
                    <li>Pose Tracker</li></td><td><li>Sensor</li>
                    <li>SLAM</li>
                    <li>Vision</li></td></tr>
                </table>
            </td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td>Users of the Go SDK <strong>must</strong> update their code to specify <code>extra</code> in the arguments that pass into each request.

{{% alert title="Important" color="note" %}}
This breaking change does NOT affect users of the Python SDK.
{{% /alert %}}

</td>
        </tr>
    <tbody>
</table>

#### Add dependencies to services

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>Adding dependencies to services allows Viam to initialize and configure resources in the correct order. For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the service.</td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td><strong>Breaking Change</strong>: This impacts users of the SLAM service. Users must now specify which sensors they are using in the <code>depends_on</code> field of the SLAM configuration.
            Other service configurations are not affected.</td>
        </tr>
    <tbody>
</table>

#### Removed width & height fields from Camera API

<table style="margin-bottom:18px">
    <tbody style="vertical-align:top;">
        <tr>
            <td width="120px"><strong>What is it?</strong></td>
            <td>We removed two fields (<code>width</code> and <code>height</code>) that were previously part of the response from the <code>GetImage</code> method in the camera API.</td>
        </tr>
        <tr>
            <td><strong>What does it affect?</strong></td>
            <td><strong>Breaking Change</strong>: This <emphasis>does not<emphasis> impact any existing camera implementations.
            Users writing custom camera API implementations no longer need to implement the <code>width</code> or <code>height</code> fields.</td>
        </tr>
    <tbody>
</table>

{{% /tab %}}
{{% /tabs %}}
