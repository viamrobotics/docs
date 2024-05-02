### MoveToJointPositions

{{< tabs >}}
{{% tab name="Python" %}}

Move each joint on the arm to the corresponding angle specified in positions.

**Parameters:**

- `positions` [(viam.proto.component.arm.JointPositions)](https://python.viam.dev/autoapi/viam/../proto/component/arm/index.html#viam.proto.component.arm.JointPositions) (required): The destination JointPositions for the arm.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_joint_positions).

``` python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Declare a list of values with your desired rotational value for each joint on
# the arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.
jointPos = arm.move_to_joint_positions(
    JointPositions(values=[0.0, 45.0, 0.0, 0.0, 0.0]))

# Move each joint of the arm to the position these values specify.
await my_arm.move_to_joint_positions(positions=jointPos)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `pb`[(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `positions` [(JointPositions)](https://flutter.viam.dev/viam_protos.component.arm/JointPositions-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/moveToJointPositions.html).

{{% /tab %}}
{{< /tabs >}}
