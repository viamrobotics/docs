You create and close both channels: `batches` when the trajectory is complete, `responses` only after the call has returned.

Waypoint timing is part of the trajectory rather than a hint:

- `Time` on the first point must be zero, and must strictly increase from one point to the next.
- If a point carries `Constraints`, the velocities on the first point must be zero.
- `Positions`, and the velocities and accelerations inside `Constraints`, follow the `referenceframe.Input` convention: radians and radians per second for revolute joints, millimeters and millimeters per second for prismatic ones. The wire format carries degrees, and the conversion happens at the boundary.

When the arm's kinematics are available, each waypoint is checked against the joint limits before it goes on the wire. A waypoint outside the limits fails the call and tears the stream down, which can happen after earlier batches are already executing.

Module authors implementing this method get the mirror image of this contract: the framework owns both channels, writes and closes `batches`, and closes `responses` after the implementation returns. See the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm) for that side of the interface.
