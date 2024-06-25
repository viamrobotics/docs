---
title: "How to train and deploy ML/computer vision models"
linkTitle: "Train computer vision models"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/collect.svg"]
description: "Collect images and do interesting things with computer vision, ML, and webhooks."
---

You can use Viam's built-in tools to train a machine learning (ML) model on your images and then deploy computer vision on your machines.

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/use-cases/ml-vision-diagram.png)

For example, you can train a model to recognize your dog and detect whether they are sitting or standing.
Then, you can configure your machine to [capture images](/use-cases/image-data/) only when your dog is in the camera frame so you don't capture hundreds of photos of an empty room.
You can then get even more image data of your dog and improve your ML model by training it on the larger dataset.

You can do all of this using the [Viam app](https://app.viam.com) user interface.
You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Create a dataset and label data](#create-a-dataset-and-label-data)
2. [Train and test a machine learning (ML) model](#train-and-test-a-machine-learning-ml-model)

{{< /alert >}}

## Create a dataset and label data

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**1. Collect images**

Start by collecting images from your cameras and syncing it to the [Viam app](https://app.viam.com).
See [Collect image data and sync it to the cloud](/use-cases/image-data/#collect-image-data-and-sync-it-to-the-cloud) for instructions.

{{< /tablestep >}}
{{< tablestep link="/services/data/dataset/">}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Label data">}}
**2. Label your images**

Once you have enough images of the objects you'd like to classify, use the interface on the **DATA** tab to label your data.
If you want to train an image classifier, use image tags.
For an object detector, use bounding boxes.

{{< /tablestep >}}
{{< tablestep link="/services/data/dataset/">}}
{{<imgproc src="/services/ml/label.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Label data">}}
**2. Create a dataset**

Use the interface on the **DATA** tab (or the [`viam data dataset add` command](/cli/#data)) to add all images you want to train the model on to a dataset.

{{< /tablestep >}}
{{< /table >}}

{{% alert title="Tip" color="tip" %}}
To keep your data organized, you can configure a tag in your data management service config panel.
This tag will be applied to all data synced from that machine in the future.
If you apply the same tag to all data gathered from all machines that you want to use in your dataset, you can filter by that tag in the Viam app **DATA** tab, or when querying data.

This is not required, since you can use other filters like time or machine ID in the **DATA** tab to isolate your data.
{{% /alert %}}

## Train and test a machine learning (ML) model

{{< table >}}
{{< tablestep link="/services/ml/train-model/">}}
{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.
Click **Train model** and follow the prompts.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**2. Deploy your ML model**

On the **Configure** page add the built-in [ML model service](/services/ml/deploy/) and select your ML model.
The service will to deploy and run the model.
Once you've added the ML model service to your machine, choose your newly-trained model from the dropdown menu in the ML model service's configuration card.

{{< /tablestep >}}
{{< tablestep link="/services/vision/">}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure a service">}}
**3. Configure an <code>mlmodel</code> vision service**

The vision service takes the the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

{{< /tablestep >}}
{{< tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier">}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your model">}}
**4. Test your classifier**

Test your ML model classifier with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud), [live camera footage,](/services/vision/mlmodel/#live-camera-footage) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

{{< /tablestep >}}
{{< /table >}}

## Next steps

See the following tutorials for examples of how to use the tools described on this page:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/verification-system/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
