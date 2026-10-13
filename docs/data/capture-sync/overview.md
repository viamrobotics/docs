---
linkTitle: "Overview"
title: "Capture and sync overview"
weight: 1
layout: "docs"
type: "docs"
description: "Choose how your machine records data and when it uploads it: fixed-rate capture, filtered capture, capture on demand, or conditional sync."
capabilities: ["data-capture"]
diataxis: overview
date: "2026-10-13"
---

The data management service records data on your machine in two independent steps:

1. **Capture** writes readings and images from your components to the machine's local disk.
2. **Sync** uploads captured files to the Viam cloud, then deletes them from the machine.

Viam has several ways to control each step.
Controlling capture changes what is recorded at all, which saves disk space, bandwidth, and storage.
Controlling sync only changes when recorded data uploads: the machine still writes everything to disk.

## Choose how to capture

| You want to | Use |
| --- | --- |
| Record components all the time, at a fixed rate | [Start data capture](/data/capture-sync/capture-and-sync-data/) |
| Record less data from a component you already capture | [Reduce capture frequency](/data/capture-sync/capture-and-sync-data/#reduce-capture-frequency) |
| Keep only camera frames where an ML model detects or classifies something | [Use a filtered camera](/data/capture-sync/filtered-camera/) |
| Keep only one component's readings that meet a condition, such as a threshold | [Build a custom filter module](/data/capture-sync/filtered-camera/#advanced-build-a-custom-filter-module) |
| Record several components together only during specific moments, on command | [Capture on demand](/data/capture-sync/capture-on-demand/) |
| Record [sequences](/data/sequences/) to train on | [Capture on demand](/data/capture-sync/capture-on-demand/) |
| Record from components on other parts of a multi-part machine | [Multi-part capture](/data/capture-sync/remote-parts-capture/) |
| Stop recording some or all components | [Stop data capture](/data/capture-sync/stop-data-capture/) |

The filtered camera and custom filter modules decide frame by frame, or reading by reading, whether one component's data is worth keeping.
Capture on demand works at a different level: it turns capture on and off for a whole list of components at once, so their data lines up in the same time windows.
You can combine them, for example by listing a filtered camera in capture on demand's resources.

## Choose when to sync

| You want to | Use |
| --- | --- |
| Upload captured data at a regular interval | [Start data capture](/data/capture-sync/capture-and-sync-data/) |
| Upload only at certain times, or when a condition is met, such as a WiFi connection | [Conditional sync](/data/capture-sync/conditional-sync/) |
| Stop uploading, but keep capturing | [Disable cloud sync](/data/capture-sync/stop-data-capture/#disable-cloud-sync) |
| Upload files that didn't come from data capture, such as logs or images from your phone | [Upload external data](/data/capture-sync/upload-other-data/) |

When sync is held back, captured data builds up on the machine.
On machines with little storage, see [Manage local storage](/data/capture-sync/capture-and-sync-data/#manage-local-storage).

## Next steps

- [Start data capture](/data/capture-sync/capture-and-sync-data/): configure capture and sync on your first component.
- [Data management reference](/data/reference/): every data management service attribute.
