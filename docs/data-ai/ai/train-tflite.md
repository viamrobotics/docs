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
  - /extend/modular-resources/examples/tflite-module/
  - /modular-resources/examples/tflite-module/
  - /registry/examples/tflite-module/
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

Common use cases for this are **security**, **quality assurance**, and **food service** applications.

Follow this guide to use your image data to train an ML model, so that your machine can make inferences about its environment.

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A dataset with labels. Click to see instructions." %}}

Follow the guide to [create a dataset](/data-ai/ai/create-dataset/) if you haven't already.

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

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:500px" alt="The shapes dataset." class="imgzoom fill">}}

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

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" style="width:500px" resize="1200x" class="imgzoom fill" >}}

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

You can also view your training jobs' logs with the [`viam train logs`](/dev/tools/cli/#train) command.

{{% /tablestep %}}
{{< /table >}}

## Test your ML model

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

Once your model has finished training, you can test it.

Ideally, you want your ML model to be able to work with a high level of confidence.
As you test it, if you notice faulty predictions or confidence scores, you will need to adjust your dataset and retrain your model.

If you trained a _classification_ model, you can test it with the following instructions.

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click on the **Images** subtab.
1. Click on an image to open the side menu, and select the **Actions** tab.
1. In the **Run model** section, select your model and specify a confidence threshold.
1. Click **Run model**

If the results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

You can test both detection models and classifier models using the following resources together:

- [a camera](/operate/reference/components/camera/)
- [a `tflite_cpu` ML model](/data-ai/ai/deploy/) with the model you just trained
- [an `mlmodel` vision service](/operate/reference/services/vision/mlmodel/) using the `tflite_cpu` model

## Next steps

Now your machine can make inferences about its environment.
The next step is to [deploy](/data-ai/ai/deploy/) the ML model and then [act](/data-ai/ai/act/) or [alert](/data-ai/ai/alert/) based on these inferences.

See the following tutorials for examples of using machine learning models to make your machine do things based on its inferences about its environment:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
