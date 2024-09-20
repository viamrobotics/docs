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

The data management service is a robust solution for handling machine data, allowing you to capture data, sync it to the cloud, and query it.
Using the data management service, you can collect data from different parts of a robot, IoT device, or any other machine.
Once collected, you can securely sync data to the cloud, and view, query, or manage it directly in the cloud without needing to manually gather data from each machine.

{{<imgproc src="/services/data/data_management.png" resize="x1100" declaredimensions=true alt="Data is captured on the machine, uploaded to the cloud, and then deleted off local storage." class="imgzoom" >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/J0NNiQD0ocQ">}}

Get started now with a quickstart guide:

{{< cards >}}
{{< card link="/get-started/collect-data/" class="green">}}
{{< /cards >}}

Or learn more about Viam's data management features, which can be broken down into on-device and cloud data capabilities:

## On-device data management

The data management service:

- Automatically captures data at the rate you specify.
   If your machine restarts, data capture resumes automatically.
- Securely transfers data to the cloud at the frequency you define.
- Automatically deletes local data after syncing for space management.

{{< cards >}}
{{% manualcard link="/services/data/capture-sync/" %}}

### Data capture and cloud sync

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
{{< relatedcard link="/servicses/vision/">}}
{{< /cards >}}

## Cloud data management

<br>
{{<imgproc src="/architecture/data-flow.svg" resize="x1100" declaredimensions=true alt="Data flowing from local disk to cloud to the Viam app, SDKs, and MQL and SQL queries." class="imgzoom">}}
<br><br>

Once your data is synced to the cloud, you can view, filter, label, and assign it to datasets from your [Viam app **DATA** page](https://app.viam.com/data/view).
You can also interact with your data using the [Viam CLI](/cli/#data), or using the [data client API](/appendix/apis/data-client/).

<!-- markdownlint-disable-file MD034 -->

{{< cards >}}
{{% manualcard link="/services/data/dataset/" %}}

### Create datasets

Label data for management and machine learning, with dynamic datasets that change with underlying data modifications.

{{% /manualcard %}}
{{% manualcard link="/how-tos/export-data/" %}}

### Export data

Export data with the Viam CLI and download your data for offline access.

{{% /manualcard %}}
{{% manualcard link="/how-tos/upload-data/" %}}

### Upload a batch of data

Upload data to the Viam app from your local computer or mobile device using the data client API, Viam CLI, or Viam mobile app.

{{% /manualcard %}}
{{< /cards >}}

### Query your data

Once your data has [synced](/services/data/capture-sync/), you can query it in multiple ways, including through the [data client API](/appendix/apis/data-client/) or [inside the Viam app](/how-tos/sensor-data-query-with-third-party-tools/).
For _tabular_ sensor data, you can also [run {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} queries](/how-tos/sensor-data-query-sdk/) against your synced data from the [Query subtab](https://app.viam.com/data/query) of the **Data** tab in the Viam app.

{{< cards >}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{% card link="/how-tos/sensor-data-query-sdk/" %}}
{{% card link="/appendix/apis/data-client/" %}}
{{< /cards >}}

### Permissions

Data management permissions vary between owners and operators.
For more information about who can do what with data, see [Data Permissions](/cloud/rbac/#data-and-machine-learning).

## API

The [data client API](/appendix/apis/data-client/) supports the following methods:

{{< expand "Methods to upload data like images or sensor readings directly to the Viam app" >}}

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

{{< /expand >}}

{{< expand "Methods to download, filter, tag, or perform other tasks on data like images or sensor readings" >}}

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

{{< /expand >}}

{{< expand "Methods to work with datasets" >}}

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

{{< /expand >}}

The data management API supports a separate set of methods that allow you to sync data to the Viam app.
For information about that API, see [Data Management API](/appendix/apis/#data-management).

For the command line interface `data` command, see [CLI](/cli/#data).

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a data management service called `"my_data_service"`, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for sample code to connect to your machine.

{{% /alert %}}

## Next steps: Train and deploy machine learning

You can use data synced to the cloud to [train machine learning models and deploy them to your machines](/how-tos/deploy-ml/) from the Viam app.

For comprehensive guides on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}
