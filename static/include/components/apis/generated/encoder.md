### GetPosition

Get the current position of the encoder in ticks or degrees.
Relative encoders return ticks since last zeroing.
Absolute encoders return degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `position_type` ([PositionType.ValueType](https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType)) (optional): The desired output type of the position.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [PositionType.ValueType](https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType)]): A tuple containing two values; the first [0] the Position of the encoder which can either be ticks since last zeroing for a relative encoder or degrees for an absolute encoder, and the second [1] the type of position the encoder returns (ticks or degrees).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get the position of the encoder in ticks
position = await my_encoder.get_position(encoder.PositionTypeTicks)
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
{{< /tabs >}}

### ResetPosition

Set the current position of the encoder to be the new zero position.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

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
{{< /tabs >}}

### GetProperties

Get a list of all the position types that are supported by a given encoder.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.encoder.encoder.Encoder.Properties](https://python.viam.dev/autoapi/viam/components/encoder/encoder/index.html#viam.components.encoder.encoder.Encoder.Properties)): Map of position types to supported status.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

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
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the encoder in its current configuration, in the [frame](/services/frame-system/) of the encoder.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

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
If you are implementing your own encoder as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} and are adding features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
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
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

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
await component.close()
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
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
