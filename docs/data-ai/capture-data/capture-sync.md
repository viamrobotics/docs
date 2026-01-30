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
updated: "2025-12-04"
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
You can also [sync data from arbitrary folders on your machine](/data-ai/capture-data/upload-other-data/#sync-data-from-another-directory).

## How data capture and data sync work

The data management service writes data from your configured Viam resources to local storage on your edge device and syncs data from the edge device to the cloud:

- The data management service writes captured data to local edge device storage (<file>~/.viam/capture</file> by default).
- The data management service syncs data to the Viam cloud at a configured sync interval using encrypted gRPC calls and deletes it from the disk once synced.
- You can capture and sync data independently; one can run without the other.

For more information, see [How sync works](/data-ai/capture-data/advanced/how-sync-works/).

<img src="/data-manager.svg" alt="Diagram showing data being captured, synced, and removed." class="aligncenter overview imgzoom" style="width:800px;height:auto" >

## Configure data capture and sync for individual resources

1. Navigate to a configured {{< glossary_tooltip term_id="resource" text="resource" >}} in **Builder** mode.
1. Find the **Data capture** section in the resource panel.
1. Click **+ Add method**.

   {{< imgproc src="/tutorials/data-management/add-method.png" alt="Disable data capture toggle" resize="800x" style="width:500px" class="shadow imgzoom" >}}

1. If you see a **Capture disabled on data management service** warning, click **Enable capture on data management service**.
1. Select a **Method** to capture data from.

   {{< alert title="Camera capture methods" color="note" >}}
   Camera components provide two similar, but distinct capture methods:

   - **GetImages**: Returns an image per camera sensor for 3D cameras (for example, "color" as JPEG for RGB sensors, "depth" as a depth map for depth sensors), or a single image for webcams, RTSP cameras etc.

   {{< /alert >}}

1. Set the capture **Frequency** in hertz, for example to `0.2` with `GetImages` on a camera to capture an image every 5 seconds.
1. **Save** your config.

You can add multiple methods with different capture frequencies.

{{< expand "Click to see resources that support data capture and cloud sync" >}}

The following components and services support data capture and cloud sync:

{{< readfile "/static/include/data/capture-supported.md" >}}

{{< alert title="Support notice" color="note" >}}
Some models do not support all options, for example webcams do not capture point clouds.
{{< /alert >}}

{{< /expand >}}

For instructions on configuring data capture and sync with JSON, see [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/).

## View captured data

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view).
1. Select the [**Images**](https://app.viam.com/data/view?view=images), [**Files**](https://app.viam.com/data/view?view=files), [**Point clouds**](https://app.viam.com/data/view?view=point+clouds), or [**Sensors**](https://app.viam.com/data/view?view=sensors) subtab.
1. Filter data by location, type, and more.

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

- [Conditional sync](/data-ai/capture-data/conditional-sync/)
- [Retention policies](/data-ai/capture-data/advanced/advanced-data-capture-sync/#cloud-data-retention)
- [Sync optimization](/data-ai/capture-data/advanced/advanced-data-capture-sync/#sync-optimization)

{{< /alert >}}

## Next steps

For more information on available configuration attributes and options like capturing directly to MongoDB or conditional sync, see [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/).
To leverage AI, you can [create a dataset](/data-ai/train/create-dataset/) with the data you've captured.
