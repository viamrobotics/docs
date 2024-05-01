### GetLengths

{{< tabs >}}
{{% tab name="Python" %}}

Get the lengths of the axes of the gantry in millimeters.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[float])](INSERT RETURN TYPE LINK): The lengths of the axes.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_lengths).

``` python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await my_gantry.get_lengths()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gantry/GantryServiceClient/getLengths.html).

{{% /tab %}}
{{< /tabs >}}
