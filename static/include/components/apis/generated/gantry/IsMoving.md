### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the gantry is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the gantry is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the
# gantry stops immediately.
await my_gantry.stop()

# Print if the gantry is currently moving.
print(my_gantry.is_moving())
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.gantry/GantryServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
