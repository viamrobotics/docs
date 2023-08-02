---
title: "Detect color with a Viam Rover"
linkTitle: "Detect Color"
weight: 41
type: "docs"
description: "Use the Vision Service in the Viam app to detect a color with the Viam Rover."
image: "/tutorials/try-viam-color-detection/detectioncam-comp-stream.png"
imageAlt: "detectionCam stream displaying a color detection"
images: ["/tutorials/try-viam-color-detection/detectioncam-comp-stream.png"]
tags: ["vision", "detector", "camera", "viam rover", "try viam", "services"]
aliases:
    - /tutorials/viam-rover/try-viam-color-detection
    - /tutorials/try-viam-color-detection
authors: [ "Hazal Mestci" ]
languages: []
viamresources: [ "vision", "camera" ]
level: "Beginner"
date: "16 December 2022"
cost: "0"
# SMEs: Hazal
---

The [Vision Service](/services/vision/) enables a robot to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the robot can recognize objects, scan QR codes, perform optical quality inspections, sort different colored objects, take measurements, and more.

In this tutorial you will learn how to configure a color detector with the Vision Service and how to leverage that detector with a transform camera to detect the color red.

You can follow this tutorial with a [rented Viam Rover](https://app.viam.com/try) or with [your own Viam Rover](/try-viam/rover-resources/).

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), we recommend that you skim through this page before renting your rover.

Be aware that if you are running out of time during your rental, you can [extend your rover rental](/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

## Add the Vision Service to detect a color

This tutorial uses the hex color #7a4f5c (a reddish color).

**Hex color #7a4f5c**: {{<imgproc src="/tutorials/try-viam-color-detection/7a4f5c.png" resize="300x" declaredimensions=true alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color.">}}

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter `my_color_detector` as the **Name**.
3. Select **Color Detector** as the **Model**.
4. Click **Create Service**.

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
      "segment_size_px": 100,
      "detect_color": "#7a4f5c",
      "hue_tolerance_pct": 0.06
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the Vision Service object to the services array in your rover’s raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "my_color_detector",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#7a4f5c",
      "hue_tolerance_pct": 0.06
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{< /tabs >}}

The configuration adds a `model` of `type` `color_detector` with the color as a parameter.
The `color_detector` is a heuristic-based detector that draws boxes around objects according to their hue.

Click **Save config** and head to the **Components** tab.

You cannot interact directly with the [Vision Service](/services/vision/).
To be able to interact with the Vision Service you must configure a camera component.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter `detect_color`.
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual cam component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

If the color is not reliably detected, increase the `hue_tolerance_pct`.

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

## Configure a transform camera to use the color detector

Viam [camera](/components/camera/) components can be [physical](/components/camera/webcam/) like the one already configured on the rover, or virtual.
A virtual camera transforms the output from a physical camera.

To view output from the color detector overlaid on images from a physical camera, you need to configure a [transform camera](/components/camera/transform/).

Navigate to the **Components** tab in the Viam app and scroll to the **Create Component** section.
To create a [transform camera](/components/camera/transform/):

1. Enter a name for **Name**, for example `detectionCam`.
2. Select `camera` as the **Type**.
3. Select `transform` as the **Model**.
4. Click **Create Component**.

![The Viam app showing the Create Component panel populated with a camera component. The name is detectionCam, the type is camera, and the model is transform.](/tutorials/try-viam-color-detection/create-component-pane.png)

Viam generates an empty **Attributes** section for the detection camera's component panel.
The panel's **Attribute Guide** section displays the available attributes for the selected component.

{{% alert title="Tip" color="tip" %}}
Attribute Guides always prefix required attributes with an asterisk.
{{% /alert %}}

![The Viam app showing the detectionCam component section. The Attributes section contains a skeleton configuration, including source, pipeline, type, and attributes. The Attributes Guide section lists the available camera component attributes. There are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon.](/tutorials/try-viam-color-detection/empty-detectioncam-component-panel.png)

Copy the following JSON configuration into the Attributes section:

```json {class="line-numbers linkable-line-numbers"}
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

| Field | Default value | Description |
| ----- | ------------- | ----------- |
| `source` | `cam` | The name of the physical camera on the rover, which provides the visual feed to get detections from. |
| `attributes` | | The attributes of this detectionCam. |
| `attributes.detector_name` | `my_color_detector` | The name of this detectionCam. |
| `attributes.confidence_threshold` | `0.3` (30%) | The percentage of confidence in the color being present the detection service needs to detect a color. |
| `type` | `detections` | The type of the component. |

![The Viam app showing the detectionCam component section. It contains the Attributes section with a skeleton configuration, including source, pipeline, type, and attributes. The panel has an Attributes section populated with transform camera component attributes. The are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon.](/tutorials/try-viam-color-detection/detectioncam-component-panel.png)

After adding the component and its attributes, click **Save config**.

## Test your transform camera in the CONTROL tab

In the **Control** tab, click on your base component and add the detection camera from the **Select Cameras** drop down.

Next, enable the keyboard and move your rover around until your camera detects the configured color.
Each time the camera detects the color, you will see a red rectangle around the color labeled with the detection confidence level.

![Base component panel displaying an example color detection.](/tutorials/try-viam-color-detection/detected-example.png)

If you scroll down in the **Control** tab, you can also click on the detectionCam's own section to view its stream there.

## Next Steps

If you're ready for more, try making your rover detect other colors.
You could also write some code with a Viam SDK to [make your Viam Rover move in a square](/tutorials/get-started/try-viam-sdk/).

{{< snippet "social.md" >}}
