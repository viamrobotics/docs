---
title: "How to train and deploy ML/computer vision models"
linkTitle: "Train computer vision models"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/train.svg"]
description: "Use your image data to create and label a dataset and train a computer vision ML model."
aliases:
  - /use-cases/deploy-ml/
  - /manage/ml/train-model/
  - /ml/train-model/
  - /services/ml/train-model/
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
level: "Beginner"
date: "2024-06-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can use Viam's built-in tools to train a machine learning (ML) model on your images and then deploy computer vision on your machines.

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/how-tos/ml-vision-diagram.png)

For example, you can train a model to recognize your dog and detect whether they are sitting or standing.
Then, you can configure your machine to [capture images](/how-tos/image-data/) only when your dog is in the camera frame so you don't capture hundreds of photos of an empty room.
You can then get even more image data of your dog and improve your ML model by training it on the larger dataset.

You can do all of this using the [Viam app](https://app.viam.com) user interface.
You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Create a dataset and label data](#create-a-dataset-and-label-data)
2. [Train a machine learning (ML) model](#train-a-machine-learning-ml-model)
3. [Deploy a machine learning model](#deploy-an-ml-model)

{{< /alert >}}

## Create a dataset and label data

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Collect data">}}
**1. Collect images**

Start by collecting images from your cameras and syncing it to the [Viam app](https://app.viam.com).
See [Collect image data and sync it to the cloud](/how-tos/image-data/#collect-image-data-and-sync-it-to-the-cloud) for instructions.

When training machine learning models, it is important to supply a variety of different data about the subject in different situations, such as from different angles or in different lighting situations.
The more varied the provided data set, the more accurate the resulting model becomes.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/label.svg" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Label data">}}
**2. Label your images**

Once you have enough images of the objects you'd like to classify, use the interface on the **DATA** tab to label your data.
If you want to train an image classifier, use image tags.
For an object detector, use bounding boxes.

<br>

{{< expand "Create image tags (for an image classifier)" >}}

You can use tags to create classification models for images.
For example, if you would like to create a model that identifies an image of a star in a set of images, tag each image containing a star with a `star` tag.
The filter also needs to include images without the star tag or with another tag like `notstar`.
If you add a `notstar` tag, you can filter the data in your dataset by selecting `star` and `notstar` from the **Tags** dropdown in the **Filtering** menu.
Alternatively you can use date ranges to filter for relevant data.

To tag an image, click on the image and select the **Image tags** mode in the menu that opens.

{{<gif webm_src="/services/data/tag-star.webm" mp4_src="/services/data/tag-star.mp4" alt="Tag image with a star label">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image.

Repeat this with all images in your dataset.

{{< /expand >}}

{{< expand "Create bounding boxes (for an object detector)" >}}

You can create one or more bounding boxes for objects in each image.
If you annotate an entire dataset, you can use these bounding boxes to create object detection models.
For example, if you would like to create a model that detects a dog in an image, add bounding boxes around the dog in each of your images and add or select the label `dog`.

To add a bounding box, click on an image and select the **Bounding box** mode in the menu that opens.
Choose an existing label or create a new label.
Click on the image where you would like to add the bounding box and drag to where the bounding box should end.

{{<gif webm_src="/services/data/label-dog.webm" mp4_src="/services/data/label-dog.mp4" alt="Add a bounding box around the dog in an image">}}

To expand the image, click on the expand side menu arrow in the corner of the image:

{{<gif webm_src="/services/data/label-dog-big.webm" mp4_src="/services/data/label-dog-big.mp4" alt="Add a bounding box around the dog in an image in a big menu">}}

Repeat this with all images in your dataset.
To see all the images that have bounding boxes, you can filter your dataset by selecting the label from the **Bounding box labels** dropdown in the **Filters** menu.

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep link="/services/data/dataset/" %}}
**2. Create a dataset**

Use the interface on the **DATA** tab (or the [`viam data dataset add` command](/cli/#data)) to add all images you want to train the model on to a dataset.

{{<gif webm_src="/services/data/add-to-dataset.webm" mp4_src="/services/data/add-to-dataset.mp4" alt="Add image to dataset">}}

To remove an image from a dataset click on the **x** button next to the dataset name.
Alternatively, you can use the [`viam data dataset remove` command](/cli/#data) to remove an image or group of images matching a specific filter using the Viam CLI.

{{% /tablestep %}}
{{< /table >}}

{{% alert title="Tip" color="tip" %}}
To keep your data organized, you can configure a tag in your data management service config panel.
This tag will be applied to all data synced from that machine in the future.
If you apply the same tag to all data gathered from all machines that you want to use in your dataset, you can filter by that tag in the Viam app **DATA** tab, or when querying data.

This is not required, since you can use other filters like time or machine ID in the **DATA** tab to isolate your data.
{{% /alert %}}

## Train a machine learning (ML) model

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/services/ml/train.svg" class="fill alignright" style="max-width: 250px" declaredimensions=true alt="Train models">}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.

Click **Train model** and follow the prompts.

You can choose between

- training a new model or updating a model
- You can use a **Built-in training** script or a [custom training script](/services/ml/training-scripts/).

Click **Next steps**.

{{% /tablestep %}}
{{% tablestep %}}
**2. Select the details for your ML model**

1. Enter a name or use the suggested name for your new model.
1. Select a **Model Type** and one or more labels to train on. Depending on the training script you've chose, you may have a number of these options:
   - **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
     If you are only using one label, ensure that the dataset you are training on also contains unlabeled images.
   - **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
   - **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.
1. Click **Train model**

{{<gif webm_src="/services/ml/train-model.webm" mp4_src="/services/ml/train-model.mp4" alt="Train a model UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Wait for your model to train**

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.
You will receive an email when your model finishes training.

![The trained model](/services/ml/petfeeder-model.png)

{{% /tablestep %}}
{{% tablestep %}}
**4. Debug your training job**

If your training job failed you can check your job's logs with the [CLI](/cli/).

You can obtain the job's id by listing the jobs:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<INSERT ORG ID> --job-status=unspecified
```

Then use the job id to get your training job's logs:

```sh {class="command-line" data-prompt="$"}
viam train logs --job-id=<JOB ID>
```

{{% /tablestep %}}
{{< /table >}}

## Deploy an ML model

To use ML models with your machine, you must first deploy the model using an ML model service. The ML model service will run the model and allow the vision service to use it:

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**1. Deploy your ML model**

If you haven't already, [create a machine](/cloud/machines/#add-a-new-machine) and [set it up](/cloud/machines/#set-up-a-new-machine).
Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Here, add an [ML model service](/services/ml/deploy/) that supports the ML model you just trained and add the model as the **Model**.
For example use the `TFLite CPU` ML model service for TFlite ML models.
This service will deploy and run the model.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/" %}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure a service">}}
**2. Configure an <code>mlmodel</code> vision service**

The vision service takes the the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier" %}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your model">}}
**3. Test your classifier**

Test your ML model classifier with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud), [live camera footage,](/services/vision/mlmodel/#live-camera-footage) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

{{% /tablestep %}}
{{< /table >}}

## Versioning for deployed models

If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the machine.
If you do not want Viam to automatically deploy the `latest` version of the model, you can edit the `"packages"` array in the [JSON configuration](/configure/#the-configure-tab) of your machine.
This array is automatically created when you deploy the model and is not embedded in your service configuration.

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
"packages": [
  {
    "package": "<model_id>/<model_name>",
    "version": "YYYY-MM-DDThh-mm-ss",
    "name": "<model_name>",
    "type": "ml_model"
  }
]
```

## Next steps

To work with datasets programmatically, see the data API which includes several methods to work with datasets:

{{< cards >}}
{{% card link="/appendix/apis/data-client/" %}}
{{< /cards >}}

See the following tutorials for examples of how to use the tools described on this page:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/verification-system/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
