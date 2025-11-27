### Play

Play the given audio data.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `data` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): audio bytes to play.
- `info` (viam.components.audio_out.audio_out.AudioInfo) (optional): (optional) information about the audio data such as codec, sample rate, and channel count.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_out = AudioOut.from_robot(robot=machine, name="my_audio_out")

# With audio info
audio_info = AudioInfo(codec=AudioCodec.PCM16, sample_rate_hz=44100, num_channels=2)
await my_audio_out.play(audio_data, audio_info)

# Without audio info (when codec encodes information within audio_data)
await my_audio_out.play(audio_data)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.play).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `data` [([]byte)](https://pkg.go.dev/builtin#byte)
- `info` [(*utils.AudioInfo)](https://pkg.go.dev/go.viam.com/rdk/utils#AudioInfo)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/audioout#AudioOut).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `audioData` (Uint8Array) (required): The audio data to play.
- `audioInfo` ([AudioInfo](https://ts.viam.dev/classes/commonApi.AudioInfo.html)) (optional): Information about the audio format (optional, required
  for raw pcm data).
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const audioOut = new VIAM.AudioOutClient(machine, 'my_audio_out');
const audioData = new Uint8Array([...]); // Your audio data
const audioInfo = { codec: 'pcm16', sampleRateHz: 48000, numChannels: 2 };
await audioOut.play(audioData, audioInfo);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioOutClient.html#play).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `audioData` [Uint8List](https://api.flutter.dev/flutter/dart-typed_data/Uint8List-class.html) (optional)
- `audioInfo` [AudioInfo](https://flutter.viam.dev/viam_protos.common.common/AudioInfo-class.html) (optional)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[PlayResponse](https://flutter.viam.dev/viam_protos.component.audioout/PlayResponse-class.html)\>

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioOutClient/play.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the audio device’s properties.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.components.audio_out.audio_out.AudioOut.Properties): The properties of the audio output device.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_out = AudioOut.from_robot(robot=machine, name="my_audio_out")
properties = await my_audio_out.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(utils.Properties)](https://pkg.go.dev/go.viam.com/rdk/utils#Properties)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/audioout#AudioOut).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise< { numChannels: number; sampleRateHz: number; supportedCodecs: string[] },>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const audioOut = new VIAM.AudioOutClient(machine, 'my_audio_out');
const properties = await audioOut.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioOutClient.html#getproperties).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[GetPropertiesResponse](https://flutter.viam.dev/viam_protos.common.common/GetPropertiesResponse-class.html)\>

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioOutClient/getProperties.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the audio out component in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the audio out component.
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
my_audio_out = AudioOut.from_robot(robot=machine, name="my_audio_out")
geometries = await my_audio_out.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.get_geometries).

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
my_audio_out = AudioOut.from_robot(robot=machine, name="my_audio_out")
command = {"cmd": "test", "data1": 500}
result = await my_audio_out.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.do_command).

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
myAudioOut, err := audio_out.FromProvider(machine, "my_audio_out")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myAudioOut.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioOutClient.html#docommand).

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

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/AudioOutClient/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this audio out component.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_audio_out_name = AudioOut.get_resource_name("my_audio_out")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myAudioOut, err := audioout.FromProvider(machine, "my_audio_out")

err = myAudioOut.Name()
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
audio_out.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/AudioOutClient.html#name).

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
my_audio_out = AudioOut.from_robot(robot=machine, name="my_audio_out")
await my_audio_out.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/audio_out/client/index.html#viam.components.audio_out.client.AudioOutClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myAudioOut, err := audioout.FromProvider(machine, "my_audio_out")

err = myAudioOut.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
