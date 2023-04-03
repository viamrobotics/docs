---
title: "Input Controller Component"
linkTitle: "Input Controller"
weight: 60
type: "docs"
no_list: true
description: "An input controller, like a gamepad or joystick, is a device humans use to control a robot's actions."
tags: ["input controller", "components"]
image: "/components/img/components/controller.png"
imageAlt: "input controller"
# SME: James
---

You are likely already familiar with human-interface devices, like keyboards and mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers, from your daily life.

Configuring an *input* component allows you to use devices like these with your robot, enabling you to control your robot's actions by interacting with the device.

This component currently supports devices like gamepads and joysticks that contain one or more [Controls](#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](#registercontrolcallback) to the [Controls](#control-field) with the `input` API.

The callback functions can then handle the [Events](#events) that are sent when the Control is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

Most robots with an input controller need at least the following hardware:

- A computer capable of running `viam-server`.
- A power supply cable or batteries for the input device and the robot.
- A component that you can direct the input to control, like an [arm](/components/arm/) or [motor](/components/motor).

## Configuration

Configuration depends on the `model` of your device.

For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`gamepad`](gamepad) | X-box, Playstation, and similar controllers with Linux support. |
| [`gpio`](gpio) | Customizable GPIO/ADC based device using a board component. |
| [`mux`](mux) | [Multiplexed](https://en.wikipedia.org/wiki/Multiplexer) controller, combining multiple sources of input. |
| [`webgamepad`](webgamepad) | A remote, web based gamepad. |
| [`fake`](fake) | A model for testing, with [no physical hardware - see GitHub.](https://github.com/viamrobotics/rdk/tree/main/components/input/fake) |

Once you've configured your input controller according to model type, you can write code to define how your robot processes the input from the controller.

## Control your robot with an input controller with Viam's client SDK libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries.

The following example assumes you have a controller called "my_controller" configured as a component of your robot.
If your input controller has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
from viam.components.input import Controller, Control, EventType
from viam.robot.client import RobotClient

# Define a function to connect to the robot.
async def connect_controller():
    creds = Credentials(
        type='robot-location-secret',
        payload= "xyzabclocationexample"), # ADD YOUR LOCATION SECRET VALUE. This can be found in the Code Sample tab of app.viam.com.
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("robot123example.locationxyzexample.viam.com", # ADD YOUR ROBOT REMOTE ADDRESS. This can be found in the Code Sample tab of app.viam.com.
    opts)

# Define a function to handle the controller.
async def handleController(controller):

    # Get the most recent events on the controller.
    resp = await controller.get_events()

    # Print the event, showing Control types.
    print(f'Controls:\n{resp}')

    # Use register_control_callback() to define how to handle Events from Controls.
    ...

async def main():

    # Connect to your robot.
    myRobotWithController = await connect_controller()

    # Get your controller from the robot.
    myController = Controller.from_robot(robot=myRobotWithController, name='my_controller')

    # Log an info message with the names of the different resources that are connected to your robot.
    print('Resources:')
    print(myController.resource_names)

    # Get the controller's Controls.
    resp = await myController.get_controls()

    # Print out the controller's Controls.
    print(f'Controls:\n{resp}')

    # Run the handleController function.
    await handleController(myController)

    # Wait to disconnect from the robot.
    await myRobotWithController.close()

if __name__ == '__main__':
    asyncio.run(main())

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
    "context"

    "github.com/edaniels/golog"
    "github.com/pkg/errors"
    "go.viam.com/rdk/components/input"
    "go.viam.com/utils"
    "golang.org/x/exp/slices"
)

// Define a function to handle the controller.
func handleController(controller input.Controller) {
    # Get the most recent events on the controller.
    resp, err := controller.Events()

    // Use RegisterControlCallback() to define how to handle Events from Controls.
    ...
}

func main() {
    utils.ContextualMain(mainWithArgs, golog.NewDevelopmentLogger("client"))
}


func mainWithArgs(ctx context.Context, args []string, logger golog.Logger) (err error) {

    // Connect to your robot.
    myRobotWithController, err := client.New(
        context.Background(),
        "xyzabclocationexample", // ADD YOUR LOCATION SECRET VALUE. This can be found in the Code Sample tab of app.viam.com.
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type:    utils.CredentialsTypeRobotLocationSecret,
            Payload: "robot123example.locationxyzexample.viam.com" // ADD YOUR ROBOT REMOTE ADDRESS. This can be found in the Code Sample tab of app.viam.com.
        })),
    )

    // Get the controller from the robot.
    myController, err := input.FromRobot(myRobotWithController, "my_controller")

    // Log any errors that occur and exit if an error is found.
    if err != nil {
        logger.Fatalf("cannot get controller: %v", err)
    }

    // Log an info message with the names of the different resources that are connected to your robot.
    logger.Info("Resources:")
    logger.Info(myRobotWithController.ResourceNames())

    // Get the controller's Controls.
    controls, err := myController.Controls(context.Background(), nil)

    // Print out the controller's Controls.
    logger.Info("Controls:")
    logger.Info(resp)

    // Log any errors that occur.
    if err != nil {
        logger.Fatal(err)
    }

    // Run the handleController function.
    err := HandleController(myController)

    // Delay closing your connection to your robot.
    err = myRobotWithController.Start(ctx)
    defer myRobotWithController.Close(ctx)

    // Watch for errors.
    if err != nil {
        return err
    }

    // Wait to exit mainWithArgs() until Context is Done.
    <-ctx.Done()

    return nil

}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}
The `Controller` interface is defined in [the Viam RDK](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go).

{{% /alert %}}

For more examples see [Usage Examples](#usage-examples).

## Types

### Event Object

Each `Event` object represents a singular event from the input device, and has four fields:

1. `Time`: `time.Time` the event occurred.
2. `Event`: `EventType` indicating the type of event (for example, a specific button press or axis movement).
3. `Control`: `Control` indicating which [Axis](#axis-controls), [Button](#button-controls), or Pedal on the controller has been changed.
4. `Value`: `float64` indicating the position of an [Axis](#axis-controls) or the state of a [Button](#button-controls) on the specified control.

#### EventType Field

A string-like type indicating the specific type of input event, such as a button press or axis movement.

- To select for events of all type when registering callback function with [RegisterControlCallback](#registercontrolcallback), you can use `AllEvents` as your `EventType`.
- The registered function is then called in addition to any other callback functions you've registered, every time an `Event` happens on your controller.
This is useful for debugging without interrupting normal controls, or for capturing extra or unknown events.

Registered `EventTypes` definitions:

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
ALL_EVENTS = "AllEvents"
"""
Callbacks registered for this event will be called in ADDITION to other registered event callbacks.
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
Relative position is reported via Value, a la mice, or simulating axes with up/down buttons.
"""
```

See [the Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/input/index.html#viam.components.input.EventType) for the most current version of supported `EventTypes`.

{{% /tab %}}
{{% tab name="Go" %}}

``` go {class="line-numbers linkable-line-numbers"}
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

#### Control Field

A string representing the physical input location, like a specific axis or button, of your `Controller` that the [Event Object](#event-object) is coming from.

Registered `Control` types are defined as follows:

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
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

### Axis Controls

{{% alert title="Note" color="note" %}}
Currently, only `Absolute` axes are supported.

`Relative` axes, reporting a relative change in distance, used by devices like mice and trackpads, will be supported in the future.
{{% /alert %}}

Analog devices like joysticks and thumbsticks which "return to center/neutral" on their own use `Absolute` axis control types.

These controls report a `PositionChangeAbs` [EventType](#eventtype-field).

**Value:** A `float64` between `-1.0` and `+1.0`.

- `1.0`: Maximum position in the positive direction.
- `0.0`: Center, neutral position.
- `-1.0`: Maximum position in the negative direction.

#### AbsoluteXY Axes

If your input controller has an analog stick, this is what the stick's controls report as.

Alternatively, if your input controller has *two* analog sticks, this is what the left joystick's controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteX` | Stick Left | Neutral | Stick Right |
| `AbsoluteY` | Stick Forward | Neutral | Stick Backwards |

#### AbsoluteR-XY Axes

If your input controller has *two* analog sticks, this is what the right joystick's controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteRX` | Stick Left | Neutral | Stick Right |
| `AbsoluteRY` | Stick Forward | Neutral | Stick Backwards |

- For `Y` axes, the positive direction is "nose up," and indicates *pulling* back on the joystick.

#### Hat/D-Pad Axes

If your input controller has a directional pad with analog buttons on the pad, this is what those controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteHat0X` | Left DPAD Button Press | Neutral | Right DPAD Button Press |
| `AbsoluteHat0Y` | Up DPAD Button Press | Neutral | Down DPAD Button Press |

#### Z Axes (Analog Trigger Sticks)

{{% alert title="Note" color="note" %}}
Devices like analog triggers and gas or brake pedals use `Absolute` axes, but they only report position change in the positive direction.
The neutral point of the axes is still `0.0`.
{{% /alert %}}

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteZ` | | Neutral | Stick Pulled |
| `AbsoluteRZ` | | Neutral | Stick Pulled |

`Z` axes are usually not present on most controller joysticks.

If present, they are typically analog trigger sticks, and unidirectional, scaling only from `0` to `1.0` as they are pulled, as shown above.

`AbsoluteZ` is reported if there is one trigger stick, and `AbsoluteZ` (left) and `AbsoluteRZ` (right) is reported if there are two trigger sticks.

Z axes can be present on flight-style joysticks, reporting *yaw*, or left/right rotation, as shown below.
This is not common.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteZ` | Stick Left Yaw | Neutral | Stick Right Yaw |
| `AbsoluteRZ` | Stick Left Yaw | Neutral | Stick Right Yaw |

### Button Controls

Button Controls report either `ButtonPress` or `ButtonRelease` as their [EventType](#eventtype-field).

**Value:**

- `0`: released
- `1`: pressed

#### Action Buttons (ABXY)

If your input controller is a gamepad with digital action buttons, this is what the controls for these buttons report as.

{{% alert title="Tip" color="tip" %}}
As different systems label the actual buttons differently, we use compass directions for consistency.

- `ButtonSouth` corresponds to "B" on Nintendo, "A" on XBox, and "X" on Playstation.
- `ButtonNorth` corresponds to "X" on Nintendo, "Y" on XBox, and "Triangle" on Playstation.
{{% /alert %}}

|Diamond 4-Action Button Pad | Rectangle 4-Action Button Pad |
|--|--|
|<table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonNorth`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Bottom</td></tr><tr><td>`ButtonEast`</td><td>Right</td></tr><tr><td>`ButtonWest`</td><td>Left</td></tr> </table>| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonNorth`</td><td>Top-left</td></tr><tr><td>`ButtonSouth`</td><td>Bottom-right</td></tr><tr><td>`ButtonEast`</td><td>Top-right</td></tr><tr><td>`ButtonWest`</td><td>Bottom-left</td></tr> </table>|

| Horizontal 3-Action Button Pad | Vertical 3-Action Button Pad |
|--|--|
|<table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonWest`</td><td>Left</td></tr><tr><td>`ButtonSouth`</td><td>Center</td></tr><tr><td>`ButtonEast`</td><td>Right</td></tr> </table>| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonWest`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Center</td></tr><tr><td>`ButtonEast`</td><td>Bottom</td></tr> </table>|

| Horizontal 2-Action Button Pad | Vertical 2-Action Button Pad |
|--|--|
|<table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonEast`</td><td>Right</td></tr><tr><td>`ButtonSouth`</td><td>Left</td></tr><tr> </table>| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonEast`</td><td>Top</td></tr><tr><td>`ButtonSouth`</td><td>Bottom</td></tr> </table>|

#### Trigger Buttons (Bumper)

If your input controller is a gamepad with digital trigger buttons, this is what the controls for those buttons report as.

| 2-Trigger Button Pad | 4-Trigger Button Pad |
|--|--|
|<table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonLT`</td><td>Left</td></tr><tr><td>`ButtonRT`</td><td>Right</td></tr> </table>| <table> <tr><th>Name</th><th>Description</th></tr><tr><td>`ButtonLT`</td><td>Top-left</td></tr><tr><td>`ButtonRT`</td><td>Top-right</td></tr><tr><td>`ButtonLT2`</td><td>Bottom-left</td></tr><tr><td>`ButtonRT2`</td><td>Bottom-right</td></tr> </table>|

#### Digital Buttons for Sticks

If your input controller is a gamepad with "clickable" thumbsticks, this is what thumbstick presses report as.

| Name | Description |
| ---- | ----------- |
| `ButtonLThumb` | Left or upper button for stick |
| `ButtonRThumb` | Right or lower button for stick |

#### Miscellaneous Buttons

Many devices have additional buttons.
If your input controller is a gamepad with these common buttons, this is what the controls for those buttons report as.

| Name | Description |
| ---- | ----------- |
| `ButtonSelect` | Select or - |
| `ButtonStart` | Start or + |
| `ButtonMenu` | Usually the central "Home" or Xbox/PS "Logo" button |
| `ButtonRecord` | Recording |
| `ButtonEStop` | Emergency Stop (on some industrial controllers) |

## API

The input controller component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [Controls](#controls) | Get a list of input `Controls` that this Controller provides. |
| [Events](#events) | Get the current state of the Controller as a map of the most recent [Event](#event-object) for each [Control](#control-field). |
| [RegisterControlCallback](#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](#eventtype-field) selected occurs on the given [Control](#control-field). |
<!-- | [TriggerEvent](#triggerevent) | Directly send an [Event](#event-object) to your robot. | -->
| [DoCommand](#docommand) | Sends or receives model-specific commands. |

### RegisterControlCallback

Defines a callback function to execute whenever one of the [EventTypes](#eventtype-field) selected occurs on the given [Control](#control-field).

You can only register one callback function per [Event](#event-object) for each [Control](#control-field).
A second call to register a callback function for a [EventType](#eventtype-field) on a [Control](#control-field) replaces any function that was already registered.

You can pass a `nil` function here to "deregister" a callback.

{{% alert title="Note" color="note" %}}
Registering a callback for the `ButtonChange` [EventType](#eventtype-field) is merely a convenience for filtering.
Doing so registers the same callback to both `ButtonPress` and `ButtonRelease`, but `ButtonChange` is not reported in an actual [Event Object](#event-object).
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `control` [(Control)](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): The [Control](#control-field) to register the function for.
- `triggers` [(List[EventType])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.EventType): The [EventTypes](#eventtype-field) that trigger the function.
- `function` [([ControlFunction])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback): The function to run when the specified triggers are invoked.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback).

```python {class="line-numbers linkable-line-numbers"}
# Define a function to handle pressing the Start Menu Button "BUTTON_START" on your controller, printing out the start time.
def print_start_time(event):
    print(f'Start Menu Button was pressed at this time:\n{event.time}')

# Define a function that handles the controller.
async def handle_controller(controller):

    # Get the list of Controls on the controller.
    controls = await controller.get_controls()

    # If the "BUTTON_START" Control is found, register the function print_start_time to fire when "BUTTON_START" has the event "ButtonPress" occur.
    if Control.BUTTON_START in controls:
        controller.register_control_callback(Control.BUTTON_START, [EventType.BUTTON_PRESS], print_start_time)
    else:
        print("Oops! Couldn't find the start button control! Is your controller connected?")
        exit()

    while True:
        await asyncio.sleep(1.0)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.
- `control`[(Control)](https://pkg.go.dev/go.viam.com/rdk/components/input#Control): The [Control](#control-field) to register the function for.
- `ctrlFunc` [(ControlFunction)](https://pkg.go.dev/go.viam.com/rdk/components/input#ControlFunction): The function to run when the specified triggers are invoked.
- `triggers` [([]EventType)](https://pkg.go.dev/go.viam.com/rdk/components/input#EventType): The [EventTypes](#eventtype-field) that trigger the function.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go {class="line-numbers linkable-line-numbers"}
// Define a function that handles the controller.
func handleController(controller input.Controller) {

    // Define a function to handle pressing the Start Menu Button "ButtonStart" on your controller, logging the start time.
    printStartTime := func(ctx context.Context, event input.Event) {
        logger.Info("Start Menu Button was pressed at this time: %v", event.Time)
    }

    // Define the EventType "ButtonPress" to serve as the trigger for printStartTime.
    triggers := [1]input.EventType{input.ButtonPress}

    // Get the controller's Controls.
    controls, err := myController.Controls(context.Background(), nil)

    // If the "ButtonStart" Control is found, register the function printStartTime to fire when "ButtonStart" has the event "ButtonPress" occur.
    if slices.Contains(controls, Control.ButtonStart) {
        err := controller.RegisterControlCallback(context.Background(), Control: input.ButtonStart, triggers, printStartTime, nil)
    }
     else {
        logger.Fatalf("Oops! Couldn't find the start button control! Is your controller connected?")
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### Events

This method returns the current state of the controller as a map of [Event Objects](#event-object), representing the most recent event that has occured on each available [Control](#control-field).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `events` [(Dict[Control, Event])](https://docs.python.org/3/library/typing.html#typing.Dict): A dictionary mapping the most recent Event for each Control.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/input/input.html#Controller.get_events).

```python {class="line-numbers linkable-line-numbers"}
# Get the most recent Event for each Control.
recent_events = await myController.get_events()

# Print out the most recent Event for each Control.
print(f'Recent Events:\n{recent_events}')
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `events` [(map[Control]Event)](https://pkg.go.dev/go.viam.com/rdk/components/input#Control): A map mapping the most recent Event for each Control.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go {class="line-numbers linkable-line-numbers"}
// Get the most recent Event for each Control.
recent_events, err := myController.Events(context.Background(), nil)

// Log any errors that occur and exit if an error is found.
if err != nil {
  logger.Fatalf("cannot get list of recent events from controller: %v", err)
}

// Log the most recent Event for each Control.
logger.Info("Recent Events: %v", recent_events)
```

{{% /tab %}}
{{< /tabs >}}

### Controls

Get a list of the [Controls](#control-field) that your controller provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `controls` [(List[Control])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): List of Controls provided by the controller.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/input/input.html#Controller.get_position).

```python {class="line-numbers linkable-line-numbers"}
my_input_controller = Controller.from_robot(robot=myRobotWithController, name='my_controller') ...

# Get the list of Controls provided by the controller.
controls = await my_input_controller.get_controls()

# Print the list of Controls provided by the controller.
print(f'Controls:\n{controls}')
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `controls` [([]float64)](https://pkg.go.dev/builtin#float64): List of controls provided by the controller.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go {class="line-numbers linkable-line-numbers"}
myController, err := controller.FromRobot(myRobotWithController, "my_controller")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
} ...

// Get the list of Controls provided by the controller.
controls, err := myController.Controls(context.Background(), nil)

// Log any errors that occur and exit if an error is found.
if err != nil {
  logger.Fatalf("cannot get controls provided by controller: %v", err)
}

// Log the list of Controls provided by the controller.
logger.Info("Controls:")
logger.Info(controls)
```

{{% /tab %}}
{{< /tabs >}}
<!-- ### TriggerEvent NOTE: This method should be documented when support is available for all input components.

Directly send an [Event Object](#event-object) from external code.

{{% alert title="Note" color="note" %}}
This method is currently only supported for input controllers of model `webgamepad`.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `event` [(Event)](#event-object): The `Event` to trigger on the controller.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/input/input.html#Controller.trigger_event).

```python {class="line-numbers linkable-line-numbers"}
# Define a "Button is Pressed" event for the control BUTTON_START.
button_is_pressed_event = Event(time(), EventType.BUTTON_PRESS, Control.BUTTON_START, 1.0)

# Trigger the event on your controller. Set this trigger to timeout if it has not completed in 7 seconds.
await myController.trigger_event(event=my_event, timeout=7.0)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `event` [(Event)](#event-object): The `Event` to trigger on the controller.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go {class="line-numbers linkable-line-numbers"}
// Define a "Button is Pressed" event for the control ButtonStart.
buttonIsPressedEvent := input.Event{Time: time.Now(), Event: input.ButtonPress, Control: input.ButtonStart, Value: 1.0}

// Trigger the event on your controller.
err := myController.TriggerEvent(ctx Context.background(), buttonIsPressedEvent, nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot trigger event on controller: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}} -->

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own input controller and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_input_controller = Controller.from_robot(robot, "my_controller")

command = {"cmd": "test", "data1": 500}
result = my_input_controller.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/#the-do-method).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` (`cmd map[string]interface{}`): The command to execute.

**Returns:**

- `result` (`cmd map[string]interface{}`): Result of the executed command.
- `error` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
  myController, err := input.FromRobot(robot, "my_controller")

  command := map[string]interface{}{"cmd": "test", "data1": 500}
  result, err := myController.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/9be13108c8641b66fd4251a74ea638f47b040d62/components/input/input.go#L254).

{{% /tab %}}
{{< /tabs >}}

## Usage Examples

### Control a Wheeled Base with a Logitech G920 Steering Wheel Controller

The following Python code is an example of controlling a wheeled base with a Logitech G920 steering wheel controller, configured as a `gamepad` input controller.

``` python {id="python-example" class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.components.input import Control, Controller, EventType
from viam.proto.common import Vector3
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

turn_amt = 0
modal = 0
cmd = {}

async def connect_robot(host, payload):
    creds = Credentials(
        type='robot-location-secret',
        payload=payload),
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
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
        controller.register_control_callback(Control.ABSOLUTE_PEDAL_ACCELERATOR, [EventType.POSITION_CHANGE_ABSOLUTE], handle_accelerator)
    else:
        print("Accelerator Pedal not found! Exiting! Are your steering wheel and pedals hooked up?")
        exit()

    if Control.ABSOLUTE_PEDAL_BRAKE in resp:
        controller.register_control_callback(Control.ABSOLUTE_PEDAL_BRAKE, [EventType.POSITION_CHANGE_ABSOLUTE], handle_brake)
    else:
        print("Brake Pedal not found! Exiting!")
        exit()

    if Control.ABSOLUTE_PEDAL_CLUTCH in resp:
        controller.register_control_callback(Control.ABSOLUTE_PEDAL_CLUTCH, [EventType.POSITION_CHANGE_ABSOLUTE], handle_clutch)
    else:
        print("Accelerator Pedal not found! Exiting! Are your steering wheel and pedals hooked up?")
        exit()

    if Control.ABSOLUTE_X in resp:
        controller.register_control_callback(Control.ABSOLUTE_X, [EventType.POSITION_CHANGE_ABSOLUTE], handle_turning)
    else:
        print("Wheel not found! Exiting!")
        exit()

    while True:
        await asyncio.sleep(0.01)
        global cmd
        if "y" in cmd:
            respon = await modal.set_power(linear=Vector3(x=0,y=cmd["y"],z=0), angular=Vector3(x=0,y=0,z=turn_amt))
            cmd = {}
            print(respon)

async def main():
    # ADD YOUR ROBOT REMOTE ADDRESS and LOCATION SECRET VALUES.
    # This can be found in the Code Sample tab of app.viam.com.
    g920_robot = await connect_robot("robot123example.locationxyzexample.viam.com", "xyzabclocationexample")
    modal_robot = await connect_robot("robot123example.locationxyzexample.viam.com", "xyzabclocationexample")

    g920 = Controller.from_robot(g920_robot, 'wheel')
    global modal
    modal = Base.from_robot(modal_robot, 'modal-base-server:base')

    await handleController(g920)

    await g920_robot.close()
    await modal_robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Drive a robot with Four Wheels & a Skid Steer Platform

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

{{% alert title="Note" color="note" %}}
Access the complete repository for the Python example on [Github](https://github.com/viamrobotics/intermode/blob/main/controller_client/wheel.py).
{{% /alert %}}

## SDK Documentation

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/input/index.html)
- [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/input)

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
    {{% card link="/tutorials/control/yahboom-rover" size="small" %}}
    {{% card link="/tutorials/control/scuttle-gamepad" size="small" %}}
{{< /cards >}}
