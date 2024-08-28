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
2. [Train and test a machine learning (ML) model](#train-and-test-a-machine-learning-ml-model)

{{< /alert >}}

## Create a dataset and label data

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**1. Collect images**

Start by collecting images from your cameras and syncing it to the [Viam app](https://app.viam.com).
See [Collect image data and sync it to the cloud](/how-tos/image-data/#collect-image-data-and-sync-it-to-the-cloud) for instructions.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Label data">}}
**2. Label your images**

Once you have enough images of the objects you'd like to classify, use the interface on the **DATA** tab to label your data.
If you want to train an image classifier, use image tags.
For an object detector, use bounding boxes.

{{< expand "Create image tags (for an image classifier)" >}}

You can use tags to [create classification models](/services/ml/train-model/#train-a-model) for images.
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
If you annotate an entire dataset, you can use these bounding boxes to [create object detection models](/services/ml/train-model/#train-a-model).
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

## Train and test a machine learning (ML) model

{{< table >}}
{{% tablestep link="/services/ml/train-model/"%}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.
Click **Train model** and follow the prompts.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**2. Deploy your ML model**

If you haven't already, [create a machine](/cloud/machines/#add-a-new-machine) and [set it up](/cloud/machines/#set-up-a-new-machine).
Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Here, add the built-in [TFLite CPU ML model service](/services/ml/deploy/) and select the ML model you just trained as the **Model**.
This service will deploy and run the model.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/" %}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure a service">}}
**3. Configure an <code>mlmodel</code> vision service**

The vision service takes the the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier" %}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your model">}}
**4. Test your classifier**

Test your ML model classifier with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud), [live camera footage,](/services/vision/mlmodel/#live-camera-footage) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

{{% /tablestep %}}
{{< /table >}}

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
