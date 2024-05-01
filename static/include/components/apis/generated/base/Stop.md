### Stop

{{< tabs >}}
{{% tab name="Python" %}}

Stop the base.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.stop).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base forward 10 mm at a velocity of 50 mm/s.
await my_base.move_straight(distance=10, velocity=50)

# Stop the base.
await my_base.stop()

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/stop.html).

{{% /tab %}}
{{< /tabs >}}
