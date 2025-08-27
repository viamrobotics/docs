### GetGeometries

Get all the geometries associated with the generic component in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the generic component.
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
my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")
geometries = await my_generic_component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.get_geometries).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[Geometry](https://ts.viam.dev/classes/commonApi.Geometry.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const generic = new VIAM.GenericComponentClient(
  machine,
  'my_generic_component'
);

// Get the geometries of this component
const geometries = await generic.getGeometries();
console.log('Geometries:', geometries);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GenericComponentClient.html#getgeometries).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands.
If you are implementing your own generic component and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")
command = {"cmd": "test", "data1": 500}
result = await my_generic_component.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.do_command).

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
myGenericComponent, err := generic.FromRobot(machine, "my_generic_component")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myGenericComponent.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GenericComponentClient.html#docommand).

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

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this generic component.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_generic_component_name = Generic.get_resource_name("my_generic_component")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGenericComponent, err := generic.FromRobot(machine, "my_generic_component")

err = myGenericComponent.Name()
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
generic_component.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GenericComponentClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myGenericResourceName = myGeneric.getResourceName("my_generic");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Generic/getResourceName.html).

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
my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")
await my_generic_component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.close).

{{% /tab %}}
{{< /tabs >}}
