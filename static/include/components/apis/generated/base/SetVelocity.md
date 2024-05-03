### SetVelocity

{{< tabs >}}
{{% tab name="Python" %}}

Set the linear and angular velocities of the base.

**Parameters:**

- `linear` [(viam.components.base.Vector3)](<INSERT PARAM TYPE LINK>) (required): Velocity in mm/sec
- `angular` [(viam.components.base.Vector3)](<INSERT PARAM TYPE LINK>) (required): Velocity in deg/sec
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Set the linear velocity to 50 mm/sec and the angular velocity to
# 15 degree/sec.
await my_base.set_velocity(
    linear=Vector3(x=0, y=50, z=0), angular=Vector3(x=0, y=0, z=15))
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- [(linear)](<INSERT PARAM TYPE LINK>):
- `angular` [(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `angular` [(Vector3)](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `linear` [(Vector3)](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/setVelocity.html).

{{% /tab %}}
{{< /tabs >}}
