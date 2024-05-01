### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the base is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the base is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Check whether the base is currently moving.
moving = await my_base.is_moving()
print('Moving: ', moving)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
