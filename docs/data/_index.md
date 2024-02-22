---
title: "Data Management"
linkTitle: "Data Management"
weight: 440
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
icon: true
images: ["/services/icons/data-management.svg"]
menuindent: true
# SME: Alexa Greenberg
---

The data management service is a robust solution for smart machine data handling, [data capture](/data/capture/), and [cloud synchronization](/data/cloud-sync/).
Using the data management service, you can collect data from different parts of a robot, IoT device, or any other machine.
Once collected, you can configure which data to securely sync to the cloud, and view, sort, or manage it directly in the cloud without needing to manually gather data from each machine.

## Overview

![Data is captured on the machine, uploaded to the cloud, and then deleted off local storage.](/data/data_management.png)

Viam's data management features can be broken down into on-device and cloud data capabilities:

### On-device data management

Manage data directly on your robot, with configurable data capture from various components, automated recovery after interruptions, and secure cloud synchronization for efficient data storage and management.

{{< cards >}}
{{% manualcard link="/data/capture/" %}}

#### Data capture

Configurable for various robot components like cameras, sensors, and motors; set capture frequency, with automatic resumption after robot restarts.

{{% /manualcard %}}
{{% manualcard link="/data/cloud-sync/" %}}

#### Cloud sync

Securely transfer data to cloud at the frequency you define, resilient to interruptions, and delete local data post-sync for space management.

{{% /manualcard %}}
{{< /cards >}}

### Cloud data management

Experience streamlined data handling with advanced querying, viewing, and filtering capabilities, along with efficient data labeling and exporting tools.

{{< cards >}}
{{% manualcard link="/data/query/" %}}

#### Data querying

Make SQL or MQL queries on synced sensor data, accessible through the Viam app and MQL-compatible clients.

{{% /manualcard %}}
{{% manualcard link="/data/view/" %}}

#### Viewing and filtering data

View and filter different data types in the cloud, with the option to delete data on the Viam app.

{{% /manualcard %}}
{{% manualcard link="/data/dataset/" %}}

#### Creating datasets

Label data for management and machine learning, with dynamic datasets that change with underlying data modifications.

{{% /manualcard %}}
{{% manualcard link="/data/export/" %}}

#### Exporting data

Export data with the Viam CLI and download your data for offline access.

{{% /manualcard %}}
{{< /cards >}}

## Get started

### Collect your data and send to the Viam platform

You must [configure data capture](/data/capture/) and [cloud sync](/data/cloud-sync/) with the data management service to be able to view, label, and export data.

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

### Query your data

Once you have [synced](/data/cloud-sync/), you can query the data you've collected in multiple ways, including through the [data client API](/build/program/apis/data-client/) or [inside the Viam app](/data/query/).
For _tabular_ sensor data, you can run {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} queries against your synced data from the [Query subtab](https://app.viam.com/data/query) of the **Data** tab in the Viam app.

### Permissions

Data management permissions vary between owners and operators.
For more information about who can do what with data, see [Data Permissions](/fleet/rbac/#data-and-machine-learning).

## API

The data management service supports the following methods:

{{< readfile "/static/include/services/apis/data.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a data management service called `"my_data_service"`, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

{{% /alert %}}

### Sync

{{% alert title="Important" color="tip" %}}

This method is not yet available in the Viam Python SDK.

{{% /alert %}}

Sync data stored on the machine to the cloud.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager).

```go {class="line-numbers linkable-line-numbers"}
data, err := datamanager.FromRobot(robot, "my_data_service")

// Sync data stored on the machine to the cloud.
err := data.Sync(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Next steps: train and deploy machine learning

You can use data synced to the cloud to [train machine learning models](/ml/train-model/) and then [deploy these models to your machines](/ml/) from the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
