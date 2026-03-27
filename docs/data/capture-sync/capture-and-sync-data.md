---
linkTitle: "Start data capture"
title: "Start data capture"
weight: 5
layout: "docs"
type: "docs"
description: "Capture data from any resource and sync it to the cloud."
date: "2025-01-30"
aliases:
  - /data/capture-and-sync-data/
  - /build/foundation/capture-and-sync-data/
  - /foundation/capture-and-sync-data/
---

Configure your machine to automatically record sensor readings, camera images, and other component data, then sync it to the cloud. For an overview of how data capture and sync work, see the [Manage data overview](/data/overview/).

## 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.

## 2. Enable data capture on a component

1. Find your component (for example, `my-camera`) in the machine configuration.
2. Scroll to the **Data capture** section in the component's configuration
   panel.
3. Click **+ Add method**.
4. If this is your first time configuring data capture, Viam will prompt you to
   enable the **data management service**. Click to enable it. This adds the
   service to your machine configuration and enables both capture and cloud
   sync.
5. Select the method to capture:
   - For a camera, select **GetImages**. This captures a frame from the camera
     each time it fires.
   - For a sensor, select **Readings**. This records the sensor's current
     values.
6. Set the **capture frequency**. This is specified in hertz (captures per
   second):
   - `0.5` = one capture every 2 seconds
   - `0.2` = one capture every 5 seconds
   - `1` = one capture per second
   - Start low. For cameras, `0.5` Hz is a reasonable starting point. You can
     always increase it later.
7. Click **Save** in the upper right.

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

1. In the Viam app, click the **DATA** tab in the top navigation.
2. You should see captured data appearing. For camera captures, you will see
   image thumbnails. For sensor data, you will see tabular entries.
3. Use the filters on the left to narrow by:
   - **Machine** -- select your specific machine
   - **Component** -- select the component you configured
   - **Time range** -- pick a recent window
   - **Data type** -- Images or Tabular

If you see data flowing in, capture and sync are working correctly.

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

- By default, captured data is stored in `~/.viam/capture` before syncing. If
  sync is disabled or the machine is offline for an extended period, this
  directory can grow large.
- Re-enable sync or manually clear the capture directory if needed.
- Check that the **Syncing** toggle is on in the data management service
  configuration.

{{< /expand >}}

## What's next

- [Query data](/data/query-data/): write queries, set up data pipelines, and export data
- [Add computer vision](/vision/configure/): run ML models on your camera feed and capture detection results
- [Create a dataset](/train/create-a-dataset/): organize captured images into training datasets
- [Advanced configuration](/data/reference/): JSON-level config, retention policies, and sync optimization
