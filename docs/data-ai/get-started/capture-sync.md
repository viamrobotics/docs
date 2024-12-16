---
linkTitle: "Capture edge data"
title: "Capture and sync edge data"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Capture data from a resource on your machine and sync the data to the cloud."
date: "2024-12-03"
---

You can use data management service to capture and sync data from your machine to the cloud.
Once you have configured the data management service, you can specify the data you want to capture at a resource level.

To configure data capture and cloud sync, you must have one of the following components and services configured on your machine:

{{< readfile "/static/include/data/capture-supported.md" >}}

## Configure the data management service

To start, configure a data management service to capture and sync the resource data.

From your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), add the `data management` service.
On the panel that appears, configure data capture and sync attributes as applicable.
To both capture data and sync it to the cloud, keep both **Capturing** and **Syncing** switched on.

Click the **Save** button in the top right corner of the page to save your config.

{{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="Data capture configuration card." resize="600x" >}}

For more advanced attribute configuration information, see [Data management service configuration](/data-ai/reference/data/#data-management-service-configuration).

## Configure data capture

Scroll to the config card you wish to configure data capture and sync on.

In the **Data capture** section:

- Click the **Method** dropdown and select the method you want to capture.
- Set the frequency in hz, for example to `0.1` to capture an image every 10 seconds.

For example, with a camera component capturing the `ReadImage` method every 3.03 seconds:

{{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="Data capture configuration card." resize="600x" >}}

Click the **Save** button in the top right corner of the page to save your config.

For more advanced attribute configuration information, see [Resource data capture configuration](/data-ai/reference/data/#resource-data-capture-configuration).

## Stop data capture

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your resource's configuration card, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## View captured data

To view all the captured data you have access to, go to the [**DATA** tab](https://app.viam.com/data/view) where you can filter by location, type of data, and more.

You can also access data from a resource or machine part menu.

## Next steps

Now that you have captured data, you could [create a dataset](/data-ai/ai/create-dataset) and use this data to [train your own Machine Learning model](/data-ai/ai/train-tflite/) with the Viam platform.
