---
title: "Gantry Component"
linkTitle: "Gantry"
draft: false
weight: 50
type: "docs"
description: "Explanation of gantry configuration and usage in Viam."
# SME: Rand
---

## Overview

A gantry is a specific type of robot component that uses only linear links to move an end effector in 3D space. 
A gantry can only control the position of the end effector, and is a commonly used machine design for simple positioning and placement. 
A linear axis has the advantage of being a stiffer machine layout than an open chain of links, and holding or repetitively positioning the end effector is more attainable in this configuration.

### Requirements

A gantry in Viam requires the following:

* A board or controller that can detect changes in voltage on gpio pins.
* A motor:
    * An encoded motor 
    * A stepper motor
        * Requires limit switches to be set in the gantry config or offsets to be set in stepper motor.
* Limit switches to attach to the brackets 

A customized encoded motor controller can be used in the configuration of a gantry to move the linear rail. 
This component abstracts this type of hardware to give the user an easy interface for moving many linear rails.

Since gantries are linearly moving components, each gantry can only move in one axis within the limits of its length. 

Each gantry can be given a reference [frame](/services/frame-system.md/) in the configuration that describes its translation and orientation to the world.

A multi-axis gantry is composed of many single-axis gantries. 
The multiple axis system is composed of the supplied gantry names. 
The system will then use any reference frames in the single-axis configs to place the gantries in the correct position and orientation.
The “world” frame of each gantry becomes the moveable frame of the gantry before it in order. 

## Attribute Configuration

### Single-Axis Gantry Attributes

The attributes are configured as such for a single-axis gantry:


<table>
  <tr>
   <td><strong>Attribute</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>board
   </td>
   <td>The name of the board that is connected to the and limit pin switches.
   </td>
  </tr>
  <tr>
   <td>motor
   </td>
   <td>The name of the motor that moves the gantry.
   </td>
  </tr>
  <tr>
   <td>limit_pins
   </td>
   <td>The pins attached to the limit switches on either end. Optional for encoded motor gantry types.
   </td>
  </tr>
  <tr>
   <td>limit_pin_enabled
   </td>
   <td>Is the Limit Pin enabled? I.e., true (pin HIGH)?
   </td>
  </tr>
  <tr>
   <td>mm_per_revolution
   </td>
   <td>How far the gantry moves linearly per one revolution of the motor’s output shaft. 
<p>
This typically corresponds to 
<p>
Distance = PulleyDiameter * 2 * pi
<p>
or the pitch of a linear screw.
   </td>
  </tr>
  <tr>
   <td>gantry_rpm
   </td>
   <td>The gantry’s motor’s default rpm.
   </td>
  </tr>
  <tr>
   <td>axis
   </td>
   <td>The axis in which the gantry is allowed to move relative to the reference frame (x, y, z). 
<p>
You can add a frame to a single-axis gantry attribute to describe its position in the local “world” frame.
<p>
See <a href="/services/frame-system">Frame System</a> for further information.
   </td>
  </tr>
  </table>

A frame can also be added to a one axis gantry attribute to describe its position in the local “world” [frame](/services/frame-system.md/).

### Multi-Axis Gantry Attributes

In addition to the attributes for single-axis gantries, multi-axis gantries also use these attributes:

<table>
  <tr>
   <td><strong>Attribute</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><strong>subaxes_list</strong>
   </td>
   <td>A complete list of the sub-axes that compose the multi-axis gantry.
   </td>
  </tr>
 
</table>

## Gantry Methods 

All gantries implement the following methods:

<table>
  <tr>
   <td><strong>Method Name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><file>GetPosition </file>
   </td>
   <td>Returns an array of floats that describe the current position to the gantry in each axis on which it moves.
<p>
The units are millimeters. A single-axis gantry returns a list with one element. A three-axis gantry returns a list containing three elements.
   </td>
  </tr>
  <tr>
   <td><file>MoveToPosition </file>
   </td>
   <td>Takes in a list of positions (units millimeters) and moves each axis of the gantry to the corresponding position. 
<p>
The number of elements in the list must equal the number of moveable axes on the gantry, and the order of the elements in the list correspond to the order of the axes present in the gantry.
   </td>
  </tr>
  <tr>
   <td><file>GetLengths </file>
   </td>
   <td>Returns a list of lengths of each axis of the gantry in millimeters.
   </td>
  </tr>
  <tr>
   <td><file>Stop </file>
   </td>
   <td>Stops the actuating components of the Gantry.
   </td>
  </tr>
  <tr>
   <td><file>Do </file>
   </td>
   <td>Viam supplies this interface on each component to allow for additional, non-standard functionality that users may wish to include that is <em>not</em> available from  Viam’s interfaces.
   </td>
  </tr>
  <tr>
   <td><file>ModelFrame </file>
   </td>
   <td>Returns the Gantry model. This interface is used in Motion Planning. It is an interface that is used in <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  <tr>
   <td><file>CurrentInputs </file>
   </td>
   <td>gets the positions of each axis of the gantry and transforms them into an Input type. It is used by the <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  <tr>
   <td><file>GoToInputs </file>
   </td>
   <td>returns results from motion planning and Inputs to the gantry, and sends them to MoveToPosition as positions. It is used by the <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  </table>


## Code Examples

### Example Multi-Axis Gantry Configuration

``` json
{
    "components": [
        {
            "name": "local",
            "type": "board",
            "model": "pi"
        },
        {
            "name": "xmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirx",
                    "pwm": "pwmx",
                    "step": "stepx"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "ymotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "diry",
                    "pwm": "pwmy",
                    "step": "stepy"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "zmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirz",
                    "pwm": "pwmz",
                    "step": "stepz"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "xaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "xlim1",
                    "xlim2"
                ],
                "motor": "xmotor",
                "rpm": 500,
                "axis": {
                    "x": 1,
                    "y": 0,
                    "z": 0
                }
            }
        },
        {
            "name": "yaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "ylim1",
                    "ylim2"
                ],
                "motor": "ymotor",
                "rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 1,
                    "z": 0
                }
            }
        },
        {
            "name": "zaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "zlim1",
                    "zlim2"
                ],
                "motor": "zmotor",
                "rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 0,
                    "z": 1
                }
            },
            "frame": {
                "parent": "world",
                "orientation": {
                    "type": "euler_angles",
                    "value": {
                        "roll": 0,
                        "pitch": 40,
                        "yaw": 0
                    }
                },
                "translation": {
                    "x": 0,
                    "y": 3,
                    "z": 0
                }
            }
        },
        {
            "name": "test",
            "type": "gantry",
            "model": "multiaxis",
            "attributes": {
                "subaxes_list": [
                    "xaxis",
                    "yaxis",
                    "zaxis"
                ]
            }
        }
    ]
}
```

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/gantry/index.html)
