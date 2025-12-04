---
linkTitle: "How sync works"
title: "How sync works"
tags: ["data management", "data", "services"]
weight: 12
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Data capture and sync work differently for viam-server and viam-micro-server."
date: "2024-12-18"
updated: "2025-12-04"
---

Data capture and cloud sync work differently for `viam-server` and `viam-micro-server`.

{{< tabs >}}
{{% tab name="viam-server" %}}

The data is captured locally on the machine's storage and, by default, stored in the <FILE>~/.viam/capture</FILE> directory:

<!-- prettier-ignore -->
| Architecture | Default directory |
| ------------ | ----------------- |
| Windows | With `viam-agent`: <FILE>C:\Windows\system32\config\systemprofile\.viam\capture</FILE>. Manual installation: <FILE>C:\Users\admin\.viam\capture</FILE>. |
| Linux | When running with root or sudo users: <FILE>/root/.viam/capture</FILE>. |
| macOS | <FILE>/Users/\<username\>/.viam/capture</FILE>. |

{{% expand "Can't find the directory data is stored in? Click here." %}}

The relative path for the data capture directory depends on where `viam-server` is run from, as well as the operating system of the machine.

To find the `$HOME` value, check your machine's logs on startup, which will log it in the environment variables:

```sh
2025-01-15T14:27:26.073Z    INFO    rdk    server/entrypoint.go:77    Starting viam-server with following environment variables    {"HOME":"/home/johnsmith"}
```

{{% /expand%}}

If a machine restarts for any reason, data capture automatically resumes and any data already stored but not yet synced is synced.

The service can capture data from multiple resources at the same or different frequencies.
The service does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.
Avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

Data capture is frequently used with cloud sync.
You can start and stop capture and sync independently.
You can also enable cloud sync without data capture and it will sync data in the capture directory, as well as the additional sync paths configured in the `viam-server` config.
If you place data like images or files in the `~/.viam/capture` directory or another directory set up for sync with the data manager, for example with the `"additional_sync_paths"` config attribute, it will sync this data to the cloud.

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

Viam's data management service is designed to safeguard against data loss, data duplication, and otherwise compromised data.

If the internet becomes unavailable or the machine needs to restart during the sync process, the sync is interrupted.
If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval between retries reaches one hour, at which point the service retries the sync every hour.
When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.
If the interruption happens mid-file, sync resumes from the beginning of that file.

To avoid syncing files that are still being written to, the data management service only syncs arbitrary files that haven't been modified in the previous 10 seconds.
This default can be changed with the [`file_last_modified_millis` config attribute](/data-ai/capture-data/advanced/advanced-data-capture-sync/#click-to-view-data-management-attributes).

## Automatic data deletion

If cloud sync is enabled, the data management service deletes captured data from the disk once it has successfully synced to the cloud.

{{< alert title="Warning" color="warning" >}}

If your robot is offline and can't sync and your machine's disk fills up beyond a certain threshold, the data management service will delete captured data to free up additional space and maintain a working machine.

{{< /alert >}}

The data management service will also automatically delete local data in the event your machine's local storage fills up.
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

## Storage

Data that is successfully synced to the cloud is automatically deleted from local storage.

When a machine loses its internet connection, it cannot resume cloud sync until it can reach the Viam Cloud again.

{{<imgproc src="/services/data/data_management.png" resize="x1100" declaredimensions=true alt="Data is captured on the machine, uploaded to the cloud, and then deleted off local storage." class="imgzoom" >}}

To ensure that the machine can store all data captured while it has no connection, you need to provide enough local data storage.

For information about automatic data deletion when storage fills up, see [Automatic data deletion](#automatic-data-deletion) above.

Data capture supports capturing tabular data directly to MongoDB in addition to capturing to disk.
For more information, see [Capture directly to MongoDB](/data-ai/capture-data/advanced/advanced-data-capture-sync/#capture-directly-to-your-own-mongodb-cluster).
