### GetPosition

Get the current position of the encoder in ticks or degrees.
Relative encoders return ticks since last zeroing.
Absolute encoders return degrees.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `position_type` ([viam.proto.component.encoder.PositionType.ValueType](https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType)) (optional): The desired output type of the position.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [PositionType.ValueType](https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType)]): A tuple containing two values; the first \[0] the position of the encoder which can either be
ticks since last zeroing for a relative encoder or degrees for an absolute encoder, and the second \[1] the type of
position the encoder returns (ticks or degrees).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name='my_encoder')

# Get the position of the encoder in ticks
position = await my_encoder.get_position(PositionType.POSITION_TYPE_TICKS_COUNT)
print("The encoder position is currently ", position[0], position[1])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positionType` [(PositionType)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#PositionType): Specify whether to get the current position in ticks (encoder.PositionTypeTicks) or in degrees (`encoder.PositionTypeDegrees`). If you are not sure which position type your encoder supports but it is a built-in Viam-supported model, you can leave this parameter unspecified (`encoder.PositionTypeUnspecified`) and it will default to the correct position type.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The current position (measured in ticks or degrees).
- [(PositionType)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#PositionType): The type of position the encoder returns (ticks or degrees).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(machine, "my_encoder")
if err != nil {
  logger.Fatalf("cannot get encoder: %v", err)
}

// Get the position of the encoder in ticks
position, posType, err := myEncoder.Position(context.Background(), encoder.PositionTypeTicks, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `positionType` ([PositionType](https://ts.viam.dev/enums/encoderApi.PositionType.html)) (optional): The type of position the encoder returns (ticks or
  degrees).
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<readonly [number, [PositionType](https://ts.viam.dev/enums/encoderApi.PositionType.html)]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const encoder = new VIAM.EncoderClient(machine, 'my_encoder');

// Get the position of the encoder in ticks
const [position, posType] = await encoder.getPosition(
  EncoderPositionType.POSITION_TYPE_TICKS_COUNT
);
console.log('The encoder position is currently', position, posType);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/EncoderClient.html#getposition).

{{% /tab %}}
{{< /tabs >}}

### ResetPosition

Set the current position of the encoder to be the new zero position.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name='my_encoder')

# Reset the zero position of the encoder.
await my_encoder.reset_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.reset_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(machine, "my_encoder")
if err != nil {
  logger.Fatalf("cannot get encoder: %v", err)
}

err = myEncoder.ResetPosition(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const encoder = new VIAM.EncoderClient(machine, 'my_encoder');

// Reset the zero position of the encoder
await encoder.resetPosition();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/EncoderClient.html#resetposition).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get a list of all the position types that are supported by a given encoder.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.encoder.encoder.Encoder.Properties](https://python.viam.dev/autoapi/viam/components/encoder/encoder/index.html#viam.components.encoder.encoder.Encoder.Properties)): Map of position types to supported status.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name='my_encoder')

# Get whether the encoder returns position in ticks or degrees.
properties = await my_encoder.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Properties): The position types supported by the encoder model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(machine, "my_encoder")

// Get whether the encoder returns position in ticks or degrees.
properties, err := myEncoder.Properties(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[encoderApi](https://ts.viam.dev/modules/encoderApi.html).[GetPropertiesResponse](https://ts.viam.dev/classes/encoderApi.GetPropertiesResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const encoder = new VIAM.EncoderClient(machine, 'my_encoder');

// Get whether the encoder returns position in ticks or degrees
const properties = await encoder.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/EncoderClient.html#getproperties).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the encoder in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the encoder.
The [motion](/operate/reference/services/motion/) and [navigation](/operate/reference/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name="my_encoder")
geometries = await my_encoder.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_geometries).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own encoder as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name="my_encoder")
command = {"cmd": "test", "data1": 500}
result = await my_encoder.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(machine, "my_encoder")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myEncoder.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(
  Struct.fromJson({
    myCommand: { key: 'value' },
  })
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/EncoderClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this encoder with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder_name = Encoder.get_resource_name("my_encoder")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_resource_name).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=machine, name="my_encoder")
await my_encoder.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(machine, "my_encoder")

err = myEncoder.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
