### SetMode

{{< tabs >}}
{{% tab name="Python" %}}

Set the Mode the service is operating in.

**Parameters:**

- `mode` [(viam.services.navigation.Mode.ValueType)](<INSERT PARAM TYPE LINK>) (required): The Mode for the service to operate in.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.set_mode).

``` python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `mode` [(Mode)](https://pkg.go.dev#Mode):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `mode` [(Mode)](https://flutter.viam.dev/viam_protos.service.navigation/Mode-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/setMode.html).

{{% /tab %}}
{{< /tabs >}}
