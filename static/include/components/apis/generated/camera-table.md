<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetImages`](/dev/reference/apis/components/camera/#getimages) | `GetImages` is used for getting simultaneous images from different imagers from 3D cameras along with associated metadata, and single images from non-3D cameras, for example webcams, RTSP cameras, etc. in the image list in the response. |
| [`GetPointCloud`](/dev/reference/apis/components/camera/#getpointcloud) | Get a point cloud from the camera as bytes with a MIME type describing the structure of the data. |
| [`GetProperties`](/dev/reference/apis/components/camera/#getproperties) | Get the camera intrinsic parameters and camera distortion, as well as whether the camera supports returning point clouds. |
| [`DoCommand`](/dev/reference/apis/components/camera/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetGeometries`](/dev/reference/apis/components/camera/#getgeometries) | Get all the geometries associated with the camera in its current configuration, in the frame of the camera. |
| [`GetResourceName`](/dev/reference/apis/components/camera/#getresourcename) | Get the `ResourceName` for this camera. |
| [`Close`](/dev/reference/apis/components/camera/#close) | Safely shut down the resource and prevent further use. |
