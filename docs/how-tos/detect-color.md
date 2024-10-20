---
title: "Detect color with a webcam"
linkTitle: "Detect Color"
type: "docs"
description: "Detect colors and their location in an image with any webcam and a vision service."
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
platformarea: ["ml"]
level: "Beginner"
date: "2022-12-16"
updated: "2024-10-20"
cost: "0"
---

WebRTC is a powerful technology that allows developers to build apps with video streams.
Adding computer vision allows machines to analyze images and gain meaningful information from video streams.
You can then program the machines to act based on this data, for example by alerting you.

Imagine a factory's storage unit.
To know what to restock, there are cameras, so someone can view the camera feeds to see stock levels rather than having to check in person.

Computer vision let's us do even better.
The factory adds red paint to the walls of the factory at level where they need to restock.
Now, a computer can monitor the live stream of the stock levels and as soon as the red color becomes visible, it can alert a supervisor.

This guide will show you how to use any webcam alongside a computer to detect the color red with the vision service.

{{< alert title="You will learn" color="tip" >}}

- How to create a machine and install `viam-server`
- How to configure a webcam
- How to use the color detection vision service

{{< /alert >}}

## Requirements

You don't need to buy or own any hardware to follow along.
If you have the following components, you can follow along on your own hardware:

- A Linux or macOS computer that can run `viam-server`.
- A webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer.

{{% expand "No computer or webcam?" %}}
No problem.
Use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components to test with, including a webcam.

Once you have borrowed a rover, go to the **CONFIGURE** tab of the machine, find the cameras and click on the **Test** panel at the bottom of each camera's configuration panel to test the camera stream.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can perceive.

If your rover is facing a wall, find the base configuration panel and click on its **Test** panel.
Use the controls to drive your rover to a different location.
You can use picture in picture mode on one of the cameras so you can see where you're driving.

Now that you have seen that the cameras on your Try Viam rover work, **continue with Step 4**.

{{< alert title="Tip" color="tip" >}}
Be aware that if you are running out of time during your rental, you can [extend your rover rental](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{% /expand%}}

## Instructions

To use Viam with your device, you must install Viam and create a configuration that describes the connected camera.
Then you can add the vision service to detect colors from your camera's live feed.

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

First, make sure to connect your webcam to your machine if it's not already connected (like with an inbuilt laptop webcam).

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

Click the **Save** button in the top right corner of the page to save your configuration.
Then click on the **Test** panel at the bottom of the camera's configuration panel to test the camera stream.

If you don't see an image stream, use the video path dropdown to select your camera path.

For more detailed configuration information and troubleshooting, see the [`webcam` docs](/components/camera/webcam/).

{{% /expand %}}
{{% expand "Step 4: Configure a color detection vision service" %}}

The vision service enables a machine to use its cameras to see and interpret the world around it.
The service also allows you to create different types of detectors with which the machine can recognize objects, scan QR codes, perform optical quality inspections, and more.
The `color_detector` model of the vision service is a heuristic-based detector that detects colors and their location within an image.

In this guide, we use the color `#7a4f5c` or `rgb(122, 79, 92)` (a reddish color).

<div style="display: flex;">
<span style="margin-right: 1rem;"><b>Hex color #7a4f5c</b>:</span> {{<imgproc src="/tutorials/try-viam-color-detection/7a4f5c.png" resize="150x" declaredimensions=true alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color.">}}
</div>

{{< tabs >}}
{{% tab name="Builder" %}}

On your machine's **CONFIGURE** tab, add a `vision` service and select the `color detector` model.

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

{{% /expand %}}
{{% expand "Step 5: Test color detection" %}}

Click the **Save** button in the top right corner of the page to save your vision service configuration.

Now, test your color detection in the **Test** section of the computer vision service's configuration panel.

You will see your camera stream and see detections as labeled boxes on the images along with labels and confidence data:

![Detection of the color rose](/services/vision/rose-detection.png)

If the color is not reliably detected, change the color detector's configuration.
Increase the **Hue Tolerance** or decrease the segment size.

{{< alert title="Colors can vary based on lighting" color="tip" >}}
We recommend you verify the desired color detection value under the lighting conditions your machine will be in when in use.

To determine a color value from the camera stream, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

{{% /expand %}}
{{% expand "(Optional) Step 6: Limit the number of detections" %}}

If you are seeing a lot of detections, adjust the hue tolerance to be smaller or the segment size to be bigger.

Click the **Save** button in the top right corner of the page to save your configuration and close and reopen the **Test** panel of the vision service configuration panel.
You must close and reopen the panel for the new configuration to take effect.

{{% /expand %}}

## Next steps

You can now detect colors on a camera stream using any device and any webcam.
You can also use the vision service with more sophisticated Machine Learning models.
To learn more about how to access the data from a vision service programmatically or use machine learning models with a vision service, see:

{{< cards >}}
{{% card link="/appendix/apis/services/vision/" customTitle="Vision Service API" %}}
{{% card link="/how-tos/detect-people/" %}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
