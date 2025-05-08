---
linkTitle: "Sync"
title: "Sync edge data"
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

You can use the data management service to capture data from [supported components and services](/data-ai/data/capture-sync/#click-to-see-resources-that-support-data-capture-and-cloud-sync), then sync it to the cloud.
You can also sync data from arbitrary folders on your machine.

## How data capture and data sync works

The data management service writes data from your configured Viam resources to local storage on your edge device and syncs data from the edge device to the cloud:

- The data management service writes captured data to local edge device storage (<file>~/.viam/capture</file> by default).
- The data management service syncs data to the Viam cloud at a configured sync interval using encrypted gRPC calls and deletes it from the disk once synced.
- You can capture and sync data independently; one can run without the other.

For more information, see [How sync works](/data-ai/data/advanced/how-sync-works/).

## Configure data capture and sync for individual resources

1. Navigate to a configured {{< glossary_tooltip term_id="resource" text="resource" >}} in **Builder** mode in the [Viam app](https://app.viam.com).
1. Find the **Data capture** section in the resource panel.
1. Click **+ Add method**.

   {{< imgproc src="/tutorials/data-management/add-method.png" alt="Disable data capture toggle" resize="700x" class="shadow" >}}

1. If you see a warning **Capture disabled on data management service**, click **Enable capture on data management service**.
1. Select a **Method** to capture data from.
1. Set the capture **frequency** in hertz, for example to `0.2` with `ReadImage` on a camera to capture an image every 5 seconds.
1. **Save** your config.

You can add multiple methods with different capture frequencies.

{{< expand "Click to see resources that support data capture and cloud sync" >}}

The following components and services support data capture and cloud sync:

{{< readfile "/static/include/data/capture-supported.md" >}}

{{< alert title="Support notice" color="note" >}}
Some models do not support all options, for example webcams do not capture point clouds.
{{< /alert >}}

{{< /expand >}}

For instructions on configuring data capture and sync with JSON, go to [Advanced data capture and sync configurations](/data-ai/reference/advanced-data-capture-sync/) and follow the instructions for JSON examples.

## View captured data

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view).
1. Filter data by location, type of data, and more.

## Stop data capture or data sync

### Stop data capture for a specific resource

1. Navigate to the **Data capture** section of your resource's configuration card.
1. Toggle the configured capture method's switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-capture-resource.png" alt="Disable data capture toggle" resize="500x" class="shadow" >}}

1. **Save** your config.

### Stop data capture for all resources

1. Navigate to the **Data capture** section of the data management service configuration card.
1. Toggle the **Capturing** switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-capture.png" alt="Disable data capture toggle" resize="300x" class="shadow" >}}

1. **Save** your config.

### Disable data sync

1. Navigate to the **Cloud sync** section of the data management service configuration card.
1. Toggle the **Syncing** switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-sync.png" alt="Disable data sync toggle" resize="300x" class="shadow" >}}

1. **Save** your config.

{{< alert title="Tip: More ways to control data capture or sync" color="tip" >}}

For other ways to control data synchronization, see:

- [Conditional sync](/data-ai/data/conditional-sync/)
- [Retention policies](/data-ai/reference/advanced-data-capture-sync/#cloud-data-retention)
- [Sync optimization](/data-ai/reference/advanced-data-capture-sync/#sync-optimization)

{{< /alert >}}

## Next steps

For more information on available configuration attributes and options like capturing directly to MongoDB or conditional sync, see [Advanced data capture and sync configurations](/data-ai/reference/advanced-data-capture-sync/).
You can now use your data to [create a training dataset](/data-ai/get-started/create-training-dataset/).
