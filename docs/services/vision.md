---
title: Vision Service Documentation
summary: Explanation of the vision service, its configuration, its functionality, and its interfaces.
authors:
    - Matt Dannenberg
    - Bijan Haney
date: 2022-05-19
---
# The Viam Vision Service

## Intro and Summary

The vision service enables the robot to use its on-board cameras to intelligently see and interpret the world around it. The current features available through the vision service are:

* **2D Object detection:** Allows a user to get bounding boxes around identified objects in a 2D image according to a user-defined algorithm. 
* **3D Object segmentation**: Allows a user to get point clouds of identified objects in a 3D image according to a user-defined algorithm.

The vision service is a default service on the robot, and can be initialized without attributes. 


## 2D Object Detection

2D Object Detection is the process of taking a 2D image from a camera and identifying and drawing a box around the distinct “objects” of interest in the scene. 

What an object “is” depends on what is required for the task at hand. To accommodate the open-endedness of what kind of object a user may need to identify, the service provides different types of detectors, both heuristic and machine-learning based, so that users can create, register, and use detectors suited for their own purposes.

### Hardware

Any camera that can return 2D images can use 2D object detection. This essentially means that the driver for the camera implements the `get_frame` method. 
The Viam platform natively supports the following models of camera:  

* `webcam`

### Configuring your detectors

To add a detector to your robot, you need to add the _name_, _type_, and _parameters_ of the desired detector to the “register_detectors” field in the attributes field of the vision service config. 

```
"services": [
    {
        "type": "vision",
        "attributes": {
          "register_detectors": [
            {
              "name": "my_color_detector", 
              "type": "color",
              "parameters": {
                "detect_color" : "#A3E2FF",
                "tolerance": 0.06,
                "segment_size": 100
              }
            },
            {
              "name": "my_tflite_detector", 
              "type": "tflite",
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
### Detector Types
The types of the detector supported are:

* **color**: this is a heuristic based detector that draws boxes around objects according to their hue (does not detect black and white).
* **tflite**: this a machine-learning based detector that draws bounding boxes according to the specified tensorflow-lite model file available on the robot’s hard drive. 

#### Color detector attributes

* **detect_color**: the color to detect in the image, as a string of the form #RRGGBB. The color is written as a hexadecimal string prefixed by ‘#’.
* **tolerance**: A number between 0.0 and 1.0 and defines how strictly the detector must match to the color requested. 0.0 means the color must match exactly, while 1.0 will match to every color, regardless of the input color.  0.05 is a good starting value.
* **segment_size:** An integer that sets a minimum size (in pixels) of the returned objects, and filters out all other found objects below that size. 

#### TFLite detector attributes 

* **model_path**: The path to the .tflite model file, as a string. This attribute is absolutely required.
* **num_threads**: An integer that defines how many CPU threads to use to run inference. The default value is 1.
* **label_path**: The path to a .txt file that holds class labels for your TFLite model, as a string. The text file is 
expected to be an ordered listing of the class labels.


### The Detection API 

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation for the API.

### Detections

The returned detections consist of the bounding box around the found object, as well as its label and confidence score.

* `x_min`, `y_min`, `x_max`, `y_max` (int): These specify the bounding box around the object.
* `class_name` (string): specifies the label of the found object.
* `confidence` (float): specifies the confidence of the assigned label between 0.0 and 1.0.


## 3D Object Segmentation

3D object segmentation returns a list of the found “objects”. This is a list of point clouds with associated meta-data, like the label, the 3D bounding box and center coordinate of the object. Future updates to the service may return more information about the objects.

The segmentation feature requires 

1. A camera that can provide 3D data,
2. The name of the segmenter to be used, and 
3. The parameters necessary to specify/fine-tune the segmenter

### Hardware

Any camera that can return 3D pointclouds can use 3D object segmentation. This essentially means that the driver for the camera implements the `get_pointcloud` method. There are some segmenter types that base their segmentation algorithm on detections. For these types of segmenters, the `get_frame` method must also be implemented.

### Default Segmenters

There are two segmenter options currently available by default, the **radius_clustering** segmenter, and any detector you added in the "register_detectors" field.

#### radius_clustering (slow - expect 30s of waiting)

Radius_clustering is a segmenter that finds well separated objects above a flat plane. It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.  The segmenter requires 3 parameters. Unfortunately it is a bit slow, and can take up to 30s to segment the scene.

1. **min_points_in_plane**
    * min_points_in_plane is an integer that specifies how many points there must be in a flat surface for it to count as a plane. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps.
2. **min_points_in_segment**
    * min_points_in_segment is an integer that sets a minimum size to the returned objects, and filters out all other found objects below that size. 
3. **clustering_radius_mm**
    * clustering_radius_mm is a floating point number that specifies how far apart points can be (in units of  mm) in order to be considered part of the same object. A small clustering radius will more likely split different parts of a large object into distinct objects. A large clustering radius may aggregate closely spaced objects into one object.
    * 3.0 is an all right starting value.
4. **Mean_k_filtering (optional)**
    * mean_k_filtering is an integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the number of min_points_in_segment. 
    * Start with 5% and go up if objects are still too noisy.
    * If you don’t want to use the filtering, set the number to 0 or less.

#### Detector Segmenters

Any detector has all the information needed to also be a segmenter. Any detector defined in “register_detectors” field or added later to the vision service becomes a segmenter with the same name. It begins with finding the 2D bounding boxes, and then returns the list of 3D point cloud projection of the pixels within those bounding boxes.

1. **mean_k**
    * Mean_k  is an integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the number of min_points_in_segment. 
    * Start with 5% and go up if objects are still too noisy.
    * If you don’t want to use the filtering, set the number to 0 or less.
2. **sigma**
    * Sigma is a floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 
    * 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. 

### The Segmentation API

Check out the [Python SDK](https://python.viam.dev/autoapi/viam/services/vision/index.html) documentation for the API.

### Segmentation within the web UI

![segmentation](https://user-images.githubusercontent.com/8298653/173641977-4f34c1f9-5f31-4579-82bb-06b739f03eac.gif)

1. Click on the 3D img of a given camera to load the point cloud view.
2. Select your segmenter of interest - that will populate the list of necessary parameters that need to be filled in to use the segmenter.
3. Fill in the segmenter parameters (explanation of fields for each segmenter are in the next section)
4. Click Find Segments and wait for the segments to load
5. A list of the found objects will appear below the Find Segments button. 


