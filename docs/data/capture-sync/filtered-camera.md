---
linkTitle: "Filtered camera"
title: "Capture only the images you need"
weight: 8
layout: "docs"
type: "docs"
description: "Use an ML model on the machine to decide which camera frames to capture, so only frames that match a label or detection are stored and synced."
capabilities: ["data-capture"]
diataxis: how-to
date: "2025-01-30"
aliases:
  - /data/filter-at-the-edge/
  - /build/data/filter-at-the-edge/
  - /data-ai/capture-data/filter-before-sync/
  - /how-tos/image-data/
  - /tutorials/projects/filtered-camera/
---

Cameras produce more frames than most applications need, and most consecutive frames are nearly identical.
Instead of capturing every frame and sorting through them later, you can have the machine decide which frames are worth keeping.
Frames that don't match are never written to disk, so they cost no storage, bandwidth, or cloud storage.

The [`filtered-camera`](https://app.viam.com/module/viam/filtered-camera) registry module does this by running an ML vision model on each frame and gating capture on the result.
It wraps an existing camera and a vision service so data capture sees a pre-filtered stream.

For other ways to reduce how much your machine captures and syncs, see [Capture and sync overview](/data/capture-sync/overview/).

## How it works

The filtered camera sits between a raw camera and the data manager:

1. A raw **camera** component (for example, a USB webcam) provides the image stream.
2. A **vision service** runs an ML classifier or detector against each image and returns classifications or detections with confidence scores.
3. A **`filtered-camera`** component wraps the camera and the vision service. It continuously pulls frames from the camera into an in-memory ring buffer, asks the vision service to score each frame, and marks a frame as "interesting" when a classification or detection passes a confidence threshold you configure.
4. **Data capture** is configured on the `filtered-camera` component, not on the raw camera. Because the filtered camera is itself a camera component, the data manager captures from it the same way it would from any other camera. Only frames that passed the filter are ever written to disk.
5. The normal sync pipeline uploads the captured files to the cloud.

The raw camera's image stream is unchanged: the CONTROL tab, other services, and anything else on the machine still see every frame. Only the filtered camera, and therefore only data capture, sees the filtered subset.

Optionally, you can configure a pre-trigger buffer with `window_seconds_before` and a post-trigger buffer with `window_seconds_after`. When a frame triggers the filter, the module includes the buffered frames from those windows alongside the trigger frame. Use this when you need context leading up to or after an event.

## Prerequisites

- A configured camera component on your machine. See [Configure a camera](/hardware/common-components/add-a-camera/) if you need to set one up.
- The data management service configured. See [Start data capture](/data/capture-sync/capture-and-sync-data/) for instructions.

## Use a filtered camera

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

## Advanced: build a custom filter module

For filtering needs that go beyond what the `filtered-camera` module provides, you can write your own module. Common examples:

- A sensor wrapper that only reports readings above a threshold (for example, temperature above 50 degrees C)
- A camera filter with custom logic specific to your application
- A filter that combines data from multiple sensors before deciding what to capture

The pattern is: write a module that wraps an existing component, evaluates its data against your criteria, and only returns data worth capturing. Configure data capture on the wrapper component instead of the raw component.

See [Write a module](/build-modules/write-a-driver-module/) for the general module development guide. The key technique is accessing the source component through the `dependencies` parameter in your module's constructor.

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
- Reduce `window_seconds_before` and `window_seconds_after`. Every trigger also
  captures the buffered frames from those windows.
- Set `cooldown_s` to suppress new triggers for a while after each capture
  window, if events arrive in bursts.
- Lower the capture frequency on the filtered camera to keep fewer frames from
  each event.

{{< /expand >}}

## What's next

- [Capture on demand](/data/capture-sync/capture-on-demand/): start and stop capture on several components at once. You can list a filtered camera as one of its resources.
- [Query data](/data/query-data/): write SQL and MQL queries against your filtered data.
- [Create a dataset](/train/create-a-dataset/): use filtered captures to build cleaner training datasets for ML models.
