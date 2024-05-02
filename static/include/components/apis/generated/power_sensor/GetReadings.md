### GetReadings

{{< tabs >}}
{{% tab name="Python" %}}

Obtain the measurements/data specific to this sensor. If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, viam.utils.SensorReading])](INSERT RETURN TYPE LINK):  The readings for the PowerSensor. Can be of any type. Includes voltage in volts (float), current inamperes (float), is_ac (bool), and power in watts (float).   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_readings).

``` python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_power_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.powersensor/PowerSensorServiceClient/getReadings.html).

{{% /tab %}}
{{< /tabs >}}
