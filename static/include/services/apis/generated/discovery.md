### DiscoverResources

Get a list of component configs of all resources available to configure on a machine based on the hardware that is connected to or part of the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.app.robot.ComponentConfig]](https://python.viam.dev/autoapi/viam/proto/app/robot/index.html#viam.proto.app.robot.ComponentConfig)): A list of ComponentConfigs that describe
the components found by a discover service.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_discovery = DiscoveryClient.from_robot(machine, "my_discovery")

# Get the discovered resources
result = await my_discovery.discover_resources(
    "my_discovery",
)
discoveries = result.discoveries
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/discovery/client/index.html#viam.services.discovery.client.DiscoveryClient.discover_resources).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]resource.Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
  // Get the discovered resources of a Discovery Service.
  cfgs, err := myDiscoveryService.DiscoverResources(ctx, nil)
  if err != nil {
    logger.Fatal(err)
  }
   // Print out the discovered resources.
  for _, cfg := range cfgs {
    fmt.Printf("Name: %v\tModel: %v\tAPI: %v", cfg.Name, cfg.Model, cfg.API)
    fmt.Printf("Attributes: ", cfg.Attributes)
  }
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/discovery#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[ComponentConfig](https://ts.viam.dev/classes/appRobotApi.ComponentConfig.html)[]>): * The list of ComponentConfigs.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DiscoveryClient.html#discoverresources).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[ComponentConfig](https://flutter.viam.dev/viam_protos.app.robot/ComponentConfig-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var resources = await myDiscoveryService.discoverResources('myWebcam');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DiscoveryClient/discoverResources.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_discovery_svc_name = DiscoveryClient.get_resource_name("my_discovery_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/discovery/client/index.html#viam.services.discovery.client.DiscoveryClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myDiscoverySvc, err := discovery.FromRobot(machine, "my_discovery_svc")

err = myDiscoverySvc.Name()
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
discovery.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DiscoveryClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DiscoveryClient/getResourceName.html).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands.
If you are implementing your own generic service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_discovery_svc = DiscoveryClient.from_robot(robot=machine, "my_discovery_svc")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

await my_discovery_svc.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/discovery/client/index.html#viam.services.discovery.client.DiscoveryClient.do_command).

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
myDiscoverySvc, err := discovery.FromRobot(machine, "my_discovery_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myDiscoverySvc.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/DiscoveryClient.html#docommand).

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

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/DiscoveryClient/doCommand.html).

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
my_discovery_svc = DiscoveryClient.from_robot(robot=machine, name="my_discovery_svc")
await my_discovery_svc.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/discovery/client/index.html#viam.services.discovery.client.DiscoveryClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myDiscoverySvc, err := discovery.FromRobot(machine, "my_discovery_svc")

err = myDiscoverySvc.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
