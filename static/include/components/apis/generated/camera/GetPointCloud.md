### GetPointCloud

{{< tabs >}}
{{% tab name="Python" %}}

Get the next point cloud from the camera. This will be returned as bytes with a mimetype describing the structure of the data. The consumer of this call should encode the bytes into the formatted suggested by the mimetype.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(Tuple[bytes, str])](INSERT RETURN TYPE LINK):  A tuple containing two values; the first [0] the pointcloud data, and the second [1] the mimetype of thepointcloud (e.g. PCD).   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_point_cloud).

``` python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

data, _ = await camera.get_point_cloud()

# write the point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(data)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `pointcloud`[(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/pointcloud#pointcloud):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.camera/CameraServiceClient/getPointCloud.html).

{{% /tab %}}
{{< /tabs >}}
