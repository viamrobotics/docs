---
title: "Try Viam: Detect a Color with your Viam Rover using the Vision Service"
linkTitle: "Try Viam: Color Detection"
weight: 41
type: "docs"
description: "Instructions for using the Vision Service in the Viam app to detect a color with the Viam Rover."
# SMEs: Hazal
---

## Introduction

This tutorial will guide you through using a [Try Viam](https://app.viam.com/try) Rover rental to detect the color red by adding a color detector to Viam's [vision service](/services/vision/). 
The only prerequisite is you need to have an active reservation for one of Viam's rental rovers.
We already added different colors around the rink on each wall.  

But why should I use this service, one might ask? 
The vision service enables the robot to use its on-board cameras to see and interpret the world around it. 
The service also grants you the ease of creating different types of detectors, which allows you to then leverage them to program your robots to do interesting things. 
We can recognize objects, scan QR codes, perform optical quality inspections, sort different colored objects, take measurements, etc. The opportunities are endless. 

Now let’s dive in. 

## Adding the vision service

Let’s start with adding the vision service to your rover.
In Viam App, head to the **CONFIG** tab, and click on **SERVICES**. 
Scroll down to the **Create Service** section. 

1. Enter “vision” in **Type** from the drop-down. 
2. Enter “vision” in **Name**.
3. Click **Create Service**.

{{< figure src="../img/try-viam-color-detection/create-service.png" width="400px" alt="Screenshot from the Viam app's Create Service tab. It lists the type as “vision” and name as “vision”, with a Create Service button on the right." title="Create Service pane from CONFIG -> SERVICES" >}}

Clicking **Create Service** automatically creates a new service for your rover, but that does not set any attributes for the service. 

{{< figure src="../img/try-viam-color-detection/vision-service-tab.png" width="700px" alt="Screenshot from the Viam app showing the Vision service panel. The panel has an empty “Attributes” section with an empty line numbered, 1. On the upper right side there is a trash bin icon." title="Vision service panel displaying an empty Attributes section." >}}

Copy the following configuration into the attributes of your rover’s vision service. 

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

After adding the detector configuration, the vision service panel should look like this:

{{< figure src="../img/try-viam-color-detection/populated-service-attributes.png" width="700px" alt="Screenshot from the Viam app showing the Vision service panel. The panel has an Attributes panel populated with vision service attributes. On the upper right side there is a trash bin icon." title="Vision service tab displaying a populated Attributes Panel." >}}

This configuration creates a detector that will find the hex color #7a4f5c (a reddish color) when you use it with images from your robot’s cameras.
You can change the color to your liking and experiment with it. 
You can also play with the `hue_tolerance_pct` value to detect this color with more or less precision.

**Hex color #7a4f5c**: <img src="../img/try-viam-color-detection/7a4f5c.png" alt="A color swatch for the color that you will be detecting with your color detector. It's a reddish, maroon color." >

The `color_detector` we use is a heuristic-based detector that draws boxes around objects according to their hue (note that the detector does not detect black, perfect greys[^pg], or white).

[^pg]:"Perfect shades of grey" are those greys where the red, green, and blue color component values are equal, i.e., R=G=B. For example, in hex: #A3A3A3; in RGB: 128, 128, 128.

To learn more, head to our [Vision Service](/services/vision/) topic (ht<span></span>tps://docs.viam.com/services/vision/) for additional information on how to configure and use Viam's Vision Service.
Now, click **SAVE CONFIG** and head to the **COMPONENTS** tab.

## How to configure a transform camera to use the color detector

{{% alert title="Tip" color="tip" %}}
Object colors can vary dramatically based on the light source.
In your own projects, or if you decide to pick another color to detect, verify the desired color detection value under actual lighting conditions.
For example, by using a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia), to determine the color value from the actual cam component image.
{{% /alert %}}

After adding the vision service and color detector, we’ll add a new [camera](/components/camera/) to our Viam Rover. 
Viam camera components can be [physical](/components/camera/#webcam) (like that already configured on the rover), or virtual (such as the [transform camera](/components/camera/#transform), which transforms the output from the physical camera). 
To display the detections, we will use the transform camera. 

To learn more about the camera component, head to the [Camera component](/components/camera/) topic. 

Scroll down to see the **Create Component** section in **COMPONENTS** tab of the Viam app. 

1. Enter the desired name in **Name**. We named ours, “detectionCam”.
2. Enter “camera” in **Type**. 
3. Enter “transform” in **Model**.
4. Click **Create Component**.

{{< figure src="../img/try-viam-color-detection/create-component-pane.png" width="600px" alt="Screenshot from the Viam app showing the Create Component panel populated with a cam component. The name is detectionCam, the type is camera, and the model is transform. The Create Component button is on the right." title="Create Component panel populated with a camera component." >}}

After creating the component, Viam automatically generates an empty **Attributes** section for the detectionCam's component panel. 
The panel's **Attribute Guide** section displays the available attributes for the selected component. 

{{< figure src="../img/try-viam-color-detection/empty-detectioncam-component-panel.png" width="700px" alt="Screenshot from the Viam app showing the detectionCam component section. The “Attributes” section contains a skeleton configuration, including source, pipeline, type, and attributes. The Attributes Guide section lists the available camera component attributes. There are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon." title="An unpopulated Create Component panel for a camera component." >}}

{{% alert title="Note" color="note" %}}
Attribute Guides always prefix required attributes with an asterisk.
{{% /alert %}}

`source` is the name of the physical camera on the rover, which is the camera you want to get the detections from. 
The camera's name in the config is “cam”, so we will use that. 
The `Type` will be “detections”. 
In **Attributes**, you must add a `detector_name`. 
We named ours “my_color_detector”.
Next, you must add the `confidence_threshold`. 
We picked 0.3 which means if the detection service is 30% confident of the color, it will detect it. 

{{< figure src="../img/try-viam-color-detection/detectioncam-component-panel.png" width="700px" alt="Screenshot from the Viam app showing the detectionCam component section. It contains the “Attributes” section with a skeleton configuration, including source, pipeline, type, and attributes. The panel has an Attributes section populated with transform camera component attributes. The are buttons labeled Data Capture Configuration, and Frame, and a drop-down labeled, Depends On. On the upper right there is a trash bin icon." title="The detectionCam component displayed on the Camera Component Panel." >}}

JSON configuration is here if you wish to copy paste it into your Viam rover's config:

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

After adding the component and its attributes, click **SAVE CONFIG** and head to the **CONTROL** tab.

## Testing your transform camera with the vision service in the control tab 

In the **CONTROL** tab, toggle your base component and add the detection camera from **Select Cameras** drop down. 
detectionCam should be available if you have configured your component and service correctly. 
When you enable the keyboard, you will be able to move the rover and see how your detection works. 
Each time your camera sees the color, it will draw a red rectangle around it labeled with the detection confidence level. 

{{< figure src="../img/try-viam-color-detection/detected-example.png" width="700px" alt="." title="Base component panel displaying an example color detection.sss" >}}

We recommend that you test the functionality of Viam's vision services and cameras by enabling your other camera, cam, to compare its view with the detection camera's view. 

{{< figure src="../img/try-viam-color-detection/both-cams.png" width="700px" alt="Screenshot from the Viam app showing the base component panel with the keyboard buttons W, A, S, D. The Keyboard enabled button is green (enabled). The cam stream is on the right, with the detectionCam stream displayed below it. The displays have identical views. The detectionCam stream displays an overlay of a red color detection box with the label,“rose:1.00” surrounding the red square." title="Base component panel displaying the cam and detectionCam streams for comparison." >}}

If you scroll down in the  **CONTROL** tab, you will see the detectionCam's own section. You can also view its stream there.

{{< figure src="../img/try-viam-color-detection/detectioncam-comp-stream.png" width="600px" alt="Screenshot from the Viam app showing the detectionCam component panel. The Hide Camera button is green. The Refresh Frequency selector is set to live, and the Export Frequency button is beside it on the right. The detectionCam stream is visible and displays a red square surrounded by a red a color detection box labeled Rose:1.00." title="detectionCam stream displaying a color detection." >}}
## Summary

Congratulations! 
If you followed along, you have successfully used Viam to make your rental rover detect the color red in the rental rink. 
You have learned how to configure a color detector with the vision service, and how to leverage that detector with a transform camera.

If you are ready to continue tinkering with your rental rover, head to our ["How to use the Viam SDK to control your Viam Rover" tutorial](/tutorials/try-viam-sdk/) ([https://docs.viam.com/tutorials/try-viam-sdk/](/tutorials/try-viam-sdk/)). 
In that tutorial, we will introduce you to the Viam SDK (software development kit) so that you can write code in either Python or Golang to make your Viam Rover move in a square. 

If you want to connect with other developers learning how to build robots or if you have any issues whatsoever during Try Viam experience, let us know on the [Viam Community Slack](http://viamrobotics.slack.com/), and we will be happy to help you get up and running.
