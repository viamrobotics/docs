<!-- prettier-ignore -->
| Method Name                                                     | Description                                                                  |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`Options.with_api_key`](/build/program/apis/robot/#optionswith_api_key) | Create Robot client connection options with an API key as credentials. |
| [`AtAddress`](/build/program/apis/robot/#ataddress) | Create a robot client that is connected to the robot at the provided address. |
| [`WithChannel`](/build/program/apis/robot/#withchannel) | Create a robot that is connected to a robot over the given channel. |
| [`Refresh`](/build/program/apis/robot/#refresh) | Manually refesh the underlying parts of the robot. |
| [`Status`](/build/program/apis/robot/#status) | Get the status of the robot's components. |
| [`GetOperations`](/build/program/apis/robot/#getoperations) | Get the list of operations currently running on the robot. |
| [`CancelOperation`](/build/program/apis/robot/#canceloperation) | Cancel the specified operation on the robot. |
| [`BlockForOperation`](/build/program/apis/robot/#blockforoperation) | Blocks on the specified operation on the robot. |
| [`TransformPose`](/build/program/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |
| [`DiscoverComponents`](/build/program/apis/robot/#discovercomponents) | Get a list of discovered component configurations.                           |
| [`FrameSystemConfig`](/build/program/apis/robot/#framesystemconfig)   | Get the configuration of a robot's frame system.                             |
| [`Status`](/build/program/apis/robot/#status)                         | Get the status of each of the resources on the robot.                        |
| [`Close`](/build/program/apis/robot/#close)                           | Close the connections and stop periodic tasks across the robot.              |
| [`StopAll`](/build/program/apis/robot/#stopall)                       | Cancel all operations for the robot and stop its movement.                   |
| [`ResourceNames`](/build/program/apis/robot/#resourcenames)           | Get a list of all the robot's resources.                                     |
