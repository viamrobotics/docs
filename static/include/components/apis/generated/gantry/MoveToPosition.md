### MoveToPosition

{{< tabs >}}
{{% tab name="Python" %}}

Move the gantry to a new position at the requested speeds.

**Parameters:**

- `positions` [(List[float])](<INSERT PARAM TYPE LINK>) (required): List of positions for the axes to move to, in millimeters.
- `speeds` [(List[float])](<INSERT PARAM TYPE LINK>) (required):
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.move_to_position).

``` python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Create a list of positions for the axes of the gantry to move to. Assume in
# this example that the gantry is multi-axis, with 3 axes.
examplePositions = [1, 2, 3]

exampleSpeeds = [3, 9, 12]

# Move the axes of the gantry to the positions specified.
await my_gantry.move_to_position(
    positions=examplePositions, speeds=exampleSpeeds)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- [(positionsMm)](<INSERT PARAM TYPE LINK>):
- [(float64)](https://pkg.go.dev/builtin#float64):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `positionsMm` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)> (required):
- `speedsMmPerSec` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gantry/GantryServiceClient/moveToPosition.html).

{{% /tab %}}
{{< /tabs >}}
