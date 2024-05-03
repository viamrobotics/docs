### GetPosition

{{< tabs >}}
{{% tab name="Python" %}}

Report the position of the encoder. The value returned is the current position in terms of it’s position_type. The position will be either in relative units (ticks away from a zero position) for PositionType.TICKS or absolute units (degrees along a circle) for PositionType.DEGREES.

**Parameters:**

- `position_type` [(viam.proto.component.encoder.PositionType.ValueType)](<INSERT PARAM TYPE LINK>) (optional): The desired output type of the position
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Tuple[float, viam.proto.component.encoder.PositionType.ValueType])](INSERT RETURN TYPE LINK):  A tuple containing two values; the first [0] the Position of the encoder which can either beticks since last zeroing for a relative encoder or degrees for an absolute encoder, and the second [1] the type of position the encoder returns (ticks or degrees).   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_position).

``` python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get the position of the encoder in ticks
position = await my_encoder.get_position(encoder.PositionTypeTicks)
print("The encoder position is currently ", position[0], position[1])
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `positionType` [(PositionType)](https://pkg.go.dev#PositionType):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64):
- [(PositionType)](https://pkg.go.dev#PositionType):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `positionType` [(PositionType)](https://flutter.viam.dev/viam_protos.component.encoder/PositionType-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.encoder/EncoderServiceClient/getPosition.html).

{{% /tab %}}
{{< /tabs >}}
