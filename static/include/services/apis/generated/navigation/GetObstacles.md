### GetObstacles

{{< tabs >}}
{{% tab name="Python" %}}

Get an array or list of the obstacles currently in the service’s data storage. These are objects designated for the robot to avoid when navigating. These include all transient obstacles which are discovered by the vision services configured for the navigation service, in addition to the obstacles that are configured as a part of the service.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.services.navigation.GeoObstacle])](INSERT RETURN TYPE LINK): A list comprised of each GeoObstacle in the service’s data storage. These are objects designated for the robot to avoid when navigating.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_obstacles).

``` python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each obstacle stored by the navigation service
obstacles = await my_nav.get_obstacles()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `spatialmath`[(GeoObstacle)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/spatialmath#GeoObstacle):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/getObstacles.html).

{{% /tab %}}
{{< /tabs >}}
