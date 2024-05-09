`GetPose` gets the location and orientation of a component within the [frame system](../frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the machine's existing frame system with supplemental frames.
