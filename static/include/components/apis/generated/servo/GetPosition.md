### GetPosition

{{< tabs >}}
{{% tab name="Python" %}}

Get the current angle (degrees) of the servo.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The current angle of the servo in degrees.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.get_position).

``` python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Get the current set angle of the servo.
pos1 = await my_servo.get_position()

# Move the servo from its origin to the desired angle of 20 degrees.
await my_servo.move(20)

# Get the current set angle of the servo.
pos2 = await my_servo.get_position()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint32)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.servo/ServoServiceClient/getPosition.html).

{{% /tab %}}
{{< /tabs >}}
