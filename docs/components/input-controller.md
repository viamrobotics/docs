---
title: "Input Controller Component"
linkTitle: "Input Controller"
weight: 60
type: "docs"
description: "An input controller, like a gamepad or elevator button panel, is a device humans use to control a robot's actions."
tags: ["input controller", "components"]
icon: "img/components/controller.png"
# SME: James
---
## Input Interface

The Input interface is defined in [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) and you should view that file for details on specific methods and their uses.

### Overview/Concepts

#### Controller Interface

Input devices provide a Controller interface with three methods:

1. Controls() provides a list of input Controls that this Controller provides.
1. Events() returns a map of the most recent input event for each Control. This is the current state of the controller and can be polled for simple uses.
1. RegisterControlCallback() accepts a callback function that will be executed whenever one of the events selected occurs for the given control. This is the preferred method for real-time control. Note that you can only register one callback function per event for each control. A second call to register a callback function for a given event type on a given control replaces any previously registered function with the newly registered callback function for that event. You can also pass a "nil" function which will effectively "deregister" a callback as well.

#### Events

`Events` are passed to registered callback functions and are returned by Events(). They represent a singular event from the input device and have four fields:

1. Time
1. Event (This is an input.EventType, and represents a change in status of a control, i.e. a button press, a button release, or a change in position along a joystick axis.)
1. Control (This is an input.Control, and represents the axis/button/etc. involved.)
1. Value (this is a float64, used for the position of an axis, or state of a button.)

#### EventType

`EventType` is an enumerated list, with items like ButtonPress, ButtonRelease, PositionChangeAbs, Connect, Disconnect, etc. See [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the current list.
This type is returned as part of every event (per above) and also used to select events the callback is interested in when registering.
One note is that the special AllEvents value, if registered, will be called IN ADDITION TO any other callbacks registered. This is useful for debugging without interrupting normal controls, or for capturing extra/unknown events.

#### Control types

`input.Control` is another enumerated list that represents "well known" control types. For example, the X and Y axis of a primary joystick (a type of control which reports absolute position) should always be input.AbsoluteX and input.AbsoluteY. The secondary (right hand) joystick/thumbstick is input.AbsoluteRY and input.AbsoluteRY. Buttons are things line input.ButtonStart, or for trigger buttons, input.LT/RT. The typical 4-button configuration (under the right thumb) on most game pads uses generic compass directions instead of letter/shape labels, so that mappings aren't XBox/Nintendo/Playstation specific. Ex: "ButtonSouth" is the bottom-most button of the four, and corresponds to "B" on Nintendo, "A" on XBox, and "X" on Playstation. "ButtonNorth" is likewise X/Y/Triangle. See [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the full/current list. If new types need to be added, care should be taken to make them as generic and universal as possible. Look to the symbols in the Linux events subsystem for examples.

#### Axes

`Axes` can be either Absolute or Relative. Absolute axes report where they are each time and this is the method used by things like joysticks/thumbsticks, analog triggers, etc.--basically anything that "returns to center" on its own. Relative axes, on the other hand, are used by mice/trackpads/etc., and report a relative change in distance.
For now, only the gamepad implementation exists, so only Absolute axes are in use. Absolute axes report a "PostionChangeAbs" EventType and the Value is a float64 between -1.0 and +1.0, with center/neutral always being 0.0. The one special case is single-direction axes (like analog triggers, gas/brake pedals, etc.) On these, the "neutral" point is still 0.0, but they may only ever go into the positive direction. Lastly, note that for Y (vertical) axes, the positive direction is "nose up" which is pulling back on the stick.

#### Buttons

Buttons are a simpler case. They report either ButtonPress or ButtonRelease as their EventType, and the value is either 0 (for released) or 1 (for pressed.) Note that registering a callback for the ButtonChange event is merely a convenience for filtering, and will register the same callback to both ButtonPress and ButtonRelease, but ButtonChange will not be reported in an actual Event.

## Gamepad Driver

The Gamepad module provides an `input.Controller` interface that represents a standard gamepad, such as an xbox or playstation type game controller. It currently only supports Linux, and uses the input event subsystem.

### Configuration Example

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": "TestGamepad",
            "model": "gamepad",
            "type": "input_controller",
            "attributes": {
                "dev_file": "",
                "auto_reconnect": true
            }
        }
    ]
}
```

#### dev_file

If `dev_file` is left blank (as shown above) or not included, it will search and use the first gamepad it finds. If you want to specify a device, give the absolute path to the input device event file. Ex: <file>/dev/input/event42</file>

#### auto_reconnect

This determines if the device will automatically reconnect a device (or wait for one to be connected during startup), or if it should fail when a device is not connected. Note this applies to remote (gRPC) and local (bluetooth or direct USB connected) devices as well. Defaults to false if not included.

### Unknown/New Gamepad Types

There are currently mappings for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi.) The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo. Because of that, any unknown gamepad will be be mapped that way. If you have another controller though, feel free to submit a PR with new mappings.

### Sample (motor control)

The below example defines a single callback function (motorCtl) that handles input events, and turns them into motor.SetPower() commands. It's essentially all that's needed to drive a four wheel, skid steer platform, and uses the L/R analog triggers to control a "winder" motor, that raises/lowers a front end (like a bulldozer.) Lastly, it registers this callback for a selected set of axes.

```go {class="line-numbers linkable-line-numbers"}
motorCtl := func(ctx context.Context, event input.Event) {
    if event.Event != input.PositionChangeAbs {
        return
    }

    speed := float32(math.Abs(event.Value))

    switch event.Control {
        case input.AbsoluteY:
            motorFL.SetPower(ctx, speed)
            motorBL.SetPower(ctx, speed)
        case input.AbsoluteRY:
            motorFR.SetPower(ctx, speed * -1)
            motorBR.SetPower(ctx, speed * -1)
        case input.AbsoluteZ:
            motorWinder.SetPower(ctx, speed)
        case input.AbsoluteRZ:
            motorWinder.SetPower(ctx, speed * -1)
    }
}

for _, control := range []input.Control{input.AbsoluteY, input.AbsoluteRY, input.AbsoluteZ, input.AbsoluteRZ} {
    err = g.RegisterControlCallback(ctx, control, []input.EventType{input.PositionChangeAbs}, motorCtl)
}
```

## WebGamepad

This allows a gamepad to be connected remotely, via a browser and the html5 Gamepad API. To use it, add a component to the robot's config like below:

### Config

{{% alert="Note" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller. This restriction will be removed in the future.
{{% /alert %}}

``` json
{
    "components": [
        {
            "name": "WebGamepad",
            "model": "webgamepad",
            "type": "input_controller"
        }
    ]
}
```

### Use

When viewing a robot's UI (e.g. myrobot.local:8080) you'll see the WebGamepad component. Connect any compatible gamepad to your PC and press any button/stick (for privacy/security the browser won't report a gamepad until an input has been sent) and you should see the name of your controller appear, and the input displays respond to the controls. When ready, click "Enable" in the upper right to "connect" the controller to the robot, and let it begin receiving inputs.

## Mux

The Mux input controller simply combines one or more other controllers (sources) into a single virtual controller. This allows control from different locations (such as the web and a locally connected gamepad) or combining different controllers into one. (For example a joystick could be added to a numpad.)

### Config

``` json
{
    "components": [
        {
            "name": "Gamepad",
            "model": "gamepad",
            "type": "input_controller",
            "attributes": {
                "dev_file": "",
                "auto_reconnect": true
            }
        },
        {
            "name": "WebGamepad",
            "model": "webgamepad",
            "type": "input_controller"
        },
        {
            "name": "Mux",
            "model": "mux",
            "type": "input_controller",
            "depends_on": [
                "Gamepad",
                "WebGamepad"
            ],
            "attributes": {
                "sources": [
                    "Gamepad",
                    "WebGamepad"
                ]
            }
        }
    ]
}

```

Note the "depends_on" section. This tells the config loading code to fully load the source components first.

## SDK Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/input/index.html)
