---
linkTitle: "Default control interface"
title: "Default control interface"
weight: 25
layout: "docs"
type: "docs"
description: "Use the CONTROL tab or the Viam mobile app to remotely test and operate your machines."
aliases:
  - /manage/troubleshoot/teleoperate/default-interface/
  - /fleet/control/
  - /manage/app-usage/
  - /monitor/teleoperate/
---

The CONTROL tab provides a ready-made interface for testing and operating any configured machine. Every component and service on the machine gets a control card with relevant controls and readouts. No code required.

For a purpose-built operator interface with only the widgets you need, see [Teleop workspaces](/monitor/teleop-workspaces/). For a fully custom app with SDK access, see [Build apps](/build-apps/).

## Web UI

Navigate to your machine's page in the Viam app and click the **CONTROL** tab.

Each configured component and service appears as a card. What you can do depends on the resource type:

| Resource type      | What you can do                                          |
| ------------------ | -------------------------------------------------------- |
| Arm                | Move joints, set joint positions, read current positions |
| Base               | Drive with an arrow pad, set speed with a power slider   |
| Board              | Read and write GPIO pins, ADC/DAC values                 |
| Button             | View button state, simulate press                        |
| Camera             | View live feed, capture frames                           |
| Encoder            | Read position and ticks                                  |
| Gantry             | Move axes, read positions                                |
| Gripper            | Open, close, stop                                        |
| Input controller   | View button and axis states                              |
| Motor              | Set power, set RPM, go to position, read position        |
| Movement sensor    | Read position, orientation, velocity                     |
| Power sensor       | Read voltage, current, power                             |
| Sensor             | Read current values                                      |
| Servo              | Set angle, read current angle                            |
| Switch             | Toggle position                                          |
| Generic component  | Send custom commands (DoCommand)                         |
| Discovery service  | View discovery results                                   |
| ML model service   | Run inference                                            |
| Navigation service | View and set navigation goals                            |
| SLAM service       | View map and pose                                        |
| Vision service     | Run detections and classifications on camera feeds       |
| Generic service    | Send custom commands (DoCommand)                         |

You can switch between machine parts directly from the CONTROL tab using the part selector at the top.

## Viam mobile app

The Viam mobile app provides similar access from your phone:

- See which machines are online
- View live camera feeds
- Adjust component settings
- Switch between components
- [View machine logs](/monitor/troubleshoot/#check-logs)
- [Upload images from your phone to the cloud](/data/capture-sync/upload-other-data/)

The mobile app is available on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="/appstore.png" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="/googleplay.png" width="200px" alt="google play store icon" class="center-if-small" >
</a>
