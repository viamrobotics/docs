### GetObjectPointClouds

{{< tabs >}}
{{% tab name="Python" %}}

Returns a list of the 3D point cloud objects and associated metadata in the latest picture obtained from the specified 3D camera (using the specified segmenter).

**Parameters:**

- `camera_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The name of the camera
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.proto.common.PointCloudObject])](INSERT RETURN TYPE LINK): The pointcloud objects with metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_object_point_clouds).

``` python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

# Grab the 3D camera from the machine
cam1 = Camera.from_robot(robot, "cam1")
# Grab the object segmenter you configured on your machine
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")
# Get the objects from the camera output
objects = await my_segmenter.get_object_point_clouds(cam1)
# write the first object point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(objects[0].point_cloud)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `cameraName`[(string)](https://pkg.go.dev/builtin#string):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `viz`[(Object)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/vision#Object):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getObjectPointClouds.html).

{{% /tab %}}
{{< /tabs >}}
