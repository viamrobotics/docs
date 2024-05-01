### GetJointPositions

{{< tabs >}}
{{% tab name="Python" %}}

Get the JointPositions representing the current position of the arm.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(viam.proto.component.arm.JointPositions)](INSERT RETURN TYPE LINK): The current JointPositions for the arm.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_joint_positions).

``` python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the current position of each joint on the arm as JointPositions.
pos = await my_arm.get_joint_positions()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `pb`[(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#pb):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/getJointPositions.html).

{{% /tab %}}
{{< /tabs >}}
