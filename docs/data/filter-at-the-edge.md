---
linkTitle: "Filter at the edge"
title: "Filter at the edge"
weight: 31
layout: "docs"
type: "docs"
description: "Reduce data volume, bandwidth, and storage costs by filtering data on the machine before syncing to the cloud."
date: "2025-01-30"
aliases:
  - /build/data/filter-at-the-edge/
  - /data-ai/capture-data/filter-before-sync/
  - /how-tos/image-data/
  - /tutorials/projects/filtered-camera/
---

Reduce the volume of data your robot captures and syncs. Robots can generate gigabytes per day from cameras and sensors, but most of that data is redundant. Edge filtering means the machine decides what is worth recording or syncing, so you save bandwidth, storage costs, and noise in your datasets.

This is especially important for machines on cellular connections, metered networks, or with limited local storage.

This page covers three approaches, from simplest to most powerful:

1. **Reduce capture frequency** -- capture less often.
2. **Use a filtered camera** -- use an ML model to decide frame-by-frame what to capture.
3. **Conditional sync** -- capture locally but only sync when conditions are met.

## Reduce capture frequency (time-based sampling)

The simplest filter is capturing less often. If you configured your camera at
1 Hz (one frame per second), consider whether you actually need that rate.

1. In the [Viam app](https://app.viam.com), navigate to your machine's
   **CONFIGURE** tab.
2. Find the component you are capturing from (for example, `my-camera`).
3. In the **Data capture** section, find the capture method you configured.
4. Change the **frequency** to a lower value:
   - `1` Hz = 1 capture per second = ~2.5&nbsp;GB/day for camera images
   - `0.1` Hz = 1 capture every 10 seconds = ~250 MB/day
   - `0.0167` Hz = 1 capture per minute = ~25 MB/day
   - `0.00028` Hz = 1 capture per hour = ~0.4 MB/day
5. Click **Save**.

The change takes effect immediately. No restart required.

{{< alert title="Tip" color="tip" >}}

Start with the lowest frequency that meets your needs. You can always
increase it later once you understand your data volume and bandwidth budget.

{{< /alert >}}

This approach works well when you need periodic snapshots but not continuous
monitoring. It does not help when you need to capture specific events, like
"only save images when there is a person in the frame". For event-based
capture, skip ahead to [Use a filtered camera with ML](#use-a-filtered-camera-with-ml).

## Configure conditional sync

Conditional sync lets you capture data locally at full frequency but only upload
it to the cloud when certain conditions are met. This is useful when you want
a local buffer of recent data but only care about syncing data that meets
specific criteria.

You configure conditional sync through the data management service in your
machine's configuration. The sync configuration supports conditions based on
sensor readings, component states, or other data sources on your machine.

1. In the Viam app, go to your machine's **CONFIGURE** tab.
2. Find the **data management** service in your configuration. If you do not see
   it, add it by clicking **+**, selecting **Service**, and choosing **data
   management**.
3. In the data management service configuration, set the **Sync interval** to
   control how frequently synced data is uploaded. A longer interval means data
   accumulates locally before being sent in batches.
4. To add sync conditions, you can use the `selective_syncer_name` attribute to
   specify a custom module that controls when sync occurs. This module
   programmatically decides whether accumulated data should be synced based on
   any logic you define -- sensor thresholds, time of day, connectivity status,
   or external triggers.

For example, you might write a selective sync module that checks a temperature
sensor and only triggers sync when the reading exceeds a threshold. The data
management service calls into your module to determine whether to proceed with
each sync cycle.

{{< alert title="Note" color="note" >}}

Conditional sync still captures data locally at your configured
frequency. It only controls when that data gets uploaded. Make sure your
machine has enough local storage for the capture buffer (see
[Manage local storage](#manage-local-storage) below).

{{< /alert >}}

## Use a filtered camera with ML

The [`filtered-camera`](https://app.viam.com/module/viam/filtered-camera) registry module captures only the images you actually care about by running an ML vision model on each frame and gating capture on the result. It wraps an existing camera and a vision service so data capture sees a pre-filtered stream.

### How it works

The filtered camera sits between a raw camera and the data manager:

1. A raw **camera** component (for example, a USB webcam) provides the image stream.
2. A **vision service** runs an ML classifier or detector against each image and returns classifications or detections with confidence scores.
3. A **`filtered-camera`** component wraps the camera and the vision service. It continuously pulls frames from the camera into an in-memory ring buffer, asks the vision service to score each frame, and marks a frame as "interesting" when a classification or detection passes a confidence threshold you configure.
4. **Data capture** is configured on the `filtered-camera` component, not on the raw camera. Because the filtered camera is itself a camera component, the data manager captures from it the same way it would from any other camera. Only frames that passed the filter are ever written to disk.
5. The normal sync pipeline uploads the captured files to the cloud.

The raw camera's image stream is unchanged: the CONTROL tab, other services, and anything else on the machine still see every frame. Only the filtered camera, and therefore only data capture, sees the filtered subset.

Optionally, you can configure a pre-trigger buffer with `window_seconds_before` and a post-trigger buffer with `window_seconds_after`. When a frame triggers the filter, the module includes the buffered frames from those windows alongside the trigger frame. Use this when you need context leading up to or after an event.

### Prerequisites

- A configured camera component on your machine. See [Configure a camera](/reference/components/camera/) if you need to set one up.
- The data management service configured. See [Start data capture](/data/capture-sync/capture-and-sync-data/) for instructions.

### Instructions

{{< table >}}
{{% tablestep start=1 %}}
**Add an ML model service to your machine**

Add an ML model service on your machine that is compatible with the ML model you want to use, for example [TFLite CPU](https://github.com/viam-modules/mlmodel-tflite).

{{% /tablestep %}}
{{% tablestep %}}
**Select a suitable ML model**

Click **Select model** on the ML model service configuration panel, then select an [existing model](https://app.viam.com/registry?type=ML+Model) you want to use, or click **Upload a new model** to upload your own.
If you're not sure which model to use, you can use [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO) from the **Registry**, which can detect people and animals, among other things.

{{% /tablestep %}}
{{% tablestep %}}
**Add a vision service to use with the ML model**

The vision service is the bridge between the ML model service and the camera images. It loads the ML model and exposes classifier or detector methods that the filtered camera calls on each frame.

Add and configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep %}}
**Configure the filtered camera**

Add a `camera / filtered-camera` component on your machine. Set `camera` to the name of the raw camera you want to filter, and add a `vision_services` entry that references the vision service you just configured, along with the classification labels or detection classes you want to capture.

For example, to capture images only when a person is detected with at least 80% confidence:

```json {class="line-numbers linkable-line-numbers"}
{
  "camera": "camera-1",
  "vision_services": [
    {
      "vision": "vision-1",
      "objects": {
        "Person": 0.8
      }
    }
  ],
  "window_seconds_before": 0,
  "window_seconds_after": 0
}
```

Key attributes:

| Attribute               | Required | Description                                                                                                                                                                             |
| ----------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `camera`                | Yes      | Name of the camera to filter.                                                                                                                                                           |
| `vision_services`       | Yes      | List of vision services with their trigger criteria. Each entry needs a `vision` (the service name) and one of `classifications` or `objects` (a map of label to confidence threshold). |
| `window_seconds_before` | Yes      | Seconds of buffered frames to include before a trigger. Set to `0` for no pre-buffer.                                                                                                   |
| `window_seconds_after`  | Yes      | Seconds of buffered frames to include after a trigger. Set to `0` for no post-buffer.                                                                                                   |
| `image_frequency`       | No       | Rate in Hz at which the filtered camera pulls frames from the raw camera into its buffer. Default: `1.0`.                                                                               |
| `cooldown_s`            | No       | Seconds to suppress new triggers after a capture window ends. Useful when events happen in bursts. Default: `0`.                                                                        |

You can configure more than one `vision_services` entry to trigger on multiple conditions. Use `"*"` as a label to match any classification or detection above the confidence threshold. For the full attribute reference, see the [module README on GitHub](https://github.com/viam-modules/filtered_camera#attributes).

{{% /tablestep %}}
{{% tablestep %}}
**Configure data capture on the filtered camera**

Configure data capture on the **filtered camera**, not on the raw camera, following the same process as [Start data capture](/data/capture-sync/capture-and-sync-data/). Use the `GetImages` capture method and choose a capture frequency.

If the raw camera already has data capture configured, remove it. Otherwise you will capture both the unfiltered stream and the filtered stream.

{{% /tablestep %}}
{{% tablestep %}}
**Save and verify**

Save the config. Place an object your ML model can detect in front of the camera and wait for the next sync interval.

On the **DATA** tab in the Viam app, click **Images** (the default view). You should see frames appear only when the trigger condition was met. If no frames appear:

- **Test the vision service directly.** On the machine's **CONTROL** tab, open the vision service panel and point the camera at a known object. The panel shows live classifications and detections with their confidence scores. If no classifications or detections reach your threshold, the filtered camera has nothing to capture.
- **Check the logs.** The machine's **LOGS** tab shows the filtered camera's filtering decisions if you set `"debug": true` in its config.
- **Confirm capture is on the filtered camera.** Data capture must be on the `filtered-camera` component, not the underlying camera.

{{% /tablestep %}}
{{% tablestep %}}
**(Optional) Trigger sync with custom logic**

By default, captured data syncs at the interval you set on the data management service. If you need to sync only at certain times or when other conditions are met, see [Conditional sync](/data/capture-sync/conditional-sync/).

{{% /tablestep %}}
{{< /table >}}

{{< alert title="Build your own filtering module" color="tip" >}}

If the `filtered-camera` module does not meet your needs, you can build a custom filtering module. See [Write a module](/build-modules/write-a-driver-module/) for the general module development guide. The next section covers the pattern.

{{< /alert >}}

## Build a custom filter module

For filtering needs that go beyond what the `filtered-camera` module provides, you can write your own module. Common examples:

- A sensor wrapper that only reports readings above a threshold (for example, temperature above 50 degrees C)
- A camera filter with custom logic specific to your application
- A filter that combines data from multiple sensors before deciding what to capture

The pattern is: write a module that wraps an existing component, evaluates its data against your criteria, and only returns data worth capturing. Configure data capture on the wrapper component instead of the raw component.

See [Write a module](/build-modules/write-a-driver-module/) for the general module development guide. The key technique is accessing the source component through the `dependencies` parameter in your module's `reconfigure` method.

## Manage local storage

On constrained machines (Raspberry Pi, Jetson Nano, single-board computers),
local storage is limited. Understanding how Viam manages the capture directory
helps you avoid filling the disk.

### How local storage works

- Captured data is written to the capture directory (default: `$HOME/.viam/capture`). When `viam-server` is installed through `viam-agent` it runs as root, so the path is `/root/.viam/capture`. See [Capture directories](/data/reference/#capture-directories) for the full per-platform breakdown.
- Each capture is written as a `.capture` file: length-delimited binary protobuf. The first message is metadata describing the capture; the remaining messages hold the captured data. Images and tabular readings use the same container format.
- The sync process uploads `.capture` files and deletes them after successful upload.
- If sync is disabled or the network is down, files accumulate locally.

### Configure storage limits

You can configure the maximum storage that data capture will use on disk. In
your data management service configuration, set the `maximum_capture_file_size_bytes`
attribute to limit the size of individual capture files, and monitor the overall
capture directory size.

To check current disk usage of the capture directory (substitute `/root/.viam/capture` if `viam-server` runs as root through `viam-agent`):

```bash
du -sh "$HOME/.viam/capture"
```

To monitor it over time:

```bash
watch -n 60 du -sh "$HOME/.viam/capture"
```

### Best practices for constrained machines

- **Use the lowest capture frequency that meets your needs.** Every reduction in
  frequency directly reduces storage pressure.
- **Enable sync.** Without sync, local storage fills indefinitely.
- **Use filtered capture.** The filtered camera and threshold sensor modules
  above reduce what gets written to disk, not just what gets synced.
- **Monitor disk space.** Set up a simple cron job or health check that alerts
  you when the capture directory exceeds a size threshold.
- **Adjust sync interval.** A shorter sync interval (for example, every 30 seconds)
  keeps the local buffer small. A longer interval (for example, every 5 minutes)
  reduces network requests but requires more local storage.

## Try it

### Verify your filtering is working

1. Configure one of the filtering techniques above on your machine.
2. Open the **DATA** tab in the Viam app.
3. Compare data volume before and after filtering:
   - Check how many new entries appear per minute with your filter active.
   - Compare to the rate you saw in
     [Capture and sync data](/data/capture-sync/capture-and-sync-data/) before
     filtering.
4. For the filtered camera, verify that captured images show meaningful
   variation between consecutive frames.

## Troubleshooting

{{< expand "Filtered camera module not loading" >}}

- Check the module logs in the Viam app (**LOGS** tab) for import errors or
  configuration issues.
- Verify that the camera name in the filtered camera attributes matches
  the name of your actual camera component exactly. Names are case-sensitive.
- Ensure the `filtered_camera` module is added to your machine and that
  the vision service and ML model service are both configured.

{{< /expand >}}

{{< expand "No data captured after enabling filter" >}}

- Verify that your ML model can detect the objects you expect. Test the vision
  service from the **CONTROL** tab to see its classifications and detections live.
- Confirm the source camera is still working. Check the raw camera's test panel
  in the Viam app.
- Verify that data capture is configured on the filtered camera component, not
  only on the raw camera.

{{< /expand >}}

{{< expand "Too much data still being captured" >}}

- Increase the confidence threshold in your filtered camera configuration to
  require higher confidence before capturing.
- Reduce the capture frequency on the filtered camera. Even with filtering, a
  high capture frequency means more comparisons and more opportunities for a
  frame to be flagged as changed.
- For sensor data, verify that `min_value` is set correctly and that the
  `field` name matches the actual key in the sensor readings.

{{< /expand >}}

{{< expand "Local disk filling up despite sync being enabled" >}}

- Check your network connection. If the machine cannot reach Viam's cloud, data
  accumulates locally.
- Verify that both **Capturing** and **Syncing** are enabled in the data
  management service configuration.
- Check the sync interval. A very long sync interval combined with high capture
  frequency can cause the local buffer to grow between sync cycles.
- Run `du -sh "$HOME/.viam/capture"` to check current usage (or `/root/.viam/capture` when `viam-server` runs as root).

{{< /expand >}}

## What's next

- [Query data](/data/query-data/) -- write SQL and MQL queries against your
  filtered, high-signal dataset.
- [Create a dataset](/train/create-a-dataset/) -- use filtered captures to
  build cleaner training datasets for ML models.
- [Write a module](/build-modules/write-a-driver-module/) -- learn more about
  building and deploying custom modules on Viam.
