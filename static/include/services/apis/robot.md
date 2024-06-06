<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`Options.with_api_key`](/appendix/apis/robot/#optionswith_api_key) | Create RobotClient connection options with an API key as credentials. |
| [`AtAddress`](/appendix/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/appendix/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/appendix/apis/robot/#refresh) | Manually refresh the underlying parts of the machine. |
| [`GetOperations`](/appendix/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`CancelOperation`](/appendix/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/appendix/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`TransformPose`](/appendix/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`DiscoverComponents`](/appendix/apis/robot/#discovercomponents) | Get a list of discovered component configurations.                           |
| [`FrameSystemConfig`](/appendix/apis/robot/#framesystemconfig)   | Get the configuration of a machine's frame system.                             |
| [`Status`](/appendix/apis/robot/#status)                         | Get the status of each of the resources on the machine.                        |
| [`Close`](/appendix/apis/robot/#close)                           | Close the connections and stop periodic tasks across the machine.              |
| [`StopAll`](/appendix/apis/robot/#stopall)                       | Cancel all operations for the machine and stop its movement.                   |
| [`ResourceNames`](/appendix/apis/robot/#resourcenames)           | Get a list of all the machine's resources.                                     |
| [`GetCloudMetadata`](/appendix/apis/robot/#getcloudmetadata) | Returns app-related information about the robot. |
