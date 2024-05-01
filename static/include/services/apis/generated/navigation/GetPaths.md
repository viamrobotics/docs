### GetPaths

{{< tabs >}}
{{% tab name="Python" %}}

Get each path, the series of geo points the robot plans to travel through to get to a destination waypoint, in the machine’s motion planning.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[viam.proto.service.navigation.Path])](INSERT RETURN TYPE LINK): An array comprised of Paths, where each path is either a user-provided destination or a Waypoint, along with the corresponding set of geopoints. This outlines the route the machine is expected to take to reach the specified destination or Waypoint.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_paths).

``` python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each path stored by the navigation service
paths = await my_nav.get_paths()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Path)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getPaths.html).

{{% /tab %}}
{{< /tabs >}}
