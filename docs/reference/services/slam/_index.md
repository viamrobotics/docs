---
title: "SLAM service reference"
linkTitle: "SLAM"
weight: 60
layout: "docs"
type: "docs"
description: "Simultaneous localization and mapping (SLAM) allows your machine to create a map of its surroundings and find its location within that map."
date: "2026-04-18"
aliases:
  - /operate/reference/services/slam/
  - /services/slam/
  - /mobility/slam/
---

{{% alert title="Stability Notice" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your machine to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM service supports the integration of SLAM as a service on your machine.
You can conduct SLAM with data collected live by a [RPlidar](https://github.com/viamrobotics/rplidar) or with LIDAR data you provide in configuration, and easily view the map you build by clicking on **View SLAM library** on your location's page:

![Completed SLAM maps in the SLAM library tab](/services/slam/view-map-page.png)

## Used with

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{< relatedcard link="/reference/components/camera/" alt_title="RPlidar" alt_link="https://github.com/viamrobotics/rplidar" required="yes">}}
{{< relatedcard link="/reference/components/movement-sensor/" required="no" >}}
{{< relatedcard link="/reference/components/base/" required="no" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

Integrated SLAM libraries include the following.
Click the model name for configuration instructions.

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`viam:slam:cartographer`](cartographer/) | [The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data. |
| [`viam:cloudslam-wrapper:cloudslam`](cloudslam/) | [cloudslam-wrapper](https://github.com/viam-modules/cloudslam-wrapper) Allows you to run supported SLAM algorithms in the cloud. |

## API

The SLAM service API supports the following methods:

<!-- Method links point to /reference/apis/services/slam/ which does not exist yet.
     Using inline table until the API page is created. -->

<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| `GetPosition` | Get the current position of the component the SLAM service is configured to source point cloud data from in the SLAM map as a `Pose`. |
| `GetPointCloudMap` | Get the point cloud map. |
| `GetInternalState` | Get the internal state of the SLAM algorithm required to continue mapping/localization. |
| `GetProperties` | Get information about the current SLAM session. |
| `Reconfigure` | Reconfigure this resource. |
| `DoCommand` | Execute model-specific commands that are not otherwise defined by the service API. |
| `Close` | Safely shut down the resource and prevent further use. |

## SLAM mapping best practices

The best way to improve map quality is by taking extra care when creating the initial map.
While in a slam session, you should:

- turn gently and gradually, completely avoiding sudden quick turns
- make frequent loop closures, arriving back at a previously mapped area so the machine can correct for errors in the map layout
- stay relatively (but not extremely) close to walls
- use a machine that can go smoothly over bumps and transitions between flooring areas
- drive at a moderate speed
- when using a wheeled base, try to include an [odometry movement sensor](/reference/components/movement-sensor/wheeled-odometry/). This helps the SLAM algorithm keep track of where the machine is moving.
- it is important to note that the [adxl345 accelerometer](https://github.com/viam-modules/analog-devices/) on the [Viam Rover 1](/try/) **will not** satisfy the movement sensor requirement.

You can find additional assistance in the [Troubleshooting section](/monitor/troubleshoot/).
