### RemoveWaypoint

{{< tabs >}}
{{% tab name="Python" %}}

Remove a waypoint from the service’s data storage. If the robot is currently navigating to this waypoint, the motion will be canceled, and the robot will proceed to the next waypoint.

**Parameters:**

- `id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The MongoDB ObjectID of the Waypoint to remove from the service’s data storage.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.remove_waypoint).

``` python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Remove the waypoint matching that ObjectID from the service's data storage
await my_nav.remove_waypoint(waypoint_id)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `id`[(ObjectID)](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#ObjectID):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/removeWaypoint.html).

{{% /tab %}}
{{< /tabs >}}
