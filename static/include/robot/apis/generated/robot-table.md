<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetOperations`](/appendix/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`ResourceNames`](/appendix/apis/robot/#resourcenames) | Get a list of all known resource names connected to this machine. |
| [`CancelOperation`](/appendix/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/appendix/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`DiscoverComponents`](/appendix/apis/robot/#discovercomponents) | Get a list of discovered component configurations. |
| [`FrameSystemConfig`](/appendix/apis/robot/#framesystemconfig) | Get the configuration of the frame system of a given machine. |
| [`TransformPose`](/appendix/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`TransformPCD`](/appendix/apis/robot/#transformpcd) | Transforms the pointcloud to the desired frame in the robot's frame system. |
| [`GetStatus`](/appendix/apis/robot/#getstatus) | Get the status of the resources on the machine. |
| [`StopAll`](/appendix/apis/robot/#stopall) | Cancel all current and outstanding operations for the machine and stop all actuators and movement. |
| [`Log`](/appendix/apis/robot/#log) | Create a LogEntry object from the log to send to the RDK over gRPC. |
| [`GetCloudMetadata`](/appendix/apis/robot/#getcloudmetadata) | Get app-related information about the robot. |
| [`Options.with_api_key`](/appendix/apis/robot/#optionswith_api_key) | Create a `RobotClient.Options` using an API key as credentials. |
| [`AtAddress`](/appendix/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/appendix/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/appendix/apis/robot/#refresh) | Manually refresh the underlying parts of this machine. |
| [`Shutdown`](/appendix/apis/robot/#shutdown) | Shutdown shuts down the machine. |
| [`Close`](/appendix/apis/robot/#close) | Close the underlying connections and stop any periodic tasks across all constituent parts of the machine. |
