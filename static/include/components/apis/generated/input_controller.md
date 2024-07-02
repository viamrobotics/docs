### GetControls

Get a list of the [Controls](#control-field) that your controller provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.components.input.input.Control]](https://python.viam.dev/autoapi/viam/components/input/input/index.html#viam.components.input.input.Control)): List of controls provided by the Controller.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the list of Controls provided by the controller.
controls = await my_controller.get_controls()

# Print the list of Controls provided by the controller.
print(f"Controls: {controls}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_controls).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]Control)](https://pkg.go.dev/go.viam.com/rdk/components/input#Control): List of Controls provided by the controller.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the list of Controls provided by the controller.
controls, err := myController.Controls(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{< /tabs >}}

### GetEvents

This method returns the current state of the controller as a map of [Event Objects](#event-object), representing the most recent event that has occurred on each available [Control](#control-field).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([Dict[viam.components.input.input.Control, viam.components.input.input.Event]](https://python.viam.dev/autoapi/viam/components/input/input/index.html#viam.components.input.input.Control)): The most recent event for each input.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the most recent Event for each Control.
recent_events = await my_controller.get_events()

# Print out the most recent Event for each Control.
print(f"Recent Events: {recent_events}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_events).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map[Control]Event)](https://pkg.go.dev/go.viam.com/rdk/components/input#Event): A map mapping the most recent Event for each Control.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the most recent Event for each Control.
recent_events, err := myController.Events(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{< /tabs >}}

### TriggerEvent

Directly send an [Event Object](#event-object) from external code.

{{% alert title="Support Notice" color="note" %}}
This method is currently only supported for input controllers of model `webgamepad`.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `event` ([viam.components.input.input.Event](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.Event)) (required): The event to trigger.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Define a "Button is Pressed" event for the control BUTTON_START.
button_is_pressed_event = Event(
    time(), EventType.BUTTON_PRESS, Control.BUTTON_START, 1.0)

# Trigger the event on your controller. Set this trigger to timeout if it has
# not completed in 7 seconds.
await myController.trigger_event(event=my_event, timeout=7.0)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.trigger_event).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `event` [(Event)](https://pkg.go.dev/go.viam.com/rdk/components/input#Event): The `Event` to trigger on the controller.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Triggerable).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the input controller in its current configuration, in the [frame](/services/frame-system/) of the input controller.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_geometries).

{{% /tab %}}
{{< /tabs >}}

### RegisterControlCallback

Defines a callback function to execute whenever one of the [EventTypes](#eventtype-field) selected occurs on the given [Control](#control-field).

You can only register one callback function per [Event](#event-object) for each [Control](#control-field).
A second call to register a callback function for a [EventType](#eventtype-field) on a [Control](#control-field) replaces any function that was already registered.

You can pass a `nil` function here to "deregister" a callback.

{{% alert title="Tip" color="tip" %}}
Registering a callback for the `ButtonChange` [EventType](#eventtype-field) is merely a convenience for filtering.
Doing so registers the same callback to both `ButtonPress` and `ButtonRelease`, but `ButtonChange` is not reported in an actual [Event Object](#event-object).
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `control` ([viam.components.input.input.Control](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.Control)) (required): The control to register the function for.
- `triggers` ([List[viam.components.input.input.EventType]](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.EventType)) (required): The events that will trigger the function.
- `function` (viam.components.input.input.ControlFunction) (optional): The function to run on specific triggers.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Define a function to handle pressing the Start Menu Button "BUTTON_START" on
# your controller, printing out the start time.
def print_start_time(event):
    print(f"Start Menu Button was pressed at this time: {event.time}")


# Define a function that handles the controller.
async def handle_controller(controller):
    # Get the list of Controls on the controller.
    controls = await controller.get_controls()

    # If the "BUTTON_START" Control is found, register the function
    # print_start_time to fire when "BUTTON_START" has the event "ButtonPress"
    # occur.
    if Control.BUTTON_START in controls:
        controller.register_control_callback(
            Control.BUTTON_START, [EventType.BUTTON_PRESS], print_start_time)
    else:
        print("Oops! Couldn't find the start button control! Is your "
            "controller connected?")
        exit()

    while True:
        await asyncio.sleep(1.0)


async def main():
    # ... < INSERT CONNECTION CODE FROM MACHINE'S CODE SAMPLE TAB >

    # Get your controller from the machine.
    my_controller = Controller.from_robot(
        robot=myRobotWithController, name="my_controller")

    # Run the handleController function.
    await handleController(my_controller)

    # ... < INSERT ANY OTHER CODE FOR MAIN FUNCTION >
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.register_control_callback).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `control` [(Control)](https://pkg.go.dev/go.viam.com/rdk/components/input#Control): The [Control](#control-field) to register the function for.
- `triggers` [([]EventType)](https://pkg.go.dev/go.viam.com/rdk/components/input#EventType): The [EventTypes](#eventtype-field) that trigger the function.
- `ctrlFunc` [(ControlFunction)](https://pkg.go.dev/go.viam.com/rdk/components/input#ControlFunction): The function to run when the specified triggers are invoked.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Define a function to handle pressing the Start Menu button, "ButtonStart", on your controller and logging the start time
printStartTime := func(ctx context.Context, event input.Event) {
    logger.Info("Start Menu Button was pressed at this time: %v", event.Time)
}

// Define the EventType "ButtonPress" to serve as the trigger for printStartTime.
triggers := []input.EventType{input.ButtonPress}

// Get the controller's Controls.
controls, err := controller.Controls(ctx, nil)

// If the "ButtonStart" Control is found, trigger printStartTime when "ButtonStart" the event "ButtonPress" occurs.
if !slices.Contains(controls, input.ButtonStart) {
    return errors.New("button `ButtonStart` not found; controller may be disconnected")
}
Mycontroller.RegisterControlCallback(context.Background(), input.ButtonStart, triggers, printStartTime, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own input controller and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
