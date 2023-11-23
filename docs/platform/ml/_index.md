---
title: "Machine Learning"
linkTitle: "Machine Learning"
weight: 40
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's built-in machine learning capabilities to train image classification models and deploy these models to your machines."
image: "/platform/ml/training.png"
imageAlt: "Machine Learning"
images: ["/platform/ml/training.png"]
aliases:
  - /manage/ml/
# SME: Aaron Casas
---

{{<imgproc src="/platform/ml/training.png" class="alignright" resize="400x" declaredimensions=true alt="ML training">}}

Viam includes a built-in [machine learning (ML) service](/platform/build/configure/services/ml/) which provides your robot with the ability to learn from data and adjust its behavior based on insights gathered from that data.
Common use cases include:

- Object detection and classification which enable machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Speech recognition, natural language processing, and speech synthesis, which enable machines to verbally communicate with us.

However, your robot can make use of machine learning with nearly any kind of data.

Viam natively supports [TensorFlow Lite](https://www.tensorflow.org/lite) ML models as long as your models adhere to the [model requirements](/platform/build/configure/services/ml/#tflite_cpu-limitations).

## Use machine learning with your machine

<table>
  <tr>
    <th>{{<imgproc src="/platform/ml/collect.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Collect data">}}
      <b>1. Collect</b>
      <p>Start by collecting data from your cameras, sensors, or any other source on your machine with the <a href="/platform/build/configure/services/data/">data management service</a>. You can <a href="/platform/data/view/">view the data</a> on the <b>Data tab</b>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/platform/ml/label.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Label data">}}
      <b>2. Create a Dataset and Label</b>
      <p>Once you have collected data, <a href="/platform/data/dataset/">label your data and create a dataset</a> in preparation for training machine learning models.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/platform/ml/train.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Train models">}}
      <b>3. Train or upload an ML model</b>
      <p>Use your labeled data to <a href="/platform/ml/train-model/">train your own models</a> for object detection and classification using data from the <a href="/platform/build/configure/services/data/">data management service</a> or <a href="/platform/ml/upload-model/">add an existing model</a>.</p>
    </th>
  </tr>
  <tr>
    <td>
      <b>4. Deploy your ML model</b>
      <p>To make use of ML models with your machine, use the built-in <a href="/platform/build/configure/services/ml/">ML model service</a> to deploy and run the model.</p>
    </td>
  </tr>
  <tr>
    <td>{{<imgproc src="/platform/ml/configure.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Configure a service">}}
      <b>5. Configure a service</b>
      <p>For object detection and classification, you can use the <a href="/platform/build/configure/services/vision/">vision service</a>, which provides an <a href="/platform/build/configure/services/vision/detection/#configure-an-mlmodel-detector">ml model detector</a> and an <a href="/platform/build/configure/services/vision/classification/#configure-an-mlmodel-classifier">ml model classifier</a> model.</p>
      <p>For other usage, you can use a <a href="/platform/registry/">modular resource</a> to integrate it with your robot.</p>
</td>
  </tr>
  <tr>
    <td>{{<imgproc src="platform/ml/deploy.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Deploy your model">}}
      <b>6. Test your detector or classifier</b>
      <p>Test your <a href="/platform/build/configure/services/vision/detection/#test-your-detector">mlmodel detector</a> or <a href="/platform/build/configure/services/vision/classification/#test-your-classifier">mlmodel classifier</a>.</p>
    </td>
  </tr>
</table>

## Tutorials

{{< cards >}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{% card link="/platform/registry/examples/tflite-module/" %}}
{{< /cards >}}
