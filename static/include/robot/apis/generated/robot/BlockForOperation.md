### BlockForOperation

{{< tabs >}}
{{% tab name="Python" %}}

Blocks on the specified operation on the robot. This function will only return when the specific operation has finished or has been cancelled.

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of operation to block on.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.block_for_operation).

``` python {class="line-numbers linkable-line-numbers"}
await robot.block_for_operation("INSERT OPERATION ID")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/blockForOperation.html).

{{% /tab %}}
{{< /tabs >}}
