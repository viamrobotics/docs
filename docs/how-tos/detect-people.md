---
title: "Detect objects in a camera stream"
linkTitle: "Detect objects or people"
type: "docs"
tags: ["vision", "data", "services", "quickstart", "ml", "camera", "webcam"]
no_list: true
description: "Detect people and their location in an image with any webcam and a vision service."
images: ["/get-started/quickstarts/vision-card.png"]
imageAlt: "Person detected in camera stream"
authors: []
weight: 30
no_list: true
cost: "0"
resource: "quickstart"
aliases:
  - /get-started/quickstarts/detect-people/
  - /get-started/detect-people/
languages: []
viamresources: ["camera", "mlmodel", "vision"]
platformarea: ["ml"]
level: "Beginner"
date: "2024-07-31"
updated: "2024-10-20"
cost: "0"
---

WebRTC is a powerful technology that allows developers to build apps with video streams.
Like an app that provides you a live stream of your house's security cameras.

Adding Computer Vision allows machines to analyze images and gain meaningful information from video streams.
You can then program the machines to act based on this data, for example by alerting you when people appear on your camera stream.

In this guide you'll use a publicly available machine learning model to detect people on a camera stream.

{{< alert title="You will learn" color="tip" >}}

- How to create a machine and install `viam-server`
- How to configure a webcam
- How to deploy a machine learning model
- How to use the machine learning model with a vision service

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/P6sZPIMnhBU">}}

## Requirements

You don't need to buy or own any hardware to follow along.
If you have the following components, you can follow along on your own hardware:

- A Linux or macOS that can run `viam-server`.
- A webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer.

{{% expand "No computer or webcam?" %}}
No problem. Use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components to test with, including a webcam.
You may not be able to test using the supplied ML model, as your borrowed rover will generally not be able to see people.
We recommend you follow the [Detect color with a Webcam](/how-tos/detect-color/) guide instead.

Once you have borrowed a rover, go to the **CONFIGURE** tab of the machine, find the cameras and click on the **Test** panel at the bottom of each camera's configuration panel to test the camera stream.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can _perceive_.

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
Then you can add the ML model service to deploy and run the machine learning model that can detect people and the vision service that applies the model to your camera's live feed.

{{%expand "Step 1: Create a new machine" %}}

Go to the [Viam app](https://app.viam.com) and add a new machine by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll be able to connect, configure, and control your machine.

{{% /expand%}}
{{%expand "Step 2: Install viam-server" %}}

Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer, start running it and connect it to the Viam app.
Select the Platform you want to install `viam-server` on.

{{% /expand%}}
{{%expand "Step 3: Configure your webcam" %}}

First, make sure to connect your webcam to your machine if it's not already connected (like with an inbuilt laptop webcam).

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

Click the **Save** button in the top right corner of the page to save your configuration.
Then click on the **Test** panel at the bottom of the camera's configuration panel to test the camera stream.

If you don't see an image stream, use the video path dropdown to select your camera path.

For more detailed configuration information and troubleshooting, see the [`webcam` docs](/components/camera/webcam/).

{{% /expand%}}
{{%expand "Step 4: Deploy a person detection model" %}}

In this guide you'll use a publicly available model to detect people.
You will deploy this model to your machine using the ML model service.

Click **+**, click **Service** and select the `ML model` type, then select the `TFLite CPU` model.
Create the service.

In the resulting ML model service configuration pane, ensure that **Deploy model on machine** is selected for the **Deployment** field.

Then click on **Select model**, switch to the **Registry** tab and select the **people** model by **ml-models-scuttle** to deploy a model that has been trained to be able to detect people.
This model is a TFLite model.

For more detailed information, including optional attribute configuration, see the [`tflite_cpu` docs](/services/ml/tflite_cpu/).

{{% /expand%}}
{{%expand "Step 5: Configure a vision service" %}}

The ML model service runs the person detection model on your machine.
To use the deployed model to detect people on a camera stream, you need to additionally configure a vision service.
This service applies the ML model to the camera input stream.

Add a `vision` **Service** and select the `ML model` model.

Select the ML model service your person detector model is deployed with (which you created in step 4) from the **ML Model** dropdown.

{{% /expand%}}
{{%expand "Step 6: Test person detection" %}}

Click the **Save** button in the top right corner of the page to save your configuration.

Now, test your person detection in the **Test** section of the computer vision service's configuration panel or on the **CONTROL** tab.

You will see your camera stream and see detections as labeled boxes on the images along with labels and confidence data.
Detections with the label `Person` and a high confidence score show positive person detections, but the ML model can also detect other objects:

{{<imgproc src="/get-started/quickstarts/vision-card-more-detections.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card with a lower default minimum confidence threshold." class="imgzoom">}}

{{% /expand%}}
{{%expand "(Optional) Step 7: Limit the number of detections" %}}

If you are seeing a lot of detections, you can set a minimum confidence threshold.

On the configuration page of the vision service in the top right corner, click **{}** (Switch to advanced).
Add the following line to the JSON configuration to set the `default_minimum_confidence` of the detector:

```json
"default_minimum_confidence": 0.82
```

The full configuration for the attributes of the vision service should resemble:

```json {class="line-numbers linkable-line-numbers" data-line="3"}
{
  "mlmodel_name": "mlmodel-1",
  "default_minimum_confidence": 0.82
}
```

This optional attribute reduces your detections output by filtering out detections below the threshold of 82% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration and close and reopen the **Test** panel of the vision service configuration panel.
Now if you view detections, you will only see detections with a confidence value higher than the `"default_minimum_confidence"` attribute.

{{<imgproc src="/get-started/quickstarts/vision-card.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card." >}}

{{% /expand%}}

## Next steps

You can now detect people or other objects on a camera stream using any device and any webcam.
If you need a model to detect objects specific to your use case, you can use the Viam platform to train your own models or upload externally-trained models:

{{< cards >}}
{{% card link="/appendix/apis/services/vision/" customTitle="Vision Service API" %}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
