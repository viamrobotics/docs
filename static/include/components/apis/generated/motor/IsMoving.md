### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the motor is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the motor is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently moving.
moving = await my_motor.is_moving()
print('Moving: ', moving)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
