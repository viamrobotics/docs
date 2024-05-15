<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`Options.with_api_key`](/program/apis/robot/#optionswith_api_key) | Create RobotClient connection options with an API key as credentials. |
| [`AtAddress`](/program/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/program/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/program/apis/robot/#refresh) | Manually refresh the underlying parts of the machine. |
| [`GetOperations`](/program/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`CancelOperation`](/program/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/program/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`TransformPose`](/program/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`DiscoverComponents`](/program/apis/robot/#discovercomponents) | Get a list of discovered component configurations.                           |
| [`FrameSystemConfig`](/program/apis/robot/#framesystemconfig)   | Get the configuration of a machine's frame system.                             |
| [`Status`](/program/apis/robot/#status)                         | Get the status of each of the resources on the machine.                        |
| [`Close`](/program/apis/robot/#close)                           | Close the connections and stop periodic tasks across the machine.              |
| [`StopAll`](/program/apis/robot/#stopall)                       | Cancel all operations for the machine and stop its movement.                   |
| [`ResourceNames`](/program/apis/robot/#resourcenames)           | Get a list of all the machine's resources.                                     |
| [`GetCloudMetadata`](/program/apis/robot/#getcloudmetadata) | Returns app-related information about the robot. |
