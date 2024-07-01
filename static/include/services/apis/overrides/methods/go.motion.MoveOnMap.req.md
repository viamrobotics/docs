<!-- retain-formatting -->
A `MoveOnMapReq` which contains the following values:
  - `ComponentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
  - `Destination` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
  - `SlamName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [SLAM service](/services/slam/) from which the SLAM map is requested.
  - `MotionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
    - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
    - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the machine.
    - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
    - `PlanDeviationM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the the **CONTROL** tab, the underlying calls to `MoveOnMap()` use 0.5 m instead.
    - `LinearMPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Linear velocity this machine should target when moving.
    - `AngularDegsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Angular velocity this machine should target when turning.
  - `Obstacles` [(\[\]spatialmath.Geometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): Obstacles, specified in the SLAM frame coordinate system, to be considered when planning the motion of the component.
  - `Extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
