### StopAll

{{< tabs >}}
{{% tab name="Python" %}}

Cancel all current and outstanding operations for the robot and stop all actuators and movement.

**Parameters:**

- `extra` [(Mapping[str, Any])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName) (required): Extra options to pass to the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

``` python {class="line-numbers linkable-line-numbers"}
# Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stop_all()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[StopExtraParameters](https://flutter.viam.dev/viam_protos.robot.robot/StopExtraParameters-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/stopAll.html).

{{% /tab %}}
{{< /tabs >}}
