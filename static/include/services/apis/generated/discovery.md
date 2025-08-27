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
