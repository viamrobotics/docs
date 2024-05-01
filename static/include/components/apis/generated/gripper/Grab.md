### Grab

{{< tabs >}}
{{% tab name="Python" %}}

Instruct the gripper to grab.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Indicates if the gripper grabbed something.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.grab).

``` python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Grab with the gripper.
grabbed = await my_gripper.grab()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gripper/GripperServiceClient/grab.html).

{{% /tab %}}
{{< /tabs >}}
