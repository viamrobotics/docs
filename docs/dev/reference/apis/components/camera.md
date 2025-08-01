---
title: "Camera API"
linkTitle: "Camera"
weight: 40
type: "docs"
description: "Give commands for getting images or point clouds."
icon: true
images: ["/icons/components/camera.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/components/camera/
# updated: ""  # When the content was last entirely checked
---

The camera API allows you to give commands to your [camera components](/operate/reference/components/camera/) for getting images or point clouds.

The API for camera components allows you to:

- Request single images in 2D color, or display z-depth.
- Request a point cloud.
  Each 3D point cloud image consists of a set of coordinates (x,y,z) representing depth in mm.

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## API

{{< readfile "/static/include/components/apis/generated/camera.md" >}}
