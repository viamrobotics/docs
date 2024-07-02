---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 30
type: "docs"
description: "Simultaneous localization and mapping (SLAM) allows your machine to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: true
images: ["/services/icons/slam.svg"]
no_list: true
aliases:
  - "/services/slam/"
  - "/mobility/slam/"
# SMEs: John N.
---

{{% alert title="Stability Notice" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

{{% alert title="Cloud SLAM temporarily not available in live mode" color="caution" %}}

Running models of the SLAM service in the cloud with live mode is temporarily disabled.
[Collect a dataset and use offline mode](/services/slam/cartographer/#use-previously-captured-data) instead.

{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your machine to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM service supports the integration of SLAM as a service on your machine.
You can conduct SLAM with data collected live by a [RPlidar](https://github.com/viamrobotics/rplidar) or with LIDAR data you provide in configuration, and easily view the map you build on the **SLAM library** tab of your location's page in the [Viam app](https://app.viam.com):

![Completed SLAM maps in the SLAM library tab](/services/slam/view-map-page.png)

## Used with

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{< relatedcard link="/components/camera/" alt_title="RPlidar" alt_link="https://github.com/viamrobotics/rplidar" required="yes">}}
{{< relatedcard link="/components/movement-sensor/" required="no" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

Integrated SLAM libraries include the following.
Click the model name for configuration instructions.

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`viam:slam:cartographer`](cartographer/) | [The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data. |

## API

The SLAM service supports the following methods:

{{< readfile "/static/include/services/apis/generated/slam-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a SLAM service called `"my_slam_service"`, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for boilerplate code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/slam.md" >}}
