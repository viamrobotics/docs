---
title: "Detect Color with a Webcam"
linkTitle: "Detect Color"
type: "docs"
description: "Detect colors using a webcam and the Viam vision service. Without writing code, you will be able to view your camera stream, with detection bounding boxes."
imageAlt: "camera stream displaying a color detection"
images: ["/tutorials/try-viam-color-detection/detected-example.png"]
tags: ["vision", "detector", "camera", "services"]
resource: "quickstart"
aliases:
  - /tutorials/viam-rover/try-viam-color-detection/
  - /tutorials/try-viam-color-detection/
  - /tutorials/services/try-viam-color-detection/
  - /tutorials/services/basic-color-detection/
authors: ["Hazal Mestci"]
languages: []
viamresources: ["vision", "camera"]
level: "Beginner"
date: "2022-12-16"
updated: "2024-09-03"
cost: "0"
# SMEs: Hazal
---

In this guide you will detect the color red using your computer's webcam and the Viam vision service.
Without writing any code, you will be able to view your camera stream, with detection bounding boxes, from the Viam app control interface.

{{< alert title="You will learn" color="tip" >}}

- How to configure a webcam
- How to use the color detection vision service

{{< /alert >}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
If you have the following components, you can follow along on your own hardware:

- A Linux, macOS or WSL computer that can run `viam-server`.
- A webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer.

{{% expand "No computer or webcam?" %}}
No problem.
Use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components to test with, including a webcam.

Once you have borrowed a rover, go to the **CONFIGURE** tab of the machine, find the cameras and click on the **Test** panel at the bottom of each camera's configuration panel to test the camera stream.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can _perveive_.

If your rover is facing a wall, find the base configuration panel and click on its **Test** panel.
Use the controls to drive your rover to a different location.

Now that you have seen that the cameras on your Try Viam rover work, **continue with Step 4**.

{{< alert title="Tip" color="tip" >}}
Be aware that if you are running out of time during your rental, you can [extend your rover rental](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{% /expand%}}

{{% expand "Have your own rover?" %}}

If you are running this tutorial on [your own Viam Rover](/appendix/try-viam/rover-resources/), make sure you have [configured your rover](/appendix/try-viam/rover-resources/rover-tutorial-fragments/).
Go to the **CONFIGURE** tab of the machine, find the camera and click on the **Test** panel at the bottom of the camera's configuration panel to test the camera stream.

{{% /expand%}}

## Instructions

Follow these instructions to configure your machine and test detecting colors:

{{% expand "Step 1: Create a new machine" %}}

Add a new machine in the [Viam app](https://app.viam.com) by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add Machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll find a variety of tools for working with your machine.

{{% /expand%}}
{{% expand "Step 2: Install viam-server" %}}

Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer, start running it and connect it to the Viam app.
Select the Platform you want to install `viam-server` on.

{{% /expand%}}
{{% expand "Step 3: Configure your webcam" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

Click the **Save** button in the top right corner of the page to save your configuration.
Then click on the **Test** panel at the bottom of the camera's configuration panel to test the camera stream.

If you don't see an image stream, you need to [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{% /expand %}}
{{% expand "Step 4: Configure a color detection vision service" %}}

The [vision service](/services/vision/) enables a robot to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the robot can recognize objects, scan QR codes, perform optical quality inspections, and more.
The `color_detector` model of the vision service is a heuristic-based detector that draws boxes around objects according to their hue.

In this guide, we use the color `#7a4f5c` or `rgb(122, 79, 92)` (a reddish color).

<div style="display: flex;">
<span style="margin-right: 1rem;"><b>Hex color #7a4f5c</b>:</span> {{<imgproc src="/tutorials/try-viam-color-detection/7a4f5c.png" resize="150x" declaredimensions=true alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color.">}}
</div>

{{< tabs >}}
{{% tab name="Builder" %}}

On your machine's **CONFIGURE** tab, add a `vision` **Service** and select the `color detector` model.

In the resulting vision service panel, click the color picker box to set the color to be detected.
For this tutorial, set the color to `rgb(122, 79, 92)` or use hex code `#7a4f5c`.

Then, set **Hue Tolerance** to `0.06` and **Segment size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to a reddish color, the hue tolerance set to 0.06, and the segment size set to 100.](/appendix/try-viam/try-viam/vision-service-config.png)

{{% /tab %}}
{{% tab name="JSON Mode" %}}

On your machine's **CONFIGURE** tab, select **JSON** mode on the **CONFIGURE** tab.
Add the vision service object to the services array in your rover’s JSON configuration:

```json {class="line-numbers linkable-line-numbers" data-line="2-11"}
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

Click the **Save** button in the top right corner of the page to save your vision service configuration.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter.
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under the lighting conditions your machine will be in when in use.

To determine the color value from the camera stream, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

{{% /expand %}}
{{% expand "Step 5: Test color detection" %}}

Now, test your color detection in the **Test** section of the computer vision service's configuration panel or on the **CONTROL** tab.

You will see your camera stream and see detections as labeled boxes on the images along with labels and confidence data:

![Detection of the color rose](/services/vision/rose-detection.png)

If the color is not reliably detected, change the color detectors configuration and increase the **Hue Tolerance** or decrease the segment size.

{{% /expand %}}
{{% expand "(Optional) Step 6: Limit the number of detections" %}}

If you are seeing a lot of detections, adjust the hue tolerance to be smaller or the segment size to be bigger.

Click the **Save** button in the top right corner of the page to save your configuration and close and reopen the **Test** panel of the vision service configuration panel.
You must close and reopen the panel for the new configuration to take effect.

{{% /expand %}}

## Next steps

You can now detect colors on a camera stream.
Of course these detections are not just accessible from the Viam app, but you can also use the [vision service API](/services/vision/#api).

You can also use the vision service with Machine Learning models:

{{< cards >}}
{{% card link="/get-started/detect-people/" %}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{< /cards >}}

To learn about coding with Viam's SDKs, try [making a rover move in a square](/get-started/drive-rover/).

{{< cards >}}
{{% card link="/get-started/drive-rover/" %}}
{{< /cards >}}
