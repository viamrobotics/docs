### MoveToPosition

{{< tabs >}}
{{% tab name="Python" %}}

Move the end of the arm to the Pose specified in pose.

**Parameters:**

- `pose` [(viam.components.arm.Pose)](<INSERT PARAM TYPE LINK>) (required): The destination Pose for the arm.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_position).

``` python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose.
await my_arm.move_to_position(pose=examplePose)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `pose`[(Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/spatialmath#Pose):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `to` [(Pose)](https://flutter.viam.dev/viam_sdk/Pose-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/moveToPosition.html).

{{% /tab %}}
{{< /tabs >}}
