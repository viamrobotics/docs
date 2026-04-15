---
linkTitle: "Tune detection quality"
title: "Tune detection quality"
weight: 30
layout: "docs"
type: "docs"
description: "Match a detection quality symptom to the mlmodel vision service attribute that fixes it. Covers bounding box order, input normalization, per-label thresholds, and tensor remapping."
date: "2026-04-14"
aliases:
  - /vision/tune/
---

Your vision service is configured and returning detections, but the results are wrong in a specific way. This guide matches common failure modes to the `mlmodel` vision service attribute that fixes each one. Most tuning is a configuration change, not a code change.

Before tuning, confirm the service is producing any results at all through the [Control tab](/vision/configure/#6-test-from-the-control-tab). If the service is not registered in the role you expected (for example, it registered as a classifier when you wanted a detector), see [How the vision service works](/vision/how-it-works/).

## Pick your symptom

| What you see                                      | Likely cause                                                                   | Attribute                                                                                                                                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Boxes appear shifted, rotated 90°, or mirrored    | Model outputs bounding box coordinates in a different order than Viam expects. | [`xmin_ymin_xmax_ymax_order`](#bounding-boxes-appear-shifted-or-mirrored)                                                                                                            |
| Wrong labels, or all labels fire at once          | Input preprocessing does not match training (channel order or normalization).  | [`input_image_bgr`](#wrong-labels-or-every-label-fires), [`input_image_mean_value`](#wrong-labels-or-every-label-fires), [`input_image_std_dev`](#wrong-labels-or-every-label-fires) |
| Model loads but returns zero detections           | Confidence threshold too high, wrong tensor names, or missing label file.      | [`default_minimum_confidence`](#zero-detections), [`remap_input_names`](#zero-detections), [`remap_output_names`](#zero-detections), [`label_path`](#zero-detections)                |
| One label fires constantly; others never do       | Global confidence threshold is wrong for at least one class.                   | [`label_confidences`](#one-label-dominates-or-others-never-fire)                                                                                                                     |
| Startup error about tensor names                  | Model's tensor names do not match the vision service's expected names.         | [`remap_input_names`](#tensor-names-do-not-match), [`remap_output_names`](#tensor-names-do-not-match)                                                                                |
| Startup error about zero in `input_image_std_dev` | Standard deviation cannot contain zero values.                                 | [Fix preprocessing values](#wrong-labels-or-every-label-fires)                                                                                                                       |

All attributes below are set on the `mlmodel` vision service, not on the underlying ML model service. See the [`mlmodel` reference](/reference/services/vision/mlmodel/) for the full attribute table.

## Bounding boxes appear shifted or mirrored

The `mlmodel` vision service expects the detection model to output bounding boxes as `[xmin, ymin, xmax, ymax]`. Many models (especially custom YOLO variants and some SavedModel exports) output them in a different order, such as `[ymin, xmin, ymax, xmax]`.

Set `xmin_ymin_xmax_ymax_order` to the permutation that reorders the model's output into the expected order. The four entries are indices into the model's output, not into the expected output:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "xmin_ymin_xmax_ymax_order": [1, 0, 3, 2]
  }
}
```

The example above says "my model's output position 1 holds xmin, position 0 holds ymin, position 3 holds xmax, position 2 holds ymax." Use `[0, 1, 2, 3]` (the default) when the model already outputs in `xmin, ymin, xmax, ymax` order.

**How to diagnose:** Run the Control tab overlay and compare box locations to what is actually in the image. If boxes look rotated, mirrored, or shifted by half the frame, this is almost always the coordinate order.

## Wrong labels or every label fires

Neural network models are typically trained on preprocessed images: pixel values are normalized, channel order is either RGB or BGR, and the image is resized a particular way. If the vision service's preprocessing does not match what the model expects, the model sees garbage input and its labels will not match what is actually in the frame.

Three attributes control preprocessing:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "input_image_bgr": true,
    "input_image_mean_value": [127.5, 127.5, 127.5],
    "input_image_std_dev": [127.5, 127.5, 127.5]
  }
}
```

- **`input_image_bgr`** (default `false`): set to `true` when the model was trained on BGR images (OpenCV convention) rather than RGB. If all detections have unrelated colors or every label fires simultaneously, try flipping this first.
- **`input_image_mean_value`**: per-channel mean subtracted from each pixel before inference. Requires at least 3 values, one per color channel. Common values: `[127.5, 127.5, 127.5]` for models trained on centered `[-1, 1]` input, or `[0.485, 0.456, 0.406]` scaled by 255 for ImageNet-trained models.
- **`input_image_std_dev`**: per-channel standard deviation each pixel is divided by after mean subtraction. Must be non-zero. Common values: `[127.5, 127.5, 127.5]`.

Leave all three unset when the model was trained on raw pixel values in `[0, 255]` without normalization. The vision service skips preprocessing in that case.

**How to find the right values:** Check the model card or the training script. Standard detection architectures publish their preprocessing conventions. Look up the values for MobileNet, EfficientDet, YOLO variants, or ResNet in that architecture's documentation.

## Zero detections

If the model loads successfully but `GetDetections` always returns an empty list, work through these in order:

### Lower the confidence threshold temporarily

`default_minimum_confidence` applies to every detection. A model that is nearly right but not confident may have its output filtered before you see it:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "default_minimum_confidence": 0.1
  }
}
```

Run the Control tab. If low-confidence detections now appear, the model is working but miscalibrated. Raise the threshold back to a sensible value (typically `0.4` to `0.6`) once you understand what the model is producing. If still zero detections with a low threshold, the problem is elsewhere.

### Verify tensor names and label file

Check `viam-server` logs for startup errors mentioning input or output tensor names. If the model's tensors are not named as the service expects (see [tensor name requirements](/reference/services/vision/mlmodel/#tensor-name-requirements)), the service logs what it saw and produces no detections.

Add `remap_input_names` and `remap_output_names` to bridge them. See [Tensor names do not match](#tensor-names-do-not-match) below.

If the service loads but labels are numeric class IDs (for example, `3`, `7`) rather than human-readable names like `person` or `car`, set `label_path` to your labels file:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "label_path": "/home/viam/my_labels.txt"
  }
}
```

The file must be one label per line. Line number (zero-indexed) is the class ID.

## One label dominates or others never fire

A single global `default_minimum_confidence` does not suit every model or every application. A model may be very confident about `PERSON` detections (95%+ for real people) but less confident about `CAT` (60-80%). With a global threshold of `0.7`, you miss half of the cats. With a threshold of `0.5`, you get false-positive people constantly.

Set per-label thresholds with `label_confidences`:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "label_confidences": {
      "PERSON": 0.85,
      "CAT": 0.5,
      "DOG": 0.5
    }
  }
}
```

When `label_confidences` is set, `default_minimum_confidence` is ignored. Labels not listed are filtered out entirely. If you want those labels to pass through, include them in the map with their own threshold.

**How to pick values:** Run the Control tab and observe the confidence scores of real detections against known-good and known-bad objects. Set each threshold just below the lowest confidence your model produces for true positives of that class.

## Tensor names do not match

The `mlmodel` vision service expects specific tensor names:

- Detector input: `image`. Detector outputs: `location`, `category`, `score`.
- Classifier input: `image`. Classifier output: `probability`.

If your model uses different names (common when you export from custom training scripts), the service fails to register or produces no results. Use `remap_input_names` and `remap_output_names` to bridge them:

```json
{
  "attributes": {
    "mlmodel_name": "my_model",
    "remap_input_names": {
      "input_tensor:0": "image"
    },
    "remap_output_names": {
      "detection_boxes:0": "location",
      "detection_classes:0": "category",
      "detection_scores:0": "score"
    }
  }
}
```

Keys are the model's actual tensor names. Values are what the vision service expects. Check `viam-server` startup logs for the exact names the model exposes. The service logs them when it cannot fulfill any role.

Viam-trained ML models already use the expected names, so `remap_input_names` and `remap_output_names` are only needed for models trained elsewhere.

## Verify every change

After each attribute change, save the configuration and let `viam-server` reconfigure. Watch the **CONTROL** tab for a few seconds:

1. Open the vision service card and select your camera in the **Camera** dropdown.
2. Point the camera at a known object your model was trained on.
3. Confirm the overlay shows a bounding box with the expected label.
4. Move the object out of frame and confirm the box disappears.

If results do not change after saving, check `viam-server` logs for a configuration error. The service may have kept its previous configuration and logged a parse error instead of applying your edit.

## Next steps

- [mlmodel reference](/reference/services/vision/mlmodel/): every attribute in one place
- [How the vision service works](/vision/how-it-works/): why the two-service split matters for retraining and redeployment
- [Detect objects](/vision/object-detection/detect/): once tuning is done, put detections to use in code
