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
You can capture data from [supported components and services](#supported-resources) or from arbitrary folders on your machines.

## Configure the data management service

To start, configure the data management service to capture and sync data.

From your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), add the `data management` service.
On the panel that appears, configure data capture and sync attributes as applicable.
To both capture data and sync it to the cloud, keep both **Capturing** and **Syncing** switched on.

Click the **Save** button in the top right corner of the page to save your config.

{{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="Data capture configuration card." resize="600x" >}}

For more advanced attribute configuration information, see [Data management service configuration](/data-ai/reference/data/#data-management-service-configuration).

## Configure data capture

Scroll to the resource card you wish to configure data capture and sync on.

In the **Data capture** section:

- Click the **Method** dropdown and select the method you want to capture.
- Set the frequency in hz, for example to `0.1` to capture an image every 10 seconds.

For example, a camera component configured to capture the `ReadImage` method every 3.03 seconds:

{{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="Data capture configuration card." resize="600x" >}}

Click the **Save** button in the top right corner of the page to save your config.

For more advanced attribute configuration information, see [Resource data capture configuration](/data-ai/reference/data/#resource-data-capture-configuration).

{{< expand "Automatic data deletion details" >}}

If cloud sync is enabled, the data management service deletes captured data once it has successfully synced to the cloud.

With `viam-server`, the data management service will also automatically delete local data in the event your machine's local storage fills up.
Local data is automatically deleted when _all_ of the following conditions are met:

- Data capture is enabled on the data management service
- Local disk usage percentage is greater than or equal to 90%
- The Viam capture directory is at least 50% of the current local disk usage

If local disk usage is greater than or equal to 90%, but the Viam capture directory is not at least 50% of that usage, a warning log message will be emitted instead and no action will be taken.

Automatic file deletion only applies to files in the specified Viam capture directory, which is set to `~/.viam/capture` by default.
Data outside of this directory is not touched by automatic data deletion.

If your machine captures a large amount of data, or frequently goes offline for long periods of time while capturing data, consider moving the Viam capture directory to a larger, dedicated storage device on your machine if available.
You can change the capture directory using the `capture_dir` attribute.

You can also control how local data is deleted if your machine's local storage becomes full, using the `delete_every_nth_when_disk_full` attribute.

{{< /expand >}}

## Stop data capture

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your resource's configuration card, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## View captured data

To view all the captured data you have access to, go to the [**DATA** tab](https://app.viam.com/data/view) where you can filter by location, type of data, and more.

You can also access data from a resource or machine part menu.

## Supported resources

The following components and services support data capture and cloud sync:

{{< readfile "/static/include/data/capture-supported.md" >}}

## Next steps

Now that you have captured data, you could [create a dataset](/data-ai/ai/create-dataset) and use this data to [train your own Machine Learning model](/data-ai/ai/train-tflite/) with the Viam platform.
