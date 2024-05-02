### FrameSystemConfig

{{< tabs >}}
{{% tab name="Python" %}}

Get the configuration of the [frame](/mobility/frame-system/) system of a given robot.

**Parameters:**

- `additional_transforms` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform) (optional):

**Returns:**

- [(List[viam.proto.robot.FrameSystemConfig])](INSERT RETURN TYPE LINK): The configuration of a given robot’s frame system.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

``` python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the machine.
frame_system = await robot.get_frame_system_config()
print(f"frame system configuration: {frame_system}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):

**Returns:**

- `framesystem`[(Config)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/robot/framesystem#Config):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `supplementalTransforms` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/frameSystemConfig.html).

{{% /tab %}}
{{< /tabs >}}
