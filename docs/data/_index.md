---
linkTitle: "Manage data"
title: "Manage data"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "Capture sensor data and images on your robot, sync to the cloud, and query, export, or visualize your data."
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

Robots generate sensor readings, images, point clouds, and other data continuously. Viam captures this data on the machine, syncs it to the cloud, and makes it queryable, exportable, and usable for ML training without building a custom data pipeline.

## What are you trying to do?

| Goal                                           | Start here                                                                                                    |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Record sensor data or images from my robot     | [Capture and sync data](/data/capture-sync/capture-and-sync-data/)                                            |
| Reduce data volume before syncing to the cloud | [Filter at the edge](/data/filter-at-the-edge/)                                                               |
| Query or analyze captured data                 | [Query data](/data/query/query-data/)                                                                         |
| Build scheduled data transformations           | [Configure data pipelines](/data/query/configure-data-pipelines/)                                             |
| Export data to my own database or tools        | [Export data](/data/export/export-data/) or [Sync to your database](/data/export/sync-data-to-your-database/) |
| Build monitoring dashboards                    | [Visualize data](/data/visualize-data/)                                                                       |
| Get alerts when data meets a condition         | [Trigger on data events](/data/trigger-on-data/)                                                              |
| Debug what my robot did                        | [Debug and trace](/data/debug-and-trace/)                                                                     |
| Upload data from outside the capture pipeline  | [Upload external data](/data/capture-sync/upload-other-data/)                                                 |

## How data flows

Viam's data management service captures data from configured components, writes it to local storage, and syncs it to the cloud:

1. You configure which components to capture from and at what frequency.
2. Captured data is written to local disk (default: `~/.viam/capture`).
3. A separate sync process uploads data to Viam's cloud at a configurable interval, then deletes local files.
4. In the cloud, tabular data (sensor readings) is stored in MongoDB. Binary data (images, point clouds) is stored in blob storage.
5. From there you can query with SQL or MQL, export to your own tools, build datasets for ML training, or visualize in dashboards.

Capture and sync run independently: you can capture without syncing, or sync files from other sources without using Viam's capture.

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

## All pages in this section

- [Capture and sync data](/data/capture-sync/capture-and-sync-data/): configure data capture and cloud sync
- [Advanced data capture and sync](/data/capture-sync/advanced-data-capture-sync/): JSON-level configuration reference
- [Conditional sync](/data/capture-sync/conditional-sync/): sync based on sensor conditions
- [Stop data capture](/data/capture-sync/stop-data-capture/): disable capture or sync
- [Upload external data](/data/capture-sync/upload-other-data/): upload files from outside the capture pipeline
- [LoRaWAN](/data/capture-sync/lorawan/): capture data from LoRaWAN sensors
- [Filter at the edge](/data/filter-at-the-edge/): reduce data volume before syncing
- [Query data](/data/query/query-data/): query captured data with SQL or MQL
- [Query reference](/data/query/query-reference/): schema, operators, and optimization
- [Configure data pipelines](/data/query/configure-data-pipelines/): scheduled data transformations
- [Hot data store](/data/query/hot-data-store/): fast queries on recent data
- [Export data](/data/export/export-data/): download data with the CLI
- [Sync to your database](/data/export/sync-data-to-your-database/): integrate with external databases
- [Visualize data](/data/visualize-data/): build dashboards with Teleop or Grafana
- [Trigger on data events](/data/trigger-on-data/): alerts when data meets conditions
- [Debug and trace](/data/debug-and-trace/): distributed tracing for debugging
