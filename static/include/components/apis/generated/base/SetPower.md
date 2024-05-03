### SetPower

{{< tabs >}}
{{% tab name="Python" %}}

Set the linear and angular velocity of the Base When linear is 0, the the base will spin. When angular is 0, the the base will move in a straight line. When both linear and angular are 0, the base will stop. When linear and angular are both nonzero, the base will move in an arc, with a tighter radius if angular power is greater than linear power.

**Parameters:**

- `linear` [(viam.components.base.Vector3)](<INSERT PARAM TYPE LINK>) (required): The linear component. Only the Y component is used for wheeled base. Positive implies forwards.
- `angular` [(viam.components.base.Vector3)](<INSERT PARAM TYPE LINK>) (required): The angular component. Only the Z component is used for wheeled base. Positive turns left; negative turns right.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Make your wheeled base move forward. Set linear power to 75%.
print("move forward")
await my_base.set_power(
    linear=Vector3(x=0, y=-.75, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base move backward. Set linear power to -100%.
print("move backward")
await my_base.set_power(
    linear=Vector3(x=0, y=-1.0, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base spin left. Set angular power to 100%.
print("spin left")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=1))

# Make your wheeled base spin right. Set angular power to -75%.
print("spin right")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=-.75))
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

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/setPower.html).

{{% /tab %}}
{{< /tabs >}}
