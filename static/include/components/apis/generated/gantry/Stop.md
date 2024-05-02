### Stop

{{< tabs >}}
{{% tab name="Python" %}}

Stop all motion of the gantry. It is assumed that the gantry stops immediately.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.stop).

``` python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the gantry stops
# immediately.
await my_gantry.stop()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gantry/GantryServiceClient/stop.html).

{{% /tab %}}
{{< /tabs >}}
