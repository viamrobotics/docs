### GetReadings

{{< tabs >}}
{{% tab name="Python" %}}

Obtain the measurements/data specific to this sensor. If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, viam.utils.SensorReading])](INSERT RETURN TYPE LINK): The readings for the MovementSensor. Can be of any type.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_readings).

``` python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the latest readings from the movement sensor.
readings = await my_movement_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.movementsensor/MovementSensorServiceClient/getReadings.html).

{{% /tab %}}
{{< /tabs >}}
