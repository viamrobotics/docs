---
linkTitle: "Start data capture"
title: "Start data capture"
weight: 5
layout: "docs"
type: "docs"
description: "Capture data from any resource and sync it to the cloud."
capabilities: ["data-capture"]
diataxis: how-to
date: "2025-01-30"
aliases:
  - /data/capture-and-sync-data/
  - /build/foundation/capture-and-sync-data/
  - /foundation/capture-and-sync-data/
  - /data-ai/capture-data/capture-sync/
---

Configure your machine to automatically record sensor readings, camera images, and other component data, then sync it to the cloud. For the other ways to control what your machine captures and when it syncs, see the [Capture and sync overview](/data/capture-sync/overview/).

## 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.

## 2. Enable data capture on a component {#configure-data-capture}

1. Find your component (for example, `my-camera`) in the machine configuration.
2. Click the **Data Capture** button.
3. If you see a "Data management service missing" banner, click
   **Create data management service**, click **Save**, navigate back to
   your component, and click the **Data Capture** button again.
4. Select the method to capture:
   - For a camera, select **GetImages**. This captures a frame from the camera
     each time it fires.
   - For a sensor, select **Readings**. This records the sensor's current
     values.
5. Set the **capture frequency**. This is specified in hertz (captures per
   second):
   - `0.5` = one capture every 2 seconds
   - `0.2` = one capture every 5 seconds
   - `1` = one capture per second
   - Start low. For cameras, `0.5` Hz is a reasonable starting point. You can
     always increase it later.
6. Click **Save** in the upper right.

After saving, `viam-server` begins capturing immediately. You do not need to
restart anything.

{{< alert title="Tip" color="tip" >}}

You can add multiple capture methods to a single component (for example,
capture both `GetImages` and `NextPointCloud` from the same camera), each
with its own frequency.

{{< /alert >}}

## 3. Capture from additional components (optional)

Repeat step 2 for any other components you want to capture from. Each
component's data capture is independent -- you can have a camera capturing
images every 2 seconds and a sensor capturing readings every 10 seconds at the
same time.

To capture from components on another part of a multi-part machine, see [Multi-part capture](/data/capture-sync/remote-parts-capture/).

## 4. Sync data from another directory (optional)

You can also sync files from directories outside of the default capture path.
This is useful for uploading a batch of existing data or syncing files that another process writes to a folder on your machine.

In the data management service configuration, add the directory path to **Additional paths** (or `"additional_sync_paths"` in JSON mode).

{{< alert title="Caution" color="caution" >}}

Data synced from additional paths is deleted from the device after upload, just like captured data.
If you want to keep a local copy, copy the data to a new folder and sync that folder instead.

{{< /alert >}}

{{<imgproc src="/services/data/data-sync-temp.png" resize="x1100" declaredimensions=true alt="Data service configured with an additional sync path." style="width: 600px" class="shadow imgzoom" >}}

## 5. Verify data is syncing

Wait 30 seconds to a minute for data to accumulate and sync, then:

1. In the Viam app, click the **DATA** tab in the top navigation. The tab opens on the **Images** view by default.
2. For camera captures, you should see image thumbnails appearing. For sensor data, click the **Sensors** tab to see the latest readings from each machine and resource. To see historical rows of tabular data, click the small search icon next to a resource on the Sensors tab to open the query editor.
3. Use the filters on the left to narrow by:
   - **Machine** -- select your specific machine
   - **Component** -- select the component you configured
   - **Time range** -- pick a recent window

If you see data flowing in, capture and sync are working correctly.

## Reduce capture frequency {#reduce-capture-frequency}

The amount of data a component produces scales directly with its capture frequency: dropping a camera from `1` Hz to `0.1` Hz cuts its data volume by ten.
If you need periodic snapshots rather than continuous monitoring, lower the frequency:

1. On your machine's **CONFIGURE** tab, find the component you capture from.
2. In its **Data capture** section, change the **frequency** of the capture method.
3. Click **Save**.

The change takes effect immediately, without a restart.

A lower frequency doesn't help when you need to capture specific events, such as only the frames with a person in them.
For that, use a [filtered camera](/data/capture-sync/filtered-camera/) or [capture on demand](/data/capture-sync/capture-on-demand/).

## Manage local storage {#manage-local-storage}

Captured data is written to the machine's capture directory, then deleted after it syncs.
If sync is disabled, held back by [conditional sync](/data/capture-sync/conditional-sync/), or the machine is offline, files accumulate on disk.
When the disk is nearly full, the data management service [deletes captured files automatically](/data/reference/#automatic-deletion) to keep the machine running, so unsynced data can be lost.

On machines with little storage, such as single-board computers:

- **Use the lowest capture frequency that meets your needs.** Every reduction in frequency directly reduces storage pressure.
- **Keep sync enabled.** Without sync, the capture directory grows until automatic deletion starts.
- **Capture only what you need.** A [filtered camera](/data/capture-sync/filtered-camera/) or [capture on demand](/data/capture-sync/capture-on-demand/) reduces what gets written to disk, not just what gets synced.
- **Choose the sync interval deliberately.** A short interval, such as every 30 seconds, keeps the local backlog small. A longer interval reduces network requests but needs more local storage.
- **Monitor disk usage.** Check the size of the capture directory, and set up an alert or health check if it grows past a threshold:

  ```sh {class="command-line" data-prompt="$"}
  du -sh "$HOME/.viam/capture"
  ```

  Use `/root/.viam/capture` when `viam-server` runs as root through `viam-agent`. See [Capture directories](/data/reference/#capture-directories) for every platform.

## Supported resources {#supported-resources}

Any built-in or modular component that implements a capturable method can be configured for data capture. The following table lists the most commonly captured component types and their methods:

| Component type  | Capturable methods                                                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Camera          | `ReadImage`, `GetImages`, `NextPointCloud`, `GetWorldPose`                                                                                              |
| Audio in        | `GetAudio`, `GetWorldPose`                                                                                                                              |
| Sensor          | `GetReadings`, `GetWorldPose`                                                                                                                           |
| Movement sensor | `GetPosition`, `GetLinearVelocity`, `GetAngularVelocity`, `GetCompassHeading`, `GetLinearAcceleration`, `GetOrientation`, `GetReadings`, `GetWorldPose` |
| Encoder         | `GetTicksCount`, `GetWorldPose`                                                                                                                         |
| Motor           | `GetPosition`, `IsPowered`, `GetWorldPose`                                                                                                              |
| Power sensor    | `GetVoltage`, `GetCurrent`, `GetPower`, `GetReadings`, `GetWorldPose`                                                                                   |
| Servo           | `GetPosition`, `GetWorldPose`                                                                                                                           |
| Arm             | `GetEndPosition`, `GetJointPositions`, `GetWorldPose`                                                                                                   |
| Gantry          | `GetPosition`, `GetLengths`, `GetWorldPose`                                                                                                             |
| Board           | `Analogs`, `Gpios`, `GetWorldPose`                                                                                                                      |
| Vision service  | `CaptureAllFromCamera`                                                                                                                                  |
| SLAM service    | `GetPosition`, `GetPointCloudMap`                                                                                                                       |

Every component also supports `GetWorldPose` (requires a configured [frame system](/motion-planning/frame-system/)) and `DoCommand`. Modular components that return readings through any of these methods are automatically capturable.

## Troubleshooting

{{< expand "No data appears in the Data tab" >}}

- **Wait a minute.** Data must be captured locally and then synced to the cloud.
  The first entries can take 30-60 seconds to appear.
- **Is the data management service enabled?** Go to your machine's
  **CONFIGURE** tab and check that the data management service exists and both
  **Capturing** and **Syncing** are toggled on.
- **Is capture configured on the component?** Verify that the component's Data
  capture section shows at least one method with a non-zero frequency.
- **Is the machine online?** Data syncs only when the machine has a network
  connection. Check the machine's status indicator in the Viam app.

{{< /expand >}}

{{< expand "Data appears but images are missing or blank" >}}

- Verify the camera works in the test panel first. If the test panel shows
  nothing, the issue is with the camera configuration, not data capture.
- Check that the capture method is **GetImages**, not another method.

{{< /expand >}}

{{< expand "Data capture frequency seems wrong" >}}

- The frequency is in hertz (captures per second), not seconds between captures.
  `0.5` Hz means once every 2 seconds, not twice per second.
- High-frequency capture (above 1 Hz for cameras) generates large amounts of
  data. Start with `0.5` Hz or lower unless you need high-frequency capture.

{{< /expand >}}

{{< expand "Local disk filling up" >}}

- By default, captured data is stored in `$HOME/.viam/capture` before syncing
  (`/root/.viam/capture` when `viam-server` runs as root through `viam-agent`).
  If sync is disabled or the machine is offline for an extended period, this
  directory can grow large.
- Check that the **Syncing** toggle is on in the data management service
  configuration.
- Check the network connection. If the machine can't reach the Viam cloud, data
  accumulates locally.
- Check the sync interval. A long sync interval combined with a high capture
  frequency lets the local backlog grow between sync cycles.
- See [Manage local storage](#manage-local-storage).

{{< /expand >}}

## What's next

- [Query data](/data/query-data/): write queries, set up data pipelines, and export data
- [Add computer vision](/vision/configure/): run ML models on your camera feed and capture detection results
- [Capture on demand](/data/capture-sync/capture-on-demand/): start and stop capture on several components at once with a capture control sensor, and record sequences
- [Create a dataset](/train/create-a-dataset/): organize captured images into training datasets
- [Reference](/data/reference/): JSON-level config, retention policies, and sync optimization
