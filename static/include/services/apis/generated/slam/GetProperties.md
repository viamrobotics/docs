### GetProperties

{{< tabs >}}
{{% tab name="Python" %}}

Get information regarding the current SLAM session.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.slam.slam.SLAM.Properties)](INSERT RETURN TYPE LINK): The properties of SLAM

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_properties).

``` python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the properties of your current SLAM session.
slam_properties = await slam_svc.get_properties()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):

**Returns:**

- [(Properties)](https://pkg.go.dev#Properties):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getProperties.html).

{{% /tab %}}
{{< /tabs >}}
