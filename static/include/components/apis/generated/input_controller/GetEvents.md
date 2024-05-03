### GetEvents

{{< tabs >}}
{{% tab name="Python" %}}

Returns the most recent Event for each input (which should be the current state)

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Dict[viam.components.input.input.Control, viam.components.input.input.Event])](INSERT RETURN TYPE LINK): The most recent event for each input

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_events).

``` python {class="line-numbers linkable-line-numbers"}
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the most recent Event for each Control.
recent_events = await my_controller.get_events()

# Print out the most recent Event for each Control.
print(f"Recent Events: {recent_events}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `Control` [(Event)](https://pkg.go.dev#Event):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `controller` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.input_controller/InputControllerServiceClient/getEvents.html).

{{% /tab %}}
{{< /tabs >}}
