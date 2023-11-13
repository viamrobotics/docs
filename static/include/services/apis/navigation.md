<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Mode`](/services/navigation/#mode) | Get the mode the service is operating in.
[`SetMode`](/services/navigation/#setmode) | Set the mode the service is operating in.
[`Location`](/services/navigation/#location) | Get the current location of the robot.
[`Waypoints`](/services/navigation/#waypoints) | Get the waypoints currently in the service's data storage.
[`AddWaypoint`](/services/navigation/#addwaypoint) | Add a waypoint to the service's data storage.
[`RemoveWaypoint`](/services/navigation/#removewaypoint) | Remove a waypoint from the service's data storage.
[`Paths`](/services/navigation/#paths) | Get each path, the series of geo points the robot plans to travel through to get to a destination waypoint, in the robot's motion planning.
[`Obstacles`](/services/navigation/#obstacles) | Get the obstacles currently in the service's data storage.
[`DoCommand`](/services/navigation/#docommand) | Execute model-specific commands that are not otherwise defined by the service API.
[`Close`](/services/navigation/#close) | Safely shut down the resource and prevent further use.
