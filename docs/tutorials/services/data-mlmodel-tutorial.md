---
title: "Capture Data and Train a Model"
linkTitle: "Capture Data and Train a Model"
weight: 4
type: "docs"
description: "Configure data capture and cloud sync, filter and tag captured data, and train an ML model."
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/services/ml/training.png"]
aliases:
tags: ["data management", "data", "mlmodel", "vision", "services", "try viam"]
authors: []
languages: []
viamresources: ["data_manager", "mlmodel", "vision", "camera"]
level: "Beginner"
date: "2023-02-08"
cost: "0"
no_list: true
---

With all three services working together, your machine will be able to analyze its camera feed for the presence of specific shapes, such as a red star or blue circle.
When it detects a likely match, it will overlay a confidence score onto the camera feed alongside the name of the detected shape, indicating how closely the shape in the camera frame matches a shape it has seen before.

## The data management service

The [data management](/services/data/) service has two parts: [data capture](/services/data/capture/) and [cloud sync](/services/data/cloud-sync/).

- **Data capture** allows you to capture data locally from specific components on your machine running Viam.
  You can choose the components, corresponding methods, and the frequency of the data capture from the [Viam app](https://app.viam.com/).

- **Cloud sync** runs in the background and uploads your machine's captured data to the Viam app at a defined frequency.
  Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your machine has low network bandwidth.
  With cloud sync enabled for a component, data captured locally to your machine is automatically deleted after a successful sync.
  Data synced between your machine and the Viam app is encrypted in transit (over the wire) and when stored in the cloud (at rest).

Data capture and data sync are frequently used together, and are both enabled by default when you add the data management service to your machine.
However, if you want to manage your machine's captured data yourself, you can enable data capture but disable data sync.
If you are capturing data to a device with limited storage, or intend to capture a large amount of data, see [automatic data deletion](/services/data/capture/#automatic-data-deletion).

To capture data from your machine and sync to the Viam app, add the data management service and configure data capture for at least one component.
