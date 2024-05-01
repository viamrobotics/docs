### IsPowered

{{< tabs >}}
{{% tab name="Python" %}}

Returns whether or not the motor is currently running.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(Tuple[bool, float])](INSERT RETURN TYPE LINK):  A tuple containing two values; the first [0] value indicates whether the motor is currently powered, andthe second [1] value indicates the current power percentage of the motor.   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_powered).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently running.
powered = await my_motor.is_powered()

print('Powered: ', powered)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/isPowered.html).

{{% /tab %}}
{{< /tabs >}}
