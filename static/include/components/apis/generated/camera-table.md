<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetImage`](/components/camera/#getimage) | Return an image from the camera. |
| [`GetImages`](/components/camera/#getimages) | Get simultaneous images from different imagers, along with associated metadata. |
| [`GetPointCloud`](/components/camera/#getpointcloud) | Get a point cloud from the camera as bytes with a MIME type describing the structure of the data. |
| [`GetProperties`](/components/camera/#getproperties) | Get the camera intrinsic parameters and camera distortion, as well as whether the camera supports returning point clouds. |
| [`DoCommand`](/components/camera/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetGeometries`](/components/camera/#getgeometries) | Get all the geometries associated with the camera in its current configuration, in the frame of the camera. |
| [`FromRobot`](/components/camera/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`GetResourceName`](/components/camera/#getresourcename) | Get the `ResourceName` for this camera with the given name. |
| [`Close`](/components/camera/#close) | Safely shut down the resource and prevent further use. |
