### SetPower

{{< tabs >}}
{{% tab name="Python" %}}

Sets the “percentage” of power the motor should employ between -1 and 1. When power is negative, the rotation will be in the backward direction.

**Parameters:**

- `power` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Power between -1 and 1 (negative implies backwards).
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.set_power).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the power to 40% forwards.
await my_motor.set_power(power=0.4)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `powerPct`[(float64)](https://pkg.go.dev/builtin#float64):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `powerPct` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/setPower.html).

{{% /tab %}}
{{< /tabs >}}
