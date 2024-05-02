### Stop

{{< tabs >}}
{{% tab name="Python" %}}

Stop the gripper. It is assumed the gripper stops immediately.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.stop).

``` python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Stop the gripper.
await my_gripper.stop()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gripper/GripperServiceClient/stop.html).

{{% /tab %}}
{{< /tabs >}}
