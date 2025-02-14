---
linkTitle: "Capture and sync edge data"
title: "Capture and sync edge data"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
platformarea: ["data"]
description: "Capture data from a resource on your machine and sync the data to the cloud."
date: "2024-12-03"
aliases:
  - /services/data/capture/
  - /data/capture/
  - /build/micro-rdk/data_management/
  - /services/data/capture/
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
  - /services/data/
  - /data/
  - /manage/data/export/
  - /data/export/
  - /services/data/export/
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
---

You can use the data management service to capture data from [supported components and services](/data-ai/capture-data/capture-sync/#click-to-see-resources-that-support-data-capture-and-cloud-sync), then sync it to the cloud.
You can also sync data from arbitrary folders on your machine.

## How data capture and data sync works

The data management service writes data from your configured Viam resources to local storage on your edge device and syncs data from the edge device to the cloud:

- The data management service writes captured data to local edge device storage (<file>~/.viam/capture</file> by default).
- The data management service syncs data to the Viam cloud at a configured sync interval using encrypted gRPC calls and deletes it from the disk once synced.
- You can capture and sync data independently; one can run without the other.

For more information, see [How sync works](/data-ai/capture-data/advanced/how-sync-works/).

<<<<<<< HEAD
## Configure the data management service for your machine

{{< tabs >}}
{{% tab name="Config Builder" %}}

From your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), add the `data management` service.
On the panel that appears, configure data capture and sync attributes as applicable.
To both capture data and sync it to the cloud, keep both **Capturing** and **Syncing** switched on.

Click the **Save** button in the top right corner of the page to save your config.

{{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="Data capture configuration card." resize="600x" class="shadow" >}}

{{% /tab %}}
{{% tab name="JSON Example" %}}

{{< tabs >}}
{{% tab name="viam-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "name": "my-data-manager",
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 1,
        "capture_dir": "",
        "tags": [],
        "capture_disabled": false,
        "sync_disabled": true,
        "delete_data_on_part_deletion": true,
        "delete_every_nth_when_disk_full": 5,
        "maximum_num_sync_threads": 250
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "services": [
    {
      "name": "my-data-manager",
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": [],
        "sync_interval_mins": 3
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the data management service:

{{< expand "Click to view data management attributes" >}}

<!-- prettier-ignore -->
| Name               | Type   | Required? | Description | `viam-micro-server` Support |
| ------------------ | ------ | --------- | ----------- | ------------------- |
| `capture_disabled` | bool   | Optional | Toggle data capture on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. Note that even if capture is on for the whole part, but is not on for any individual {{< glossary_tooltip term_id="component" text="components" >}} (see Step 2), data is not being captured. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `capture_dir`      | string | Optional | Path to the directory on your machine where you want to store captured data. If you change the directory for data capture, only new data is stored in the new directory. Existing data remains in the directory where it was stored. <br> Default: `~/.viam/capture` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `tags` | array of strings | Optional | Tags to apply to all images or tabular data captured by this machine part. May include alphanumeric characters, underscores, and dashes. |  |
| `sync_disabled` | bool | Optional | Toggle cloud sync on or off for the entire machine {{< glossary_tooltip term_id="part" text="part" >}}. <br> Default: `false` |  |
| `additional_sync_paths` | string array | Optional | Paths to any other directories on your machine from which you want to sync data to the cloud. Once data is synced from a directory, it is automatically deleted from your machine. We recommend using absolute paths. For relative paths, see [How sync works](/data-ai/capture-data/advanced/how-sync-works/#cant-find-the-directory-data-is-stored-in-click-here). |  |
| `sync_interval_mins` | float | Optional | Time interval in minutes between syncing to the cloud. Viam does not impose a minimum or maximum on the frequency of data syncing. However, in practice, your hardware or network speed may impose limits on the frequency of data syncing. <br> Default: `0.1`, meaning once every 6 seconds. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_data_on_part_deletion` | bool | Optional | Whether deleting this {{< glossary_tooltip term_id="machine" text="machine" >}} or {{< glossary_tooltip term_id="part" text="machine part" >}} should result in deleting all the data captured by that machine part. <br> Default: `false` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `delete_every_nth_when_disk_full` | int | Optional | How many files to delete when local storage meets the [fullness criteria](/data-ai/capture-data/advanced/how-sync-works/#storage). The data management service will delete every Nth file that has been captured upon reaching this threshold. Use JSON mode to configure this attribute. <br> Default: `5`, meaning that every fifth captured file will be deleted. |   |
| `maximum_num_sync_threads` | int | Optional | Max number of CPU threads to use for syncing data to the Viam Cloud. <br> Default: [runtime.NumCPU](https://pkg.go.dev/runtime#NumCPU)/2 so half the number of logical CPUs available to viam-server |   |
| `mongo_capture_config.uri` | string | Optional | The [MongoDB URI](https://www.mongodb.com/docs/v6.2/reference/connection-string/) data capture will attempt to write tabular data to after it is enqueued to be written to disk. When non-empty, data capture will capture tabular data to the configured MongoDB database and collection at that URI.<br>See  `mongo_capture_config.database` and  `mongo_capture_config.collection` below for database and collection defaults.<br>See [Data capture directly to MongoDB](/data-ai/capture-data/advanced/how-sync-works/#storage) for an example config.|   |
| `mongo_capture_config.database` | string | Optional | When `mongo_capture_config.uri` is non empty, changes the database data capture will write tabular data to. <br> Default: `"sensorData"`   |   |
| `mongo_capture_config.collection` | string | Optional | When `mongo_capture_config.uri` is non empty, changes the collection data capture will write tabular data to.<br> Default: `"readings"`   |   |
| `cache_size_kb` | float | Optional | `viam-micro-server` only. The maximum amount of storage bytes (in kilobytes) allocated to a data collector. <br> Default: `1` KB. |  <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `file_last_modified_millis` | float | Optional | The amount of time to pass since arbitrary files were last modified until they are synced. Normal <file>.capture</file> files are synced as soon as they are able to be synced. <br> Default: `10000` milliseconds. |   |

{{< /expand >}}

## Configure data capture for individual resources
=======
## Configure data capture and sync for individual resources
>>>>>>> d6526a8b9 (Simplify page)

1. Navigate to a configured {{< glossary_tooltip term_id="resource" text="resource" >}} in **Builder** mode in the [Viam app](https://app.viam.com).
1. Find the **Data capture** section in the resource panel.
1. Click **+ Add method**.

   {{< imgproc src="/tutorials/data-management/add-method.png" alt="Disable data capture toggle" resize="700x" >}}

1. If you see a warning **Capture disabled on data management service**, click **Enable capture on data management service**.
1. Select a **Method** to capture data from.
1. Set the capture **frequency** in hertz, for example to `0.2` with `ReadImage` on a camera to capture an image every 5 seconds.
1. **Save** your config.

You can add multiple methods with different capture frequencies.

{{< expand "Click to see resources that support data capture and cloud sync" >}}

The following components and services support data capture and cloud sync:

{{< readfile "/static/include/data/capture-supported.md" >}}

{{< alert title="Support notice" color="note" >}}
Some models do not support all options, for example webcams do not capture point clouds.
{{< /alert >}}

{{< /expand >}}

For instructions on configuring data capture and sync with JSON, go to [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/) and follow the instructions for JSON examples.

## View captured data

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view).
1. Filter data by location, type of data, and more.

## Stop data capture or data sync

### Stop data capture for a specific resource

1. Navigate to the **Data capture** section of your resource's configuration card.
1. Toggle the configured capture method's switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-capture-resource.png" alt="Disable data capture toggle" resize="500x" >}}

1. **Save** your config.

### Stop data capture for all resources

1. Navigate to the **Data capture** section of the data management service configuration card.
1. Toggle the **Capturing** switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-capture.png" alt="Disable data capture toggle" resize="300x" >}}

1. **Save** your config.

### Disable data sync:

1. Navigate to the **Cloud sync** section of the data management service configuration card.
1. Toggle the **Syncing** switch to **Off**.

   {{< imgproc src="/tutorials/data-management/disable-sync.png" alt="Disable data sync toggle" resize="300x" >}}

1. **Save** your config.

{{< alert title="Tip: More ways to control data capture or sync" color="tip" >}}

For other ways to control data synchronization, see:

- [Conditional sync](/data-ai/capture-data/conditional-sync/)
- [Retention policies](/data-ai/capture-data/advanced/advanced-data-capture-sync/#cloud-data-retention)
- [Sync optimization](/data-ai/capture-data/advanced/advanced-data-capture-sync/#sync-optimization)

{{< /alert >}}

## Next steps

For more information on available configuration attributes and options like capturing directly to MongoDB or conditional sync, see [Advanced data capture and sync configurations](/data-ai/capture-data/advanced/advanced-data-capture-sync/).
To leverage AI, you can now [create a dataset](/data-ai/ai/create-dataset/) with the data you've captured.
