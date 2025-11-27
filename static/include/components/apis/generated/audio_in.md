### GetAudio

Get a stream of audio from the device.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `codec` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The desired codec of the returned audio data.
- `duration_seconds` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): duration of the stream. 0 = indefinite stream.
- `previous_timestamp_ns` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): starting timestamp in nanoseconds for recording continuity.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_in = AudioIn.from_robot(robot=machine, name="my_audio_in")

stream = await my_audio_in.get_audio(
    codec=AudioCodec.PCM16,
    duration_seconds=10.0,
    previous_timestamp_ns=0
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.get_audio).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `codec` [(string)](https://pkg.go.dev/builtin#string)
- `durationSeconds` [(float32)](https://pkg.go.dev/builtin#float32)
- `previousTimestampNs` [(int64)](https://pkg.go.dev/builtin#int64)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `chan` [(*AudioChunk)](https://pkg.go.dev/go.viam.com/rdk/components/audioin#AudioChunk)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/audioin#AudioIn).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `codec` (string) (required)
- `durationSeconds` (number) (required)
- `previousTimestamp` (bigint) (optional)
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (AsyncIterable<[AudioChunk](https://ts.viam.dev/interfaces/AudioChunk.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const audioIn = new VIAM.AudioInClient(machine, 'my_audio_in');
const stream = audioIn.getAudio(VIAM.AudioCodec.PCM16, 3, 0n, {});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioInClient.html#getaudio).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `codec` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (optional)
- `durationSeconds` [double](https://api.flutter.dev/flutter/dart-core/double-class.html)? (optional)
- `previousTimestampNanoseconds` [Int64](https://pub.dev/documentation/fixnum/1.1.1/fixnum/Int64-class.html)? (optional)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Stream](https://api.flutter.dev/flutter/dart-async/Stream-class.html)\<[GetAudioResponse](https://flutter.viam.dev/viam_protos.component.audioin/GetAudioResponse-class.html)\>

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioInClient/getAudio.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the audio device’s properties.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.components.audio_in.audio_in.AudioIn.Properties): The properties of the audio in device.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_in = AudioIn.from_robot(robot=machine, name="my_audio_in")
properties = await my_audio_in.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(utils.Properties)](https://pkg.go.dev/go.viam.com/rdk/utils#Properties)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/audioin#AudioIn).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise< { numChannels: number; sampleRateHz: number; supportedCodecs: string[] },>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const audioIn = new VIAM.AudioInClient(machine, 'my_audio_in');
const properties = await audioIn.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioInClient.html#getproperties).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[GetPropertiesResponse](https://flutter.viam.dev/viam_protos.common.common/GetPropertiesResponse-class.html)\>

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioInClient/getProperties.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the audio in component in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the audio in component.
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
my_audio_in = AudioIn.from_robot(robot=machine, name="my_audio_in")
geometries = await my_audio_in.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.get_geometries).

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
If you are implementing your own arm and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

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
my_audio_in = AudioIn.from_robot(robot=machine, name="my_audio_in")
command = {"cmd": "test", "data1": 500}
result = await my_audio_in.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.do_command).

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
myAudioIn, err := audio_in.FromProvider(machine, "my_audio_in")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myAudioIn.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioInClient.html#docommand).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioInClient/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this audio in component.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_in_name = AudioIn.get_resource_name("my_audio_in")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myAudioIn, err := audioin.FromProvider(machine, "my_audio_in")

err = myAudioIn.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (string): The name of the resource.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
audio_in.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioInClient.html#name).

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
my_audio_in = AudioIn.from_robot(robot=machine, name="my_audio_in")
await my_audio_in.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_in/client/index.html#viam.components.audio_in.client.AudioInClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myAudioIn, err := audioin.FromProvider(machine, "my_audio_in")

err = myAudioIn.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
