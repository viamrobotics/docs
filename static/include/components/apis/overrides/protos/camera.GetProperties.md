Get the camera intrinsic parameters and camera distortion, as well as whether the camera supports returning point clouds.
The response also names the default reference frame: the frame that the points `GetPointCloud` returns are expressed in.
An empty name means the frame is unknown, and the named frame is not guaranteed to exist in the frame system.
