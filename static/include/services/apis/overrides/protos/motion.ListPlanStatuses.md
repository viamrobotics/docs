Returns the statuses of plans created by [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) or [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) calls that meet at least one of the following conditions since the motion service initialized:

- the plan's status is in progress
- the plan's status changed state within the last 24 hours

All repeated fields are in chronological order.
