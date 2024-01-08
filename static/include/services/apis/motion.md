<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/mobility/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/mobility/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/mobility/motion/#moveonmap) | Move a [base](/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.
[`MoveOnGlobe`](/mobility/motion/#moveonglobe) | Move a [base](/components/base/) component to a destination GPS point. Use a [Movement Sensor](/components/movement-sensor/) to measure the machine's GPS coordinates.
[`StopPlan`](/mobility/motion/#stopplan) | Stop a [base](/components/base/) component being moved by an in progress [`MoveOnGlobe`](/mobility/motion/#moveonglobe) call.
[`GetPlan`](/mobility/motion/#getplan) | Returns the plan history of the most recent [`MoveOnGlobe`](/mobility/motion/#moveonglobe) call to move a [base](/components/base/) component.
[`ListPlanStatuses`](/mobility/motion/#listplanstatuses) | Returns the plan statuses created by [`MoveOnGlobe`](/mobility/motion/#moveonglobe) calls.
[`DoCommand`](/mobility/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/mobility/motion/#close) | Safely shut down the resource and prevent further use.
