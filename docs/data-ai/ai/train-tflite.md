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

Follow this guide to use your image data to train an ML model, so that your machine can make inferences about its enviroment.

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A dataset with labels. Click to see instructions." %}}

Follow the guide to [create a dataset](/data-ai/ai/create-dataset/) if you haven't already.

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

You can train a TFLite model using **Built-in training**.

Click **Next steps**.

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:500px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Fill in the details for your ML model**

Enter a name for your new model.

Select a **Task Type**:

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
As you test it, if you notice faulty predictions or confidence scores, you will need to adjust your dataset and retrain your model.

If you trained a classification model, you can test it with the following instructions.
If you trained a detection model, move on to [deploy an ML model](/data-ai/ai/deploy/).

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click on the **Images** subtab.
1. Click on an image to open the side menu, and select the **Actions** tab.
1. In the **Run model** section, select your model and specify a confidence threshold.
1. Click **Run model**

If the results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

## Next steps

Now your machine can make inferences about its environment. The next step is to [act](/data-ai/ai/act/) or [alert](/data-ai/ai/alert/) based on these inferences.

See the following tutorials for examples of using machine learning models to make your machine do things based on its inferences about its environment:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
