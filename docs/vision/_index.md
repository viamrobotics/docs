---
linkTitle: "Computer vision"
title: "Computer vision"
weight: 55
layout: "docs"
type: "docs"
no_list: true
description: "Add computer vision to your machine: deploy ML models, run inference on camera feeds, detect and classify objects, measure depth, and act or alert on results."
aliases:
  - /build/vision-detection/
  - /vision-detection/
  - /vision/how-to/
---

Use these guides to add vision capabilities to your machine.
The standard pipeline is: configure a camera, deploy an ML model, add a vision service, then use detections or classifications in your code.

**Not sure whether to use detection or classification?** Detection finds _where_ objects are in an image (bounding boxes). Classification tells you _what_ the whole image contains (labels). Use detection when you need object locations; use classification when you just need to categorize the scene.

{{< cards >}}
{{% card link="/vision/configure/" %}}
{{% card link="/vision/detect/" %}}
{{% card link="/vision/classify/" %}}
{{% card link="/vision/track/" %}}
{{% card link="/vision/measure-depth/" %}}
{{% card link="/vision/act-on-detections/" %}}
{{% card link="/vision/alert-on-detections/" %}}
{{< /cards >}}
