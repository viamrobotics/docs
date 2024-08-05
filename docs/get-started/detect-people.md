---
title: "Detect People with a Webcam in 4 minutes"
linkTitle: "Detect people (4 min)"
type: "docs"
tags: ["vision", "data", "services", "quickstart", "ml", "camera", "webcam"]
no_list: true
description: "Use Viam's machine learning capabilities to deploy a person detector ML model to your machine."
images: ["/get-started/quickstarts/vision-card.png"]
imageAlt: "Person detected in camera stream"
authors: []
weight: 30
languages: ["python", "go", "typescript", "flutter", "c++"]
viamresources: ["camera", "mlmodel", "vision"]
no_list: true
level: "Beginner"
date: "2024-07-31"
cost: "0"
resource: "quickstart"
aliases:
  - /get-started/quickstarts/detect-people/
---

This quickstart is part of a series.
If you haven't read through [Learn Viam](/get-started/), [driven a rover](/get-started/drive-rover/), and [controlled a motor](/get-started/control-motor/), we recommend you do so before continuing.

In this guide you'll use machine learning to detect people in a camera stream.

{{< alert title="You will learn" color="tip" >}}

- How to configure a webcam
- How to deploy a machine learning model
- How to use the machine learning model with a vision service

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/-sXdxbBVrso">}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
If you have the following components, you can follow along on your own hardware:

- A Linux, maxOS or WSL computer that can run `viam-server`.
- A webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer.

{{% expand "No computer or webcam?" %}}
No problem.
Use [Try Viam](https://app.viam.com/try) to borrow a rover online which is already configured with some components to test with.
If you are using a Try Viam rover **start with Step 4**.
You may not be able to test using the supplied ML model, as your borrowed rover will generally not be able to see people.
If that is the case, use the [`color_detector`](/services/vision/color_detector/) vision service to test detecting colors.
{{% /expand%}}

## Instructions

Follow these instructions to configure your machine and test detections:

{{%expand "Step 1: Create a new machine" %}}

{{< alert title="Tip" color="tip" >}}
If you followed the [Control a motor](/get-started/control-motor/) quickstart and have installed `viam-server` already on a machine that has a webcam, you can use the same machine and skip to step 3.
{{< /alert >}}

Add a new machine in the [Viam app](https://app.viam.com) by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add Machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll find a variety of tools for working with your machine.

{{% /expand%}}
{{%expand "Step 2: Install viam-server" %}}

Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer, start running it and connect it to the Viam app.
Select the OS that's appropriate for your computer.
For example, **Mac** for a MacBook.
Select **RDK** as the RDK type.

{{% /expand%}}
{{%expand "Step 3: Configure your webcam" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

Click the **Save** button in the top right corner of the page to save your configuration.
Then click on the **Test** panel at the bottom of the camera's configuration panel to test the camera stream.

If you don't see an image stream, you need to [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{% /expand%}}
{{%expand "Step 4: Deploy a person detection model" %}}

Now add an `ML model` service that can detect a person:
Click **+**, click **Service** and select the `ML model` type, then select the `TFLite CPU` model.
Create the service.

In the resulting ML model service configuration pane, ensure that **Deploy model on machine** is selected for the **Deployment** field.

Click on **Select models**.
Click on the **Registry** tab and search for "people".
Select the **people** model by **ml-models-scuttle**.

Click the **Save** button in the top right corner of the page to save your configuration and deploy an object detection TFLite model that has been trained to be able to detect a person.

For more detailed information, including optional attribute configuration, see the [`tflite_cpu` docs](/services/ml/deploy/tflite_cpu/).

{{% /expand%}}
{{%expand "Step 5: Configure a vision service" %}}

To use the deployed person detection model to detect people on a camera stream, you need to configure a vision service.
This service applies the ML model to the camera input stream.

Add a `vision` **Service** and select the `ML model` model.

Select the ML model service your person detector model is deployed on (which you created in step 4) from the **ML Model** dropdown.
Click the **Save** button in the top right corner of the page to save your vision service configuration.

{{% /expand%}}
{{%expand "Step 6: Test person detection" %}}

Now, test your person detection on in the **Test** section of the computer vision service's configuration panel or on the **CONTROL** tab.

You will see your camera stream and see detections as labeled boxes on the images along with position, dimension, class and confidence data.
Detections in class `Person` with a high confidence score show positive person detections, but the ML model can also detect other objects:

{{<imgproc src="/get-started/quickstarts/vision-card-more-detections.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card with a lower default minimum confidence threshold." >}}

{{% /expand%}}
{{%expand "(Optional) Step 7: Limit the number of detections" %}}

If you are seeing a lot of detections, you can set a minimum confidence threshold.

On the configuration page of the vision service in the top right corner, click **{}** (Switch to advanced).
Add the following JSON to the JSON configuration to set the `default_minimum_confidence` of the detector:

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

This optional attribute reduces your detections output (which you'll view in step 7) by filtering out detections below the threshold of 82% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration.
For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

Now if you view detections, you will only see detections with a confidence value higher than the `"default_minimum_confidence"` attribute.

{{<imgproc src="/get-started/quickstarts/vision-card.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card." >}}

{{% /expand%}}

## Next steps

You can now detect people on a camera stream.
Of course these detections are not just accessible from the Viam app, but you can also use the [vision service API](/services/vision/#api).

Next, you'll learn how to collect data from sensors or cameras using the data management service:

{{< cards >}}
{{% card link="/get-started/collect-data/" %}}
{{< /cards >}}
