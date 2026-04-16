---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake camera model. Returns a static gradient image and point cloud for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/fake/"
  - "/operate/reference/components/camera/fake/"
component_description: "A camera model for testing."
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a gradient.
This camera also returns a point cloud.

## Configuration

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "fake",
  "api": "rdk:component:camera",
  "attributes": {
    "width": <int>,
    "height": <int>
  }
}
```

## Attributes

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `width` | int | Optional | The width of the image in pixels. The maximum width is 10000. <br> Default: `1280` |
| `height` | int | Optional | The height of the image in pixels. The maximum height is 10000. <br> Default: `720` |
| `animated` | bool | Optional | If you want the camera stream visible on the **CONTROL** tab to be animated. <br> Default: `False` |
| `rtp_passthrough` | bool | Optional | If true, `GetImages` will ignore width, height, and animated config params. Default: `False`. |
| `model` | bool | Optional  | If true, provides `IntrinsicParams` and `DistortionParams` for the camera. Default: `False`. |
