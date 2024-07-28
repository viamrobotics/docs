---
title: "Input Controller Component"
linkTitle: "Input Controller"
weight: 60
type: "docs"
no_list: true
description: "An input controller, like a gamepad or joystick, is a device humans use to control a machine's actions."
tags: ["input controller", "components"]
icon: true
images: ["/icons/components/controller.svg"]
modulescript: true
aliases:
  - "/components/input-controller/"
hide_children: true
# SME: James
---

You are likely already familiar with human-interface devices, like keyboards and mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers, from your daily life.

Configuring an _input_ component allows you to use devices like these with your machine, enabling you to control your machine's actions by interacting with the device.

This component currently supports devices like gamepads and joysticks that contain one or more [Controls](#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](/components/input-controller/#registercontrolcallback) to the [Controls](#control-field) with the `input` API.

The callback functions can then handle the [Events](/components/input-controller/#getevents) that are sent when the Control is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

Most machines with an input controller need at least the following hardware:

- A computer capable of running `viam-server`.
- A power supply cable or batteries for the input device and the machine.
- A component that you can direct the input to control, like an [arm](/components/arm/) or [motor](/components/motor/).

## Related services

{{< cards >}}
{{< relatedcard link="/services/base-rc/" >}}
{{< /cards >}}

## Available models

To use your input controller component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="RDK" %}}

{{<resources api="rdk:component:input_controller" type="input_controller" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in the micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## Control your machine with an input controller with Viam's client SDK libraries

Once you've configured your input controller according to model type, you can write code to define how your machine processes the input from the controller.

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have an input controller called `"my_controller"` configured as a component of your machine.
If your input controller has a different name, change the `name` in the code.

Be sure to import the input controller package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.input import Control, Controller, EventType
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/input"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The input controller component supports the following methods:

{{< readfile "/static/include/components/apis/generated/input_controller-table.md" >}}

{{< readfile "/static/include/components/apis/generated/input_controller.md" >}}

## API types

The `input` API defines the following types:

### Event object

Each `Event` object represents a singular event from the input device, and has four fields:

1. `Time`: `time.Time` the event occurred.
2. `Event`: `EventType` indicating the type of event (for example, a specific button press or axis movement).
3. `Control`: `Control` indicating which [Axis](#axis-controls), [Button](#button-controls), or Pedal on the controller has been changed.
4. `Value`: `float64` indicating the position of an [Axis](#axis-controls) or the state of a [Button](#button-controls) on the specified control.

#### EventType field

A string-like type indicating the specific type of input event, such as a button press or axis movement.

- To select for events of all type when registering callback function with [RegisterControlCallback](/components/input-controller/#registercontrolcallback), you can use `AllEvents` as your `EventType`.
- The registered function is then called in addition to any other callback functions you've registered, every time an `Event` happens on your controller.
  This is useful for debugging without interrupting normal controls, or for capturing extra or unknown events.

Registered `EventTypes` definitions:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
ALL_EVENTS = "AllEvents"
"""
Callbacks registered for this event will be called in ADDITION to other
registered event callbacks.
"""

CONNECT = "Connect"
"""
Sent at controller initialization, and on reconnects.
"""

DISCONNECT = "Disconnect"
"""
If unplugged, or wireless/network times out.
"""

BUTTON_PRESS = "ButtonPress"
"""
Typical key press.
"""

BUTTON_RELEASE = "ButtonRelease"
"""
Key release.
"""

BUTTON_HOLD = "ButtonHold"
"""
Key is held down. This will likely be a repeated event.
"""

BUTTON_CHANGE = "ButtonChange"
"""
Both up and down for convenience during registration, not typically emitted.
"""

POSITION_CHANGE_ABSOLUTE = "PositionChangeAbs"
"""
Absolute position is reported via Value, a la joysticks.
"""

POSITION_CHANGE_RELATIVE = "PositionChangeRel"
"""
Relative position is reported via Value, a la mice, or simulating axes with
up/down buttons.
"""
```

See [the Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/input/index.html#viam.components.input.EventType) for the most current version of supported `EventTypes`.

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
 // Callbacks registered for this event will be called in ADDITION to other registered event callbacks.
AllEvents EventType = "AllEvents"

// Sent at controller initialization, and on reconnects.
Connect EventType = "Connect"

// If unplugged, or wireless/network times out.
Disconnect EventType = "Disconnect"

// Typical key press.
ButtonPress EventType = "ButtonPress"

// Key release.
ButtonRelease EventType = "ButtonRelease"

// Key is held down. This will likely be a repeated event.
ButtonHold EventType = "ButtonHold"

// Both up and down for convenience during registration, not typically emitted.
ButtonChange EventType = "ButtonChange"

// Absolute position is reported via Value, a la joysticks.
PositionChangeAbs EventType = "PositionChangeAbs"

// Relative position is reported via Value, a la mice, or simulating axes with up/down buttons.
PositionChangeRel EventType = "PositionChangeRel"
```

See [the Viam RDK](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of supported `EventTypes`.

{{% /tab %}}
{{< /tabs >}}

#### Control field

A string representing the physical input location, like a specific axis or button, of your `Controller` that the [Event Object](#event-object) is coming from.

Registered `Control` types are defined as follows:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Axes
ABSOLUTE_X = "AbsoluteX"
ABSOLUTE_Y = "AbsoluteY"
ABSOLUTE_Z = "AbsoluteZ"
ABSOLUTE_RX = "AbsoluteRX"
ABSOLUTE_RY = "AbsoluteRY"
ABSOLUTE_RZ = "AbsoluteRZ"
ABSOLUTE_HAT0_X = "AbsoluteHat0X"
ABSOLUTE_HAT0_Y = "AbsoluteHat0Y"

# Buttons
BUTTON_SOUTH = "ButtonSouth"
BUTTON_EAST = "ButtonEast"
BUTTON_WEST = "ButtonWest"
BUTTON_NORTH = "ButtonNorth"
BUTTON_LT = "ButtonLT"
BUTTON_RT = "ButtonRT"
BUTTON_LT2 = "ButtonLT2"
BUTTON_RT2 = "ButtonRT2"
BUTTON_L_THUMB = "ButtonLThumb"
BUTTON_R_THUMB = "ButtonRThumb"
BUTTON_SELECT = "ButtonSelect"
BUTTON_START = "ButtonStart"
BUTTON_MENU = "ButtonMenu"
BUTTON_RECORD = "ButtonRecord"
BUTTON_E_STOP = "ButtonEStop"

# Pedals
ABSOLUTE_PEDAL_ACCELERATOR = "AbsolutePedalAccelerator"
ABSOLUTE_PEDAL_BRAKE = "AbsolutePedalBrake"
ABSOLUTE_PEDAL_CLUTCH = "AbsolutePedalClutch"
```

See [the Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/input/index.html#viam.components.input.Control) for the most current version of supported `Control` types.

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Axes.
AbsoluteX     Control = "AbsoluteX"
AbsoluteY     Control = "AbsoluteY"
AbsoluteZ     Control = "AbsoluteZ"
AbsoluteRX    Control = "AbsoluteRX"
AbsoluteRY    Control = "AbsoluteRY"
AbsoluteRZ    Control = "AbsoluteRZ"
AbsoluteHat0X Control = "AbsoluteHat0X"
AbsoluteHat0Y Control = "AbsoluteHat0Y"

// Buttons.
ButtonSouth  Control = "ButtonSouth"
ButtonEast   Control = "ButtonEast"
ButtonWest   Control = "ButtonWest"
ButtonNorth  Control = "ButtonNorth"
ButtonLT     Control = "ButtonLT"
ButtonRT     Control = "ButtonRT"
ButtonLT2    Control = "ButtonLT2"
ButtonRT2    Control = "ButtonRT2"
ButtonLThumb Control = "ButtonLThumb"
ButtonRThumb Control = "ButtonRThumb"
ButtonSelect Control = "ButtonSelect"
ButtonStart  Control = "ButtonStart"
ButtonMenu   Control = "ButtonMenu"
ButtonRecord Control = "ButtonRecord"
ButtonEStop  Control = "ButtonEStop"

// Pedals.
AbsolutePedalAccelerator Control = "AbsolutePedalAccelerator"
AbsolutePedalBrake       Control = "AbsolutePedalBrake"
AbsolutePedalClutch      Control = "AbsolutePedalClutch"
```

See [Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of supported `Control` types.

{{% /tab %}}
{{< /tabs >}}

### Axis controls

{{% alert title="Support Notice" color="note" %}}
Currently, only `Absolute` axes are supported.

`Relative` axes, reporting a relative change in distance, used by devices like mice and trackpads, will be supported in the future.
{{% /alert %}}

Analog devices like joysticks and thumbsticks which return to center/neutral on their own use `Absolute` axis control types.

These controls report a `PositionChangeAbs` [EventType](#eventtype-field).

**Value:** A `float64` between `-1.0` and `+1.0`.

- `1.0`: Maximum position in the positive direction.
- `0.0`: Center, neutral position.
- `-1.0`: Maximum position in the negative direction.

#### AbsoluteXY axes

If your input controller has an analog stick, this is what the stick's controls report as.

Alternatively, if your input controller has _two_ analog sticks, this is what the left joystick's controls report as.

| Name        | `-1.0`        | `0.0`   | `1.0`           |
| ----------- | ------------- | ------- | --------------- |
| `AbsoluteX` | Stick Left    | Neutral | Stick Right     |
| `AbsoluteY` | Stick Forward | Neutral | Stick Backwards |

#### AbsoluteR-XY axes

If your input controller has _two_ analog sticks, this is what the right joystick's controls report as.

| Name         | `-1.0`        | `0.0`   | `1.0`           |
| ------------ | ------------- | ------- | --------------- |
| `AbsoluteRX` | Stick Left    | Neutral | Stick Right     |
| `AbsoluteRY` | Stick Forward | Neutral | Stick Backwards |

- For `Y` axes, the positive direction is "nose up," and indicates _pulling_ back on the joystick.

#### Hat/D-Pad axes

If your input controller has a directional pad with analog buttons on the pad, this is what those controls report as.

<!-- prettier-ignore -->
| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteHat0X` | Left DPAD Button Press | Neutral | Right DPAD Button Press |
| `AbsoluteHat0Y` | Up DPAD Button Press | Neutral | Down DPAD Button Press |

#### Z axes (analog trigger sticks)

{{% alert title="Info" color="info" %}}
Devices like analog triggers and gas or brake pedals use `Absolute` axes, but they only report position change in the positive direction.
The neutral point of the axes is still `0.0`.
{{% /alert %}}

| Name         | `-1.0` | `0.0`   | `1.0`        |
| ------------ | ------ | ------- | ------------ |
| `AbsoluteZ`  |        | Neutral | Stick Pulled |
| `AbsoluteRZ` |        | Neutral | Stick Pulled |

`Z` axes are usually not present on most controller joysticks.

If present, they are typically analog trigger sticks, and unidirectional, scaling only from `0` to `1.0` as they are pulled, as shown above.

`AbsoluteZ` is reported if there is one trigger stick, and `AbsoluteZ` (left) and `AbsoluteRZ` (right) is reported if there are two trigger sticks.

Z axes can be present on flight-style joysticks, reporting _yaw_, or left/right rotation, as shown below.
This is not common.

| Name         | `-1.0`         | `0.0`   | `1.0`           |
| ------------ | -------------- | ------- | --------------- |
| `AbsoluteZ`  | Stick Left Yaw | Neutral | Stick Right Yaw |
| `AbsoluteRZ` | Stick Left Yaw | Neutral | Stick Right Yaw |

### Button controls

Button Controls report either `ButtonPress` or `ButtonRelease` as their [EventType](#eventtype-field).

**Value:**

- `0`: released
- `1`: pressed

#### Action buttons (ABXY)

If your input controller is a gamepad with digital action buttons, this is what the controls for these buttons report as.

{{% alert title="Tip" color="tip" %}}
As different systems label the actual buttons differently, we use compass directions for consistency.

- `ButtonSouth` corresponds to "B" on Nintendo, "A" on XBox, and "X" on Playstation.
- `ButtonNorth` corresponds to "X" on Nintendo, "Y" on XBox, and "Triangle" on Playstation.
  {{% /alert %}}

<!-- prettier-ignore -->
| Diamond 4-Action Button Pad | Rectangle 4-Action Button Pad |
| - | - |
| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonNorth`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Bottom</td></tr><tr><td>`ButtonEast`</td><td>Right</td></tr><tr><td>`ButtonWest`</td><td>Left</td></tr> </table> | <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonNorth`</td><td>Top-left</td></tr><tr><td>`ButtonSouth`</td><td>Bottom-right</td></tr><tr><td>`ButtonEast`</td><td>Top-right</td></tr><tr><td>`ButtonWest`</td><td>Bottom-left</td></tr> </table> |

<!-- prettier-ignore -->
| Horizontal 3-Action Button Pad | Vertical 3-Action Button Pad |
| - | - |
| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonWest`</td><td>Left</td></tr><tr><td>`ButtonSouth`</td><td>Center</td></tr><tr><td>`ButtonEast`</td><td>Right</td></tr> </table> | <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonWest`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Center</td></tr><tr><td>`ButtonEast`</td><td>Bottom</td></tr> </table> |

<!-- prettier-ignore -->
| Horizontal 2-Action Button Pad | Vertical 2-Action Button Pad |
| - | - |
| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonEast`</td><td>Right</td></tr><tr><td>`ButtonSouth`</td><td>Left</td></tr><tr> </table> | <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonEast`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Bottom</td></tr> </table> |

#### Trigger buttons (bumpers)

If your input controller is a gamepad with digital trigger buttons, this is what the controls for those buttons report as.

<!-- prettier-ignore -->
| 2-Trigger Button Pad | 4-Trigger Button Pad |
| - | - |
| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonLT`</td><td>Left</td></tr><tr><td>`ButtonRT`</td><td>Right</td></tr> </table> | <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonLT`</td><td>Top-left</td></tr><tr><td>`ButtonRT`</td><td>Top-right</td></tr><tr><td>`ButtonLT2`</td><td>Bottom-left</td></tr><tr><td>`ButtonRT2`</td><td>Bottom-right</td></tr> </table> |

#### Digital buttons for sticks

If your input controller is a gamepad with "clickable" thumbsticks, this is what thumbstick presses report as.

| Name           | Description                     |
| -------------- | ------------------------------- |
| `ButtonLThumb` | Left or upper button for stick  |
| `ButtonRThumb` | Right or lower button for stick |

#### Miscellaneous buttons

Many devices have additional buttons.
If your input controller is a gamepad with these common buttons, this is what the controls for those buttons report as.

| Name           | Description                                         |
| -------------- | --------------------------------------------------- |
| `ButtonSelect` | Select or -                                         |
| `ButtonStart`  | Start or +                                          |
| `ButtonMenu`   | Usually the central "Home" or Xbox/PS "Logo" button |
| `ButtonRecord` | Recording                                           |
| `ButtonEStop`  | Emergency Stop (on some industrial controllers)     |

## Usage examples

### Control a wheeled base with a Logitech G920 steering wheel controller

The following Python code is an example of controlling a wheeled {{% glossary_tooltip term_id="base" text="base"%}} with a Logitech G920 steering wheel controller, configured as a `gamepad` input controller.

```python {id="python-example" class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.components.input import Control, Controller, EventType
from viam.proto.common import Vector3
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

turn_amt = 0
modal = 0
cmd = {}


async def connect_robot(host, api_key, api_key_id):
    opts = RobotClient.Options.with_api_key(
      api_key=api_key,
      api_key_id=api_key_id
    )
    return await RobotClient.at_address(host, opts)


def handle_turning(event):
    global turn_amt
    turn_amt = -event.value
    print("turning:", turn_amt)


def handle_brake(event):
    if event.value != 0:
        print("braking!:", event.value)
        global cmd
        cmd = {"y": 0}
        print("broke")


def handle_accelerator(event):
    print("moving!:", event.value)
    global cmd
    accel = (event.value - 0.1) / 0.9
    if event.value < 0.1:
        accel = 0

    cmd = {"y": accel}


def handle_clutch(event):
    print("moving!:", event.value)
    global cmd
    accel = (event.value - 0.1) / 0.9
    if event.value < 0.1:
        accel = 0

    cmd = {"y": -accel}


async def handleController(controller):
    resp = await controller.get_events()
    # Show the input controller's buttons/axes
    print(f'Controls:\n{resp}')

    if Control.ABSOLUTE_PEDAL_ACCELERATOR in resp:
        controller.register_control_callback(
            Control.ABSOLUTE_PEDAL_ACCELERATOR,
            [EventType.POSITION_CHANGE_ABSOLUTE],
            handle_accelerator)
    else:
        print("Accelerator Pedal not found! Exiting! Are your steering wheel" +
              " and pedals hooked up?")
        exit()

    if Control.ABSOLUTE_PEDAL_BRAKE in resp:
        controller.register_control_callback(
            Control.ABSOLUTE_PEDAL_BRAKE,
            [EventType.POSITION_CHANGE_ABSOLUTE],
            handle_brake)
    else:
        print("Brake Pedal not found! Exiting!")
        exit()

    if Control.ABSOLUTE_PEDAL_CLUTCH in resp:
        controller.register_control_callback(
            Control.ABSOLUTE_PEDAL_CLUTCH,
            [EventType.POSITION_CHANGE_ABSOLUTE],
            handle_clutch)
    else:
        print("Accelerator Pedal not found! Exiting! Are your steering wheel" +
              " and pedals hooked up?")
        exit()

    if Control.ABSOLUTE_X in resp:
        controller.register_control_callback(
            Control.ABSOLUTE_X,
            [EventType.POSITION_CHANGE_ABSOLUTE],
            handle_turning)
    else:
        print("Wheel not found! Exiting!")
        exit()

    while True:
        await asyncio.sleep(0.01)
        global cmd
        if "y" in cmd:
            res = await modal.set_power(
                linear=Vector3(x=0, y=cmd["y"], z=0),
                angular=Vector3(x=0, y=0, z=turn_amt))
            cmd = {}
            print(res)


async def main():
    # ADD YOUR MACHINE REMOTE ADDRESS and API KEY VALUES.
    # These can be found in app.viam.com's CONNECT tab's Code sample page.
    # Toggle 'Include secret' to show the API key values.
    g920_robot = await connect_robot(
        "robot123example.locationxyzexample.viam.com", "API_KEY", "API_KEY_ID")
    modal_robot = await connect_robot(
        "robot123example.locationxyzexample.viam.com", "API_KEY", "API_KEY_ID")

    g920 = Controller.from_robot(g920_robot, 'wheel')
    global modal
    modal = Base.from_robot(modal_robot, 'modal-base-server:base')

    await handleController(g920)

    await g920_robot.close()
    await modal_robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Drive a robot with four wheels and a skid steer platform

The following Go code is part of an example of using an input controller to drive a robot with four wheels & a skid steer platform.

The `motorCtl` callback function controls 5 motors: left front & back `FL` `BL`, right front & back `FL` `BL`, and a `winder` motor that raises and lowers a front-end like a bulldozer.

The `event.Control` logic is registered as a callback function to determine the case for setting the power of each motor from which button is pressed on the input controller.

```go {id="go-example" class="line-numbers linkable-line-numbers"}
// Define a single callback function
motorCtl := func(ctx context.Context, event input.Event) {
    if event.Event != input.PositionChangeAbs {
        return
    }

    speed := float32(math.Abs(event.Value))

    // Handle input events, commands to set the power of motor components (SetPower method)
    switch event.Control {
        case input.AbsoluteY:
            motorFL.SetPower(ctx, speed, nil)
            motorBL.SetPower(ctx, speed, nil)
        case input.AbsoluteRY:
            motorFR.SetPower(ctx, speed * -1, nil)
            motorBR.SetPower(ctx, speed * -1, nil)
        case input.AbsoluteZ:
            motorWinder.SetPower(ctx, speed, nil)
        case input.AbsoluteRZ:
            motorWinder.SetPower(ctx, speed * -1, nil)
    }
}

// Registers callback from motorCtl for a selected set of axes
for _, control := range []input.Control{input.AbsoluteY, input.AbsoluteRY, input.AbsoluteZ, input.AbsoluteRZ} {
    err = g.RegisterControlCallback(ctx, control, []input.EventType{input.PositionChangeAbs}, motorCtl)
}
```

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/configure/configure-rover" %}}
{{% card link="/tutorials/control/gamepad" %}}
{{< /cards >}}
