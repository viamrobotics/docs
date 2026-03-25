---
linkTitle: "Manage data"
title: "Manage data"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "Capture, query, filter, pipeline, export, and visualize data."
aliases:
  - /build/data/
  - /services/data/capture/
  - /data/capture/
  - /build/micro-rdk/data_management/
  - /services/data/cloud-sync/
  - /data/cloud-sync/
  - /services/data/capture-sync/
  - /how-tos/sensor-data/
  - /services/data/
  - fleet/data-management/
  - /manage/data-management/
  - /services/data-management/
  - /manage/data/
  - /data-management/
  - /manage/data/view/
  - /data/view/
  - /services/data/view/
  - /how-tos/collect-data/
  - /how-tos/collect-sensor-data/
  - /get-started/quickstarts/collect-data/
  - /use-cases/collect-sensor-data/
  - /use-cases/image-data/
  - /get-started/collect-data/
  - /fleet/data-management/
  - /data-ai/capture-data/capture-sync/
  - /data/data-capture-reference/
  - /data/how-sync-works/
  - /data-ai/capture-data/advanced/how-sync-works/
  - /data/capture-sync/how-sync-works/
  - /data-ai/
  - /data-ai/capture-data/
  - /data-ai/data/
---

Viam's data management service captures data from configured resources, writes it to local storage, and syncs it to the cloud.
From there you can query, filter, build pipelines, sync to your own database, or visualize your data.

- Captured data is written to <file>~/.viam/capture</file> by default.
- A separate sync process uploads data to Viam's cloud at a configured interval, then deletes local files.
- Capture and sync run independently: you can use one without the other.

<img src="/data-manager.svg" alt="Diagram showing data being captured, synced, and removed." class="aligncenter overview imgzoom" style="width:800px;height:auto" >

## How capture and sync work

The data management service can capture from multiple resources at the same or different frequencies.
There is no software-imposed limit on capture frequency, but your hardware may impose practical limits. Avoid setting rates higher than your hardware can sustain.

If a machine restarts, data capture automatically resumes and any data not yet synced is synced.

You can enable sync without data capture.
If you place files in the capture directory or in a directory listed in `"additional_sync_paths"`, the sync process uploads them to the cloud.

## Capture directories

By default, captured data is stored in <file>~/.viam/capture</file>.
The actual path depends on your platform:

<!-- prettier-ignore -->
| Platform | Default directory |
| -------- | ----------------- |
| Windows | With `viam-agent`: <FILE>C:\Windows\system32\config\systemprofile\.viam\capture</FILE>. Manual installation: <FILE>C:\Users\admin\.viam\capture</FILE>. |
| Linux | With root or sudo: <FILE>/root/.viam/capture</FILE>. |
| macOS | <FILE>/Users/\<username\>/.viam/capture</FILE>. |

{{% expand "Can't find the capture directory?" %}}

The path depends on where `viam-server` runs and the operating system.
Check your machine's startup logs for the `$HOME` value:

```sh
2025-01-15T14:27:26.073Z    INFO    rdk    server/entrypoint.go:77    Starting viam-server with following environment variables    {"HOME":"/home/johnsmith"}
```

{{% /expand%}}

You can change the capture directory with the `capture_dir` attribute.
See [Advanced data capture and sync configurations](/data/capture-sync/advanced-data-capture-sync/) for details.

## Security and data integrity

Data is encrypted in transit using {{< glossary_tooltip term_id="grpc" text="gRPC" >}} and encrypted at rest by the cloud storage provider.

The sync process is designed to prevent data loss and duplication:

- If the connection drops during sync, the service retries at exponentially increasing intervals (up to once per hour) until the connection is restored.
- Sync resumes where it left off without duplicating data. If an interruption happens mid-file, that file is re-uploaded from the beginning.
- To avoid syncing files still being written to, the service waits until a file hasn't been modified for 10 seconds. This is [configurable](/data/capture-sync/advanced-data-capture-sync/#data-management-service-attributes).

## Local storage and automatic deletion

After data syncs successfully, it is automatically deleted from local storage.
While a machine is offline, captured data accumulates locally.
Make sure your machine has enough storage to buffer data during expected offline periods.

{{< alert title="Warning" color="warning" >}}
If your machine is offline and its disk fills up, the data management service will delete captured data to free space and keep the machine running.
{{< /alert >}}

Automatic deletion triggers when _all_ of these conditions are met:

- Data capture is enabled
- Local disk usage is ≥ 90%
- The capture directory accounts for ≥ 50% of local disk usage

If disk usage is ≥ 90% but the capture directory is less than 50% of that, a warning is logged and no data is deleted.

Automatic deletion only affects files in the capture directory. Data outside it is never touched.

If your machine captures a large amount of data or frequently goes offline, consider pointing `capture_dir` to a larger, dedicated storage device.
You can also control deletion behavior with the `delete_every_nth_when_disk_full` attribute.
See [Advanced data capture and sync configurations](/data/capture-sync/advanced-data-capture-sync/) for both options.

## Supported resources

The following components and services support data capture and cloud sync.
Not all models support all methods. For example, webcams do not capture point clouds.

{{< readfile "/static/include/data/capture-supported.md" >}}

## Micro-RDK

The micro-RDK (for ESP32 and similar microcontrollers) supports data capture with a limited set of resources.
See the **Micro-RDK** tab in the supported resources table above for details.

On micro-RDK devices, captured data is stored in the ESP32's flash memory until it is uploaded to the cloud.
If the machine restarts before all data is synced, unsynced data since the last sync point is lost.
High frequency data collection (> 100 Hz) requires special considerations on the ESP32.

## Advanced configuration

For JSON-level configuration options including retention policies, sync optimization, direct MongoDB capture, and remote parts capture, see [Advanced data capture and sync configurations](/data/capture-sync/advanced-data-capture-sync/).

## Related pages

- [Capture and sync](/data/capture-sync/): configure data capture and cloud sync
- [Query](/data/query/): query, aggregate, and analyze captured data
- [Export and integrate](/data/export/): export data or sync it to your own database
- [Filter at the edge](/data/filter-at-the-edge/): reduce data before syncing with ML, thresholds, or frequency tuning
- [Visualize data](/data/visualize-data/): build dashboards with Teleop or Grafana
- [Trigger on data events](/data/trigger-on-data/): send alerts when data syncs from a machine
