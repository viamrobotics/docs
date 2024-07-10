Describes where the `component_name` should end up.
Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).
Note that the destination pose is relative to the distal end of the specified frame.
This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of `{X: 10, Y: 0, Z: 0}` will move that arm’s end effector by 10 mm in the local `X` direction.
