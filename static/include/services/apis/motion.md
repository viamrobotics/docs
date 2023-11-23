<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/platform/build/configure/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/platform/build/configure/services/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/platform/build/configure/services/motion/#moveonmap) | Move a [base](/platform/build/configure/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.
[`MoveOnGlobe`](/platform/build/configure/services/motion/#moveonglobe) | Move a [base](/platform/build/configure/components/base/) component to a destination GPS point. Use a [Movement Sensor](/platform/build/configure/components/movement-sensor/) to measure the robot's GPS coordinates.
[`DoCommand`](/platform/build/configure/services/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/platform/build/configure/services/motion/#close) | Safely shut down the resource and prevent further use.
