### DiscoverComponents

{{< tabs >}}
{{% tab name="Python" %}}

Get the list of discovered component configurations.

**Parameters:**

- `queries` [(List[viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery) (required): The list of component models to lookup configurations for.

**Returns:**

- [(List[viam.proto.robot.Discovery])](INSERT RETURN TYPE LINK): A list of discovered component configurations.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components).

``` python {class="line-numbers linkable-line-numbers"}
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `resource`[(DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/resource#DiscoveryQuery):

**Returns:**

- `resource`[(Discovery)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/resource#Discovery):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `queries` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[DiscoveryQuery](https://flutter.viam.dev/viam_protos.robot.robot/DiscoveryQuery-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/discoverComponents.html).

{{% /tab %}}
{{< /tabs >}}
