### Home

{{< tabs >}}
{{% tab name="Python" %}}

Home the gantry to find it’s starting and ending positions

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): whether the gantry has run the homing sequence successfully

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.home).

``` python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

await my_gantry.home()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gantry/GantryServiceClient/home.html).

{{% /tab %}}
{{< /tabs >}}
