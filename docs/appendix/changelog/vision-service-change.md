---
title: Vision service
date: "2023-04-01"
color: "changed"
---

{{% alert title="Important: Breaking Change" color="note" %}}

The [vision service](/ml/vision/) became more modular in RDK [v0.2.36](https://github.com/viamrobotics/rdk/releases/tag/v0.2.36), API [v0.1.118](https://github.com/viamrobotics/api/releases/tag/v0.1.118), and Python SDK [v0.2.18](https://github.com/viamrobotics/viam-python-sdk/releases/tag/v0.2.18).

Find more information on each of the changes below.

{{% /alert %}}

<!-- markdownlint-disable MD001 -->

#### Use individual vision service instances

You need to create **an individual vision service instance** for each detector, classifier, and segmenter model.
You can no longer be able to create one vision service and register all of your detectors, classifiers, and segmenters within it.

{{%expand "Click for details on how to migrate your code." %}}

#### API calls

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

{{< tabs >}}
{{% tab name="New Way" %}}

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

```python {class="line-numbers linkable-line-numbers"}
my_object_detector = VisionClient.from_robot(robot, "find_objects")
img = await cam.get_image()
detections = await my_object_detector.get_detections(img)
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```python {class="line-numbers linkable-line-numbers"}
vision = VisionServiceClient.from_robot(robot)
img = await cam.get_image()
detections = await vision.get_detections(img, "find_objects")
```

{{% /tab %}}
{{< /tabs >}}

#### Color detector configurations

You can replace existing color detectors by [configuring new ones in the UI](/ml/vision/mlmodel/) or you can update the [Raw JSON configuration of your machines](/build/configure/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "blue_square",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 100,
            "detect_color": "#1C4599",
            "hue_tolerance_pct": 0.07,
            "value_cutoff_pct": 0.15
        }
    },
    {
        "name": "green_triangle",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 200,
            "detect_color": "#62963F",
            "hue_tolerance_pct": 0.05,
            "value_cutoff_pct": 0.20
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "segment_size_px": 100,
                    "detect_color": "#1C4599",
                    "hue_tolerance_pct": 0.07,
                    "value_cutoff_pct": 0.15
                },
                "name": "blue_square",
                "type": "color_detector"
            },
            {
                "parameters": {
                    "segment_size_px": 200,
                    "detect_color": "#62963F",
                    "hue_tolerance_pct": 0.05,
                    "value_cutoff_pct": 0.20
                },
                "name": "green_triangle",
                "type": "color_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite detector configurations

You can replace existing TFLite detectors by [configuring new ones in the UI](/ml/vision/mlmodel/) or you can update the [Raw JSON configuration of your machines](/build/configure/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "person_detector",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/file.tflite",
            "label_path": "/path/to/labels.tflite",
            "num_threads": 1
        }
    },
    {
        "name": "person_detector",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "person_detector"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/file.tflite",
                    "label_path": "/path/to/labels.tflite",
                    "num_threads": 1
                },
                "name": "person_detector",
                "type": "tflite_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite Classifier configurations

You can replace existing TFLite classifiers by [configuring new ones in the UI](/ml/vision/mlmodel/) or you can update the [Raw JSON configuration of your machines](/build/configure/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "fruit_classifier",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/classifier_file.tflite",
            "label_path": "/path/to/classifier_labels.txt",
            "num_threads": 1
        }
    },
    {
        "name": "fruit_classifier",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "fruit_classifier"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/classifier_file.tflite",
                    "label_path": "/path/to/classifier_labels.txt",
                    "num_threads": 1
                },
                "name": "fruit_classifier",
                "type": "tflite_classifier"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Radius Clustering 3D segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/ml/vision/obstacles_pointcloud/) or you can update the [Raw JSON configuration of your machines](/build/configure/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "rc_segmenter",
        "type": "vision",
        "model": "obstacles_pointcloud"
        "attributes": {
            "min_points_in_plane": 1000,
            "min_points_in_segment": 50,
            "clustering_radius_mm": 3.2,
            "mean_k_filtering": 10
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "min_points_in_plane": 1000,
                    "min_points_in_segment": 50,
                    "clustering_radius_mm": 3.2,
                    "mean_k_filtering": 10
                },
                "name": "rc_segmenter",
                "type": "radius_clustering_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Detector to 3D segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/ml/vision/detector_3d_segmenter/) or you can update the [Raw JSON configuration of your machines](/build/configure/#the-config-tab):

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "my_segmenter",
        "type": "vision",
        "model": "detector_3d_segmenter"
        "attributes": {
            "detector_name": "my_detector",
            "confidence_threshold_pct": 0.5,
            "mean_k": 50,
            "sigma": 2.0
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "detector_name": "my_detector",
                    "confidence_threshold_pct": 0.5,
                    "mean_k": 50,
                    "sigma": 2.0
                },
                "name": "my_segmenter",
                "type": "detector_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand%}}

#### Add and remove models using the machine config

You must add and remove models using the [machine config](/build/configure/).
You will no longer be able to add or remove models using the SDKs.

#### Add machine learning vision models to a vision service

The way to add machine learning vision models is changing.
You will need to first register the machine learning model file with the [ML model service](/ml/) and then add that registered model to a vision service.
