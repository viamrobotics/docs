Execute model-specific commands that are not otherwise defined by the service API.
If you are implementing your own motion service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

### Teleop commands

The builtin motion service provides teleop DoCommands for low-latency, collision-aware arm control.

The following DoCommand keys are available:

- `teleop_start`: Starts the teleop pipeline. Pass a JSON-encoded `MoveRequest` protobuf specifying the component name, world state, and optional constraints. You can include an initial destination pose or omit it to start without an initial target.
- `teleop_move`: Sends a new target pose to the running pipeline. Pass a JSON-encoded `PoseInFrame` protobuf. The pipeline uses latest-value semantics: if a new pose arrives before the previous one is processed, the newer pose replaces it.
- `teleop_stop`: Stops the teleop pipeline.
- `teleop_status`: Returns the pipeline status including whether it's running, the number of queued poses and plans, timing metrics (`last_inputs_ms`, `last_plan_ms`, `last_exec_ms`, `last_exec_wait_ms`), execution counts (`plan_count`, `exec_count`), and any recent errors.
