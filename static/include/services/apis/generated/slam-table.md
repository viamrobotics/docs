<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetPosition`](/reference/apis/services/slam/#getposition) | Get the current position of the component the SLAM service is configured to source point cloud data from in the SLAM map as a `Pose`. |
| [`GetPointCloudMap`](/reference/apis/services/slam/#getpointcloudmap) | Get the point cloud map. |
| [`GetInternalState`](/reference/apis/services/slam/#getinternalstate) | Get the internal state of the SLAM algorithm required to continue mapping/localization. |
| [`GetProperties`](/reference/apis/services/slam/#getproperties) | Get information about the current SLAM session. |
| [`InternalStateFull`](/reference/apis/services/slam/#internalstatefull) | `InternalStateFull` concatenates the streaming responses from `InternalState` into the internal serialized state of the SLAM algorithm. |
| [`PointCloudMapFull`](/reference/apis/services/slam/#pointcloudmapfull) | `PointCloudMapFull` concatenates the streaming responses from `PointCloudMap` into a full point cloud. |
| [`Reconfigure`](/reference/apis/services/slam/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/reference/apis/services/slam/#docommand) | Execute model-specific commands that are not otherwise defined by the service API. |
| [`GetResourceName`](/reference/apis/services/slam/#getresourcename) | Get the `ResourceName` for this instance of the SLAM service. |
| [`Close`](/reference/apis/services/slam/#close) | Safely shut down the resource and prevent further use. |
