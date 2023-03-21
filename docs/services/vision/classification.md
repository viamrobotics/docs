---
title: "Classification (or 2D image classification)"
linkTitle: "Classification"
weight: 20
type: "docs"
description: "Select an algorithm that outputs a class label and confidence score associated with a 2D image."
tags: ["vision", "computer vision", "CV", "services", "classification"]
# SMEs: Bijan, Khari
---

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

Which class labels may be considered for classification varies and will depend on the machine learning model and how it was trained.

### Classification API

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation or the [Go RDK docs](https://pkg.go.dev/go.viam.com/rdk/vision) for the API.

#### Classification

The returned classifications consist of the image's class label and confidence score.

* `class_name` (string): specifies the label of the found object.
* `confidence` (float): specifies the confidence of the assigned label between 0.0 and 1.0.

### Classifier Types

The types of classifiers supported are:

* **tflite_classifier**: this a machine-learning based classifier that returns a class label and confidence score according to the specified tensorflow-lite model file available on the robot’s hard drive.

#### TFLite classifier parameters

* **model_path**: The path to the .tflite model file, as a string.
This attribute is absolutely required.
* **num_threads**: An integer that defines how many CPU threads to use to run inference.
The default value is 1.
* **label_path**: The path to a .txt file that holds class labels for your TFLite model, as a string.
The SDK expects this text file to contain an ordered listing of the class labels.
Without this file, classes will read "1", "2", and so on.
