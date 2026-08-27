### ListUUIDs

List all world state transform UUIDs.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)])

**Example:**

```python {class="line-numbers linkable-line-numbers"}
worldstatestore = WorldStateStoreClient.from_robot(robot=machine, name="builtin")

uuids = await worldstatestore.list_uuids()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.list_uuids).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([][]byte)](https://pkg.go.dev/builtin#byte)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// List the world state uuids of a WorldStateStore Service.
uuids, err := myWorldStateStoreService.ListUUIDs(ctx, nil)
if err != nil {
  logger.Fatal(err)
}
// Print out the world state
for _, uuid := range uuids {
  fmt.Printf("UUID: %v", uuid)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/worldstatestore#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional): Additional arguments to the method.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<string[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const worldStateStore = new VIAM.WorldStateStoreClient(machine, 'builtin');

// Get all transform UUIDs
const uuids = await worldStateStore.listUUIDs();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#listuuids).

{{% /tab %}}
{{< /tabs >}}

### GetTransform

Get a world state transform by UUID.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `uuid` ([bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)) (required): The UUID of the transform to retrieve.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.common.Transform](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform))

**Example:**

```python {class="line-numbers linkable-line-numbers"}
worldstatestore = WorldStateStoreClient.from_robot(robot=machine, name="builtin")

transform = await worldstatestore.get_transform(uuid=b"some-uuid")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.get_transform).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `uuid` [([]byte)](https://pkg.go.dev/builtin#byte)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*commonpb.Transform)](https://pkg.go.dev/go.viam.com/api/common/v1#Transform)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the transform by uuid.
obj, err := myWorldStateStoreService.GetTransform(ctx, myUUID, nil)
if err != nil {
  logger.Fatal(err)
}
// Print out the transform.
fmt.Printf("Name: %v\nPose: %+v\nMetadata: %+v\nGeometry: %+v", obj.Name, obj.Pose, obj.Metadata, obj.Geometry)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/worldstatestore#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `uuid` (string) (required): The UUID of the transform to retrieve.
- `extra` (None) (optional): Additional arguments to the method.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[TransformWithUUID](https://ts.viam.dev/interfaces/TransformWithUUID.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const worldStateStore = new VIAM.WorldStateStoreClient(machine, 'builtin');

// Get a specific transform by UUID
const transform = await worldStateStore.getTransform(uuid);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#gettransform).

{{% /tab %}}
{{< /tabs >}}

### StreamTransformChanges

Stream changes to world state transforms.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([AsyncGenerator[viam.proto.service.worldstatestore.StreamTransformChangesResponse, None]](https://python.viam.dev/autoapi/viam/proto/service/worldstatestore/index.html#viam.proto.service.worldstatestore.StreamTransformChangesResponse))

**Example:**

```python {class="line-numbers linkable-line-numbers"}
worldstatestore = WorldStateStoreClient.from_robot(robot=machine, name="builtin")

async for change in worldstatestore.stream_transform_changes():
    print(f"Transform {change.transform.uuid} {change.change_type}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.stream_transform_changes).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*TransformChangeStream)](https://pkg.go.dev/go.viam.com/rdk/services/worldstatestore#TransformChangeStream)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
changes, err := myWorldStateStoreService.StreamTransformChanges(ctx, nil)
if err != nil {
  logger.Fatal(err)
}
for {
  change, err := changes.Next()
  if err == io.EOF {
    break
  }
  if err != nil {
    logger.Fatal(err)
  }
  fmt.Printf("Change: %v\n", change)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/worldstatestore#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional): Additional arguments to the method.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (AsyncGenerator<[TransformChangeEvent](https://ts.viam.dev/types/TransformChangeEvent.html), void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const worldStateStore = new VIAM.WorldStateStoreClient(machine, 'builtin');

// Stream transform changes
const stream = worldStateStore.streamTransformChanges();
for await (const change of stream) {
  console.log('Transform change:', change.changeType, change.transform);
}
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#streamtransformchanges).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own vision service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes])

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_world_state_store_svc = World_State_StoreClient.from_robot(robot=machine, "my_world_state_store_svc")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

await my_world_state_store_svc.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.do_command).

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
myWorldStateStoreSvc, err := worldstatestore.FromProvider(machine, "my_world_state_store_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myWorldStateStoreSvc.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute. Accepts either a [Struct](https://ts.viam.dev/classes/Struct.html) or a plain object,
  which will be converted automatically.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
// Plain object (recommended)
const result = await resource.doCommand({
  myCommand: { key: 'value' },
});

// Struct (still supported)
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(Struct.fromJson({ myCommand: { key: 'value' } }));
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetStatus

Get the current status of the world state store service as a map of key-value pairs describing its state.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): :   The status of the service.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
status = await service.get_status()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStoreClient.get_status).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myWorldStateStoreSvc, err := worldstatestore.FromProvider(machine, "my_world_state_store_svc")

status, err := myWorldStateStoreSvc.Status(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#getstatus).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the ResourceName for this Resource with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): :   The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_world_state_store_svc_name = WorldStateStoreClient.get_resource_name("my_world_state_store_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myWorldStateStoreSvc, err := worldstatestore.FromProvider(machine, "my_world_state_store_svc")

err = myWorldStateStoreSvc.Name()
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
world_state_store.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/WorldStateStoreClient.html#name).

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
my_world_state_store_svc = World_State_StoreClient.from_robot(robot=machine, name="my_world_state_store_svc")
await my_world_state_store_svc.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/worldstatestore/index.html#viam.services.worldstatestore.WorldStateStore.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myWorldStateStoreSvc, err := worldstatestore.FromProvider(machine, "my_world_state_store_svc")

err = myWorldStateStoreSvc.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
