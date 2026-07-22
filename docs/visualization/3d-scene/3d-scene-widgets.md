---
linkTitle: "3D scene widgets"
title: "3D scene widgets"
weight: 40
layout: "docs"
type: "docs"
description: "Overlay live data on the 3D scene with widgets: an arm's joint positions and a camera's live feed."
aliases:
  - /visualization/3d-scene-tools/3d-scene-widgets/
---

Widgets are floating panels you overlay on the 3D scene to read live data next to the 3D
view. Each widget is draggable and resizable.

## Enable a widget

Open the **Settings** panel (the gear icon in the scene toolbar) and select **Widgets**.
Toggle a widget on and it appears floating over the viewport; toggle it off to remove it. The
panel lists two kinds of widget: **Arm positions**, and a **Camera widgets** section with one
toggle per configured camera. A third widget, the [frame POV](#frame-pov), opens from the
Details panel instead.

## Arm positions

The **Arm positions** widget shows the live joint angles of an arm. It lists each joint by
index with its current position in degrees, and updates as the arm moves:

| Joint | Position (degrees) |
| ----- | ------------------ |
| 0     | -0.00              |
| 1     | -11.29             |
| 2     | -20.05             |
| ...   | ...                |

If your machine has more than one arm, a **Select arm** dropdown at the top of the widget
chooses which arm's joints to show. Use this widget to read an arm's current configuration
while you inspect its pose in the 3D view.

## Camera widgets

A camera widget shows a camera's live feed as a panel over the 3D scene, with its current
frame rate, for example `20.0fps`. Each configured camera has its own toggle under
**Camera widgets**.

A resolution dropdown on the widget sets the feed size: **Default**, `1280x720`, `640x360`,
`320x180`, `160x90`, or `80x44`. A lower resolution costs less bandwidth, which helps when
you watch several cameras at once or work over a slow connection. For how a camera's data
appears in the scene itself, see [Cameras](/visualization/perception/cameras/).

## Frame POV

The frame POV widget renders the scene from a selected frame's perspective, so you can
check what a camera's view covers, or what an end effector approaches, from its configured
pose. Select an entity in the **World** panel, then click the camera icon (**View from this
frame**) in the Details panel. A panel titled **POV** opens for that frame; open one per
frame you want to watch.
