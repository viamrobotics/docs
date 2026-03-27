---
linkTitle: "Stop data capture"
title: "Stop or disable data capture"
weight: 6
layout: "docs"
type: "docs"
description: "Stop capturing data for specific resources, all resources, or disable cloud sync."
date: "2025-01-30"
aliases:
  - /data/stop-data-capture/
  - /build/foundation/stop-data-capture/
  - /foundation/stop-data-capture/
---

## What problem this solves

You have data capture running but need to turn it off, either temporarily
(during maintenance, testing, or debugging) or permanently (you're done
collecting data for a component).

You can stop data capture at different levels of granularity: disable it for a single resource, turn it off for all resources on a machine, or leave capture running locally but stop syncing to the cloud.

## Stop data capture for a specific resource

To stop capturing data from a single component while leaving other components'
capture running:

1. Navigate to your machine's **CONFIGURE** tab in the Viam app.
2. Find the component you want to stop capturing from.
3. Scroll to the **Data capture** section in the component's configuration panel.
4. Toggle the configured capture method's switch to **Off**.
5. Click **Save**.

The component stops capturing immediately. Other components with data capture
configured continue capturing normally.

## Stop data capture for all resources

To stop all data capture across your entire machine at once:

1. Navigate to your machine's **CONFIGURE** tab.
2. Find the **data management** service in your configuration.
3. Toggle the **Capturing** switch to **Off**.
4. Click **Save**.

This disables capture for every component on the machine. Individual component
capture configurations are preserved. When you re-enable capturing, each
component resumes capturing with its previously configured methods and
frequencies.

## Disable cloud sync

To stop syncing captured data to the cloud while optionally continuing to
capture locally:

1. Navigate to your machine's **CONFIGURE** tab.
2. Find the **data management** service in your configuration.
3. Toggle the **Syncing** switch to **Off**.
4. Click **Save**.

With sync disabled, data continues to accumulate in the local capture directory
(`~/.viam/capture` by default) but is not transmitted to the cloud. When you
re-enable sync, the backlog of locally captured data syncs automatically.

{{< alert title="Note" color="note" >}}

If you leave sync disabled for an extended period while capture continues,
the local capture directory can grow large. Monitor disk space on your machine
if you plan to capture without syncing.

{{< /alert >}}

## Troubleshooting

{{< expand "Data still appearing in the cloud after disabling capture" >}}

- Click **Save** after toggling the switch. Changes don't take effect until saved.
- Data that was already captured and queued for sync will still sync even after
  capture is disabled. Wait for the sync backlog to drain.

{{< /expand >}}

{{< expand "Want to delete already-captured data" >}}

Stopping capture prevents new data from being collected, but does not delete
existing data. To delete data that has already synced to the cloud, use the
**DATA** tab in the Viam app to filter and delete specific data entries.

{{< /expand >}}

{{< expand "Local capture directory still has files after re-enabling sync" >}}

After re-enabling sync, it may take a few minutes for the backlog to upload.
Files are removed from the local directory after successful sync. If files
persist, check that the machine has network connectivity and that the
**Syncing** switch is on.

{{< /expand >}}

## What's next

- [Filter at the edge](/data/filter-at-the-edge/) -- reduce data
  volume by filtering before syncing to the cloud.
- [Create a data pipeline](/data/pipelines/create-a-pipeline/) -- create
  scheduled pipelines to aggregate and summarize captured data.
- [Supported resources](/data/#supported-resources) -- which components
  and services support data capture.
