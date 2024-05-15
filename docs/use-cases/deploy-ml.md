---
title: "Train and deploy image classification models"
linkTitle: "Train and deploy classification models"
weight: 50
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's machine learning capabilities to train image classification models and deploy these models to your machines."
images: ["/platform/ml.svg"]
imageAlt: "Machine Learning"
---

You can create and deploy an image classification model onto your machine with Viam's machine learning (ML) capabilities.
Manage the classification model fully on one platform: collect data, create a dataset and label it, and train the model for **Single** or **Multi Label Classification**.
Then, test if your model works for classifying objects in a camera stream or existing images with the `mlmodel` classification model of vision service.

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/collect.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Collect data">}}
**1. Collect**

Start by collecting images from your cameras with the [data management service](/app/data/).
You can [view the data](/app/data/view/) on the **Data tab**.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/label.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Label data">}}
**2. Create a dataset and label**

Once you have enough images of the objects you'd like to classify, [label your data and create a dataset](/app/data/dataset/) in preparation for training classification models.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/train.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Train models">}}
**3. Train an ML model**

Use your labeled data to [train your own models](/app/ml/train-model/) for object classification using data from the [data management service](/app/data/).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/registry/upload-module.svg" class="fill alignleft" style="max-width: 200px" declaredimensions=true alt="Train models">}}
**4. Deploy your ML model**

To make use of ML models with your machine, use the built-in [ML model service](/ml/) to deploy and run the model.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/configure.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Configure a service">}}
**5. Configure an <code>mlmodel</code> vision service**

For object classification, you can use the [vision service](/services/vision/), which provides an [ml model classifier](/services/vision/mlmodel/) model.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/deploy.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Deploy your model">}}
**6. Test your classifier**

Test your [mlmodel classifier](/services/vision/mlmodel/#test-your-detector-or-classifier) with [existing images in the Viam app](/services/vision/mlmodel/#existing-images-in-the-cloud), [live camera footage,](/services/vision/mlmodel/#live-camera-footage) or [existing images on a computer](/services/vision/mlmodel/#existing-images-on-your-machine).

{{< /tablestep >}}
{{< /table >}}

## Next steps

After testing your classifier, see the following to further explore Viam's data management and computer vision capabilities:

- [Export Data Using the Viam CLI](/app/data/export/): Export your synced data from the Viam cloud.
- [2D Object Detection](/services/vision/#detections): Configure your machine's camera to draw a bounding box around detected objects, based on a machine learning model.
- [Update an existing ML model](/app/ml/train-model/#train-a-new-version-of-a-model): Refine an existing ML model you have trained, and select which model version to deploy.

You can also explore our [tutorials](/tutorials/) for more machine learning ideas:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{% card link="/app/registry/examples/tflite-module/" %}}
{{< /cards >}}
