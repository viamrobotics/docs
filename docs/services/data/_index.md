---
title: "Data Management"
linkTitle: "Data Management"
weight: 10
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Capture data from machines, sync it to the cloud, and access it and train image classification and object detection models on the data."
aliases:
  - /manage/data-management/
  - /services/data-management/
  - /manage/data/
  - "/data-management/"
  - "/data-management/"
  - "/services/data/"
  - "/data/"
  - /manage/data/export/
  - /data/export/
  - /services/data/export/
  - /manage/data/view/
  - /data/view/
  - /services/data/view/
icon: true
images: ["/services/icons/data-management.svg"]
no_service: true
---

The data management service allows you to reliably capture and sync data to the cloud where you can query data from all your machines.
You can collect data from your robots, IoT devices, or any other machines, and sync all the data to one place in the cloud without needing to manually gather data from each machine.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/J0NNiQD0ocQ">}}

## On-device data management

The data management service:

- Automatically captures data at the rate you specify.
- Securely syncs data to the cloud at the frequency you define.
- Automatically deletes local data after syncing for space management.

{{< cards >}}
{{% manualcard link="/services/data/capture-sync/" title="Data capture and cloud sync" %}}

More details and how to configure capture and sync.

{{% /manualcard %}}
{{< /cards >}}

You can capture data from any of the following components and services:

{{< cards >}}
{{< relatedcard link="/components/arm/">}}
{{< relatedcard link="/components/board/">}}
{{< relatedcard link="/components/camera/">}}
{{< relatedcard link="/components/encoder/">}}
{{< relatedcard link="/components/gantry/">}}
{{< relatedcard link="/components/motor/">}}
{{< relatedcard link="/components/movement-sensor/">}}
{{< relatedcard link="/components/sensor/">}}
{{< relatedcard link="/components/servo/">}}
{{< relatedcard link="/services/vision/">}}
{{< /cards >}}

## Cloud data management

<br>
{{<imgproc src="/architecture/data-flow.svg" resize="x1100" declaredimensions=true alt="Data flowing from local disk to cloud to the Viam app, SDKs, and MQL and SQL queries." class="imgzoom">}}
<br><br>

Once your data is synced to the cloud, you can view, filter, and label data, and assign data to datasets, from your [Viam app **DATA** page](https://app.viam.com/data/view).
You can also interact with your data using the [Viam CLI](/cli/#data), or using the [data client API](/appendix/apis/data-client/).

<!-- markdownlint-disable-file MD034 -->

{{< cards >}}
{{% manualcard title="Create datasets" link="/services/data/dataset/" %}}

Label data for management and machine learning, with dynamic datasets that change with underlying data modifications.

{{% /manualcard %}}
{{% manualcard title="Export data" link="/how-tos/export-data/" %}}

Export data with the Viam CLI and download your data for offline access.

{{% /manualcard %}}
{{% manualcard title="Upload a batch of data" link="/how-tos/upload-data/" %}}

Upload data to the Viam cloud from your computer or mobile device using the data client API, the Viam CLI, or the Viam mobile app.

{{% /manualcard %}}
{{< /cards >}}

### Query your data

Once your data has [synced](/services/data/capture-sync/), you can query it using the [data client API](/appendix/apis/data-client/).
For _tabular_ sensor data, you can also [run {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} queries](/how-tos/sensor-data-query-sdk/) from the [Query subtab](https://app.viam.com/data/query) of the **Data** tab in the Viam app.

{{< cards >}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" noimage="True" %}}
{{% card link="/how-tos/sensor-data-query-sdk/" noimage="True" %}}
{{% card link="/appendix/apis/data-client/" noimage="True" %}}
{{< /cards >}}

### Permissions

Data management permissions vary between owners and operators.
For more information about who can do what with data, see [Data Permissions](/cloud/rbac/#data-and-machine-learning).

## API

The [data client API](/appendix/apis/data-client/) supports the following methods:

<br>

Methods to upload data like images or sensor readings directly to the Viam cloud:

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

<br>

Methods to download, filter, tag, or perform other tasks on data like images or sensor readings:

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

<br>

Methods to work with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

<br>

The data management API supports a separate set of methods that allow you to sync data to the Viam app.
For information about that API, see [Data Management API](/appendix/apis/services/data/).

For the command line interface `data` command, see [CLI](/cli/#data).

## Next steps: Train and deploy machine learning

You can use data synced to the cloud to [train machine learning models and deploy them to your machines](/how-tos/deploy-ml/) from the Viam app.

For comprehensive guides on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< card link="/how-tos/collect-data/">}}
{{< /cards >}}
