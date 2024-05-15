By default, returns the plan history of the most recent [`MoveOnGlobe`](/machine/services/motion/#moveonglobe) or [`MoveOnMap`](/machine/services/motion/#moveonmap) call to move a [base](/machine/components/base/) component.

The plan history for executions before the most recent can be requested by providing an `ExecutionID` in the request.

Returns a result if both of the following conditions are met:

- the execution (call to `MoveOnGlobe` or `MoveOnMap`) is still executing **or** changed state within the last 24 hours
- the machine has not reinitialized

Plans never change.

Replans always create new plans.

Replans share the `ExecutionID` of the previously executing plan.

All repeated fields are in chronological order.
