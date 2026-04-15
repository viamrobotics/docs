---
linkTitle: "How the vision service works"
title: "How the vision service works"
weight: 5
layout: "docs"
type: "docs"
description: "Why Viam splits ML inference into two services, what each one does, and how they compose to produce detections, classifications, and point cloud objects."
date: "2026-04-14"
---

Most robotics platforms handle machine learning inference as a single block: one configuration entry that loads a model and runs it against a camera. Viam splits this into two services. Understanding why makes the rest of the vision section make more sense.

## The two-service architecture

The **ML model service** handles the mechanics of running a model: reading the file from disk, allocating memory, preparing the inference runtime, and exposing an [`Infer`](/reference/apis/services/ml/#infer) method that takes and returns raw tensors.

The **vision service** handles the semantics: what does "run a detection" mean, how do you map the model's output tensors to bounding boxes, how do you associate results with camera frames, and how do you capture the image in the right format for the model.

```text
  Camera ─── Image bytes ───► Vision service ─── Tensor ───► ML model service
                                   │                                │
                                   │                                ▼
                                   │                         Raw output tensor
                                   ▼                                │
                           Detections / classifications             │
                           / 3D segments  ◄─────────────────────────┘
                           (structured, labeled)
```

This separation means:

- You can **update your model** (retrain, swap architectures, pin to a new [registry](https://app.viam.com/registry) version) without changing your vision service configuration.
- You can **run the same model against multiple cameras** by creating multiple vision services that reference one ML model service.
- **Different model formats** (TFLite, ONNX, TensorFlow, PyTorch) are handled by different ML model service implementations, but the vision service API stays the same, so your application code does not care which format you chose.
- **The vision service is what your code interacts with.** You almost never call the ML model service directly from application code.

## What the vision service decides at startup

When the built-in [`mlmodel`](/reference/services/vision/mlmodel/) vision service starts, it reads the wrapped ML model's tensor metadata and decides which of three roles the model can fulfill:

- If the outputs look like **classification outputs** (a `probability` tensor), the service registers as a classifier.
- If the outputs look like **detection outputs** (`location`, `category`, and `score` tensors), the service registers as a detector.
- If the outputs look like **3D-segmentation outputs**, the service registers as a 3D segmenter.

If the underlying model supports it, a single `mlmodel` vision service can fulfill more than one role. You can check which roles are active at runtime with [`GetProperties`](/reference/apis/services/vision/#getproperties).

If none of the roles can be fulfilled, the service logs an error at startup describing what tensors it saw. This usually happens because the tensor names or shapes do not match what the vision service expects. Use `remap_input_names` and `remap_output_names` to bridge tensor names, as described in the [`mlmodel` reference](/reference/services/vision/mlmodel/#tensor-name-requirements).

## What stays in your configuration

Only three pieces of configuration change when you swap models:

1. **The ML model service's model file** (`model_path` for local files or a [registry](https://app.viam.com/registry) package reference).
2. **Labels**, if the new model uses different classes.
3. **Preprocessing attributes** on the vision service (`input_image_mean_value`, `input_image_std_dev`, `input_image_bgr`, `xmin_ymin_xmax_ymax_order`) if the new model expects different input or output conventions.

Your application code, your camera wiring, your trigger configuration, and your module code all stay the same.

## When to reach for a different vision service model

The `mlmodel` service covers most ML-backed tasks, but two other built-in models exist for specific jobs:

- **[`color_detector`](/reference/services/vision/color_detector/)** runs entirely on heuristic hue matching. No model, no training data, no ML model service required. Use it for tasks where the target stands out by color.
- **[`viam:vision:detections-to-segments`](/reference/services/vision/detections-to-segments/)** projects 2D detections from another vision service into 3D point cloud objects using depth-camera intrinsics. Use it when a robot needs physical 3D positions of detected objects.

For anything else (face recognition, pose estimation, specialized detectors), browse the [registry](https://app.viam.com/registry).

## Next steps

- [Configure a vision pipeline](/vision/configure/) walks through adding both services in the app.
- [mlmodel reference](/reference/services/vision/mlmodel/) documents every attribute.
- [Vision service API](/reference/apis/services/vision/) documents every method your code can call.
