---
title: "Detect color with a Viam Rover"
linkTitle: "Detect Color"
type: "docs"
description: "Use the vision service in the Viam app to detect a color with the Viam Rover."
imageAlt: "detectionCam stream displaying a color detection"
images: ["/tutorials/try-viam-color-detection/detectioncam-comp-stream.png"]
tags: ["vision", "detector", "camera", "viam rover", "try viam", "services"]
aliases:
  - /tutorials/viam-rover/try-viam-color-detection
  - /tutorials/try-viam-color-detection
authors: ["Hazal Mestci"]
languages: []
viamresources: ["vision", "camera"]
level: "Beginner"
date: "2022-12-16"
# updated: ""
cost: "0"
no_list: true
# SMEs: Hazal
---

In this tutorial you will learn how to configure a color detector with the vision service and leverage that detector with a [transform camera](/components/camera/transform/) to detect the color red.

The [vision service](/ml/vision/) enables a robot to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the robot can recognize objects, scan QR codes, perform optical quality inspections, sort different colored objects, take measurements, and more.

You can follow this tutorial with a [rented Viam Rover](https://app.viam.com/try) or with [your own Viam Rover](/get-started/try-viam/rover-resources/).

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), we recommend that you skim through this page before renting your rover.

Be aware that if you are running out of time during your rental, you can [extend your rover rental](/get-started/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

## Enable the cameras

Before configuring color detection, enable the rover's camera to get a better sense of what it perceives.

- If you are running this tutorial with a [rented Viam Rover](https://app.viam.com/try), enable both provided cameras: the front-facing camera and the overhead cam.
  In the `viam_base` component panel under the **Control** tab, enable both the `cam` for the front-facing camera and the `overhead-cam:overheadcam` for an overhead view of your rover.

  ![The viam_base component panel showing both the 'cam' and 'overheadcam' camera feeds enabled.](get-started/try-viam/try-viam/enable-both-cameras.png)

  You can also view and control the camera streams from the [individual camera component panels](/get-started/try-viam/try-viam-tutorial/#camera-control).

- If you are running this tutorial on [your own Viam Rover](/get-started/try-viam/rover-resources/), enable the front facing camera.
  If you are using the `ViamRover` [fragment](/get-started/try-viam/rover-resources/rover-tutorial-fragments/) with your rover, the front facing camera is named `cam` and can be enabled in the `viam_base` component panel under the **Control** tab.

## Add the vision service to detect a color

This tutorial uses the color `#7a4f5c` or `rgb(122, 79, 92)` (a reddish color).

**Hex color #7a4f5c**: {{<imgproc src="/tutorials/try-viam-color-detection/7a4f5c.png" resize="150x" declaredimensions=true alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color.">}}

Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/robots) and configure your [vision service color detector](/ml/vision/#detections):

{{< tabs >}}
{{% tab name="Builder" %}}

1. Click the **Services** subtab and click **Create service** in the lower-left corner.

1. Select the `Vision` type, then select the `Color Detector` model.

1. Enter `my_color_detector` as the name for your detector and click **Create**.

1. In the resulting vision service panel, click the color picker box to set the color to be detected.
   For this tutorial, set the color to `rgb(122, 79, 92)` or use hex code `#7a4f5c`.

1. Then, set **Hue Tolerance** to `0.06` and **Segment Size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to a reddish color, the hue tolerance set to 0.06, and the segment size set to 100.](/get-started/try-viam/try-viam/vision-service-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
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

The `color_detector` is a heuristic-based detector that draws boxes around objects according to their hue.

Click **Save config** and head to the **Components** tab.

You cannot interact directly with the [vision service](/ml/vision/).
To be able to interact with the vision service you must configure a camera component.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter `detect_color`.
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual cam component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

If the color is not reliably detected, drag the **Hue Tolerance** slider to the right or navigate to the **Raw JSON** tab to increase the `hue_tolerance_pct`.

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

## Configure a transform camera to use the color detector

Viam [camera](/components/camera/) components can be physical like the one already configured on the rover, or virtual.
A virtual [_transform camera_](/components/camera/transform/) transforms the output from a physical camera.

To view output from the color detector overlaid on images from a physical camera, configure a transform camera:

1. Navigate to the **Config** tab in the Viam app and click the **Components** subtab.
2. Click **Create component** in the lower-left corner of the page.
3. Select `camera` as the type.
4. Select `transform` as the model.
5. Enter a name, for example `detectionCam`, and click **Create**.

{{<imgproc src="/tutorials/try-viam-color-detection/create-transform-camera.png" resize="500x" declaredimensions=true alt="The Viam app showing the Create Component panel populated with a camera component. The name is detectionCam, the type is camera, and the model is transform.">}}

Viam generates an **Attributes** section for the detection camera's component panel:

![The Viam app showing the detectionCam component section. The Attributes section contains a skeleton configuration, including source, pipeline, type, and attributes. On the upper right there is a trash bin icon.](/tutorials/try-viam-color-detection/transform-camera-config.png)

Copy the following JSON configuration into the **Attributes** section:

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

Explanations of each attribute are as follows:

- `source`: The name of the physical camera on the rover, which provides the visual feed to get detections from.
- `pipeline`: Contains the transformation objects to apply to the camera.
- `attributes`: The attributes of this transform camera.
  - `detector_name`: The name of the detector.
  - `confidence_threshold`: The percentage of confidence needed by the detection service to identify a color.
    Since we set it to `0.3`, this means that detections with less than 30% confidence won't be recognized.
  - `type`: The type of transform camera.

The filled-in transform camera configuration panel will look like this:

![The Viam app showing the detectionCam component section. The Attributes section contains a skeleton configuration, including source, pipeline, type, and attributes. On the upper right there is a trash bin icon.](/tutorials/try-viam-color-detection/transform-camera-attributes.png)

After adding the component and its attributes, click **Save config**.

## Test your transform camera in the Control tab

In the **Control** tab, click on your base component and enable the detection camera in the **Live Feeds** section.

Next, enable the keyboard and move your rover around until your camera detects the specified color.

Each time the camera detects the color, you will see a red rectangle around the color labeled with the detection confidence level.

![Base component panel displaying an example color detection.](/tutorials/try-viam-color-detection/detected-example.png)

Scroll down in the **Control** tab and select the dedicated section for detectionCam to access its live stream.

## Next steps

If you're ready for more, try making your rover detect other colors.
You could also write some code with a Viam SDK to [make your Viam Rover move in a square](/tutorials/get-started/try-viam-sdk/).

{{< snippet "social.md" >}}
