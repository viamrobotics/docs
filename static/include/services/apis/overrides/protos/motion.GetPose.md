`GetPose` gets the location and orientation of a component within the [frame system](/reference/services/frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the machine's existing frame system with supplemental frames.

This motion service method is deprecated in favor of the machine client's [`GetPose`](/reference/apis/robot/#getpose), which takes the same parameters and returns the same result: `machine.get_pose` in Python (SDK v0.83.0 and later), `machine.GetPose` in Go, and `machine.getPose` in TypeScript.
The Flutter SDK has no machine-client version, so Flutter callers still use this method.

`component_name` is the component's name as a string; earlier SDK versions took a `ResourceName` message, which now fails with `bad argument type for built-in operation`. To convert a pose you already have from one frame to another, use the machine client's `TransformPose` instead.
