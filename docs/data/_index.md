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
icon: "/services/icons/data-capture.svg"
menuindent: true
# SME: Alexa Greenberg
---

The data management service captures data from Viam components and securely syncs data to Viam's cloud.
The service is designed for flexibility and efficiency while preventing data loss, data duplication, and other data management issues.

![Data is captured on the robot, uploaded to the cloud, and then deleted off local storage.](/data/data_management.png)

The service has two parts: [data capture](/data/capture/) and [cloud sync](/data/cloud-sync/).

Once you have captured and synced data, you can:

{{< cards >}}
{{% card link="/data/view/" %}}
{{% card link="/data/dataset/" %}}
{{% card link="/data/export/" %}}
{{% card link="/data/query/" %}}
{{< /cards >}}

## Used with

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

You can configure capture frequency individually for each component.

## Requirements

You must configure data capture and cloud synchronization with the [Data Management Service](/data/) to be able to view, label, and export data.

## API

The data management service supports the following methods:

{{< readfile "/static/include/services/apis/data.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a data management service called `"my_data_service"`, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Sync

{{% alert title="Important" color="tip" %}}

This method is not yet available in the Viam Python SDK.

{{% /alert %}}

Sync data stored on the robot to the cloud.

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

// Sync data stored on the robot to the cloud.
err := data.Sync(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Use the data management service

To use the data management service, [add the data management service](/data/capture/#add-the-data-management-service) to your machine.
Then, [configure data capture](/data/capture/) and [configure cloud sync](/data/cloud-sync/) as needed.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).

### View, filter, and export data

Once you have configured data capture and cloud sync, you can [view your data](/data/view/) in the Viam app from the **Data** tab.

You can [filter your data](/data/view/#filter-data) by several categories, including by machine name, location, or timestamp range.
You can filter your data from the **Data** tab in the Viam app or using the Viam Python SDK.

You can also [export](/data/export/) your data as needed.

### Query data

If you have synced tabular data to the Viam app, you can perform {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} queries against that data.
You can chose to:

- Run SQL or MQL queries from the **Query** subtab under the **Data** tab in the Viam app.
- Directly query tabular data from a MQL-compatible client, such as `mongosh`.

See [Query Data](/data/query/) for instructions on using each of these approaches.

Only tabular data, such as [sensor](/components/sensor/) readings, can be queried in this fashion.
To search other types of data, such as images, see [Filter Data](/data/view/#filter-data).

### Train and deploy machine learning

You can use data synced to the cloud to [train machine learning models](/ml/train-model/) and then [deploy these models to your robots](/ml/) from the Viam app.
You can also [upload and use existing models](/ml/upload-model/).

## Next steps

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
