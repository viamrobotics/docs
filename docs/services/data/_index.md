---
title: "Data Management Service"
linkTitle: "Data Management"
weight: 40
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Capture data from a robot's components and sync it to the cloud."
aliases:
  - "/data-management/"
  - "/services/data-management/"
icon: "/services/icons/data-capture.svg"
# SME: Aaron Casas
---

The data management service captures data from Viam components and securely syncs data to Viam's cloud.
You can configure capture frequency individually for each component.
The service is designed for flexibility and efficiency while preventing data loss, data duplication, and other data management issues.

The service has two parts: [Data Capture](#data-capture) and [Cloud Sync](#cloud-sync).

## Data Capture

The data management service captures data from one or more components locally on the robot's storage.
The process runs in the background and, by default, stores data in the `~/.viam/capture` directory.

If a robot restarts for any reason, capture automatically resumes.

The service can capture data from multiple components at the same or different frequencies.
Viam does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.

You can change the frequency of data capture at any time for individual components.
If you use {{< glossary_tooltip term_id="fragment" text="fragments" >}}, you can change the frequency of data capture in real time for some or all robots in a fleet at the component or robot level.

For example, consider a tomato picking robot with a 3D camera and an arm.
When you configure the robot, you may set the camera to capture point cloud data at a frequency of 30Hz.
For the arm, you may want to capture joint positions at 1Hz.
If your requirements change and you want to capture data from both components at 10Hz, you can change the configurations at any time by changing the number.

Data capture is frequently used with [Cloud Sync](#cloud-sync).
However, if you want to manage your robot's captured data yourself, you can enable only data capture without cloud sync.

To configure data capture, see [data capture](../data/configure-data-capture/).

## Used With

{{< cards >}}
{{< relatedcard link="/components/arm/">}}
{{< relatedcard link="/components/camera/">}}
{{< relatedcard link="/components/encoder/">}}
{{< relatedcard link="/components/gantry/">}}
{{< relatedcard link="/components/motor/">}}
{{< relatedcard link="/components/movement-sensor/">}}
{{< relatedcard link="/components/sensor/">}}
{{< relatedcard link="/components/servo/">}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Cloud Sync

The data management service securely syncs the specified data to the cloud at the user-defined frequency.
Viam does not impose a minimum or maximum on the frequency of data syncing.
However, in practice, your hardware or network speed may impose limits on the frequency of data syncing.

If the internet becomes unavailable or the robot needs to restart during the sync process, the service will try to resume sync indefinitely.
When the connection is restored, the service resumes the syncing process where it left off without duplicating data.
For more detailed information, see [Considerations](#considerations).

Once the service syncs a file to Viam's cloud, the service deletes the file locally from the robot's configured capture location.

As before, consider the example of a tomato picking robot.
When you initially set the robot up you may want to sync captured data to the cloud every five minutes.
If you change your mind and want your robot to sync less frequently, you can change the sync frequency, for example, to once a day.

To configure cloud sync, see [configure cloud sync](../data/configure-cloud-sync/).

### Considerations

- **Security**: The data management service uses {{< glossary_tooltip term_id="grpc" text="gRPC" >}} calls to send and receive data, so your data is encrypted while in flight.
  When data is stored in the cloud, it is encrypted at rest by the cloud storage provider.

- **Data Integrity**: Viam's data management service is designed to safeguard against data loss, data duplication and otherwise compromised data.

  If the internet becomes unavailable or the robot needs to restart during the sync process, the sync is interrupted.
  If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval in between tries is at one hour at which point the service retries the sync every hour.
  When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.

  For example, if the service has uploaded 33% of the data and then the internet connection is severed, sync is interrupted.
  Once the service retries and successfully connects, data synchronization resumes at 33%.

- **Storage** When a robot loses its internet connection, it cannot resume cloud sync until it can reach the Viam cloud again.

  To ensure that the robot can store all data captured while it has no connection, you need to provide enough local data storage.

  {{< alert title="Warning" color="warning" >}}

  Currently, the data management service can use the entire available disk space to store data.
  If the robot loses connectivity and remains disconnected, data capture can eventually use all disk space.
  Currently, Viam does not safeguard against this.

  {{< /alert >}}

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

## Next Steps

To use the data management service, [add the data management service](configure-data-capture/#add-the-data-management-service) to your robot.
Then [configure data capture](configure-data-capture/) as needed and [configure cloud sync](configure-cloud-sync/).

For a comprehensive tutorial on data management, see [Intro to Data Management](../../tutorials/services/data-management-tutorial/).

### Access and Export Data

Once you have configured data capture and cloud sync, you can [view](../../manage/data/view/) and [export](../../manage/data/export/) your data.

### Train and Deploy Machine Learning

You can use data synced to the cloud to [train machine learning models](../../manage/ml/train-model/) and then [deploy these models to your robots](../../services/ml/) from the Viam app.
You can also [upload and use existing models](../../manage/ml/upload-model/).
