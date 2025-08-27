<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetOperations`](/dev/reference/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`GetMachineStatus`](/dev/reference/apis/robot/#getmachinestatus) | Get status information about the machine. |
| [`GetSessions`](/dev/reference/apis/robot/#getsessions) | Get the list of sessions currently connected to the robot. |
| [`ResourceNames`](/dev/reference/apis/robot/#resourcenames) | Get a list of all known resource names connected to this machine. |
| [`ResourceRPCSubtypes`](/dev/reference/apis/robot/#resourcerpcsubtypes) | Get a list of all resource types. |
| [`CancelOperation`](/dev/reference/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/dev/reference/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`FrameSystemConfig`](/dev/reference/apis/robot/#framesystemconfig) | Get the configuration of the frame system of a given machine. |
| [`TransformPose`](/dev/reference/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`TransformPCD`](/dev/reference/apis/robot/#transformpcd) | Transforms the pointcloud to the desired frame in the robot's frame system. |
| [`GetModelsFromModules`](/dev/reference/apis/robot/#getmodelsfrommodules) | Get a list of all models provided by local and registry modules on the machine. |
| [`StopAll`](/dev/reference/apis/robot/#stopall) | Cancel all current and outstanding operations for the machine and stop all actuators and movement. |
| [`RestartModule`](/dev/reference/apis/robot/#restartmodule) | Reload a module as if its config changed. |
| [`Log`](/dev/reference/apis/robot/#log) | Create a LogEntry object from the log to send to the RDK over gRPC. |
| [`GetCloudMetadata`](/dev/reference/apis/robot/#getcloudmetadata) | Get app-related information about the robot. |
| [`GetVersion`](/dev/reference/apis/robot/#getversion) | Return version information about the machine. |
| [`Options.with_api_key`](/dev/reference/apis/robot/#optionswith_api_key) | Create a `RobotClient.Options` using an API key as credentials. |
| [`AtAddress`](/dev/reference/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/dev/reference/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/dev/reference/apis/robot/#refresh) | Manually refresh the underlying parts of this machine. |
| [`Shutdown`](/dev/reference/apis/robot/#shutdown) | Shutdown shuts down the machine. |
| [`Close`](/dev/reference/apis/robot/#close) | Close the underlying connections and stop any periodic tasks across all constituent parts of the machine. |
