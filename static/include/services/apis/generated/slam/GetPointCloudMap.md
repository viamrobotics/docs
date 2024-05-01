### GetPointCloudMap

{{< tabs >}}
{{% tab name="Python" %}}

Get the point cloud map.

**Parameters:**

- `return_edited_map` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): signal to the SLAM service to return an edited map, if the map package contains one and if the SLAM service supports the feature
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[bytes])](INSERT RETURN TYPE LINK): Complete pointcloud in standard PCD format. Chunks of the PointCloud, concatenating all GetPointCloudMapResponse.point_cloud_pcd_chunk values.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_point_cloud_map).

``` python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the point cloud map in standard PCD format.
pcd_map = await slam_svc.get_point_cloud_map()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `returnEditedMap`[(bool)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `returnEditedMap` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.slam/SLAMServiceClient/getPointCloudMap.html).

{{% /tab %}}
{{< /tabs >}}
