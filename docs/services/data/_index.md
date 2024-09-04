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
icon: true
images: ["/services/icons/data-management.svg"]
no_service: true
# SME: Alexa Greenberg
---

The data management service is a robust solution for smart machine data handling, [data capture](/services/data/capture/), and [cloud synchronization](/services/data/cloud-sync/).
Using the data management service, you can collect data from different parts of a robot, IoT device, or any other machine.
Once collected, you can configure which data to securely sync to the cloud, and view, sort, or manage it directly in the cloud without needing to manually gather data from each machine.

![Data is captured on the machine, uploaded to the cloud, and then deleted off local storage.](/services/data/data_management.png)

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/J0NNiQD0ocQ">}}

Get started now with a quickstart guide:

{{< cards >}}
{{< card link="/get-started/collect-data/" class="green">}}
{{< /cards >}}

Or learn more about Viam's data management features, which can be broken down into on-device and cloud data capabilities:

## On-device data management

Manage data directly on your robot, with configurable data capture from various components, automated recovery after interruptions, and secure cloud synchronization for efficient data storage and management.

{{< cards >}}
{{% manualcard link="/services/data/capture/" %}}

### Data capture

Configurable for various robot components like cameras, sensors, and motors, with configurable capture frequency.
Automatically resumes after robot restarts.

{{% /manualcard %}}
{{% manualcard link="/services/data/cloud-sync/" %}}

### Cloud sync

Securely transfer data to the cloud at the frequency you define.
Resilient to interruptions, and deletes local data post-sync for space management.

{{% /manualcard %}}
{{< /cards >}}

## Cloud data management

Experience streamlined data handling with advanced querying, viewing, and filtering capabilities, along with efficient data labeling and exporting tools.

{{< cards >}}
{{% manualcard link="/how-tos/sensor-data-query-with-third-party-tools/" %}}

### Query data

Make SQL or MQL queries on synced sensor data, accessible through the Viam app and MQL-compatible clients.

{{% /manualcard %}}
{{% manualcard link="/services/data/view/" %}}

### View and filter data

View and filter different data types in the cloud, with the option to delete data on the Viam app.

{{% /manualcard %}}
{{% manualcard link="/services/data/dataset/" %}}

### Create datasets

Label data for management and machine learning, with dynamic datasets that change with underlying data modifications.

{{% /manualcard %}}
{{% manualcard link="/services/data/export/" %}}

### Export data

Export data with the Viam CLI and download your data for offline access.

{{% /manualcard %}}
{{% manualcard link="/how-tos/upload-data/" %}}

### Upload a batch of data

Upload data to the Viam app from your local computer or mobile device using the data client API, Viam CLI, or Viam mobile app.

{{% /manualcard %}}
{{< /cards >}}

#### Used with

You can configure the frequency of data capture individually for each supported component:

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
{{< /cards >}}

## Query your data

Once you have [synced](/services/data/cloud-sync/), you can query the data you've collected in multiple ways, including through the [data client API](/appendix/apis/data-client/) or [inside the Viam app](/how-tos/sensor-data-query-with-third-party-tools/).
For _tabular_ sensor data, you can [run {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} queries](/how-tos/sensor-data-query-sdk/) against your synced data from the [Query subtab](https://app.viam.com/data/query) of the **Data** tab in the Viam app.

## Permissions

Data management permissions vary between owners and operators.
For more information about who can do what with data, see [Data Permissions](/cloud/rbac/#data-and-machine-learning).

## API

The data management service supports the following methods:

{{< readfile "/static/include/services/apis/generated/data_manager-table.md" >}}

The data client API supports a separate set of methods that allow you to upload and export data to and from the Viam app.
For information about that API, see [Data Client API](/appendix/apis/data-client/).

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a data management service called `"my_data_service"`, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for sample code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/data_manager.md" >}}

## Next steps: train and deploy machine learning

You can use data synced to the cloud to [train machine learning models and deploy them to your machines](/how-tos/deploy-ml/) from the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
