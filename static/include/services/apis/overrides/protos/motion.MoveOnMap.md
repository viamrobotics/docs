Move a [base](/operate/reference/components/base/) component to a destination [pose](/operate/reference/orientation-vector/) on a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.

`MoveOnMap()` is non blocking, meaning the motion service will move the component to the destination [pose](/operate/reference/orientation-vector/) after `MoveOnMap()` returns.

Each successful `MoveOnMap()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnMap()` call.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, then `MoveOnMap` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnMap()` call by querying `GetPlan()` and `ListPlanStatuses()`.

Use the machine's position reported by the {{< glossary_tooltip term_id="slam" text="SLAM" >}} service to check the location of the machine.

`MoveOnMap()` is intended for use with the [navigation service](/operate/reference/services/navigation/), providing autonomous indoor navigation for rover [bases](/operate/reference/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnMap()`, your [SLAM service](/operate/reference/services/slam/) must implement `GetPointCloudMap()` and `GetPosition()`

Make sure the [SLAM service](/operate/reference/services/slam/) you use alongside this motion service supports the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [SLAM service API](/dev/reference/apis/services/slam/):

- It must support `GetPointCloudMap()` to report the SLAM map as a pointcloud.
- It must support `GetPosition()` to report the machine's current location on the SLAM map.
  {{< /alert >}}
