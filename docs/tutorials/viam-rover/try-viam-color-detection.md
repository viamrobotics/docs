---
title: "Detect color with a Viam Rover"
linkTitle: "Detect Color"
weight: 41
type: "docs"
description: "Use the Vision Service in the Viam app to detect a color with the Viam Rover."
tags: ["vision", "detector", "camera", "viam rover", "try viam", "services"]
# SMEs: Hazal
---

The [Vision Service](/services/vision) enables a robot to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the robot can recognize objects, scan QR codes, perform optical quality inspections, sort different colored objects, take measurements, and more.

In this tutorial you will learn how to configure a color detector with the Vision Service and how to leverage that detector with a transform camera to detect the color red.

You can follow this tutorial with a [rented Viam Rover](https://app.viam.com/try) or with [your own Viam Rover](/try-viam/rover-resources/).

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), we recommend that you skim through this page before renting your rover.

Be aware that if you are running out of time during your rental, you can [extend your rover rental](/try-viam/try-viam-tutorial/#extending-time) as long as there are no other reservations.
{{< /alert >}}

## Add the Vision Service

Navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **CONFIG** tab, and click on **SERVICES**.
Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `Vision` as the **Type**.
2. Enter `vision` as the **Name**.
3. Click **Create Service**.

<img src="../../img/try-viam-color-detection/create-service.png" alt="The Viam app's Create Service tab lists the type as vision and name as vision, with a Create Service button.">

## Detect a color

This tutorial allow uses the hex color #7a4f5c (a reddish color).

**Hex color #7a4f5c**: <img src="../../img/try-viam-color-detection/7a4f5c.png" alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color." >

Copy the following configuration, into the attributes of your rover’s Vision Service:

```json-viam
{
 "register_models": [
   {
     "type": "color_detector",
     "parameters": {
       "detect_color": "#7a4f5c",
       "hue_tolerance_pct": 0.06,
       "segment_size_px": 100
     },
     "name": "my_color_detector"
   }
 ]
}
```

<img src="../../img/try-viam-color-detection/populated-service-attributes.png" width="700px" alt="Screenshot from the Viam app showing the Vision service panel. The panel has an Attributes panel populated with Vision Service attributes. On the upper right side there is a trash bin icon.">

The configuration adds a `model` of `type` `color_detector` with the color as a parameter.
The `color_detector` is a heuristic-based detector that draws boxes around objects according to their hue.

Click **SAVE CONFIG** and head to the **COMPONENTS** tab.

You cannot interact directly with the [Vision Service](/services/vision/).
To be able to interact with the Vision Service you must configure a camera component to wrap the service.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter `detect_color`.
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual cam component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

If the color is not reliably detected, increase the `hue_tolerance_pct`.

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

## Configure a transform camera to use the color detector

Viam [camera](/components/camera/) components can be [physical](/components/camera/#webcam) like the one already configured on the rover, or virtual.
A virtual camera transforms the output from a physical camera.

To use the color detector, you need to configure a [transform camera](/components/camera/#transform).

Navigate to the Scroll down to the **COMPONENTS** tab in the Viam app and scroll to the **Create Component** section.
To create a [transform camera](/components/camera/#transform):

1. Enter a name for **Name**, for example `detectionCam`.
2. Select `camera` as the **Type**.
3. Select `transform` as the **Model**.
4. Click **Create Component**.

![The Viam app showing the Create Component panel populated with a cam component. The name is detectionCam, the type is camera, and the model is transform.](../../img/try-viam-color-detection/create-component-pane.png)

Viam generates an empty **Attributes** section for the detectionCam's component panel.
The panel's **Attribute Guide** section displays the available attributes for the selected component.

{{% alert title="Tip" color="tip" %}}
Attribute Guides always prefix required attributes with an asterisk.
{{% /alert %}}

![The Viam app showing the detectionCam component section. The Attributes section contains a skeleton configuration, including source, pipeline, type, and attributes. The Attributes Guide section lists the available camera component attributes. There are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon.](../../img/try-viam-color-detection/empty-detectioncam-component-panel.png)

Copy the following JSON configuration into the Attributes section:

```json-viam
{
 "source": "cam",
 "pipeline": [
   {
     "attributes": {
       "detector_name": "my_color_detector",
       "confidence_threshold": 0.3
     },
     "type": "detections"
   }
 ]
}
```

- `source` is the name of the physical camera on the rover, which is the camera you want to get the detections from.
  By default, the camera's name is `cam`.
- In `attributes`
  - The `detector_name` is the name of your detector.
    If you copied the one from above, the name is `my_color_detector`.
  - The `confidence_threshold` is 0.3 which means a color is detected if the detection service is at least 30% confident of the color.
- The `type` is `detections`.

![The Viam app showing the detectionCam component section. It contains the Attributes section with a skeleton configuration, including source, pipeline, type, and attributes. The panel has an Attributes section populated with transform camera component attributes. The are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon.](../../img/try-viam-color-detection/detectioncam-component-panel.png)

After adding the component and its attributes, click **SAVE CONFIG**.

## Test your transform camera in the control tab

In the **CONTROL** tab, click on your base component and add the detection camera from the **Select Cameras** drop down.
If you have configured the component and service correctly, you see the `detectionCam`.
Select it.
Next, enable the keyboard and move your rover around until your camera detects the configured color.
Each time your camera detects the color, you will see a red rectangle around the color labeled with the detection confidence level.

![Base component panel displaying an example color detection.](../../img/try-viam-color-detection/detected-example.png)

If you scroll down in the **CONTROL** tab, you can also click on the detectionCam's own section to view its stream there.

![The Viam app showing the detectionCam component panel. The Refresh Frequency selector is set to live, and the Export Frequency button is beside it. The detectionCam stream is visible and displays a red square surrounded by a red a color detection box labeled Rose:1.00."](../../img/try-viam-color-detection/detectioncam-comp-stream.png)

## Next Steps

If you're ready for more, try making your rover detect other colors.
You could also write some code with a Viam SDK to [make your Viam Rover move in a square](/tutorials/viam-rover/try-viam-sdk/).

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure to head over to the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
