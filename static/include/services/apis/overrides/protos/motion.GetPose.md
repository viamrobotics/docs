`GetPose` gets the location and orientation of a component within the [frame system](/reference/services/frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the machine's existing frame system with supplemental frames.

`component_name` is the component's name as a string; earlier SDK versions took a `ResourceName` message, which now fails with `bad argument type for built-in operation`. To convert a pose you already have from one frame to another, use the machine client's `TransformPose` instead.
