### GetPosition

{{< tabs >}}
{{% tab name="Python" %}}

Get current position of the specified component in the SLAM Map.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.slam.Pose)](INSERT RETURN TYPE LINK): The current position of the specified component

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

``` python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the current position of the specified source component in the SLAM map as a Pose.
pose = await slam.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):

**Returns:**

- `spatialmath`[(Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/spatialmath#Pose):
- [(string)](https://pkg.go.dev/builtin#string):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getPosition.html).

{{% /tab %}}
{{< /tabs >}}
