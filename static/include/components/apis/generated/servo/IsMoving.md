### IsMoving

{{< tabs >}}
{{% tab name="Python" %}}

Get if the servo is currently moving.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the servo is moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.is_moving).

``` python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

print(my_servo.is_moving())

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.servo/ServoServiceClient/isMoving.html).

{{% /tab %}}
{{< /tabs >}}
