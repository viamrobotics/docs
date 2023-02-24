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

Configuring an *input* component allows you to implement one of these devices into your robot, enabling you to control your robot's actions by interacting with the device.

Most robots with an input controller need at least the following hardware:

- A device that turns human input into electronic signals.
- A component that you can direct the input to control the position of, like an [arm](/components/arm/) or [motor](/components/motor). See those pages for additional required hardware and configuration.
- A power supply or batteries.

## Configuration

Configuration depends on which `model` the type of device you wish to configure falls under.

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

### Detailed Code Examples

{{< tabs >}}
{{% tab name="Python" %}}

The below Python code is an example of controlling a wheeled base with a Logitech G920 steering wheel controller.

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

async def connect_modal():
    creds = Credentials(
        type='robot-location-secret',
        payload='...')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('...viam.cloud', opts)

async def connect_controller():
    creds = Credentials(
        type='robot-location-secret',
        payload='...')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('...viam.cloud', opts)

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
    g920_viam = await connect_controller()
    modal_viam = await connect_modal()

    g920 = Controller.from_robot(g920_viam, 'wheel')
    global modal
    modal = Base.from_robot(modal_viam, 'modal-base-server:base')

    await handleController(g920)

    await g920_viam.close()
    await modal_viam.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

The below Go code is an example of how to use an input controller to drive a robot with four wheels & a skid steer platform.

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

{{% /tab %}}
{{< /tabs >}}

{{% alert="Note" color="note" %}}
Access the complete repository for the above Python example on Viam's Github [here](https://github.com/viamrobotics/intermode/blob/main/controller_client/wheel.py).
{{% /alert %}}

### Control your robot with an Input Controller with Viam's Client SDK Libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam app guide](/manage/app-usage/) for app-specific guidance.

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
        payload= "GRAB YOUR ROBOT LOCATION SECRET VALUE [Can be found in robot's Code Sample Tab in app.viam.com]"
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("GRAB YOUR ROBOT'S REMOTE ADDRESS [Can be found in robot's Control Tab in app.viam.com", opts)

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
    await myController.close()

if __name__ == '__main__':
    asyncio.run(main())

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
    "context"
    "github.com/pkg/errors"
    "go.viam.com/rdk/components/input"
)

// Define a function to handle the controller. 
func handleController(controller input.Controller) {
    # Get the most recent events on the controller.
    resp, err := controller.Events()

    // Use RegisterControlCallback() to define how to handle Events from Controls.
    ...
}

func main() {

    // Create an instance of a logger.
    logger := golog.NewDevelopmentLogger("client")

    // Connect to your robot.
    myRobotWithController, err := client.New(
        context.Background(),
        "GRAB YOUR ROBOT'S REMOTE ADDRESS [Can be found in robot's Control Tab in app.viam.com)",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type:    utils.CredentialsTypeRobotLocationSecret,
            Payload: "GRAB YOUR ROBOT LOCATION SECRET VALUE [Can be found in robot's Code Sample Tab in app.viam.com]",
        })),
    )

    // Get the controller from the robot.
    myController, err := input.FromRobot(myRobotWithController, "my_controller")

    // Log any errors that occur.
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

    // Delay closing your connection to your robot until main() exits.
    defer robot.Close(context.Background())

}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert="Note" color="note" %}}
The `Controller` interface is defined in the Viam RDK [here](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go).

Access complete example code for controlling a wheeled base with a Logitech G920 steering wheel on Viam's Github [here](https://github.com/viamrobotics/intermode/blob/main/controller_client/wheel.py).
{{% /alert %}}

## API

The input controller component supports the following methods:

| Method Name | Go | Python | Description |
| ----------- | -- | ------ | ----------- |
| [Controls](#controls) | [Controls][go_input]  |  [get_controls][python_get_controls] | Get a list of input `Controls` that this Controller provides. |
| [Events](#events) | [Events][go_input] | [get_events][python_get_events] | Get the current state of the Controller as a map of the most recent [Event](#event-object) for each [Control](#control-field). |
| [RegisterControlCallback](#registercontrolcallback) | [RegisterControlCallback][go_input] | [register_control_callback][python_register_control_callback] | Define a callback function to execute whenever one of the [`EventTypes`](#eventtype-field) selected occurs on the given [Control](#control-field). |
| [TriggerEvent](#triggerevent) | [TriggerEvent][go_triggerable] | [trigger_event][python_trigger_event] | Directly send an [Event](#event-object) to your robot. |

[go_input]: https://pkg.go.dev/go.viam.com/rdk/components/input#Controller
[go_triggerable]: https://pkg.go.dev/go.viam.com/rdk/components/input#Triggerable
[python_get_controls]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.get_controls
[python_get_events]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.get_events
[python_register_control_callback]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback
[python_trigger_event]: https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.trigger_event

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

// Log any errors that occur.
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
myController = Controller.from_robot(robot=myRobotWithController, name='my_controller') ...

# Get the list of Controls provided by the controller.
controls = await myController.get_controls()

# Print the list of Controls provided by the controller.
print(f'Controls:\n{controls}')
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): List of controls provided by the controller.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

```go {class="line-numbers linkable-line-numbers"}
myController, err := controller.FromRobot(myRobotWithController, "my_controller")
if err != nil {
  logger.Fatalf("cannot get controller: %v", err)
} ...

// Get the list of Controls provided by the controller.
controls, err := myController.Controls(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get controls provided by controller: %v", err)
}

// Log the list of Controls provided by the controller. 
logger.Info("Controls:")
logger.Info(controls)
```

{{% /tab %}}
{{< /tabs >}}

### RegisterControlCallback

Defines a callback function to execute whenever one of the [EventTypes](#eventtype-field) selected occurs on the given [Control](#control-field).

You can only register one callback function per [Event](#event-object) for each [Control](#control-field).
A second call to register a callback function for a [EventType](#eventtype-field) on a [Control](#control-field) replaces any function that was already registered.

You can pass a `nil` function here to "deregister" a callback.

{{% alert="Note" color="note" %}}
Registering a callback for the `ButtonChange` [EventType](#eventtype-field) is merely a convenience for filtering.
Doing so registers the same callback to both `ButtonPress` and `ButtonRelease`, but `ButtonChange` is not reported in an actual [Event Object](#event-object).
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `control` [(Control)](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): The [Control](#control-field) to register the function for.
- `triggers` [(List[EventType])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.EventType): The [EventTypes](#eventtype-field) that trigger the function.
- `function` [(Optional[ControlFunction])](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback): The function to run when the specified triggers are invoked.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Controller.register_control_callback).

```python {class="line-numbers linkable-line-numbers"}
''' import ... 
    async def connect_controller(): ... 
    [See the Code Example subsection of this page for full connection start code].
'''

# Define a function to handle pressing the Start Menu Button "BUTTON_START" on your controller, printing out the start time.
def print_start_time(event):
    print(f'Start Menu Button was pressed at this time:\n{event.time}')

# Define a function that handles the controller.
async def handle_controller(controller):

    # Get the most recent Events on the controller.
    recent_events = await controller.get_events()

    # Register the function print_start_time to fire when "BUTTON_START" has the event "ButtonPress" occur.
    if Control.BUTTON_START in recent_events:
        controller.register_control_callback(Control.BUTTON_START, [EventType.BUTTON_PRESS], print_start_time)
    else:
        print("Oops! Couldn't find that the start button was pressed! Is your controller connected?")
        exit()

    while True:
        await asyncio.sleep(0.01)

async def main():

    # Connect to your robot. 
    myRobotWithController = await connect_controller()

    # Get your controller from the robot. 
    myController = Controller.from_robot(robot=myRobotWithController, name='my_controller')

    # Run the handle_controller function.
    await handle_controller(myController)

    # Wait to disconnect from the robot.
    await myController.close()

if __name__ == '__main__':
    asyncio.run(main())
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
// import {} ... [See the Code Example subsection of this page for full connection start code.]

// Define a function to handle Events that occur on the controller. 
func handleController(controller input.Controller) {

    // Define a function to handle pressing the Start Menu Button "ButtonStart" on your controller, logging the start time.
    printStartTime := func(ctx context.Context, event input.Event) {
        logger.Info("Start Menu Button was pressed at this time: %v", event.Time)
    }

    // Define the EventType "ButtonPress" to serve as the trigger for printStartTime. 
    triggers := [1]input.EventType{input.ButtonPress}

    // Register the printStartTime function to fire when "ButtonStart" has the event "ButtonPress" occur.
    err := controller.RegisterControlCallback(context.Background(), Control: input.ButtonStart, triggers, printStartTime, nil)

    // Log any errors that occur.
    if err != nil {
    logger.Fatalf("Oops! Couldn't find that the start button was pressed! Is your controller connected?: %v", err)
    }
}

func main() {

    // Create an instance of a logger.
    logger := golog.NewDevelopmentLogger("client")

    // Connect to your robot.
    myRobotWithController, err := client.New(
        context.Background(),
        "GRAB YOUR ROBOT'S REMOTE ADDRESS [Can be found in robot's Control Tab in app.viam.com)",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type:    utils.CredentialsTypeRobotLocationSecret,
            Payload: "GRAB YOUR ROBOT LOCATION SECRET VALUE [Can be found in robot's Code Sample Tab in app.viam.com]",
        })),
    )

    // Get the controller from the robot. 
    myController, err := input.FromRobot(myRobotWithController, "my_controller")

    // Log any errors that occur.
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
    err := handleController(myController)

    // Delay closing your connection to your robot until main() exits.
    defer robot.Close(context.Background())

}
```

{{% /tab %}}
{{< /tabs >}}

### TriggerEvent

Directly send an [Event Object](#event-object) from external code.

{{% alert="Note" color="note" %}}
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
{{< /tabs >}}

## Event Object

Each `Event` object represents a singular event from the input device, and has four fields:

1. `Time`: `time.Time` the event occurred.
2. `Event`: `EventType` indicating the most recent status of the specified control on the controller.
3. `Control`: `Control` indicating which [Axis](#axis-controls), [Button](#button-controls), or Pedal on the controller has been changed.
4. `Value`: `float64` indicating the position of an [Axis](#axis-controls) or the state of a [Button](#button-controls) on the specified control.

### EventType Field

A string representing the type of Event that has occured in the [Event Object](#event-object).

- To select for events of all type when registering callback function with [RegisterControlCallback](#registercontrolcallback), you can use `AllEvents` as your `EventType`.
- The registered function is then called in addition to any other callback functions you've registered, every time an `Event` happens on your controller.
This is useful for debugging without interrupting normal controls, or for capturing extra or unknown events.

Registered `EventTypes` are defined as followed:

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
Key is held down. This wil likely be a repeated event.
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

### Control Field

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

See [the Viam RDK](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of supported `Control` types.

{{% /tab %}}
{{< /tabs >}}

See [input/input.go](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) for the most current version of the above list of supported `Controls`.

### Axis Controls

{{% alert="Note" color="note" %}}
Currently, only `Absolute` axes are supported.

`Relative` axes, reporting a relative change in distance, used by devices like mice and trackpads, will be supported in the future.
{{% /alert %}}

Devices like joysticks and thumbsticks—anything that "returns to center" on its own—use `Absolute` axis control types.

These controls report a `PositionChangeAbs` [EventType](#eventtype-field).

**Value:** A `float64` between `-1.0` and `+1.0`.

- `1.0`: Maximum position change in the positive direction.
- `0.0`: Center value. No position change.
- `-1.0`: Maximum position change in the negative direction.

#### AbsoluteXYZ Axes

If your input controller has a analog control stick, this is what the stick's controls report as.

- If your input controller is a gamepad with two analog sticks, this is what the left joystick controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteX` | Stick Left | Neutral | Stick Right |
| `AbsoluteY` | Stick Down | Neutral | Stick Up |
| `AbsoluteZ` | Stick Vertical Down | Neutral | Stick Vertical Up |

#### AbsoluteR-XYZ Axes

If your input controller has two analog sticks, this is what the right stick's controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteRX` | Stick Left | Neutral | Stick Right |
| `AbsoluteRY` | Stick Down | Neutral | Stick Up |
| `AbsoluteRZ` | Stick Vertical Down | Neutral | Stick Vertical Up |

**Y - Z up & down:**

- `Y` axes: up is "nose up," indicates *pulling* back on the joystick.
- `Z` axes: vertical up and down, indicates a *pushing* motion on the joystick.

#### AbsoluteHat Axes

If your input controller has a directional pad with analog buttons on the pad, this is what those controls report as.

| Name | `-1.0` | `0.0` | `1.0` |
| ---- | ------ | ----- | ----- |
| `AbsoluteHat0X` | Left DPAD Button Press | Neutral | Right DPAD Button Press |
| `AbsoluteHat0Y` | Up DPAD Button Press | Neutral | Down DPAD Button Press |

{{% alert="Note" color="note" %}}
Devices like analog triggers and gas or brake pedals use `Absolute` axes, but they only report position change in the positive direction.
The neutral point of the axes is still `0.0`.
{{% /alert %}}

### Button Controls

Button Controls report either `ButtonPress` or `ButtonRelease` as their [EventType](#eventtype-field).

**Value:**

- `0`: released
- `1`: pressed

#### Action Buttons (ABXY)

If your input controller is a gamepad with digital action buttons, this is what the controls for these buttons report as.

**Quick Orientation Tips:**

- `ButtonSouth` corresponds to "B" on Nintendo, "A" on XBox, and "X" on Playstation.
- `ButtonNorth` corresponds to "X" on Nintendo, "Y" on XBox, and "Triangle" on Playstation.

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

If your input controller is a gamepad with a joystick with digital buttons, this is what the controls for those buttons report as.

| Name | Description |
| ---- | ----------- |
| `ButtonLThumb` | Left or upper button for stick |
| `ButtonRThumb` | Right or lower button for stick |

#### Menu Buttons

If your input controller is a gamepad with digital menu buttons, this is what the controls for those buttons report as.

| Name | Description |
| ---- | ----------- |
| `ButtonSelect` | Select (Duo) |
| `ButtonStart` | Start (Duo) |
| `ButtonMenu` | Start (Solo) |
| `ButtonRecord` | Recording |
| `ButtonEStop` | Stop |

## Work in Progress Models

Mappings are currently available for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi.)

The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.

Because of that, any unknown gamepad will be be mapped that way.
If you have another controller that you want to use to control your robot, feel free to submit a PR on the [Viam Robotics Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) with new mappings.

## SDK Documentation

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/input/index.html)
- [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/input)

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
