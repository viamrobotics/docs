<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`Move`](/machine/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`GetPose`](/machine/services/motion/#getpose) | Get the current location and orientation of a component as a `Pose`.
[`MoveOnMap`](/machine/services/motion/#moveonmap) | Move a [base](/machine/components/base/) component to a `Pose` in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map. Use the machine's position reported by the [SLAM service](/machine/services/slam/)  to check the location of the machine.
[`MoveOnGlobe`](/machine/services/motion/#moveonglobe) | Move a [base](/machine/components/base/) component to a destination GPS point. Use a [Movement Sensor](/machine/components/movement-sensor/) to measure the machine's GPS coordinates.
[`StopPlan`](/machine/services/motion/#stopplan) | Stop a [base](/machine/components/base/) component being moved by an in progress [`MoveOnGlobe`](/machine/services/motion/#moveonglobe) or [`MoveOnMap`](/machine/services/motion/#moveonmap) call.
[`GetPlan`](/machine/services/motion/#getplan) | Returns the plan history of the most recent [`MoveOnGlobe`](/machine/services/motion/#moveonglobe) or [`MoveOnMap`](/machine/services/motion/#moveonmap) call to move a [base](/machine/components/base/) component.
[`ListPlanStatuses`](/machine/services/motion/#listplanstatuses) | Returns the plan statuses created by [`MoveOnGlobe`](/machine/services/motion/#moveonglobe) or [`MoveOnMap`](/machine/services/motion/#moveonmap) calls.
[`DoCommand`](/machine/services/motion/#docommand)     | Send arbitrary commands to the resource.
[`Close`](/machine/services/motion/#close) | Safely shut down the resource and prevent further use.
