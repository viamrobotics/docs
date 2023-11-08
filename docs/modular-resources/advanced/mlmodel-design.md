---
title: "Design your ML Models for Vision"
linkTitle: "Vision Service and Modular ML Model Design"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Design your ML Model service to work with Viam's vision services."
icon: "/services/icons/ml.svg"
# SME: Bijan Haney
---

Models of Viam's [Machine Learning (ML) model service](/services/ml/) allow you to deploy machine learning models to your smart machine.
Vision services, like [an `"mlmodel"` detector](/services/vision/detection/#configure-an-mlmodel-detector) or [classifier](/services/vision/classification/#configure-an-mlmodel-classifier), enable you to identify and classify objects in images with the predictions those deployed models make.

The two services work closely together, with the vision service relying on the deployed ML model to make inferences.
If [designing your own ML Model service](/modular-resources/) to add to [the Registry](https://app.viam.com/registry), you must try to make your ML models' shapes match the input and output tensors the vision service expects to work with if you want the two services to be able to work together out of the box.

To know what to expect, the vision service looks for descriptions of these characteristics in the [metadata](/services/mlmodel/#metadata) of the ML model, as defined in [the Python SDK](https://python.viam.dev/autoapi/viam/gen/service/mlmodel/v1/mlmodel_pb2/index.html#viam.gen.service.mlmodel.v1.mlmodel_pb2.Metadata).
For an example of this, see [Example Metadata](#example-metadata).

## Input tensor: `input_info` in metadata

For both [classification](/services/vision/classification/) and [detection](/services/vision/detection/) models, the vision service sends an input tensor to the ML Model with the following structure:

- One input tensor called `"image"` with type `uint8` or `float32` and shape `(1, height, width, 3)`, with the last channel, `3` being the RGB bytes of the pixel.
- If image `height` and `width` are unknown or variable, then `height` and/or `width` `= -1`. During inference runtime the image will have a known height and width.

## Output tensors: `output_info` in metadata

There are many ways data can be returned by the ML Model, due to the variety of machine learning models for computer vision.
While the vision service tries to take into account many different forms of models by looking at the metadata of the model, if the model does not provide metadata, the vision service will make guesses.
If you need to add structure and metadata, output that is organized in terms of the "ideal guess" will work out of the box.
The ideal guesses of the vision service are as follows:

For labels:

- To get labels that will be associated to classifications or detections, currently the vision service looks at the first element of the `output_info` list in the ML models' metadata and looks for a key called `"labels"` in its `"extra"` struct. The value of that key should be the full path to the label file on the robot.

    ```sh {class="command-line" data-prompt="$"}
    label_path = ml_model_metadata.output_info.extra["labels"]
    ```

For [classifications](/services/vision/classification/):

- The model returns 1 tensor, called `"probability"` with shape `(1, n_classifications)`
- The data is floating point numbers representing probability, between `0` and `1`.

For [detections](/services/vision/detection/):

- The model returns 3 tensors
  1. "Location": the bounding boxes
     - Shape: `(1, n_detections, 4)`
     - Bounding boxes each have shape `(xmin, ymin, xmax, ymax)`
     - Bounding boxes are the proportion of where the box corner is in the image, using a number between `0` and `1`.
  2. "Category": the labels on the boxes
     - Shape: `(1, n_detections)`
     - Integers representing the index of the label.
  3. "Score": The confidence scores of the label
     - Shape: `(batch, n_detections)`
     - Floating point numbers representing probability, between `0` and `1`.

### Example Metadata

For example, a TF lite detector model that works with the vision service is structured with the following [metadata](/services/ml/#metadata):

```json {class="line-numbers linkable-line-numbers"}
name: "EfficientDet Lite0 V1"
type: "tflite_detector"
description: "Identify which of a known set of objects might be present and provide information about their positions within the given image or a video stream."
input_info {
  name: "image"
  description: "Input image to be detected. The expected image is 320 x 320, with three channels (red, blue, and green) per pixel. Each value in the tensor is a single byte between 0 and 255."
  data_type: "uint8"
  shape: 1
  shape: 320
  shape: 320
  shape: 3
  extra {
  }
}
output_info {
  name: "location"
  description: "The locations of the detected boxes."
  data_type: "float32"
  extra {
    fields {
      key: "labels"
      value {
        string_value: "/Users/<username>/.viam/packages/.data/ml_model/effdet0-1685040512967/effdetlabels.txt"
      }
    }
  }
}
output_info {
  name: "category"
  description: "The categories of the detected boxes."
  data_type: "float32"
  associated_files {
    name: "labelmap.txt"
    description: "Label of objects that this model can recognize."
    label_type: LABEL_TYPE_TENSOR_VALUE
  }
  extra {
  }
}
output_info {
  name: "score"
  description: "The scores of the detected boxes."
  data_type: "float32"
  extra {
  }
}
output_info {
  name: "number of detections"
  description: "The number of the detected boxes."
  data_type: "float32"
  extra {
  }
}
```