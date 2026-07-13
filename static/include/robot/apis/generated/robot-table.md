<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetOperations`](/reference/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`GetMachineStatus`](/reference/apis/robot/#getmachinestatus) | Get status information about the machine including the status of the machine and its resources and the revision of the machine config. |
| [`GetSessions`](/reference/apis/robot/#getsessions) | Get the list of sessions currently connected to the robot. |
| [`ResourceNames`](/reference/apis/robot/#resourcenames) | Get a list of all known resource names connected to this machine. |
| [`ResourceRPCSubtypes`](/reference/apis/robot/#resourcerpcsubtypes) | Get a list of all resource types. |
| [`CancelOperation`](/reference/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/reference/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`FrameSystemConfig`](/reference/apis/robot/#framesystemconfig) | Get the configuration of the frame system of a given machine. |
| [`TransformPose`](/reference/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`TransformPCD`](/reference/apis/robot/#transformpcd) | Transforms the pointcloud to the desired frame in the robot's frame system. |
| [`GetModelsFromModules`](/reference/apis/robot/#getmodelsfrommodules) | Get a list of all models provided by local and registry modules on the machine. |
| [`StopAll`](/reference/apis/robot/#stopall) | Cancel all current and outstanding operations for the machine and stop all actuators and movement. |
| [`RestartModule`](/reference/apis/robot/#restartmodule) | Reload a module as if its config changed. |
| [`Log`](/reference/apis/robot/#log) | Create a LogEntry object from the log to send to the RDK over gRPC. |
| [`GetCloudMetadata`](/reference/apis/robot/#getcloudmetadata) | Get app-related information about the robot. |
| [`GetVersion`](/reference/apis/robot/#getversion) | Return version information about the machine. |
| [`Options.with_api_key`](/reference/apis/robot/#optionswith_api_key) | Create a `RobotClient.Options` using an API key as credentials. |
| [`AtAddress`](/reference/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/reference/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/reference/apis/robot/#refresh) | Manually refresh the underlying parts of this machine. |
| [`Shutdown`](/reference/apis/robot/#shutdown) | Shutdown shuts down the machine. |
| [`Close`](/reference/apis/robot/#close) | Close the underlying connections and stop any periodic tasks across all constituent parts of the machine. |
