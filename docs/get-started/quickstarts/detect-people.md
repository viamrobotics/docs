---
title: "Detect People with a Webcam"
linkTitle: "Detect people with a webcam"
weight: 50
type: "docs"
tags: ["vision", "data", "services", "quickstart", "ml", "camera", "webcam"]
no_list: true
description: "Use Viam's machine learning capabilities to deploy a person detector ML model to your machine."
images: ["/platform/ml.svg"]
imageAlt: "Machine Learning"
---

Follow this guide to detect people with a webcam on the Viam platform, using a [pre trained ML model from the registry](https://app.viam.com/ml-model/ml-models-scuttle/people):

{{<imgproc src="/get-started/quickstarts/vision-card.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card." >}}

## Requirements

- A computer: a development machine such as your laptop and optionally a single-board computer such as the Raspberry Pi
- A webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer
- An account on the [Viam app](https://app.viam.com)

Follow these instructions to configure your machine and test detections:

{{%expand "Step 1: Create a new machine" %}}

Add a new machine in the [Viam app](https://app.viam.com) by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add Machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll find a variety of tools for working with your machine.

{{% /expand%}}
{{%expand "Step 2: Install viam-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

{{% /expand%}}
{{%expand "Step 3: Configure your webcam" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

Click the **Save** button in the top right corner of the page to save your configuration.
Go to the **CONTROL** tab and expand the camera's remote control card to test the camera stream.
If you don't see an image stream, you need to [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{% /expand%}}
{{%expand "Step 4: Deploy a person detection model" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `ML model` type, then select the `TFLite CPU` model.
Enter a name or use the suggested name for your service and click **Create**.

In the resulting ML model service configuration pane, ensure that **Deploy model on machine** is selected for the **Deployment** field.

Click on **Select models** to open a dropdown with all of the ML models available to you.
Select the `ml-models-scuttle:people` model (the **people** model by **ml-models-scuttle**) to deploy an object detection TFLite model that has been trained to be able to detect a person.

Click the **Save** button in the top right corner of the page to save your configuration.

For more detailed information, including optional attribute configuration, see the [`tflite_cpu` docs](/services/ml/deploy/tflite_cpu/).

{{% /expand%}}
{{%expand "Step 5: Configure your detector" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `vision` type, then select the `ML model` model.
Enter a name or use the suggested name for your service and click **Create**.

Select the ML model service your person detector model is deployed on (which you created in step 4) from the **ML Model** dropdown.
Then, click **{}** (Switch to advanced) in the top right corner of the configuration pane.
Add the following JSON to the JSON configuration to set the `default_minimum_confidence` of the detector:

```json
"default_minimum_confidence": 0.82
```

This optional attribute simplifies your detections output (which you'll view in step 6) by filtering out detections below the threshold of 82% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration.

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

{{% /expand%}}
{{%expand "Step 6: Control person detection" %}}

Now, test your person detection with the computer vision service's remote control card.

Navigate to the **CONTROL** tab in the [Viam app](https://app.viam.com).
Click on the `vision` service's card to expand it.

Click **Refresh** to refresh the image stream and see detections as labeled boxes on the images along with position, dimension, class and confidence data.
Detections in class `Person` with a high confidence score show positive person detections, but the ML model can also detect other objects:

{{<imgproc src="/get-started/quickstarts/vision-card-more-detections.png" resize="x1100" declaredimensions=true alt="Positive person detection on the vision card with a lower default minimum confidence threshold." >}}

You can view detections with a lower confidence score from the vision control card, like in the above screenshot, by lowering the `"default_minimum_confidence"` attribute.

{{% /expand%}}

## Next steps

You can continue to test your [`mlmodel` detector](/services/vision/mlmodel/#test-your-detector-or-classifier) with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

You can use one of [Viam's SDKs](/sdks/) to write a script that captures detections and triggers an alarm when a person is detected, or even sends you photos of the person detected.
See [A Person Detection Security Robot That Sends You Photos](/tutorials/projects/send-security-photo/#use-the-viam-python-sdk-to-control-your-security-robot) for an example of this.

You can also use the Viam platform to [train your own detector or classifier](/use-cases/deploy-ml/).

You can also explore our [tutorials](/tutorials/) for more machine learning ideas:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{% card link="/registry/examples/tflite-module/" %}}
{{< /cards >}}
