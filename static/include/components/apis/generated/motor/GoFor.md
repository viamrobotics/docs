### GoFor

{{< tabs >}}
{{% tab name="Python" %}}

Spin the motor the specified number of revolutions at specified rpm. When rpm or revolutions is a negative value, the rotation will be in the backward direction. Note: if both rpm and revolutions are negative, the motor will spin in the forward direction.

**Parameters:**

- `rpm` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Speed at which the motor should move in rotations per minute (negative implies backwards).
- `revolutions` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Number of revolutions the motor should run for (negative implies backwards).
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.go_for).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor 7.2 revolutions at 60 RPM.
await my_motor.go_for(rpm=60, revolutions=7.2)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- [(rpm)](<INSERT PARAM TYPE LINK>):
- `revolutions` [(float64)](https://pkg.go.dev/builtin#float64):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `revolutions` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `rpm` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/goFor.html).

{{% /tab %}}
{{< /tabs >}}
