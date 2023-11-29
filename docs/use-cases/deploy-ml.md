---
title: "Train and deploy image classification models"
linkTitle: "Train and deploy classification models"
weight: 50
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's machine learning capabilities to train image classification models and deploy these models to your machines."
image: "/ml/training.png"
imageAlt: "Machine Learning"
images: ["/ml/training.png"]
---

Create and deploy an image classification model onto your machine with Viam's machine learning (ML) capabilities.
Manage the classification model fully on one platform: collect data, create a dataset and label it, train the model, and deploy it.
Then, test if your model works for classifying objects in a camera stream or existing images with the `mlmodel` classification model of vision service.

<table>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Collect data">}}
      <b>1. Collect</b>
      <p>Start by collecting images from your cameras with the <a href="/data/">data management service</a>. You can <a href="/data/view/">view the data</a> on the <b>Data tab</b>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/label.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Label data">}}
      <b>2. Create a Dataset and Label</b>
      <p>Once you have enough images of the objects you'd like to classify, <a href="/data/dataset/">label your data and create a dataset</a> in preparation for training classification models.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/train.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Train models">}}
      <b>3. Train or upload an ML model</b>
      <p>Use your labeled data to <a href="/ml/train-model/">train your own models</a> for object classification using data from the <a href="/data/">data management service</a>, or <a href="/ml/upload-model/">add an existing model</a>.</p>
    </th>
  </tr>
  <tr>
    <td>
      <b>4. Deploy your ML model</b>
      <p>To make use of ML models with your machine, use the built-in <a href="/ml/">ML model service</a> to deploy and run the model.</p>
    </td>
  </tr>
  <tr>
    <td>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Configure a service">}}
      <b>5. Configure a service</b>
      <p>For object classification, you can use the <a href="/ml/vision/">vision service</a>, which provides an <a href="/ml/vision/classification/#configure-an-mlmodel-classifier">ml model classifier</a> model.</p>
</td>
  </tr>
  <tr>
    <td>{{<imgproc src="ml/deploy.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Deploy your model">}}
      <b>6. Test your classifier</b>
      <p>Test your <a href="/ml/vision/classification/#test-your-classifier">mlmodel classifier</a> with <a href="/ml/vision/classification/#existing-images-in-the-cloud">existing images in the Viam app</a>, <a href="/ml/vision/classification/#live-camera-footage">live camera footage,</a> or <a href="/ml/vision/classification/#existing-images-on-your-machine">existing images on a computer</a>.</p>
    </td>
  </tr>
</table>

## Next steps

After testing your classifier, see the following to further explore Viam's data management and computer vision capabilities:

- [Export Data Using the Viam CLI](/data/export/): Export your synced data from the Viam cloud.
- [2D Object Detection](/ml/vision/detection/): Configure your machine's camera to draw a bounding box around detected objects, based on a machine learning model.
- [Update an existing ML model](/ml/train-model/#train-a-new-version-of-a-model): Refine an existing ML model you have trained, and select which model version to deploy.

You can also explore our [tutorials](/tutorials/) for more ideas.
