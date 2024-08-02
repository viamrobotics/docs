---
title: "Detect Color with a Webcam"
linkTitle: "Detect Color"
type: "docs"
description: "Use the vision service in the Viam app to detect a color."
imageAlt: "detectionCam stream displaying a color detection"
images: ["/tutorials/try-viam-color-detection/detected-example.png"]
tags: ["vision", "detector", "camera", "services"]
aliases:
  - /tutorials/viam-rover/try-viam-color-detection
  - /tutorials/try-viam-color-detection
  - /tutorials/services/try-viam-color-detection
authors: ["Hazal Mestci"]
languages: []
viamresources: ["vision", "camera"]
level: "Beginner"
date: "2022-12-16"
updated: "2024-05-15"
cost: "0"
no_list: true
# SMEs: Hazal
---

<!-- LEARNING GOALS
After following this tutorial, you will understand how the ML model service and the Vision service work together and you will be able to use both alongside the camera component to make a machine perceive the world around it.  -->

In this tutorial, you will detect the color red using your computer's webcam and the Viam vision service.
Without writing any code, you will be able to view your camera stream, with detection bounding boxes, from the Viam app control interface.

The [vision service](/services/vision/) enables a robot to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the robot can recognize objects, scan QR codes, perform optical quality inspections, sort different colored objects, take measurements, and more.

You can follow this tutorial with your own computer (laptop, desktop, or single-board computer) and webcam, or you can remotely borrow a [Viam rover](https://app.viam.com/try) if your computer is not compatible with [`viam-server`](/installation/).

{{< tabs >}}
{{% tab name="Use your own computer and webcam" %}}

## Connect your computer to the Viam app

In the [Viam app](https://app.viam.com), create a machine and follow the setup instructions on your new machine's page to install `viam-server` on your computer and connect it to the Viam app.

## Configure your webcam

1. If you are using an external USB camera, connect it to your computer.
1. With your computer powered on, check the status indicator on your machine's page in the Viam app.
   It should be green and read "Live."
1. In the **CONFIGURE** tab, click the **+** (create) button in the left side menu and select **Component**.
1. Type "webcam" and select `camera / webcam`.
   Name it `cam` and click **Create**.
1. In the webcam card, click **Show more**, then click the dropdown **video_path** menu.
   Since your machine is live, this auto-populates with all connected webcams.
   Select the camera you want to use.
1. Save the config.

## Test the webcam

1. On the **CONTROL** tab, click the **cam** card to expand it.
1. Click to enable the **View cam** toggle and view your camera's live stream.

{{% /tab %}}
{{% tab name="Use a borrowed Viam rover" %}}

Each [Try Viam rover](https://app.viam.com/try) already has `viam-server` installed and is equipped with a webcam, so Try Viam is a great option if you do not have a macOS or Linux computer and a webcam available.

{{< alert title="Tip" color="tip" >}}
If you are renting a rover, we recommend that you skim through this tutorial before renting your rover to familiarize yourself with the steps so you do not run out of time on your rental.

Be aware that if you are running out of time during your rental, you can [extend your rover rental](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

## Borrow a rover

Borrow a rover free of cost for 10 minutes (with free time extension if no one is waiting) through [Try Viam](https://app.viam.com/try).

## Enable the cameras

Before configuring color detection, enable the rover's camera to get a better sense of what it perceives.

- If you are running this tutorial with a [rented Viam Rover](https://app.viam.com/try), enable both provided cameras: the front-facing camera and the overhead cam.
  In the `viam_base` component panel under the **CONTROL** tab, enable both the `cam` for the front-facing camera and the `overhead-cam:overheadcam` for an overhead view of your rover.

  ![The viam_base component panel showing both the 'cam' and 'overheadcam' camera feeds enabled.](appendix/try-viam/try-viam/enable-both-cameras.png)

  You can also view and control the camera streams from the individual camera component panels on the [**CONTROL** page](/cloud/machines/#control).

- If you are running this tutorial on [your own Viam Rover](/appendix/try-viam/rover-resources/), enable the front facing camera.
  If you are using the `ViamRover` [fragment](/appendix/try-viam/rover-resources/rover-tutorial-fragments/) with your rover, the front facing camera is named `cam` and can be enabled in the `viam_base` component panel under the **CONTROL** tab.

{{% /tab %}}
{{< /tabs >}}

## Add the vision service to detect a color

This tutorial uses the color `#7a4f5c` or `rgb(122, 79, 92)` (a reddish color).

**Hex color #7a4f5c**: {{<imgproc src="/tutorials/try-viam-color-detection/7a4f5c.png" resize="150x" declaredimensions=true alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color.">}}

Navigate to your machine's **CONFIGURE** tab on the [Viam app](https://app.viam.com/robots) and configure your [vision service color detector](/services/vision/#detections):

{{< tabs >}}
{{% tab name="Builder" %}}

1. Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Service**.
1. Select the `vision` type, then select the `color detector` model.
1. Enter `my_color_detector` as the name for your detector and click **Create**.
1. In the resulting vision service panel, click the color picker box to set the color to be detected.
   For this tutorial, set the color to `rgb(122, 79, 92)` or use hex code `#7a4f5c`.
1. Then, set **Hue Tolerance** to `0.06` and **Segment size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to a reddish color, the hue tolerance set to 0.06, and the segment size set to 100.](/appendix/try-viam/try-viam/vision-service-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Select **JSON** mode on the **CONFIGURE** tab.
Add the vision service object to the services array in your rover’s JSON configuration:

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

Click **Save** to save your configuration.

You cannot interact directly with the [vision service](/services/vision/).
To be able to interact with the vision service you must configure a camera component.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter `detect_color`.
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual cam component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

In the following steps you'll be able to test the color detector.
If you notice the color is not reliably detected, drag the **Hue Tolerance** slider to the right or switch to **JSON** mode to increase the `hue_tolerance_pct`.

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

## Test your vision service

You can test your detector by clicking on the **Test** area of the vision service's configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream will show detections with bounding boxes around the detected colors.

![Detection of the color rose](/services/vision/rose-detection.png)

## Next steps

Try changing the detector config to detect other colors.

To do more with the vision service and incorporate machine learning, try [our person detection security robot tutorial](/tutorials/projects/send-security-photo/).

To learn about coding with Viam's SDKs, try [making a rover move in a square](/get-started/drive-rover/).

{{< snippet "social.md" >}}
