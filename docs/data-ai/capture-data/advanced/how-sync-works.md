---
linkTitle: "How sync works"
title: "How sync works"
tags: ["data management", "data", "services"]
weight: 12
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "TODO"
date: "2024-12-18"
prev: "/data-ai/capture-data/conditional-sync/"
---

Data capture and cloud sync works differently for `viam-server` and `viam-micro-server`.

{{< tabs >}}
{{% tab name="viam-server" %}}

The data is captured locally on the machine's storage and, by default, stored in the `~/.viam/capture` directory.

If a machine restarts for any reason, capture automatically resumes and any data from already stored but not yet synced is synced.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.
Avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

Data capture is frequently used with cloud sync.
However, if you want to manage your machine's captured data yourself, you can enable only data capture without cloud sync.

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

The data is captured in the ESP32's flash memory until it is uploaded to the Viam Cloud.

If the machine restarts before all data is synced, all unsynced data captured since the last sync point is lost.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, high frequency data collection (> 100Hz) requires special considerations on the ESP32.

{{% /tab %}}
{{< /tabs >}}

## Security

The data management service uses {{< glossary_tooltip term_id="grpc" text="gRPC" >}} calls to send and receive data, so your data is encrypted while in flight.
When data is stored in the cloud, it is encrypted at rest by the cloud storage provider.

## Data Integrity

Viam's data management service is designed to safeguard against data loss, data duplication and otherwise compromised data.

If the internet becomes unavailable or the machine needs to restart during the sync process, the sync is interrupted.
If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval in between tries is at one hour, at which point the service retries the sync every hour.
When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.
If the interruption happens mid-file, sync resumes from the beginning of that file.

To avoid syncing files that are still being written to, the data management service only syncs files that haven't been modified in the previous 10 seconds.

## Storage

Data that is successfully synced to the cloud is automatically deleted from local storage.

When a machine loses its internet connection, it cannot resume cloud sync until it can reach the Viam Cloud again.

{{<imgproc src="/services/data/data_management.png" resize="x1100" declaredimensions=true alt="Data is captured on the machine, uploaded to the cloud, and then deleted off local storage." class="imgzoom" >}}

To ensure that the machine can store all data captured while it has no connection, you need to provide enough local data storage.

{{< alert title="Warning" color="warning" >}}

If your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.

{{< /alert >}}

{{< expand "Automatic data deletion details" >}}

If cloud sync is enabled, the data management service deletes captured data once it has successfully synced to the cloud.

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

Data capture supports capturing tabular data directly to MongoDB in addition to capturing to disk.
For more information, see [Capture directly to MongoDB](/data-ai/reference/data/#capture-directly-to-mongodb).
