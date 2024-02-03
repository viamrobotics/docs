---
title: Width and height fields from camera API
date: "2022-11-01"
color: "removed"
---

Removed `width` and `height` from the response of the [`GetImage`](/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.
