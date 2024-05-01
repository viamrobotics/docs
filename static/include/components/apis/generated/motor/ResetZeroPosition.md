### ResetZeroPosition

{{< tabs >}}
{{% tab name="Python" %}}

Set the current position (modified by offset) to be the new zero (home) position.

**Parameters:**

- `offset` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The offset from the current position to new home/zero position.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.reset_zero_position).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the current position as the new home position with no offset.
await my_motor.reset_zero_position(offset=0.0)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `offset`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `name` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):
- `offset` [(double)](https://api.flutter.dev/flutter/dart-core/double-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/resetZeroPosition.html).

{{% /tab %}}
{{< /tabs >}}
