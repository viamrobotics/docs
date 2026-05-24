{{< alert title="Not supported by the builtin motion service" color="caution" >}}
The [builtin motion service](/reference/services/motion/) no longer implements `MoveOnMap` and returns the error `MoveOnMap not supported by builtin` when called.
The implementation was removed in [rdk#5475](https://github.com/viamrobotics/rdk/pull/5475) (November 2025).

`MoveOnMap` is still part of the motion service API, so a third-party module can implement it.
Check the [Viam registry](https://app.viam.com/registry) for a motion-service module that supports it before relying on this method.
{{< /alert >}}

Move a [base](/reference/components/base/) component to a destination [pose](/motion-planning/reference/orientation-vectors/) on a SLAM map.

`MoveOnMap()` is non blocking, meaning the motion service will move the component to the destination [pose](/motion-planning/reference/orientation-vectors/) after `MoveOnMap()` returns.

Each successful `MoveOnMap()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnMap()` call.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, then `MoveOnMap` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnMap()` call by querying `GetPlan()` and `ListPlanStatuses()`.

Use the machine's position reported by the SLAM service to check the location of the machine.

`MoveOnMap()` is intended for use with the [navigation service](/reference/services/navigation/), providing autonomous indoor navigation for rover [bases](/reference/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnMap()`, your SLAM service must implement `GetPointCloudMap()` and `GetPosition()`

Make sure the SLAM service you use alongside this motion service supports the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the SLAM service API:

- It must support `GetPointCloudMap()` to report the SLAM map as a pointcloud.
- It must support `GetPosition()` to report the machine's current location on the SLAM map.
  {{< /alert >}}
