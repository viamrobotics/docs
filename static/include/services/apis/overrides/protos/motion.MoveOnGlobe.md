Move a [base](/components/base/) component to a destination GPS point, represented in geographic notation _(latitude, longitude)_.
Use a [movement sensor](/components/movement-sensor/) to check the location of the machine.

`MoveOnGlobe()` is non blocking, meaning the motion service will move the component to the destination GPS point after `MoveOnGlobe()` returns.

Each successful `MoveOnGlobe()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnGlobe()`.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, `MoveOnGlobe` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnGlobe()` call by querying `GetPlan()` and `ListPlanStatuses()`.

`MoveOnGlobe()` is intended for use with the [navigation service](/mobility/navigation/), providing autonomous GPS navigation for rover [bases](/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnGlobe()`, your movement sensor must be able to measure the GPS location and orientation of the machine.

Make sure the [movement sensor](/components/movement-sensor/) you use supports usage of the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [movement sensor API](/components/movement-sensor/#api).

- It must support `GetPosition()` to report the machine's current GPS location.
- It must **also** support **either** `GetCompassHeading()` or `GetOrientation()` to report which way the machine is facing.
- If your movement sensor provides multiple methods, your machine will default to using the values returned by `GetCompassHeading()`.
  {{< /alert >}}

{{< alert title="Stability Notice" color="alert" >}}

The `heading` parameter is experimental.
Specifying `heading` in a request to `MoveOnGlobe` is not currently recommended if the minimum turning radius of your component is greater than zero, as this combination may cause high latency in the [motion planning algorithms](/mobility/motion/algorithms/).

Specifying `obstacles` in a request to `MoveOnGlobe()` will cause an error if you configure a `"translation"` in the `"geometries"` of any of the `GeoObstacle` objects.
Translation in obstacles is not supported by the [navigation service](/mobility/navigation/).

{{< /alert >}}
