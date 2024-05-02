### Stop

{{< tabs >}}
{{% tab name="Python" %}}

Stop the servo. It is assumed that the servo stops immediately.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.stop).

``` python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Stop the servo. It is assumed that the servo stops moving immediately.
await my_servo.stop()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.servo/ServoServiceClient/stop.html).

{{% /tab %}}
{{< /tabs >}}
