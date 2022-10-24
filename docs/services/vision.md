---
title: "Vision Service"
linkTitle: "Vision"
weight: 90
type: "docs"
description: "Explanation of the vision service, its configuration and its functionality."
---
## Intro and Summary

The vision service enables the robot to use its on-board cameras to intelligently see and interpret the world around it.  We're here to help you with everything that happens _after_ you have your image data.


Currently, there are three operations available through the vision service:

* **Detection (or 2D object detection)**: Allows a user to get bounding boxes around identified objects in a 2D image according to a user-defined algorithm. Many detection algorithms also include class label and confidence as output.
   
* **Classification (or 2D image classification)**: Allows a user to get a class label and confidence score associated with a 2D image according to a user-defined algorithm.

* **Segmentation (or 3D object segmentation)**: Allows a user to get point clouds of identified objects in a 3D image according to a user-defined algorithm.

The vision service is a default service on the robot, and can be initialized without attributes.

There is a public repo with examples of how to use the vision service on <a href="https://github.com/viamrobotics/vision-service-examples" target="_blank">ht<span></span>tps://github.com/viamrobotics/vision-service-examples</a>, as well.


## VisModels

| Operation         | VisModelType                                  | Parameters                                   |
| ----------------- | --------------------------------- | ---------------------------------- |
| Detection         | tflite\_detector   | "model\_path", "label\_path", "num\_threads" |
|| tf\_detector      | TBD - Not yet supported                       |
|| color\_detector   | "detect\_color", "tolerance\_pct", "segment\_size\_px" |
| Classification    | tflite\_classifier | "model\_path", "label\_path", "num\_threads" |
|| tf\_classifier    | TBD - Not yet supported                       |
| Segmentation      | radius\_clustering\_segmenter | "min\_points\_in\_plane", "min\_points\_in\_segment", "clustering\_radius\_mm", "mean\_k\_filtering"      |
|| detector\_segmenter |  "detector\_name", "confidence\_threshold\_pct", "mean\_k", "sigma" |

More about the parameters and model types can be found under the corresponding operation below.


## Configuring your VisModels

To add a vision model to your robot, you need to add the _name_, _type_, and _parameters_ of the desired detector to the “register_models” field in the attributes field of the vision service config. If you're using the "Config > Services" tab on Viam, you'll see that adding a vision service invites you to directly fill in the "attributes."

``` json
"services": [
    {
        "name": " ",
        "type": "vision",
        "attributes": {
          "register_models": [
            {
              "name": "my_color_detector", 
              "type": "color_detector",
              "parameters": {
                "detect_color" : "#A3E2FF",
                "hue_tolerance_pct": 0.06,
                "segment_size_px": 100
              }
            },
            {
              "name": "my_classifier", 
              "type": "tflite_classifier",
              "parameters": {
                "model_path" : "/path/to/model.tflite",
                "label_path": "/path/to/labels.txt",
                "num_threads": 1
              }
            }
          ]
        }
    }
]
```

## Detection

__2D Object Detection__ is the process of taking a 2D image from a camera and identifying and drawing a box around the distinct “objects” of interest in the scene. Any camera that can return 2D images can use 2D object detection.

What an object “is” depends on what is required for the task at hand.
To accommodate the open-ended-ness of what kind of object a user may need to identify, the service provides different types of detectors, both heuristic and machine-learning based, so that users can create, register, and use detectors suited for their own purposes.

### The Detection API

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation for the API.

#### Detections
The returned detections consist of the bounding box around the found object, as well as its label and confidence score.

* `x_min`, `y_min`, `x_max`, `y_max` (int): These specify the bounding box around the object.
* `class_name` (string): specifies the label of the found object.
* `confidence` (float): specifies the confidence of the assigned label between 0.0 and 1.0.

### Detector Types
The types of the detector supported are:

* **color_detector**: this is a heuristic based detector that draws boxes around objects according to their hue (does not detect black, gray, and white).
* **tflite_detector**: this a machine-learning based detector that draws bounding boxes according to the specified tensorflow-lite model file available on the robot’s hard drive.


#### Color detector parameters

NOTE: **Color detector does not detect black, gray and white. It only detects hues found on the color wheel.**

* **detect_color**: the color to detect in the image, as a string of the form #RRGGBB.
The color is written as a hexadecimal string prefixed by ‘#’.
* **hue_tolerance_pct**: A number > 0.0 and <= 1.0 and defines how strictly the detector must match to the hue of the color requested.
~0.0 means the color must match exactly, while 1.0 will match to every color, regardless of the input color.
0.05 is a good starting value.
* **segment_size_px:** An integer that sets a minimum size (in pixels) of a contiguous color region to be detected, and filters out all other found objects below that size.
* **saturation_cutoff_pct (optional)**: A number > 0.0 and <= 1.0 which defines the minimum saturation before a color is ignored. Defaults to 0.2.
* **value_cutoff_pct (optional)**: A number > 0.0 and <= 1.0 which defines the minimum value before a color is ignored. Defaults to 0.3.

#### TFLite detector parameters
* **model_path**: The path to the .tflite model file, as a string.
This attribute is absolutely required.
* **num_threads**: An integer that defines how many CPU threads to use to run inference.
The default value is 1.
* **label_path**: The path to a .txt file that holds class labels for your TFLite model, as a string.
The SDK expects this text file to contain an ordered listing of the class labels.
Without this file, classes will read “1”, “2”, etc.


##### TFLite Model Limitations
We strongly recommend that you package your .tflite model with metadata in the standard form given by the schema (<a href="https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs" target="_blank">found here</a>[^schema]). In the absence of metadata, your TFLite model must satisfy the following requirements:

1. A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1) 
1. At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
1. Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y. Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1. Feel free to use one of these architectures or build your own! 

[^schema]: TFLite schema: <a href="https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs" target="_blank">ht<span></span>tps://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs</a>

## Classification

__2D Image Classification__ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.  Any camera that can return 2D images can use 2D image classification.

Which class labels may be considered for classification varies and will depend on the machine learning model and how it was trained.

### The Classification API

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation for the API.

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
Without this file, classes will read “1”, “2”, etc.



## Segmentation

__3D Object Segmentation__ is the process of separating and returning a list of the found “objects” from a 3D scene.  The "objects" are a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinate of the object.   Future updates to the service may return more information about the objects.

Any camera that can return 3D pointclouds can use 3D object segmentation.


### The Segmentation API

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation for the API.

You can also build Segmenters from the **Control** tab in Viam, as well.

1. Click on a camera that supports 3D data to load the point cloud view.
2. Select your segmenter model of interest - that will populate the list of necessary parameters that need to be filled in to use the segmenter.
3. Fill in the segmenter parameters (explanation of fields for each segmenter are in the next section).
4. Click **Add Segmenter**.
4. Then select your added segmenter by name, and click **Find Segments** and wait for the segments to load.
5. A list of the found objects will appear below the **Find Segments** button.


### Segmenter Types
The types of segmenters supported are:

* **radius_clustering_segmenter**: Radius\_clustering is a segmenter that finds well separated objects above a flat plane.  It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.  Unfortunately it is a bit slow, and can take up to 30s to segment the scene.
*  **detector_segmenter**: Object segmenters are automatically created from detectors in the vision service.  Any registered detector "x" defined in “register\_models” field or added later to the vision service becomes a segmenter with the name "x\_segmenter".  It begins by finding the 2D bounding boxes, and then returns the list of 3D point cloud projection of the pixels within those bounding boxes.

#### Radius Clustering Segmenter parameters

* **min_points_in_plane** is an integer that specifies how many points there must be in a flat surface for it to count as a plane.  This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps.
* **min_points_in_segment** is an integer that sets a minimum size to the returned objects, and filters out all other found objects below that size.
* **clustering_radius_mm** is a floating point number that specifies how far apart points can be (in units of  mm) in order to be considered part of the same object.  A small clustering radius will more likely split different parts of a large object into distinct objects.  A large clustering radius may aggregate closely spaced objects into one object.
    * 3.0 is a decent starting value.
 * **mean_k_filtering (optional)** is an integer parameter used in <a href="https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html" target="_blank">a subroutine to eliminate the noise in the point clouds</a>[^mkf].  It should be set to be 5-10% of the number of min_points_in_segment.
    * Start with 5% and go up if objects are still too noisy.
    * If you don’t want to use the filtering, set the number to 0 or less.
	
[^mkf]: Mean K: <a href="https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html" target="_blank">ht<span></span>tps://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html</a>
    

#### Detector Segmenters

* **detector_name** is the name of the detector already registered in the vision service that will be turned into a segmenter.
* **confidence_threshold_pct** is a number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5.
* **mean_k** is an integer parameter used in <a href="https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html" target="_blank">a subroutine to eliminate the noise in the point clouds</a>[^mkf].  It should be set to be 5-10% of the minimum segment size.
    * Start with 5% and go up if objects are still too noisy.
    * If you don’t want to use the filtering, set the number to 0 or less.
* **sigma** is a floating point parameter used in <a href="https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html" target="_blank">a subroutine to eliminate the noise in the point clouds</a>[^mkf].
    It should usually be set between 1.0 and 2.0.
    * 1.25 is usually a good default.
    If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower.
