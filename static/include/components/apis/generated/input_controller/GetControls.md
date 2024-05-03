### GetControls

{{< tabs >}}
{{% tab name="Python" %}}

Returns a list of Controls provided by the Controller

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.components.input.input.Control])](INSERT RETURN TYPE LINK): List of controls provided by the Controller

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_controls).

``` python {class="line-numbers linkable-line-numbers"}
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the list of Controls provided by the controller.
controls = await my_controller.get_controls()

# Print the list of Controls provided by the controller.
print(f"Controls: {controls}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Control)](https://pkg.go.dev#Control):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `controller` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.input_controller/InputControllerServiceClient/getControls.html).

{{% /tab %}}
{{< /tabs >}}
