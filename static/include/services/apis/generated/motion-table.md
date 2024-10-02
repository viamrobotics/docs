<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`Move`](/appendix/apis/services/motion/#move) | The `Move` method is the primary way to move multiple components, or to move any object to any other location. |
| [`MoveOnMap`](/appendix/apis/services/motion/#moveonmap) | Move a base component to a destination pose on a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map. |
| [`MoveOnGlobe`](/appendix/apis/services/motion/#moveonglobe) | Move a base component to a destination GPS point, represented in geographic notation _(latitude, longitude)_. |
| [`GetPose`](/appendix/apis/services/motion/#getpose) | `GetPose` gets the location and orientation of a component within the frame system. |
| [`StopPlan`](/appendix/apis/services/motion/#stopplan) | Stop a base component being moved by an in progress `MoveOnGlobe` or `MoveOnMap` call. |
| [`ListPlanStatuses`](/appendix/apis/services/motion/#listplanstatuses) | Returns the statuses of plans created by `MoveOnGlobe` or `MoveOnMap` calls that meet at least one of the following conditions since the motion service initialized:  - the plan's status is in progress - the plan's status changed state within the last 24 hours  All repeated fields are in chronological order. |
| [`GetPlan`](/appendix/apis/services/motion/#getplan) | By default, returns the plan history of the most recent `MoveOnGlobe` or `MoveOnMap` call to move a base component. |
| [`Reconfigure`](/appendix/apis/services/motion/#reconfigure) | Reconfigure this resource. |
| [`FromRobot`](/appendix/apis/services/motion/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`DoCommand`](/appendix/apis/services/motion/#docommand) | Execute model-specific commands that are not otherwise defined by the service API. |
| [`GetResourceName`](/appendix/apis/services/motion/#getresourcename) | Get the `ResourceName` for this instance of the motion service with the given name. |
| [`Close`](/appendix/apis/services/motion/#close) | Safely shut down the resource and prevent further use. |
