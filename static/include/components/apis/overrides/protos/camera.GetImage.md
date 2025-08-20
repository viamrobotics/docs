Return an image from the camera.
You can request a specific MIME type but the returned MIME type is not guaranteed.
If the server does not know how to return the specified MIME type, the server returns the image in another format instead.

The available MIME types are:

- `image/vnd.viam.rgba`
- `image/vnd.viam.rgbalazy`
- `image/jpeg`
- `image/png`
- `pointcloud/pcd`
- `image/qoi`
