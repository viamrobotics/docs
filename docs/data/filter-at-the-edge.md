---
linkTitle: "Filter at the edge"
title: "Filter at the edge"
weight: 50
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
monitoring. It does not help when you need to capture specific events -- for
that, continue to the next techniques.

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

You can use the [`filtered_camera`](https://app.viam.com/module/viam/filtered-camera) registry module to selectively capture only images that contain certain objects or people, using a machine learning (ML) model.
The filtered camera wraps an existing camera and only outputs frames that match your ML model's criteria, so only interesting frames are ever written to disk.

### Prerequisites

- A configured camera component on your machine. See [Configure a camera](/reference/components/camera/) if you need to set one up.
- The data management service configured. See [Capture and sync edge data](/data/) for instructions.

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

You can think of the vision service as the bridge between the ML model service and the output from your camera.

Add and configure the `vision / ML model` service on your machine.
From the **Select model** dropdown, select the name of your ML model service (for example, `mlmodel-1`).

{{% /tablestep %}}
{{% tablestep %}}
**Configure the filtered camera**

The `filtered-camera` {{< glossary_tooltip term_id="modular-resource" text="modular component" >}} pulls the stream of images from your camera component and applies the vision service to it.

Configure a `filtered-camera` component on your machine, following the [attribute guide in the module listing](https://app.viam.com/module/viam/filtered-camera).
Use the name of your camera component as the `"camera"` to pull images from, and select the name of the vision service you just configured as your `"vision"` service.
Then add all or some of the labels your ML model uses as classifications or detections in `"classifications"` or `"objects"`.

For example, if you are using the `EfficientDet-COCO` model, you could use a configuration like the following to only capture images when a person is detected with more than 80% confidence in your camera stream.

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
  "window_seconds": 0
}
```

You can also add a buffer window with `window_seconds`, which controls the duration of a buffer of images captured before a successful match.
If you were to set `window_seconds` to `3`, the camera would also capture and sync images from the 3 seconds before a person appeared in the camera stream.

{{% /tablestep %}}
{{% tablestep %}}
**Configure data capture and sync on the filtered camera**

Configure data capture and sync on the filtered camera following the same process as described in [Capture and sync data](/data/capture-sync/capture-and-sync-data/).
The filtered camera will only capture image data that passes the filters you configured in the previous step.

Turn off data capture on your original camera component if you haven't already, so that you don't capture duplicate or unfiltered images.

{{% /tablestep %}}
{{% tablestep %}}
**Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to Viam after a short delay.

{{% /tablestep %}}
{{% tablestep %}}
**View filtered data on Viam**

Once you save your configuration, place an object that your ML model can detect within view of your camera.

Images that pass your filter will be captured and will sync at the specified sync interval, which may mean you have to wait and then refresh the page for data to appear.
Your images will begin to appear under the **DATA** tab.

If no data appears after the sync interval, check the [**Logs**](/monitor/troubleshoot/#check-logs) and ensure that the condition for filtering is met.
You can test the vision service from the [**CONTROL** tab](/monitor/teleoperate/) to see its classifications and detections live.

{{% /tablestep %}}
{{% tablestep %}}
**(Optional) Trigger sync with custom logic**

By default, the captured data syncs at the regular interval you specified in the data capture config.
If you need to trigger sync in a different way, see [Conditional cloud sync](/data/capture-sync/conditional-sync/) for a documented example of syncing data only at certain times of day.

{{% /tablestep %}}
{{< /table >}}

{{< alert title="Build your own filtering module" color="tip" >}}

If the `filtered_camera` registry module doesn't meet your needs, you can build a custom filtering module.
See [Create a data filtering module](/tutorials/configure/pet-photographer/) for a full walkthrough, or [Write a module](/build-modules/write-a-driver-module/) for general module development guidance.

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

- Captured data is written to `~/.viam/capture` by default.
- Each capture creates a file (JPEG for images, JSON for tabular data).
- The sync process uploads files and deletes them after successful upload.
- If sync is disabled or the network is down, files accumulate locally.

### Configure storage limits

You can configure the maximum storage that data capture will use on disk. In
your data management service configuration, set the `maximum_capture_file_size_bytes`
attribute to limit the size of individual capture files, and monitor the overall
capture directory size.

To check current disk usage of the capture directory:

```bash
du -sh ~/.viam/capture
```

To monitor it over time:

```bash
watch -n 60 du -sh ~/.viam/capture
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
- Run `du -sh ~/.viam/capture` to check current usage.

{{< /expand >}}

## What's next

- [Query data](/data/query/query-data/) -- write SQL and MQL queries against your
  filtered, high-signal dataset.
- [Create a dataset](/train/create-a-dataset/) -- use filtered captures to
  build cleaner training datasets for ML models.
- [Write a module](/build-modules/write-a-driver-module/) -- learn more about
  building and deploying custom modules on Viam.
