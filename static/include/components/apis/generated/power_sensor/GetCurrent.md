### GetCurrent

{{< tabs >}}
{{% tab name="Python" %}}

Get the current reading and bool IsAC

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Tuple[float, bool])](INSERT RETURN TYPE LINK): current (amperes) and bool IsAC

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_current).

``` python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the current reading from the power sensor
current, is_ac = await my_power_sensor.get_current()
print("The current is ", current, " A, Is AC: ", is_ac)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64):
- [(bool)](https://pkg.go.dev/builtin#bool):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.powersensor/PowerSensorServiceClient/getCurrent.html).

{{% /tab %}}
{{< /tabs >}}
