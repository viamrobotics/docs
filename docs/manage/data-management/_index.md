---
title: "Data Management"
linkTitle: "Data Management"
weight: 30
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Sync data captured by the robot's components to the cloud."
# SME: Aaron Casas
---

The Data Management Service captures data from Viam components and securely syncs data to Viam's cloud.
You can configure capture frequency individually for each component.
The service is designed for flexibility and efficiency while preventing data loss, data duplication, and other data management issues.

The service has two parts: [Data Capture](#data-capture) and [Cloud Sync](#cloud-sync).

## Data Capture

The Data Management Service captures data from one or more components locally on the robot's storage.
The process runs in the background and, by default, stores data in the `/.viam/capture` directory.

If a robot restarts for any reason, capture automatically resumes.

The service can capture data from multiple components at the same or different frequencies.
Viam does not impose a lower or upper limit on the frequency of data collection.
However, in practice, your hardware may impose limits on the frequency of data collection.

You can change the frequency of data capture at any time for individual components.
If you use [fragments](../../appendix/glossary/), you can change the frequency of data capture in real time for some or all robots in a fleet at the component or robot level.

For example, consider a tomato picking robot with a 3D camera and an arm.
When you configure the robot, you may set the camera to capture point cloud data at a frequency of 30Hz.
For the arm, you may want to capture joint positions at 1Hz.
If your requirements change and you want to capture data from both components at 10Hz, you can change the configurations at any time by changing the number.

Data capture is frequently used with [Cloud Sync](#cloud-sync).
However, if you want to manage your robot's captured data yourself, you can enable only data capture without cloud sync.

To configure data capture, see [data capture](../data-management/configure-data-capture).

## Cloud Sync

The Data Management Service securely syncs the specified data to the cloud at the user-defined frequency.
Viam does not impose a minimum or maximum on the frequency of data syncing.
However, in practice, your hardware or network speed may impose limits on the frequency of data syncing.

If the internet becomes unavailable or the robot needs to restart during the sync process, the service will try to resume sync indefinitely.
When the connection is restored, the service resumes the syncing process where it left off without duplicating data.
For more detailed information, see [Considerations](#considerations).

Once the service syncs a file to Viam's cloud, the service deletes the file locally from the robot's configured capture location.

As before, consider the example of a tomato picking robot.
When you initially set the robot up you may want to sync captured data to the cloud every five minutes.
If you change your mind and want your robot to sync less frequently, you can change the sync frequency, for example, to once a day.

To configure cloud sync, see [configure cloud sync](../data-management/configure-cloud-sync)

### Considerations

- **Security**: The Data Management Service uses gRPC calls to send and receive data, so your data is encrypted while in flight.
  When data is stored in the cloud, it is encrypted at rest by the cloud storage provider.

- **Data Integrity**: Viam's Data Management Service is designed to safeguard against data loss, data duplication and otherwise compromised data.

    If the internet becomes unavailable or the robot needs to restart during the sync process, the sync is interrupted.
    If the sync process is interrupted, the service will retry uploading the data at exponentially increasing intervals until the interval in between tries is at one hour at which point the service retries the sync every hour.
    When the connection is restored and sync resumes, the service continues sync where it left off without duplicating data.

    For example, if the service has uploaded 33% of the data and then the internet connection is severed, sync is interrupted.
    Once the service retries and successfully connects, data synchronization resumes at 33%.

    {{< alert title="Caution" color="caution" >}}
    If you disable cloud sync for a component that was interrupted mid-sync, data capture will not resume.
    {{< /alert >}}

<!-- TODO(npentrel): uncomment once implemented
- **Bandwidth**: Viam’s data synchronization is designed with bandwidth limitations in mind.
    The Data Management Service compresses data before sending it over the network.
    Currently, you cannot control the amount of bandwidth Viam's data synchronization processes uses. -->

- **Storage** When a robot loses its internet connection, it cannot resume cloud sync until it can reach the Viam cloud again.

    To ensure that the robot can store all data captured while it has no connection, you need to provide enough local data storage.

    {{< alert title="Warning" color="warning" >}}
    Currently, the Data Management Service can use the entire available disk space to store data.
    If the robot loses connectivity and remains disconnected, data capture can eventually use all disk space.
    Currently, Viam does not safeguard against this.
    {{< /alert >}}

## Coming Soon

- Data processing for ML model training
- ML model to robot deployment

## Next steps

To use the Data Management Service, [add the Data Management Service](configure-data-capture/#add-the-data-management-service) to your robot.
Then [configure data capture](configure-data-capture) as needed and [configure cloud sync](configure-cloud-sync).

Once you have configured data capture and cloud sync, you can [view](view) and [export](export) your data.

For a comprehensive tutorial on data management, see [Intro to Data Management](data-management-tutorial).
