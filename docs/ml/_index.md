---
title: "Machine Learning"
linkTitle: "Machine Learning"
weight: 450
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's built-in machine learning capabilities to train image classification models and deploy these models to your machines."
images: ["/platform/ml.svg"]
aliases:
  - /manage/ml/
menuindent: true
# SME: Aaron Casas
---

{{<imgproc src="/ml/training.png" class="alignright" resize="400x" declaredimensions=true alt="ML training">}}

Machine Learning (ML) provides your machines with the ability to adjust its behavior based on models that recognize patterns or make predictions.
Common use cases include:

- Object detection and classification which enable machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Speech recognition, natural language processing, and speech synthesis, which enable machines to verbally communicate with us.

However, your machine can make use of machine learning with nearly any kind of data.

To use machine learning (ML), you must deploy an [ML model service](/ml/deploy/) which runs a specified ML model.

Viam natively supports [TensorFlow Lite](https://www.tensorflow.org/lite) ML models with the `tflite_cpu` ML model service, as long as your models adhere to the [model requirements](/ml/deploy/#tflite_cpu-limitations).
Other model frameworks are supported with [modular resources](/ml/deploy/#modular-resources).

Once you have deployed a model with the ML model service you can use it with the [vision service](/ml/vision) or other modular resources from the [registry](/registry) that make use of the ML model service.

## Use machine learning with your machine

<table>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Collect data">}}
      <b>1. Collect</b>
      <p>Start by collecting data from your cameras, sensors, or any other source on your machine with the <a href="/data/">data management service</a>. You can <a href="/data/view/">view the data</a> on the <b>Data tab</b>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/label.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Label data">}}
      <b>2. Create a dataset and label</b>
      <p>Once you have collected data, <a href="/data/dataset/">label your data and create a dataset</a> in preparation for training machine learning models.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/train.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Train models">}}
      <b>3. Train or upload an ML model</b>
      <p>Use your labeled data to <a href="/ml/train-model/">train your own model</a> for object detection or classification</a>. If you don't want to train your own model, you can also <a href="/registry/">use an ML model from the registry</a> or <a href="/ml/upload-model/">upload an existing model</a>.</p>
    </th>
  </tr>
  <tr>
    <td>
      <b>4. Deploy your ML model</b>
      <p>To use ML models with your machine, you must first deploy the model using the built-in <a href="/ml/deploy/">ML model service</a>. The ML model service will run the model and allow the vision service to use it.</p>
    </td>
  </tr>
  <tr>
    <td>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 300px" declaredimensions=true alt="Configure a service">}}
      <b>5. Configure a vision service</b>
      <p>For object detection and classification, use the <a href="/ml/vision/mlmodel/"><code>mlmodel</code> detector or the <code>mlmodel</code> classifier</a> from the <a href="/ml/vision/">vision service</a>. The <code>mlmodel</code> vision service uses the ML model that you deployed with the ML model service in step 4.</p>
      <p>If you have another use case, you can use a <a href="/registry/">modular resource</a> to create a custom ML model service or a custom vision service for your machine.</p>
</td>
  </tr>
  <tr>
    <td>{{<imgproc src="ml/deploy.svg" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="Deploy your model">}}
      <b>6. Test your detector or classifier</b>
      <p>Follow the <a href="/ml/vision/mlmodel/#test-your-detector-or-classifier">instructions to test your <code>mlmodel</code> detector or classifier</a>.</p>
    </td>
  </tr>
</table>

## Tutorials

{{< cards >}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{% card link="/registry/examples/tflite-module/" %}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
