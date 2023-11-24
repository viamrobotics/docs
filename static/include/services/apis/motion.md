<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/build/configure/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/build/configure/services/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/build/configure/services/motion/#moveonmap) | Move a [base](/build/configure/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.
[`MoveOnGlobe`](/build/configure/services/motion/#moveonglobe) | Move a [base](/build/configure/components/base/) component to a destination GPS point. Use a [Movement Sensor](/build/configure/components/movement-sensor/) to measure the robot's GPS coordinates.
[`DoCommand`](/build/configure/services/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/build/configure/services/motion/#close) | Safely shut down the resource and prevent further use.
