### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the arm is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the arm is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(my_arm.is_moving())
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
