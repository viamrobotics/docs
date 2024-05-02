### RegisterControlCallback

{{< tabs >}}
{{% tab name="Python" %}}

Register a function that will fire on given EventTypes for a given Control

**Parameters:**

- `control` [(viam.components.input.input.Control)](<INSERT PARAM TYPE LINK>) (required): The control to register the function for
- `triggers` [(List[viam.components.input.input.EventType])](<INSERT PARAM TYPE LINK>) (required): The events that will trigger the function
- `function` [(viam.components.input.input.ControlFunction)](<INSERT PARAM TYPE LINK>) (optional): The function to run on specific triggers
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.register_control_callback).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `control`[(Control)](https://pkg.go.dev#Control):
- [(EventType)](https://pkg.go.dev#EventType):
- `ctrlFunc`[(ControlFunction)](https://pkg.go.dev#ControlFunction):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{< /tabs >}}
