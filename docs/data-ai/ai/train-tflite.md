---
linkTitle: "Train TFlite model"
title: "Train a TFlite model"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/train.svg"]
description: "Use your image data to train a model, so your machines can make inferences about their environments."
aliases:
  - /use-cases/deploy-ml/
  - /manage/ml/train-model/
  - /ml/train-model/
  - /services/ml/train-model/
  - /tutorials/data-management-tutorial/
  - /tutorials/data-management/
  - /data-management/data-management-tutorial/
  - /tutorials/services/data-management-tutorial/
  - /tutorials/services/data-mlmodel-tutorial/
  - /tutorials/projects/filtered-camera/
  - /how-tos/deploy-ml/
  - /how-tos/train-deploy-ml/
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
platformarea: ["ml"]
date: "2024-12-03"
---

Many machines have cameras through which they can monitor their environment.
With machine leaning, you can train models on patterns within that visual data.
You can collect data from the camera stream and label any patterns within the images.

If a camera is pointed at a food display, for example, you can label the image of the display with `full` or `empty`, or label items such as individual `pizza_slice`s.

Using a model trained on such images, machines can make inferences about their environments.
Your machines can then automatically trigger alerts or perform other actions.
If a food display is empty, the machine could, for example, alert a supervisor to restock the display.

Common use cases for this are **quality assurance** and **health and safety** applications.

{{< alert title="In this page" color="tip" >}}

1. [Create a dataset with labeled data](#create-a-dataset-and-label-data)
1. [Train a machine learning (ML) model](#train-a-machine-learning-ml-model)
1. [Test your ML model](#test-your-ml-model)
1. [Deploy your ML model](#deploy-an-ml-model)

{{< /alert >}}

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/how-tos/ml-vision-diagram.png)

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A configured camera. Click to see instructions." %}}

First, connect the camera to your machine's computer if it's not already connected (like with an inbuilt laptop webcam).

Then, navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
The `webcam` model supports most USB cameras and inbuilt laptop webcams.
You can find additional camera models in the [camera configuration](/components/camera/#configuration) documentation.

Complete the camera configuration and use the **TEST** panel in the configuration card to test that the camera is working.

{{% /expand%}}

{{% expand "No computer or webcam?" %}}
No problem.
You don't need to buy or own any hardware to complete this guide.

Use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components, including a webcam.

Once you have borrowed a rover, go to its **CONTROL** tab where you can view camera streams and also drive the rover.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can perceive.

To change what the front-facing camera is pointed at, find the **cam** camera panel on the **CONTROL** tab and click **Toggle picture-in-picture** so you can continue to view the camera stream.
Then, find the **viam_base** panel and drive the rover around.

Now that you have seen that the cameras on your Try Viam rover work, begin by [Creating a dataset and labeling data](/data-ai/ai/create-dataset/).
You can drive the rover around as you capture data to get a variety of images from different angles.

{{< alert title="Tip" color="tip" >}}
Be aware that if you are running out of time during your rental, you can [extend your rover rental](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{% /expand%}}



## Train a machine learning (ML) model

Now that you have a dataset with your labeled images, you are ready to train a machine learning model.

{{< table >}}
{{% tablestep %}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.

Click **Train model** and follow the prompts.

You can train your model using **Built-in training** or using a [training script](/registry/training-scripts/) from the Viam Registry.

Click **Next steps**.

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:500px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Fill in the details for your ML model**

Enter a name for your new model.

For built-in trainings, select a **Task Type**:

- **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
  Select this if you only have one label on each image. Ensure that the dataset you are training on also contains unlabeled images.
- **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
- **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.

Select the labels you want to train your model on from the **Labels** section. Unselected labels will be ignored, and will not be part of the resulting model.

Click **Train model**.

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" style="width:500px" resize="1200x" class="imgzoom fill aligncenter" >}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Wait for your model to train**

The model now starts training and you can follow its process on the [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the [**MODELS** tab](https://app.viam.com/data/models).

You will receive an email when your model finishes training.

{{% /tablestep %}}
{{% tablestep %}}
**4. Debug your training job**

From the [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view your training jobs' logs with the [`viam train logs`](/cli/#train) command.

{{% /tablestep %}}
{{< /table >}}

## Test your ML model

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

Once your model has finished training, you can test it.

Ideally, you want your ML model to be able to work with a high level of confidence.
As you test it, if you notice faulty predictions or confidence scores, you will need adjust your dataset and retrain your model.

If you trained a classification model, you can test it with the following instructions.
If you trained a detection model, skip to [deploy an ML model](#deploy-an-ml-model).

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click on the **Images** subtab.
1. Click on an image to open the side menu, and select the **Actions** tab.
1. In the **Run model** section, select your model and specify a confidence threshold.
1. Click **Run model**

If the results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

## Deploy an ML model

You have your trained model.
Now you can deploy it to your machines and make live inferences.

To use an ML model on your machine, you need to deploy the model with an ML model service.
The ML model service will run the model.

On its own the ML model service only runs the model.
To use it to make inferences on a camera stream, you need to use it alongside a vision service.

{{< table >}}
{{% tablestep link="/services/ml/" %}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Train models">}}
**1. Deploy your ML model**

Navigate to the **CONFIGURE** tab of one of your machine in the [Viam app](https://app.viam.com).
Add an ML model service that supports the ML model you just trained and add the model as the **Model**.
For example use the `ML model / TFLite CPU` service for TFlite ML models.
If you used the built-in training, this is the ML model service you need to use.
If you used a custom training script, you may need a different [ML model service](/services/ml/).

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/" %}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Configure a service">}}
**2. Configure an <code>mlmodel</code> vision service**

The ML model service deploys and runs the model.

The vision service works with the ML model services.
It uses the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

**Save** your changes.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier" %}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Deploy your model">}}
**3. Use your vision service**

You can test your vision service by clicking on the **Test** area of its configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream shows when the vision service identifies something.
Try pointing the camera at a scene similar to your training data.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" >}}
{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" >}}

{{% expand "Want to limit the number of shown classifications or detections? Click here." %}}

If you are seeing a lot of classifications or detections, you can set a minimum confidence threshold.

Start by setting the value to 0.8.
This reduces your output by filtering out anything below a threshold of 80% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration, then close and reopen the **Test** panel of the vision service configuration panel.
Now if you reopen the panel, you will only see classifications or detections with a confidence value higher than the `default_minimum_confidence` attribute.

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

{{% /expand%}}
{{% /tablestep %}}
{{< /table >}}

## Next steps

Now your machine can make inferences about its environment. The next step is to act based on these inferences:

- Perform actions: You can use the [vision service API](/appendix/apis/services/vision/) to get information about your machine's inferences and program behavior based on that.
- Webhooks: You can use triggers to send webhooks when certain inferences are made. For an example of this, see the [Helmet Monitoring tutorial](/tutorials/projects/helmet/)

See the following tutorials for examples of using machine learning models to make your machine do things based on its inferences about its environment:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
