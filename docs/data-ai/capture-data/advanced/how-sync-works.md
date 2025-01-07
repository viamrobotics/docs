---
linkTitle: "How sync works"
title: "How sync works"
tags: ["data management", "data", "services"]
weight: 12
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Data sync works differently for viam-server and viam-micro-server."
date: "2024-12-18"
prev: "/data-ai/capture-data/conditional-sync/"
---

Data capture and cloud sync works differently for `viam-server` and `viam-micro-server`.

{{< tabs >}}
{{% tab name="viam-server" %}}

The data is captured locally on the machine's storage and, by default, stored in the `~/.viam/capture` directory.

If a machine restarts for any reason, capture automatically resumes and any data already stored but not yet synced is synced.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.
Avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

Data capture is frequently used with cloud sync.
You can start and stop capture and sync independently.
You can also enable cloud sync without data capture and it will sync data in either the sync directory or in the additional sync paths configured in the `viam-server` config.
If a file in either the data capture directory or any of the sync paths ends with <file>.capture</file> it will be treated as a file with data that was captured by data capture.
If it ends in <file>.prog</file> it will be ignored as this extension is used by data capture to denote that a file is a capture file that's currently being written to.
If a file is in the capture directory or one of its descendants or any of the additional sync paths or their descendants and doesn't have <file>.prog</file> nor <file>.capture</file> extensions, it will be treated as an arbitrary file and, like <file>.capture</file> files, synced if data sync is enabled and the robot is able to connect to [the Viam app](https://app.viam.com).

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

## Data integrity

Viam's data management service is designed to safeguard against data loss, data duplication and otherwise compromised data.

If the internet becomes unavailable or the machine needs to restart during the sync process, the sync is interrupted.
If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval in between tries is at one hour, at which point the service retries the sync every hour.
When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.
If the interruption happens mid-file, sync resumes from the beginning of that file.

To avoid syncing files that are still being written to, the data management service only syncs arbitrary files that haven't been modified in the previous 10 seconds.
This default can be changed with the [`file_last_modified_millis` config attribute](/data-ai/capture-sync/#configure-the-data-management-service).

## Storage

Data that is successfully synced to the cloud is automatically deleted from local storage.

When a machine loses its internet connection, it cannot resume cloud sync until it can reach the Viam Cloud again.

{{<imgproc src="/services/data/data_management.png" resize="x1100" declaredimensions=true alt="Data is captured on the machine, uploaded to the cloud, and then deleted off local storage." class="imgzoom" >}}

To ensure that the machine can store all data captured while it has no connection, you need to provide enough local data storage.

If your robot is offline and can't sync and your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.
For more information, see [Automatic data deletion details](/data-ai/capture-data/capture-sync/#click-for-more-automatic-data-deletion-details)

Data capture supports capturing tabular data directly to MongoDB in addition to capturing to disk.
For more information, see [Capture directly to MongoDB](/data-ai/capture-data/capture-sync/#capture-directly-to-mongodb).
