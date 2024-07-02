<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/services/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/services/motion/#moveonmap) | Move a [base](/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map. Use the machine's position reported by the [SLAM service](/services/slam/)  to check the location of the machine.
[`MoveOnGlobe`](/services/motion/#moveonglobe) | Move a [base](/components/base/) component to a destination GPS point. Use a [Movement Sensor](/components/movement-sensor/) to measure the machine's GPS coordinates.
[`StopPlan`](/services/motion/#stopplan) | Stop a [base](/components/base/) component being moved by an in progress [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) call.
[`GetPlan`](/services/motion/#getplan) | Returns the plan history of the most recent [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) call to move a [base](/components/base/) component.
[`ListPlanStatuses`](/services/motion/#listplanstatuses) | Returns the plan statuses created by [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) calls.
[`DoCommand`](/services/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/services/motion/#close) | Safely shut down the resource and prevent further use.
