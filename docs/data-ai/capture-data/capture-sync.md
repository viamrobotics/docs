---
linkTitle: "Capture and sync edge data"
title: "Capture and sync edge data"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Capture data from a resource on your machine and sync the data to the cloud."
date: "2024-12-03"
aliases:
  - /services/data/capture/
  - /data/capture/
  - /build/micro-rdk/data_management/
  - /services/data/capture/
  - /services/data/cloud-sync/
  - /data/cloud-sync/
  - /services/data/capture-sync/
  - /how-tos/sensor-data/
  - /services/data/
  - fleet/data-management/
  - /manage/data-management/
  - /services/data-management/
  - /manage/data/
  - /data-management/
  - /services/data/
  - /data/
  - /manage/data/export/
  - /data/export/
  - /services/data/export/
  - /manage/data/view/
  - /data/view/
  - /services/data/view/
  - /how-tos/collect-data/
  - /how-tos/collect-sensor-data/
  - /get-started/quickstarts/collect-data/
  - /use-cases/collect-sensor-data/
  - /use-cases/image-data/
  - /get-started/collect-data/
  - /fleet/data-management/
---

You can use the data management service to capture data from [supported components and services](/data-ai/capture-data/capture-sync/#click-to-see-resources-that-support-data-capture-and-cloud-sync), then sync it to the cloud.
You can also sync data from arbitrary folders on your machine.

Data capture and sync in Viam involves two key pieces:

- The data management {{< glossary_tooltip term_id="service" text="service" >}} that writes captured data to local edge device storage and syncs that data with the cloud.
- Individual {{< glossary_tooltip term_id="resource" text="resource" >}} configurations that specify what data to capture and how often.

## How data capture and data sync works

The data management service writes data from your configured Viam resources to local storage on your edge device and syncs data from the edge device to the cloud:

- The data management service stores captured data locally in <file>~/.viam/capture</file> by default.
- Data is synced to the Viam cloud at a configured sync interval using encrypted gRPC calls and deleted from the disk once synced.
- You can capture and sync data independently, one can run without the other.

For more information, see [How sync works](/data-ai/capture-data/advanced/how-sync-works/).

## Configure data capture and sync for individual resources

You can capture data for any {{< glossary_tooltip term_id="resource" text="resource" >}} that supports it, including resources on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}.

Configure data capture for individual resources in their configuration by:

- Selecting which resource methods to capture data from
- Setting the capture frequency for each method

{{< expand "Click to see resources that support data capture and cloud sync" >}}

The following components and services support data capture and cloud sync:

{{< readfile "/static/include/data/capture-supported.md" >}}

{{< /expand >}}

{{% alert title="Note" color="note" %}}
The following instructions assume you are using the [app UI](https://app.viam.com) in **Builder** mode.
For instructions on configuring data capture and sync with JSON, go to [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/) and follow the instructions for JSON examples.
{{% /alert %}}

For each resource you can capture data for, there is a **Data capture** section in its panel.
Click **+ Add method** and **Create data management service**.
This creates a data management service for you that both captures and syncs data to the cloud by default.

Select a **Method** to capture from and specify a capture **Frequency** in hertz, for example to `0.1` with `ReadImage` on a camera to capture an image every 10 seconds.
You can add multiple methods with different capture frequencies.
Some methods will prompt you to add additional parameters.
The available methods, and corresponding additional parameters, will depend on the component or service type.
For example, a camera has the options `ReadImage`, `GetImages` and `NextPointCloud`.
Keep in mind that some models do not support all options, for example webcams do not capture point clouds, and choose the method accordingly.

Click the **Save** button in the top right corner of the page to save your config.

If cloud sync is enabled, the data management service deletes captured data from the disk once it has successfully synced to the cloud.

{{< alert title="Warning" color="warning" >}}

If your robot is offline and can't sync and your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.

{{< /alert >}}

{{< expand "Click for more automatic data deletion details" >}}

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

## View captured data

To view all the captured data you have access to, go to the [**DATA** tab](https://app.viam.com/data/view) where you can filter by location, type of data, and more.

You can also access data from a resource or machine part menu.

## Stop data capture and data sync

If you don't need to capture data, for instance in a test scenario, you can turn off data capture to reduce unnecessary storage.
Alternatively, see [advanced data capture and sync configurations](/data-ai/capture-data/capture-sync/#advanced-data-capture-and-sync-configurations) for other ways to control data usage, such as conditional sync or retention policies.

To turn off data capture for a specific resource's capture method (for example, a camera component capturing through the `GetImage` capture method) navigate to the **Data capture** section of your resource's configuration card and toggle the configured capture method's switch to **Off**.
You can also globally turn off data capture on the `data_manager` service configuration card by toggling the **Capturing** switch to **Off**.

To turn off data sync, navigate to the `data_manager` service configuration card and toggle the **Syncing** switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Next steps

For more information on available configuration attributes and options like capturing directly to MongoDB or conditional sync, see [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/).
To leverage AI, you can now [create a dataset](/data-ai/ai/create-dataset/) with the data you've captured.
