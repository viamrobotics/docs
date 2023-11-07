---
title: "Design your ML Model to work with Viam's Vision Services"
linkTitle: "ML Model Design"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Design your ML Model service to work with Viam's vision services."
icon: "/services/icons/ml.svg"
# SME: Bijan Haney
---

Models of Viam's Machine Learning (ML) model service, like `"tflite_cpu"`, allow you to deploy machine learning models to your smart machine.
Vision services, like [an `"mlmodel"` detector](/services/vision/detection/#configure-an-mlmodel-detector) or [classifier](/services/vision/classification/#configure-an-mlmodel-classifier) enable you to identify and classify objects in a camera stream with the predictions those deployed models make.

The two services work closely together, with the vision service relying on the deployed ML model to make inferences, and if [designing your own ML Model service](/modular-resources/) to add to [the Registry](https://app.viam.com/registry), you must try to conform your models' shapes to the input and output tensors the vision service expects to work with.

## Input tensor

For both [classification](/services/vision/classification/) and [detection](/services/vision/detection/) models, the vision service sends an input tensor to the ML Model with the following structure:

- One input tensor called `"image"` with shape `(1, image_height, image_width, 3)`, with the last channel being the RGB bytes of the pixel.

## Output tensors

There are many ways data can be returned by the ML Model, due to the variety of machine learning models for computer vision.
While the vision service tries to take into account many different forms of models by looking at the metadata of the model, if the model does not provide metadata, the vision service will make guesses.
If you need to add structure and metadata, output that is organized in terms of the "ideal guess" will work out of the box.

The ideal guesses are made in the following ways:

For [classifications](/services/vision/classification/):

- The model returns 1 tensor, called `"probability"` with shape `(1, n_classifications)`
- The data is floating point numbers representing probability, between `0` and `1`.

For [detections](/services/vision/detection/):

- The model returns 3 tensors
  1. "Location": the bounding boxes
     1. Shape: `(1, n_detections, 4)`
     2. Bounding boxes each have shape `(xmin, ymin, xmax, ymax)`
     3. Bounding boxes are the proportion of where the box corner is in the image, using a number between `0` and `1`.
  2. "Category": the labels on the boxes
     1. Shape: `(1, n_detections)`
     2. Integers representing the index of the label
  3. "Score": The confidence scores of the label
     1. Shape: `(batch, n_detections)`
     2. Floating point numbers representing probability, between `0` and `1`
