<!-- preserve-formatting -->
Information about the current SLAM session.
  An object containing four fields:

  - `SensorInfo` [(SensorInfo[])](https://pkg.go.dev/go.viam.com/api/service/slam/v1#SensorInfo): Information about the sensors (camera and movement sensor) configured for your SLAM service, including the name and type of sensor.
  - `CloudSlam` [(bool)](https://pkg.go.dev/builtin#bool): A boolean which indicates whether the session is being run in the cloud.
  - `MappingMode` [(MappingMode)](https://pkg.go.dev/go.viam.com/rdk/services/slam#MappingMode): Represents the [form of mapping and localizing the current session is performing](/services/slam/cartographer/#use-a-live-machine). This includes creating a new map, localizing on an existing map and updating an existing map.
  - `InternalStateFileType` [(string)](https://pkg.go.dev/builtin#string): The file type the service's internal state algorithm is stored in.
