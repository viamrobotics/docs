---
title: "fake"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Reference for the fake camera model on Micro-RDK. Returns a static circle-in-diamond image for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - /components/camera/fake-micro-server/
  - "/operate/reference/components/camera/fake-micro-rdk/"
component_description: "A camera model for testing."
micrordk_component: true
# SMEs: Matt Perez, Micro-RDK team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a circle inside a diamond.

{{< alert title="Software requirements" color="note" >}}
To use this model, you must follow the [Set up an ESP32 guide](/operate/install/setup-micro/#build-and-flash-custom-firmware), which enables you to install and activate the ESP-IDF.
When you create a new project with `cargo generate`, select the option to include camera module traits when prompted.
Finish building and flashing custom firmware, then return to this guide.
{{< /alert >}}

## Configuration

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "fake",
  "api": "rdk:component:camera",
  "attributes": {}
}
```
