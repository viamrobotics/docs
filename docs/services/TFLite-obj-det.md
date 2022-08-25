---
title: TFLite Object Detector
summary: Explanation of the motion service, its configuration, its functionality, and its interfaces.
authors:
    - Khari Jarrett
date: 2022-07-26
---
# The TFLite Object Detector

The TFLite Object Detector leverages TensorflowLite and the power of machine learning to draw boxes around objects of interest. 
The objects of interest are defined by your actual ML model (.tflite file). 
The parameters for the TFLite detector are:

* **model_path**, a string that is the absolute file path to the .tflite model
* **num_threads**, an integer denoting the number of CPU threads to use. Default = 1.
* **label_path**, a string that is the absolute file path to a .txt file containing an ordered listing of the class labels. Without this file, classes will read “1”, “2”, etc.


## Model Limitations

We strongly recommend that you package your .tflite model with metadata in the standard form given by the schema (link schema). In the absence of metadata, your TFLite model must satisfy the following requirements:

1. A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1) 
1. At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
1. Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y. Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1. Feel free to use one of these architectures or build your own! 
