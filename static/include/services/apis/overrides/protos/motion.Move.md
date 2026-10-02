The `Move` method is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, `Move` will:

1. Construct a full kinematic chain from goal to destination including all movable components in between.
2. Solve that chain to move the specified component frame to the destination while adhering to any constraints.
3. Execute that movement to move the actual machine.
4. Return whether or not this process succeeded.

The motion service takes the volumes associated with all configured machine components (local and remote) into account for each request to ensure that the machine does not collide with itself or other known objects.

`component_name` is the name of the component to move, as a string. Earlier SDK versions took a `ResourceName` message here; passing one now fails with `bad argument type for built-in operation`. Poses are in millimeters and degrees. If the path must avoid something that is not in the frame system, pass it as an obstacle in `world_state`.

A linear constraint makes `Move` solve for a straight-line path and refuse a curved fallback, so a segment with no direct solution returns `linear with cbirrt not allowed and no direct solutions found`. Keep the linear constraint for a short final approach and plan the rest as a free move. Read that error as the specific straight line being infeasible, not the goal being unreachable.
