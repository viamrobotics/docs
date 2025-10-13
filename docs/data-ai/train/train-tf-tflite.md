---
linkTitle: "Train TF or TFLite model"
title: "Train a TF or TFLite model"
weight: 50
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
  - /data-ai/ai/train-tflite/
  - /data-ai/train/train-tf-tflite/
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
platformarea: ["ml"]
date: "2024-12-03"
updated: "2025-10-13"
---

Many machines have cameras through which they can monitor their environment.
With machine learning (ML), you can train models on patterns within image data.
Follow this guide to use your image data to train an ML model, so that your machine can make inferences about its environment.

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A dataset that meets training requirements" %}}

To train a model, your dataset must contain the following:

{{< readfile "/static/include/data/dataset-requirements.md" >}}

Follow the guide to [create a dataset](/data-ai/train/create-dataset/).

{{% /expand %}}

## Train a machine learning model

Now that you have a dataset that contains your labeled images, you are ready to train a machine learning model.

{{< table >}}
{{% tablestep start=1 %}}
**Find your training dataset**

Navigate to your list of [**DATASETS**](https://app.viam.com/datasets) and select the one you want to train on.

{{% /tablestep %}}
{{% tablestep %}}
**Train an ML model**

Click **Train model** and follow the prompts.
You can train a TFLite model using **Built-in training**.

{{<imgproc src="/services/ml/train-model.png" resize="1200x" declaredimensions=true style="width:500px" alt="The shapes dataset." class="imgzoom fill shadow" >}}

Click **Next steps**.

{{% /tablestep %}}
{{% tablestep %}}
**Select model type**

Select between:

<!-- prettier-ignore -->
| Type | Description |
| ---- | ----------- |
| **TensorFlow Lite (TFLite)** | Best for use on mobile and edge devices with minimal resources. |
| **TensorFlow (TF)** | Best for general-purpose tasks with more computational power. |

{{% /tablestep %}}
{{% tablestep %}}
**Fill in the details for your ML model**

Enter a name for your new model.

Select a **Task Type**:

- **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
  Select this if you only have one label on each image. Ensure that the dataset you are training on also contains unlabeled images.
- **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
- **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.

Select the labels you want to train your model on from the **Labels** section. Unselected labels will be ignored and will not be part of the resulting model.

Click **Train model**.

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

{{% /tablestep %}}
{{% tablestep %}}
**Wait for your model to train**

The model now starts training and you can follow its process on the [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the [**MODELS** tab](https://app.viam.com/models).

You will receive an email when your model finishes training.

{{% /tablestep %}}
{{% tablestep %}}
**Debug your training job**

From the [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view logs for your training jobs with the [`viam train logs`](/dev/tools/cli/#train) command.

Training logs expire after 7 days.

{{% /tablestep %}}
{{< /table >}}

## Test your ML model

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

Once your model has finished training, you can test it.

Ideally, you want your ML model to perform with high confidence.
As you test it, if you notice faulty predictions or confidence scores, you will need to adjust your dataset and retrain your model.

If you trained a _classification_ model, you can test it with the following instructions.

1. Navigate to the [**DATA** page](https://app.viam.com/data/view) and click on the **Images** subtab.
1. Click on an image to open the side menu, and select the **Actions** tab.
1. In the **Run model** section, select your model and specify a confidence threshold.
1. Click **Run model**.

If the results exceed the confidence threshold, the **Run model** section shows a label and the corresponding confidence score.

You can test both TensorFlow Lite detection models and TensorFlow Lite classifier models using the following resources together:

- [a camera](/operate/reference/components/camera/)
- [a `tflite_cpu` ML model](https://app.viam.com/module/viam/tflite_cpu/) with the model you just trained
- [an `mlmodel` vision service](/operate/reference/services/vision/mlmodel/) using the `tflite_cpu` model

## Iterate on your ML model

You are unlikely to account for all false positives or false negatives during your first round of training.
To improve your ML model, try the following steps:

- **More data means better models**: Add images capturing edge cases to your training dataset, annotate them, and retrain your model using the new data.
- **Include counterexamples**: For detections, use images with and without the object you’re looking to detect.
  This helps the model distinguish the target object from the background and reduces the chances of false positives by teaching it what the object is not.
  For classifications, ensure you cover a full range of data the classifier might encounter.
- **Avoid class imbalance**: Don’t train excessively on one specific type or class, make sure each category has a roughly equal number of images.
  For instance, if you're training a dog detector, include images of various dog breeds to avoid bias towards one breed.
  An imbalanced dataset can lead the model to favor one class over others, reducing its overall accuracy.
- **Match your training images to your intended use case**: Use images that reflect the quality and conditions of your production environment.
  For example, if you plan to use a low-quality camera in production, train with low-quality images.
  Similarly, if your model will run all day, capture images in both daylight and nighttime conditions.
- **Vary your angles and distances**: Include image examples from every angle and distance that the model will see in normal use.
- **Ensure labeling accuracy**: Make sure the labels or bounding box annotations you give are accurate.

To capture more images and retrain your model using those images, complete the following steps:

1. Add the images to your training dataset.
   You can use images from existing data on the [**DATA** page](https://app.viam.com/data/) or [capture new images and add them to your training dataset](/data-ai/train/create-dataset/#capture-images).

1. Open your dataset on the **DATASETS** tab and annotate the images.

1. Repeat the [steps to train a machine learning model](/data-ai/train/train-tf-tflite/#train-a-machine-learning-model) and create a new version of your ML model.
   Your machines will automatically update to the new version of the model soon after release.

## Next steps

Now your machine can make inferences about its environment.
The next step is to [deploy](/data-ai/ai/deploy/) the ML model and then [act](/data-ai/ai/act/) or [alert](/data-ai/ai/alert/) based on these inferences.

See the following tutorials for examples of using machine learning models to make your machine do things based on its inferences about its environment:

{{< cards >}}
{{% card link="/operate/hello-world/tutorial-desk-safari/" customTitle="Desk Safari Game" %}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
