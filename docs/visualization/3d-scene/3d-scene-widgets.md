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
view. Each widget is draggable and resizable, and you turn them on and off in the scene's
settings.

## Enable a widget

Open the **Settings** panel (the gear icon in the scene toolbar) and select **Widgets**.
Toggle a widget on and it appears floating over the viewport; toggle it off to remove it. The
panel lists two kinds of widget: **Arm positions**, and a **Camera widgets** section with one
toggle per configured camera.

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

A camera widget shows a camera's live feed as a panel over the 3D scene. Each configured
camera has its own toggle under **Camera widgets**. For the feed's resolution and frame-rate
controls, see [Cameras](/visualization/perception/cameras/).
