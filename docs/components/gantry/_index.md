---
title: "Gantry Component"
linkTitle: "Gantry"
draft: true
weight: 50
type: "docs"
description: "Explanation of gantry configuration and usage in Viam."
tags: ["gantry", "components"]
icon: "img/components/gantry.png"
# SME: Rand
---

You can use a **gantry** on a robot to hold and position a variety of end-effectors: devices designed to attach to the robot and interact with the environment to perform tasks.

A gantry uses linear rails to move an end effector across space.

- This makes it a common machine design for simple positioning and placement, as a linear axis establishes a stiffer layout across the robot than an open chain of links, making holding or repetitively positioning the end effector more attainable.
- Configure a customized encoded motor controller with a gantry to move the linear rail.

This component abstracts the hardware of a gantry to give you an easy interface for moving linear rails, even many at once (multi-axis).

- A multi-axis gantry component is made up of many single-axis gantries, with each referenced in configuration in the multi-axis models' attribute `subaxes_list`.
- Each gantry can be given a reference [frame](/services/frame-system/) in configuration that describes its translation and orientation to the world.
- The system will then use any reference frames in the single-axis configs to place the gantries in the correct position and orientation. The “world” frame of each gantry becomes the moveable frame of the gantry.

Gantry components can only be controlled in terms of linear motion.
Each gantry can only move in one axis within the limits of its length.

**Requirements:**

- A [board](/components/board/) or [controller](/components/input-controller/) component that can detect changes in voltage on GPIO pins.
- A [motor](/components/motor/).
  - Encoded motor
  - Stepper motor: Requires setting limit switches in the config of the gantry or setting offsets in the config of the stepper motor.
- Limit switches to attach to the brackets

### Configuration

#### Single-Axis

For a single-axis gantry, the attributes for configuration are:

<table>
  <tr>
    <td>
      <strong>
        Attribute
      </strong>
    </td>
    <td>
      <strong>
        Description
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      board
    </td>
    <td>
      The name of the board that is connected to the and limit pin switches.
    </td>
  </tr>
  <tr>
    <td>
      motor
    </td>
    <td>
      The name of the motor that moves the gantry.
    </td>
  </tr>
  <tr>
    <td>
      limit_pins
    </td>
    <td>
      The pins attached to the limit switches on either end. Optional for encoded
      motor gantry types.
    </td>
  </tr>
  <tr>
    <td>
      limit_pin_enabled
    </td>
    <td>
      Is the Limit Pin enabled? I.e., true (pin HIGH)?
    </td>
  </tr>
  <tr>
    <td>
      mm_per_revolution
    </td>
    <td>
      How far the gantry moves linearly per one revolution of the motor’s output
      shaft.
      <p>
        This typically corresponds to
        <p>
          Distance = PulleyDiameter *2* pi
          <p>
            or the pitch of a linear screw.
    </td>
  </tr>
  <tr>
    <td>
      gantry_rpm
    </td>
    <td>
      The gantry’s motor’s default rpm.
    </td>
  </tr>
  <tr>
    <td>
      axis
    </td>
    <td>
      The axis in which the gantry is allowed to move relative to the reference
      frame (x, y, z).
      <p>
        You can add a frame to a single-axis gantry attribute to describe its
        position in the local “world” frame.
        <p>
          See
          <a href="/services/frame-system">
            Frame System
          </a>
          for further information.
    </td>
  </tr>
</table>

A frame can also be added to a one axis gantry attribute to describe its position in the local “world” [frame](/services/frame-system/).

#### Multi-Axis

In addition to the attributes for single-axis gantries, multi-axis gantries also use these attributes:

<table>
  <tr>
    <td>
      <strong>
        Attribute
      </strong>
    </td>
    <td>
      <strong>
        Description
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      <strong>
        subaxes_list
      </strong>
    </td>
    <td>
      A complete list of the sub-axes that compose the multi-axis gantry.
    </td>
  </tr>
</table>

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

### Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="install">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Relevant tutorial name</h4>
            <p style="text-align: left;">Description.</p>
        </a>
    </div>
  </div>
</div>
