### Move

{{< tabs >}}
{{% tab name="Python" %}}

Move the servo to the provided angle.

**Parameters:**

- `angle` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The desired angle of the servo in degrees.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.move).

``` python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Move the servo from its origin to the desired angle of 90 degrees.
await my_servo.move(90)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `angleDeg` [(uint32)](https://pkg.go.dev/builtin#uint32):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `angleDeg` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.servo/ServoServiceClient/move.html).

{{% /tab %}}
{{< /tabs >}}
