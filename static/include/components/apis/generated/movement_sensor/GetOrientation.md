### GetOrientation

{{< tabs >}}
{{% tab name="Python" %}}

Get the current orientation

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(viam.components.movement_sensor.Orientation)](INSERT RETURN TYPE LINK): The orientation

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_orientation).

``` python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current orientation vector of the movement sensor.
orientation = await my_movement_sensor.get_orientation()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `spatialmath`[(Orientation)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/spatialmath#spatialmath):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.movementsensor/MovementSensorServiceClient/getOrientation.html).

{{% /tab %}}
{{< /tabs >}}
