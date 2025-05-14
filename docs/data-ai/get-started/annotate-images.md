---
linkTitle: "Annotate"
title: "Annotate"
weight: 40
layout: "docs"
type: "docs"
description: "Annotate images with class tags and bounding box labels"
---

Use the interface on the [**DATA** page](https://app.viam.com/data/view) to annotate your images.
Always follow best practices when you label your images:

More data means better models

: Incorporate as much data as you practically can to improve your model's overall performance.

Include counterexamples

: Include images with and without the object you’re looking to classify.
This helps the model distinguish the target object from the background and reduces the chances of false positives by teaching the model what the object is _not_.

Avoid class imbalance

: Don't train excessively on one specific type or class, make sure each category has a roughly equal number of images.
For instance, if you're training a dog detector, include images of various dog breeds to avoid bias towards one breed.
An imbalanced dataset can lead the model to favor one class over others, reducing its overall accuracy.

Match training images to intended use case

: Use images that reflect the quality and conditions of your production environment.
For example, if you plan to use a low-quality camera in production, train with low-quality images.
Similarly, if your model will run all day, capture images in daylight, nighttime, dusk, and dawn conditions.

Vary angles and distances

: Include image examples from every angle and distance that you expect the model to handle.

Viam enables you to annotate images for the following machine learning methods:

{{< tabs >}}
{{% tab name="Classification" %}}

Classification determines a descriptive tag or set of tags for an image.
For example, classification could help you identify:

- whether an image of a food display appears `full`, `empty`, or `average`
- the quality of manufacturing output: `good` or `bad`
- what combination of toppings exists on a pizza: `pepperoni`, `sausage` and `pepper`, or `pineapple` and `ham` and `mushroom`

Viam supports single and multiple label classification.
To create a training set for classification, annotate tags to describe your images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Object detection" %}}

Object detection identifies and determines the location of certain objects in an image.
For example, object detection could help you identify:

- how many `pizza` objects appear on a counter
- the number of `bicycle` and `pedestrian` objects on a greenway
- which `plant` objects are popular with `deer` in your garden

To create a training set for object detection, annotate bounding boxes to teach your model to identify objects that you want to detect in future images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-magnemite.webm" mp4_src="/services/data/label-magnemite.mp4" alt="Add a bounding box around the magnemite pokemon in an image">}}

{{< alert title="Tip" color="tip" >}}

Once created, you can move, resize, or delete the bounding box.
{{< /alert >}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{< /tabs >}}
