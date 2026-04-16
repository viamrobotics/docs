---
title: "Camera Component"
linkTitle: "Camera"
childTitleEndOverwrite: "Camera Component"
weight: 40
type: "docs"
description: "Configuration attribute reference for built-in camera models."
no_list: true
tags: ["camera", "components"]
icon: true
images: ["/icons/components/camera.svg"]
aliases:
  - "/components/camera/"
date: "2024-10-21"
# SMEs: Bijan, vision team
---

This section documents the configuration attributes for each built-in camera model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a camera component on your machine, see [Add a camera](/hardware/common-components/add-a-camera/).
- For the methods you call on a camera in code, see the [Camera API reference](/reference/apis/components/camera/).
- For camera modules outside the built-in set (for example, `realsense` or `viamrtsp`), browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=camera). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following camera models ship with `viam-server`:

| Model                       | Description                                                                                                      |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [`webcam`](webcam/)         | The general camera model for USB cameras and laptop webcams.                                                     |
| [`ffmpeg`](ffmpeg/)         | Uses a camera device, video file, or stream as a camera component.                                               |
| [`transform`](transform/)   | Applies pipeline transformations (classifications, crop, detections, resize, rotate) to another camera's output. |
| [`fake`](fake/)             | Returns a static gradient image and point cloud, for testing.                                                    |
| [`image_file`](image-file/) | Serves color or depth image frames from a file path.                                                             |

## Micro-RDK models

The following camera models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                                     | Description                                             |
| ----------------------------------------- | ------------------------------------------------------- |
| [`fake`](micro-rdk/fake/)                 | A camera model for testing.                             |
| [`esp32-camera`](micro-rdk/esp32-camera/) | An OV2640 or OV3660 camera connected to an ESP32 board. |
