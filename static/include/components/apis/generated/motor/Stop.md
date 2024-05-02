### Stop

{{< tabs >}}
{{% tab name="Python" %}}

Stop the motor immediately, without any gradual step down.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.stop).

``` python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Stop the motor.
await my_motor.stop()
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.motor/MotorServiceClient/stop.html).

{{% /tab %}}
{{< /tabs >}}
