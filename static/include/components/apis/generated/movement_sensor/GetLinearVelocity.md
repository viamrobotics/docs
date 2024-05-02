### GetLinearVelocity

{{< tabs >}}
{{% tab name="Python" %}}

Get the current linear velocity as a Vector3 with x, y, and z axes represented in m/sec

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.components.movement_sensor.Vector3)](INSERT RETURN TYPE LINK): The linear velocity in m/sec

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_linear_velocity).

``` python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear velocity of the movement sensor.
lin_vel = await my_movement_sensor.get_linear_velocity()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `r3`[(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.movementsensor/MovementSensorServiceClient/getLinearVelocity.html).

{{% /tab %}}
{{< /tabs >}}
