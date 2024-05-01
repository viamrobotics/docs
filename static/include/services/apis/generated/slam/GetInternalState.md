### GetInternalState

{{< tabs >}}
{{% tab name="Python" %}}

Get the internal state of the SLAM algorithm required to continue mapping/localization.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[bytes])](INSERT RETURN TYPE LINK): Chunks of the internal state of the SLAM algorithm

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_internal_state).

``` python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state = await slam.get_internal_state()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getInternalState.html).

{{% /tab %}}
{{< /tabs >}}
