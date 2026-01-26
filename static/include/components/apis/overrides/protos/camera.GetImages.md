{{% alert title="Usage" color="note" %}}

You can use the [`rgb-d-overlay` module](https://app.viam.com/module/viam/rgb-d-overlay) to view and compare the camera streams returned by this method.
See the [module readme](https://github.com/viam-labs/rgb-d-overlay) for further instructions.
{{% /alert %}}

`GetImages` is used for getting simultaneous images from different imagers from 3D cameras along with associated metadata, and single images from non-3D cameras e.g. webcams, RTSP cameras etc. in the image list in the response.
Multiple images returned from `GetImages()` do not represent a time series of images.
