<!-- preserve-formatting -->
A `MoveOnGlobeReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
  - `destination` [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The location of the component's destination, represented in geographic notation as a [Point](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point) _(lat, lng)_.
  - `heading` [(float64)](https://pkg.go.dev/builtin#float64): The compass heading, in degrees, that the machine's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` 0: North, 90: East, 180: South, 270: West</li><li>Default: `0`</li></ul>
  - `movementSensorName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [movement sensor](/components/movement-sensor/) that you want to use to check the machine's location.
  - `obstacles` [([]\*spatialmath.GeoGeometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoGeometry): Obstacles to consider when planning the motion of the component, with each represented as a `GeoGeometry`. <ul><li> Default: `nil` </li></ul>
  - `motionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
    - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
    - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the machine.
    - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
    - `PlanDeviationM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in meters that the machine can deviate from the motion plan.
    - `LinearMPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Linear velocity this machine should target when moving.
    - `AngularDegsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Angular velocity this machine should target when turning.
