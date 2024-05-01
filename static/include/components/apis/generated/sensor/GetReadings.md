### GetReadings

{{< tabs >}}
{{% tab name="Python" %}}

Obtain the measurements/data specific to this sensor.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(Mapping[str, viam.utils.SensorReading])](INSERT RETURN TYPE LINK): The measurements. Can be of any type.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/client/index.html#viam.components.sensor.client.SensorClient.get_readings).

``` python {class="line-numbers linkable-line-numbers"}
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.sensor/SensorServiceClient/getReadings.html).

{{% /tab %}}
{{< /tabs >}}
