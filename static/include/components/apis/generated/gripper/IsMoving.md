### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the gripper is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the gripper is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Check whether the gripper is currently moving.
moving = await my_gripper.is_moving()
print('Moving:', moving)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gripper/GripperServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
