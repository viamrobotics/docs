<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`Options.with_api_key`](/build/program/apis/robot/#optionswith_api_key) | Create RobotClient connection options with an API key as credentials. |
| [`AtAddress`](/build/program/apis/robot/#ataddress) | Create a RobotClient that is connected to the machine at the provided address. |
| [`WithChannel`](/build/program/apis/robot/#withchannel) | Create a RobotClient that is connected to a machine over the given channel. |
| [`Refresh`](/build/program/apis/robot/#refresh) | Manually refresh the underlying parts of the machine. |
| [`GetOperations`](/build/program/apis/robot/#getoperations) | Get the list of operations currently running on the machine. |
| [`CancelOperation`](/build/program/apis/robot/#canceloperation) | Cancel the specified operation on the machine. |
| [`BlockForOperation`](/build/program/apis/robot/#blockforoperation) | Blocks on the specified operation on the machine. |
| [`TransformPose`](/build/program/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`DiscoverComponents`](/build/program/apis/robot/#discovercomponents) | Get a list of discovered component configurations.                           |
| [`FrameSystemConfig`](/build/program/apis/robot/#framesystemconfig)   | Get the configuration of a machine's frame system.                             |
| [`Status`](/build/program/apis/robot/#status)                         | Get the status of each of the resources on the machine.                        |
| [`Close`](/build/program/apis/robot/#close)                           | Close the connections and stop periodic tasks across the machine.              |
| [`StopAll`](/build/program/apis/robot/#stopall)                       | Cancel all operations for the machine and stop its movement.                   |
| [`ResourceNames`](/build/program/apis/robot/#resourcenames)           | Get a list of all the machine's resources.                                     |
| [`GetCloudMetadata`](/build/program/apis/robot/#getcloudmetadata) | Returns app-related information about the robot. |
