---
linkTitle: "Run inference"
title: "Run inference on a model"
weight: 50
layout: "docs"
type: "docs"
no_list: true
description: "TODO"
---

The vision service works with the ML model services.
It uses the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

**Save** your changes.

You can test your vision service by clicking on the **Test** area of its configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream shows when the vision service identifies something.
Try pointing the camera at a scene similar to your training data.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" >}}
{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" >}}

{{% expand "Want to limit the number of shown classifications or detections? Click here." %}}

If you are seeing a lot of classifications or detections, you can set a minimum confidence threshold.

Start by setting the value to 0.8.
This reduces your output by filtering out anything below a threshold of 80% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration, then close and reopen the **Test** panel of the vision service configuration panel.
Now if you reopen the panel, you will only see classifications or detections with a confidence value higher than the `default_minimum_confidence` attribute.

{{< /expand>}}

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

<!-- TODO: add information about running inference with an SDK -->
