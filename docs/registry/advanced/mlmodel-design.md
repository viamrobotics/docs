---
title: "Design your ML Models for Vision"
linkTitle: "ML Model Design"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training", "vision"]
description: "Design your ML Model service to work with Viam's vision services."
icon: true
images: ["/services/icons/ml.svg"]
# SME: Bijan Haney
---

The [Machine Learning (ML) model service](/ml/) allow you to deploy machine learning models to your smart machine.
Vision services, like [an `"mlmodel"` detector](/ml/vision/mlmodel/) or [classifier](/ml/vision/mlmodel/), enable your machines to identify and classify objects in images with the deployed models' predictions.

The two services work closely together, with the vision service relying on the deployed ML model to make inferences.
If you are [designing your own ML Model service](/registry/), you must try to make your ML models' shapes match the input and output tensors the `mlmodel` vision service expects to work with if you want the two services to coordinate in classification or detection.

To be able to use a deployed ML model, the `mlmodel` vision service checks for descriptions of these characteristics in the [metadata](/ml/deploy/#metadata) of the model, as defined in [the Python SDK](https://python.viam.dev/autoapi/viam/gen/service/mlmodel/v1/mlmodel_pb2/index.html#viam.gen.service.mlmodel.v1.mlmodel_pb2.Metadata).
For an example of this, see [Example Metadata](#example-metadata).

## Input tensor: `input_info` in metadata

For both [classification](/ml/vision/mlmodel/) and [detection](/ml/vision/mlmodel/) models, the vision service sends a single input tensor to the ML Model with the following structure:

- One input tensor called `"image"` with type `uint8` or `float32` and shape `(1, height, width, 3)`, with the last channel `3` being the RGB bytes of the pixel.
- If image `height` and `width` are unknown or variable, then `height` and/or `width` `= -1`. During inference runtime the image will have a known height and width.

## Output tensors: `output_info` in metadata

Data can be returned by the ML model in many ways, due to the variety of machine learning models for computer vision.
The vision service will try to take into account many different forms of models as specified by the metadata of the model.
If the model does not provide metadata, the vision service will make the following assumptions:

For [classifications](/ml/vision/#classifications):

- The model returns 1 tensor, called `"probability"` with shape `(1, n_classifications)`
- The data is floating point numbers representing probability, between `0` and `1`.
- If the data is not between `0` and `1`, the vision service computes a softmax over the data, resulting in floating point numbers between `0` and `1` representing probability.

For [detections](/ml/vision/#detections):

- The model returns 3 tensors
  1. `"Location"`: the bounding boxes
     - Shape: `(1, n_detections, 4)`
     - Bounding boxes each have shape `(xmin, ymin, xmax, ymax)`
     - Bounding boxes are the proportion of where the box corner is in the image, using a number between `0` and `1`.
  2. `"Category"`: the labels on the boxes
     - Shape: `(1, n_detections)`
     - Integers representing the index of the label.
  3. `"Score"`: The confidence scores of the label
     - Shape: `(1, n_detections)`
     - Floating point numbers representing probability, between `0` and `1`.

For labels:

- Many computer vision models have an associated 'labelfile.txt' that lists the class labels associated with the model.
  To get those labels associated with the model, currently the vision service looks at the first element of the `output_info` list in the ML models' metadata and checks for a key called `"labels"` in its `"extra"` struct.
  The value of that key should be the full path to the label file on the machine.
  See [Example Metadata](#example-metadata) for an example of this.

  ```sh {class="command-line" data-prompt="$"}
  label_path = ml_model_metadata.output_info.extra["labels"]
  ```

### Example metadata

For example, a TF lite detector model that works with the vision service is structured with the following [metadata](/ml/deploy/#metadata):

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
