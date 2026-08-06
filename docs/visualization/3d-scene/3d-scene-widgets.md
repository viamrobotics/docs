---
linkTitle: "3D scene widgets"
title: "3D scene widgets"
weight: 40
layout: "docs"
type: "docs"
description: "Overlay live controls on the 3D scene: interactive controls for any resource on the machine, and a frame's point of view."
aliases:
  - /visualization/3d-scene-tools/3d-scene-widgets/
---

Widgets are floating panels you overlay on the 3D scene so you can drive and read a machine
without leaving the 3D view. Each widget is draggable and resizable. Two kinds exist: control
widgets, which you open from the toolbar for any resource on the machine, and the
[frame POV](#frame-pov) widget, which you open from the Details panel.

## Open a control widget

Click **Control widgets** (joystick icon) in the top-right strip of the scene toolbar. A panel titled **Control
widgets** opens, listing the machine's resources grouped by type: a heading per resource type
(**Arm**, **Camera**, **Motor**, and so on), and under it one row per resource of that type,
each showing the resource's name and how many of its controls are currently open, for example
`1/2`.

Click a resource row to expand it, then toggle on a control. Each control you turn on opens
as its own panel over the viewport, titled `<resource-name> · <control>`. Toggle it off to
close the panel. If the machine has no resources with controls, the panel reads "No widgets
available for this machine."

Which widgets you have open, and where you dragged and sized their panels, are remembered per
machine part, so the layout you build survives a reload.

## What each resource offers

Control widgets come from the same library of resource controls as the machine's **CONTROL**
tab, so what a resource offers depends on its API:

- Resources whose API is broken into individual controls list one toggle per control.
- Resources without individual controls list a single **Overview** toggle that opens the
  resource's full control card.
- The motion service lists a **Move** control: the frame-aware move panel that commands the
  machine to move a selected frame, the same one the scene's move mode uses. The **CONTROL**
  tab omits the motion service, so this control is specific to the scene.
- Every resource that supports `DoCommand` also lists a **DoCommand** control: a JSON editor
  for sending a raw command and reading the response. Generic components and services, whose
  only API is `DoCommand`, list that one control.

Resources with nothing to drive do not appear at all: the data manager, the sensors service,
the shell service, and internal resources are left out of the list.

## Frame POV

The frame POV widget renders the scene from a selected frame's perspective, so you can
check what a camera's view covers, or what an end effector approaches, from its configured
pose. Select an entity in the **World** panel, then click the camera icon (**View from this
frame**) in the Details panel. A panel titled **POV: `<frame-name>`** opens for that frame;
open one per frame you want to watch.

Each POV panel has its own camera controls: a button in the top-right corner switches the
view between perspective and orthographic, and in orthographic mode a zoom slider along the
bottom sets the magnification.
