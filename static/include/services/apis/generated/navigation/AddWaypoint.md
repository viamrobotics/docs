### AddWaypoint

{{< tabs >}}
{{% tab name="Python" %}}

Add a waypoint to the service’s data storage.

**Parameters:**

- `point` [(viam.services.navigation.GeoPoint)](<INSERT PARAM TYPE LINK>) (required): The current location of the robot in the navigation service, represented in a GeoPoint with latitude and longitude values.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.add_waypoint).

``` python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

 # Create a new waypoint with latitude and longitude values of 0 degrees
 location = GeoPoint(latitude=0, longitude=0)


 # Add your waypoint to the service's data storage
 await my_nav.add_waypoint(point=location)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `geo` [(Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `location` [(GeoPoint)](https://flutter.viam.dev/viam_sdk/GeoPoint-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.navigation/NavigationServiceClient/addWaypoint.html).

{{% /tab %}}
{{< /tabs >}}
