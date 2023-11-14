<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/services/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/services/motion/#moveonmap) | Move a [base](/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.
[`MoveOnGlobe`](/services/motion/#moveonglobe) | Move a [base](/components/base/) component to a destination GPS point. Use a [Movement Sensor](/components/movement-sensor/) to measure the robot's GPS coordinates.
[`DoCommand`](/services/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/services/motion/#close) | Safely shut down the resource and prevent further use.
