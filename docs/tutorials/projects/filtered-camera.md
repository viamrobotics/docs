---
title: "Selectively Capture Data Using filtered-camera"
linkTitle: "Filtered Camera"
type: "docs"
description: "Use the filtered-camera module to selectively capture images."
images: ["/tutorials/filtered-camera-module/viam-figure-preview.png"]
imageAlt: "A wooden Viam figure being detected on a camera stream"
tags: ["camera", "vision", "detector", "mlmodel", "data"]
viamresources: ["camera", "vision", "mlmodel", "data_manager"]
platform_area: ["machine learning", "data"]
languages: []
level: "Intermediate"
date: "2023-12-20"
# updated: ""
cost: "0"
---

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="The promotional Viam wooden figure we give out at events, being correctly detected with a 0.97 confidence threshold" resize="400x"  class="alignright" >}}

With the data management service, a Viam machine can capture data from a variety of components and sync that data to the Viam app.
However, if your machine captures a large volume of data, especially image data such as pictures, you may wish to control which specific images are captured or uploaded.
