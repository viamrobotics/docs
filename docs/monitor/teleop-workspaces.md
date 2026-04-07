---
linkTitle: "Teleop workspaces"
title: "Teleop workspaces"
weight: 30
layout: "docs"
type: "docs"
description: "Build custom operator interfaces with camera feeds, sensor readouts, and component controls."
aliases:
  - /manage/troubleshoot/teleoperate/custom-interface/
---

Teleop workspaces let you build custom operator interfaces for specific tasks. Instead of seeing every resource on the CONTROL tab, you choose which widgets to display and arrange them into a focused view.

For an explanation of widget types and capabilities, see [Data dashboards overview](/monitor/dashboards/overview/). For the full CONTROL tab with all resources, see [Default control interface](/monitor/default-interface/).

## Prerequisites

{{% expand "A configured machine with teleoperable components" %}}

Your machine needs at least one camera, movement sensor, sensor, base, arm, board, gantry, gripper, motor, or servo.

See [configure a machine](/operate/modules/configure-modules/) for more information.

{{% /expand%}}

## Create a workspace

1. Navigate to the **FLEET** page and click the [**TELEOP** tab](https://app.viam.com/teleop).
1. Click **+ Create workspace**.
1. Enter a name for your workspace, replacing the placeholder text.
1. Select a **location** and **machine** from the dropdowns.

## Add widgets

1. Click **Add widget** and select a widget type.
1. Click the pencil icon in the top right of the widget to configure it.

To rearrange widgets, click and drag the grid icon in the top left of a widget.

### Available widget types

Teleop workspaces support all the widget types that dashboards support (GPS, stat, time series, table), plus two additional types for real-time interaction:

**Actuation**: control motors, servos, bases, arms, grippers, and other actuating components. Choose a component type, method, and component name.

**Camera stream**: display a live feed from a camera component. Choose a camera and set the refresh type.

For details on configuring GPS, stat, time series, and table widgets, see [Create dashboards](/monitor/dashboards/create-dashboards/). The configuration is the same, with these differences:

- Stat widgets show the most recent reading only (no windowing or aggregation).
- Table widgets support custom queries only (no column-based display).
- Time series widgets do not support the Sum window method.

For a full comparison, see the [dashboards and teleop workspaces table](/monitor/dashboards/overview/#dashboards-and-teleop-workspaces).

## Design effective operator views

A workspace is most useful when it shows only what the operator needs for their current task.

For example, a warehouse robot inspection workspace might include:

- A camera feed showing the robot's forward view
- A base actuation widget for driving
- A stat widget showing battery level
- A GPS widget showing the robot's location

An environmental monitoring workspace might include:

- Time series graphs of temperature and humidity over the last 24 hours
- A table showing the most recent readings from all sensors
- A stat widget showing the current air quality index

Start with fewer widgets and add more as you discover what the operator actually uses.
