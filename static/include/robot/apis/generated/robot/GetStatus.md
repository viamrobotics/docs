### GetStatus

{{< tabs >}}
{{% tab name="Python" %}}

Get the status of the robot’s components. You can optionally provide a list of ResourceName for which you want statuses.

**Parameters:**

- `components` [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName) (optional): Optional list of ResourceName for components you want statuses.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

``` python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the machine.
statuses = await robot.get_status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `resource` [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/resource#Name):

**Returns:**

- [(Status)](https://pkg.go.dev#Status):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `resourceNames` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/getStatus.html).

{{% /tab %}}
{{< /tabs >}}
