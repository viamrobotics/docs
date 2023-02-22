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

You should already be familiar with human-interface devices, like keyboards and mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers, from your daily life.

Configuring an *input* component allows you to implement one of these devices into your robot, enabling you to control the robot's actions by interacting with a device.

Most robots with an input controller need at least the following hardware:

- A [board component](/components/board/).
- A power supply.
- A device that turns human input into electronic signals.
- (Optional) A component that you can direct the input to control the position of, like an [arm](/components/arm/).

## Configuration

Configuration depends on which `model` the type of device you wish to implement falls under.

{{% alert="Note" color="note" %}}
In the Viam Robot Development Kit & SDKS, the "input controller" component package is defined as `input`, not `input_controller`.

See the [Viam RDK](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go), the [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/input/index.html), or the [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/input) for more information.
{{% /alert %}}

For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`gamepad`](gamepad) | Implement a linux based gamepad as an input controller. |
| [`gpio`](gpio) | Implement a GPIO/ADC based device as an input controller. |
| [`mux`](mux) | Implement a [multiplexed](https://en.wikipedia.org/wiki/Multiplexer) controller, combining multiple sources of input. |
| [`webgamepad`](webgamepad) | Implement a web based gamepad as an input controller. |
| [`fake`](fake) | A model for testing, with [no physical hardware - see Viam GitHub.](https://github.com/viamrobotics/rdk/tree/main/components/input/fake) |

Once you've configured your input controller according to model type, you can write code to define how your robot processes the input from the controller.

## Code Examples

### Control your Input Controller with Viam's Client SDK Libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/manage/app-usage/) for app-specific guidance.

The following example assumes you have a controller called "my_controller" configured as a component of your robot.
If your input controller has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
from viam.components.input import Controller, Control, EventType
from viam.robot.client import RobotClient

async def main():

    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot.
    print('Resources:')
    print(robot.resource_names)

    # Connect to your controller.
    myController = Controller.from_robot(robot=robot, name='my_controller')

    # Call a function to handle events from the controller.
    await handleController(myController)

    # Disconnect from your robot.
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())

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
        exit() ...

```

Access the full functional example code shown above on the Viam Github [here](https://github.com/viamrobotics/intermode/blob/main/controller_client/wheel.py).

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
 "go.viam.com/rdk/components/input"
)

func main() {

  // Create an instance of a logger.
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot.
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE SECURITY TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE LOCATION'S PAGE IN THE VIAM APP]",
      })),
  )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits.
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot.
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Connect to your controller.
  myGantry, err := gantry.FromRobot(robot, "my_gantry")
  if err != nil {
    logger.Fatalf("cannot get gantry: %v", err)
  }

  err := HandleController() ... // TODO: NEED TO SET THIS UP

}
```

{{% /tab %}}
{{< /tabs >}}

The `Controller` interface is defined in the Viam RDK [here](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go).
View that file for even more details on specific methods and their uses.

## Detailed Code Examples

The below Go code is an example of how to use an input controller to drive a robot with four wheels & a skid steer platform.

The `motorCtl` callback function controls 5 motors: left front & back `FL` `BL`, right front & back `FL` `BL`, and a `winder` motor that raises and lowers a front-end like a bulldozer.

- The `event.Control` logic determines the case for setting the power of each motor by which button is pressed on the input controller `input`.

{{% alert="Note" color="note" %}}
See the [motor component page](/docs/components/motor.md) for more information on motor control, and the [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/input) for more information about using Go to control your robot.
{{% /alert %}}

```go {class="line-numbers linkable-line-numbers"}
// Define a single callback function
motorCtl := func(ctx context.Context, event input.Event) {
    if event.Event != input.PositionChangeAbs {
        return
    }

    speed := float32(math.Abs(event.Value))

    // Handle input events, commands to set the power of motor components (SetPower method)
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

// Registers callback from motorCtl for a selected set of axes
for _, control := range []input.Control{input.AbsoluteY, input.AbsoluteRY, input.AbsoluteZ, input.AbsoluteRZ} {
    err = g.RegisterControlCallback(ctx, control, []input.EventType{input.PositionChangeAbs}, motorCtl)
}
```

## API

The input controller component supports the following methods:

| Method Name | Go | Python | Description |
| ----------- | -- | ------ | ----------- |
[Controls](#controls) | [Controls][go_input]  |  [get_controls][python_get_controls] | Get a list of input `Controls` that this Controller provides. | [Events](#event) | [Events][go_input] | [get_events][python_get_events] | Get the current state of the Controller as a map of the most recent [Event](#event-object) for each [Control](#control-field). | [RegisterControlCallback](#registercontrolcallback) | [RegisterControlCallback][go_input] | [register_control_callback][python_register_control_callback] | Define a callback function to execute whenever one of the [`EventTypes`](#eventtype-field) selected occurs on the given [Control](#control-field). | [TriggerEvent](#triggerevent) | [TriggerEvent][go_triggerable] | [trigger_event][python_trigger_event] | Directly send an [Event](#event), like a button press, to your robot from external code. |

[go_input]: https://pkg.go.dev/go.viam.com/rdk/components/input#Controller
[go_triggerable]: https://pkg.go.dev/go.viam.com/rdk/components/input#Triggerable
[python_get_controls]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.get_controls
[python_get_events]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.get_events
[python_register_control_callback]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback
[python_trigger_event]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.trigger_event

### Events

This method returns the current state of the controller as a map of [Event Objects](#event-object).

The map represents the most recent input event for each input [Control](#control-field) on the input controller.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `events` [(Dict[Control, Event])](https://docs.python.org/3/library/typing.html#typing.Dict): A dictionary mapping the most recent event for each input, which should be the current state of the Controller.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/controller/input.html#Controller.get_events).

```python
myController = Controller.from_robot(robot=robot, name='my_robot_with_controller')

# Get the most recent event for each input Control.
events = await myController.get_events()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `events` [(map[Control]Event)](https://pkg.go.dev/go.viam.com/rdk/components/input#Control): A map mapping the most recent event for each input, which should be the current state of the Controller.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go
myController, err := controller.FromRobot(robot, "my_robot_with_controller")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
}

// Get the most recent event for each input Control.
events, err := myController.Events(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get list of recent events from controller: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

### Controls

Get a list of the input `Controls` that this `Controller` provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `controls` [(List[Control])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): List of Controls provided by the Controller.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/controller/controller.html#Controller.get_position).

```python
myController = Controller.from_robot(robot=robot, name='my_robot_with_controller')

# Get the list of Controls provided by the Controller.
controls = await myController.get_controls()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): List of Controls provided by the Controller.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go
myController, err := controller.FromRobot(robot, "my_robot_with_controller")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
}

// Get the list of Controls provided by the Controller.
controls, err := myController.Controls(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get controls provided by controller: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

### RegisterControlCallback

Defines a callback function to execute whenever one of the [EventTypes](#eventtype-field) selected occurs on the given [Control](#control-field).

This is the preferred method for real-time control.
Note that you can only register one callback function per `Event` for each `Control`.
A second call to register a callback function for a given event type on a given `Control` replaces any previously registered function with the newly registered callback function for that event.
You can also pass a `nil` function here, which will effectively "deregister" a callback.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `control` [Control](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): The [Control](#control-field) to register the function for.
- `triggers` [List[EventType]](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.EventType): The [EventTypes](#eventtype-field) that will trigger the function.
- `function` [Optional[ControlFunction]]: The function to run on specific triggers.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback).

```python
myController = Controller.from_robot(robot=robot, name='my_robot_with_controller')

# Register a function that will fire on given EventTypes for a given Control
await myController.register_control_function()
```

<!-- TODO: finish above code sample  -->

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go
myController, err := controller.FromRobot(robot, "my_robot_with_controller")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
}

// Register a function that will fire on given EventTypes for a given Control.
err := myController.RegisterControlCallback(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot register callback function to controller: %v", err)
}

```

<!-- TODO: finish above code sample  -->

{{% /tab %}}
{{< /tabs >}}

### TriggerEvent

Directly send an [Event Object](#event-object) from external code.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `event` [(Event)](#event-object): The `Event` to trigger on the controller.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/input/input.html#Controller.trigger_event).

```python
myController = Controller.from_robot(robot=robot, name='my_gantry')

# Trigger an event on your Controller.
await myController.trigger_event(event= SomeEvent)
```

<!-- TODO: Finish the above code sample  -->

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

-
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go
myGantry, err := controller.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
}

// Get the current positions of the axes of the controller in millimeters.
position, err := myGantry.Position(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get positions of controller axes: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

Access the source code of these methods on the [Viam Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go).

## Event Object

Each `Event` object represents a singular event from the input device, and has four fields:

1. `Time`: `time.Time` the event occurred
2. `Event`: `input.EventType` representing the most recent status of the `Control` on the `Controller`, as it was changed. See [EventType Field](#eventtype-field) below for more information.
3. `Control`: `input.Control` representing which axis/button/etc. on the `Controller` was changed.
See [Control Field](#control-field) below for more information.
4. `Value`: `float64` indicating the position of an axis (`-1.0 to +1.0`) or the state of a button (`0` or `1`) on the `Controller`.

### EventType Field

A string representing the type of Event that has occured in the [Event Object](#event-object).

- To select for events of all type when registering callback function with [RegisterControlCallback](#registercontrolcallback), you can use `AllEvents` as your `EventType`.
- The registered function will then be called, *in addition to* any other callback functions you've registered, every time an `Event` happens on your `Controller`.
This is useful for debugging without interrupting normal controls, or for capturing extra or unknown events.

Registered `EventTypes` are defined as followed:

``` go {class="line-numbers linkable-line-numbers"}
// EventType list from https://github.com/viamrobotics/rdk/blob/main/components/input/input.go
const (
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
)

```

See [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of the above list of supported `EventTypes`.

### Control Field

A string representing the physical input location, like a specific axis or button, of your `Controller` that the [Event Object](#event-object) is coming from.

Registered `Control` types are defined as follows:

```go {class="line-numbers linkable-line-numbers"}
// Controls, to be expanded as new input devices are developed.
const (
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
)

```

Some explanations:

- The X and Y axis of a primary joystick, a type of `Controller` which reports absolute position, are the `Control` types `AbsoluteX` and `AbsoluteY`.
- The secondary (right hand) joystick or thumbstick is `AbsoluteRY` and `AbsoluteRY`.
- For trigger buttons, `ButtonLT` refers to the left trigger button, and `ButtonRT` refers to the right trigger button.
- `ButtonSouth` refers to the bottom-most button of four, and corresponds to "B" on Nintendo, "A" on XBox, and "X" on Playstation.
- `ButtonNorth` is, likewise, X/Y/Triangle.

The typical 4-button configuration on most gamepads uses generic compass directions instead of letter or shape labels, so these mappings are not XBox/Nintendo/Playstation gamepad specific.

See [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of the above list of supported `Controls`.

<!-- ###### Axes

`Axes` can be either Absolute or Relative.
Absolute axes report where they are each time.
This is the method used by things like joysticks/thumbsticks, analog triggers, etc.--basically anything that "returns to center" on its own.
Relative axes, on the other hand, are used by mice/trackpads/etc., and report a relative change in distance.
For now, only the `gamepad` implementation exists, so only Absolute axes are in use.
Absolute axes report a "PositionChangeAbs" EventType, and the Value is a float64 between -1.0 and +1.0, with center/neutral always being 0.0.
The one special case is single-direction axes (like analog triggers, gas/brake pedals, etc.)
On these, the "neutral" point is still 0.0, but they may only ever go into the positive direction.
Lastly, note that for Y (vertical) axes, the positive direction is "nose up" which is pulling back on the stick.

###### Buttons

Buttons are a simpler case.
They report either `ButtonPress` or `ButtonRelease` as their `EventType`, and the value is either 0 (for released) or 1 (for pressed.)
Note that registering a callback for the `ButtonChange` `Event` is merely a convenience for filtering, and will register the same callback to both `ButtonPress` and `ButtonRelease`, but `ButtonChange` will not be reported in an actual `Event`. 

## Work in Progress Models

 TODO sierra's notes for PR review: don't understand this section very well but not sure if I should remove
what is meant exactly by mappings, and where precisely would you submit a PR to? messaged matt d. s

There are currently mappings for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi.)
The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.
Because of that, any unknown gamepad will be be mapped that way.
If you have another controller though, feel free to submit a PR with new mappings. -->

## SDK Documentation

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/input/index.html)
- [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/input)

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
