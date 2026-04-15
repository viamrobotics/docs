---
linkTitle: "Deploy a custom model"
title: "Deploy a custom ML model"
weight: 14
layout: "docs"
type: "docs"
description: "Deploy a model you trained outside Viam (or trained yourself on Viam data) through an ML model service and use it with the vision service."
date: "2026-04-14"
---

Use this guide when you have a trained model file that is not already in the Viam [registry](https://app.viam.com/registry). That covers three cases:

- You trained the model on Viam data using [managed training](/train/train-a-model/) or a [custom training script](/train/custom-training-scripts/).
- You trained it entirely outside Viam (local, another cloud, a notebook).
- You found it elsewhere (GitHub, Hugging Face) and want to run it on your machines.

If you just want to pick a ready-made model from the [registry](https://app.viam.com/registry), see [Deploy an ML model from the registry](/vision/deploy-from-registry/) instead.

## 1. Confirm the model format is supported

Viam's ML model services support four model formats through module implementations. Your model must be in one of them:

- **TensorFlow Lite** (`.tflite`): uses [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu). Broadest hardware support; quantized models run on almost any CPU.
- **ONNX** (`.onnx`): uses [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu) or, for GPU on Jetson, [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack).
- **TensorFlow SavedModel**: uses [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu).
- **PyTorch** (`.pt`): uses [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu).

If your training workflow produces a different format (for example, Keras HDF5), convert to one of the supported formats before proceeding. TensorFlow Lite and ONNX are the most common targets because their runtimes are the lightest.

## 2. Meet the tensor shape and name requirements

The `mlmodel` vision service expects specific tensor conventions from the model it wraps. If the model does not match, the vision service fails to come up as a detector or classifier, or it comes up but produces garbled output.

**Detector models must expose:**

- Input tensor named `image` with shape `[batch, height, width, channels]`. The service feeds one image at a time.
- Output tensors named `location`, `category`, and `score`. Each is per-detection.

**Classifier models must expose:**

- Input tensor named `image` with the same shape.
- Output tensor named `probability`, one value per class.

**Preprocessing assumptions:**

- Input pixel values are uint8 in `[0, 255]` by default. If your model expects `[-1, 1]` or `[0, 1]` normalization, use [`input_image_mean_value` and `input_image_std_dev`](/vision/tune/#wrong-labels-or-every-label-fires) on the vision service.
- Input channel order is RGB by default. If your model expects BGR, set [`input_image_bgr: true`](/vision/tune/#wrong-labels-or-every-label-fires).
- Bounding boxes are `[xmin, ymin, xmax, ymax]` normalized to `[0, 1]`. If your model outputs a different order, use [`xmin_ymin_xmax_ymax_order`](/vision/tune/#bounding-boxes-appear-shifted-or-mirrored).

If your model disagrees with any of these assumptions, retraining is not required. Set the matching vision service attributes to bridge the gap. See [Tune detection quality](/vision/tune/).

**Tensor names:** if your model does not use the exact names above, you can remap them on the vision service without retouching the model. See [Tune detection quality](/vision/tune/#tensor-names-do-not-match).

## 3. Add the model to your organization

Models live at the organization level in Viam. Uploading a model is a one-time action per model version.

1. Navigate to the [**MODELS** tab](https://app.viam.com/models) in the Viam app.
2. Click **Upload**.
3. Choose **New model** (or **New version** if you are replacing an existing model). Under **Visibility**, choose **Private** for internal use or **Public** to publish to the [registry](https://app.viam.com/registry). Click **Next steps**.
4. Fill in the upload form:
   - **Model framework**: select the framework matching your model file (TFLite, TensorFlow, PyTorch, or ONNX).
   - Under **Upload files**, click **Choose model file** and pick your `.tflite`, `.onnx`, `.pt`, or framework-specific file. Click **Choose label file** and pick a `.txt` file with one label per line (optional but recommended; line number, zero-indexed, is the class ID).
   - **Model name**: a short identifier (letters, numbers, hyphens). This is what you will reference from the ML model service config.
   - **Task type**: pick **Object detection**, **Single label classification**, **Multi label classification**, or **Other**.
   - **Description**: one sentence describing the model.
5. Click **Upload model**.

The model is now available in your organization. You can change visibility between **Private** and **Public** later through the model's settings.

## 4. Configure the ML model service

On the machine you want the model to run on:

1. Open the **CONFIGURE** tab.
2. Click the **+** icon and select **Configuration block**.
3. In the search field, type the ML model service name matching your model's framework (for example, `tflite_cpu` for TFLite models) and select the matching result.
4. Click **Add component**, name the service (for example, `my-ml-model`), and click **Add component** again to confirm.
5. In the ML model service panel, click **Select model** and pick the model you just uploaded. Choose a version (or **Latest** during development).
6. Save.

Alternatively, if your model file lives on the machine's disk and you do not want to upload it to the cloud, point the ML model service directly at the local path:

```json
{
  "name": "my-ml-model",
  "api": "rdk:service:mlmodel",
  "model": "tflite_cpu",
  "attributes": {
    "model_path": "/home/viam/models/my_model.tflite",
    "label_path": "/home/viam/models/labels.txt"
  }
}
```

`model_path` and `label_path` are the file paths on the machine running `viam-server`. Local files work well for offline machines and air-gapped setups.

## 5. Wrap the model in a vision service

The ML model service now loads and runs your model. The vision service turns its output into detections or classifications:

1. Add a `vision/mlmodel` service.
2. Set `mlmodel_name` to the ML model service name from step 4.
3. Set `camera_name` to the default camera.
4. Save.

```json
{
  "name": "my-detector",
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my-ml-model",
    "camera_name": "camera-1"
  }
}
```

If the model does not produce detections right away, its input preprocessing or output tensor layout is probably non-standard. See [Tune detection quality](/vision/tune/).

## 6. Verify

1. Open the **CONTROL** tab.
2. Click the vision service.
3. In the **Camera** dropdown, select the camera whose feed you want the vision service to run on. Detections appear as bounding boxes on the live camera feed and refresh automatically.

If results look wrong (shifted boxes, wrong labels, or zero detections), go through [Tune detection quality](/vision/tune/). Every common failure mode maps to a specific attribute on the vision service.

## When to convert vs when to bridge

You generally do not have to modify the model itself. The vision service can bridge:

- **Non-standard tensor names** through `remap_input_names` and `remap_output_names`.
- **Non-standard preprocessing** through `input_image_mean_value`, `input_image_std_dev`, `input_image_bgr`.
- **Non-standard bounding box coordinate order** through `xmin_ymin_xmax_ymax_order`.
- **Class-specific confidence tuning** through `label_confidences`.

Convert the model itself only when its format is unsupported (for example, exporting from Keras HDF5 to TFLite) or when the tensor types are incompatible with the chosen ML model service.

## Next steps

- [Tune detection quality](/vision/tune/): fix specific detection failure modes
- [mlmodel reference](/reference/services/vision/mlmodel/): full attribute reference
- [Detect objects](/vision/detect/): use detections in code
- [Retrain when accuracy drops](/vision/retrain/): maintain quality in production
