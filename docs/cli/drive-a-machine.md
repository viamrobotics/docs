---
linkTitle: "Drive a machine"
title: "Drive a machine from the CLI"
weight: 20
layout: "docs"
type: "docs"
description: "Discover, observe, and operate any Viam machine with the CLI alone: list its resources, read its cameras and sensors, plan motion, and stop it, with one key and no SDK code."
date: "2026-09-03"
---

The CLI can call any API method a machine serves, with JSON in and JSON out.
That makes it a complete way to operate a machine from a shell, for a person or for an AI agent, without writing SDK code.
This page shows the commands in the order you need them.
For the concepts behind them, see [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/).

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated with an API key.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
A machine-scoped key can reach one machine; a location or organization key can also list and create machines.
{{< /expand >}}

## Find the machine

```sh {class="command-line" data-prompt="$"}
viam organizations list
viam locations list --organization=<org-id>
viam machines list --location=<location-id>
viam machines part list --machine=<machine-id>
viam machines part status --part=<part-id>
```

A machine has one or more parts; the main part is the one running `viam-server`.
Every command below takes `--part=<part-id>`.
`status` shows when the part was last reachable.

## Call any API method

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=<method> --data='<json>'
```

`run` invokes any gRPC method the machine serves, using the machine's own reflection, so it works for every component, service, and module.
Name the method one of two ways:

- **Full name**, for machine-level calls: `--method=viam.robot.v1.RobotService.ResourceNames`.
- **Short name with a component**: `--component=my-arm --method=GetJointPositions`.
  The CLI looks up the component's API, expands the name, and fills in the `name` field of the request.

`--data` is the request message as JSON, with field names as they appear in the proto (`camera_name`, not `cameraName`).
Omit it when the request needs nothing beyond the resource name.

## Discover what the machine has

Run these first, before any motion.

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.ResourceNames
```

Every resource on the machine, with its API.

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.GetMachineStatus
```

Every resource's state (configuring, ready, or unhealthy, with the error), the config revision the machine has applied, and module health.

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.ResourceRPCSubtypes
```

The gRPC service descriptors for every API the machine serves: method names and request fields.

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.FrameSystemConfig
```

The kinematic frame tree: which frames exist, their parents, and their geometry.

Per resource, ask for the detail you need:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-arm --method=GetKinematics
viam machines part run --part=<part-id> --component=my-arm --method=GetGeometries
viam machines part run --part=<part-id> --component=my-cam --method=GetProperties
```

The motion service prints a readable frame table with current poses:

```sh {class="command-line" data-prompt="$"}
viam machines part motion print-config --part=<part-id>
viam machines part motion print-status --part=<part-id>
```

{{< alert title="Note" color="note" >}}
The CLI has no command that prints a machine's saved configuration (models and attributes).
The SDKs can read it with `get_robot_part`.
The calls above are the runtime truth and are usually what you want.
{{< /alert >}}

## Observe

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-cam --method=GetImages
viam machines part run --part=<part-id> --component=my-cam --method=GetPointCloud
viam machines part run --part=<part-id> --component=my-sensor --method=GetReadings
viam machines part run --part=<part-id> --component=my-arm --method=GetJointPositions
viam machines part run --part=<part-id> --component=my-arm --method=GetEndPosition
```

Images and point clouds come back inline, base64-encoded in the JSON.

A vision service returns an image, detections, and object point clouds in one call:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-vision --method=CaptureAllFromCamera \
  --data='{"camera_name":"my-cam","return_image":true,"return_detections":true,"return_object_point_clouds":true}'
```

Detections only:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-vision --method=GetDetectionsFromCamera \
  --data='{"camera_name":"my-cam"}'
```

`--stream=1s` repeats a call on an interval and prints each result.
It is polling, not a video stream; live video is on the machine's page in the Viam app.

## Act

Prefer planned motion.
The motion service takes a goal pose and returns collision-checked motion against the frame system's geometry and any obstacles you declare.
An arm's own `MoveToPosition` is unplanned and will drive straight through things.

```sh {class="command-line" data-prompt="$"}
viam machines part motion get-pose --part=<part-id> --component=my-gripper
viam machines part motion set-pose --part=<part-id> --component=my-gripper \
  --x=300 --y=250 --z=900 --ox=0 --oy=0 --oz=-1 --theta=0
```

`set-pose` moves a component's frame to a pose in the world frame: millimeters, and an orientation vector with theta in degrees.

The same call through the raw API, with a declared obstacle and a straight-line constraint:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=builtin --method=Move --data='{
  "component_name": "my-gripper",
  "destination": {"reference_frame": "world",
                  "pose": {"x": 300, "y": 250, "z": 900, "o_x": 0, "o_y": 0, "o_z": -1, "theta": 0}},
  "world_state": {"obstacles": [{"reference_frame": "world", "geometries": [
      {"center": {"x": 450, "y": -50, "z": 780, "o_z": 1},
       "box": {"dims_mm": {"x": 60, "y": 60, "z": 60}}, "label": "blue-block"}]}]},
  "constraints": {"linear_constraint": [{"line_tolerance_mm": 5, "orientation_tolerance_degs": 5}]}
}'
```

`--data` is parsed as a single string, so the line breaks above are only for readability; writing the same JSON on one line works identically and can be easier to quote correctly in a script.

Typed verbs on components:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-gripper --method=Open
viam machines part run --part=<part-id> --component=my-gripper --method=Grab
viam machines part run --part=<part-id> --component=my-gripper --method=IsHoldingSomething
viam machines part run --part=<part-id> --component=my-arm --method=MoveToJointPositions \
  --data='{"positions": {"values": [0, -90, 0, -90, 90, 0]}}'
viam machines part run --part=<part-id> --component=my-base --method=SetVelocity \
  --data='{"linear": {"y": 100}, "angular": {"z": 0}}'
viam machines part run --part=<part-id> --component=my-motor --method=SetPower --data='{"power_pct": 0.5}'
```

Anything a resource offers beyond its typed API goes through `DoCommand`.
The request wraps your command in a `command` object:

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --component=my-service --method=DoCommand \
  --data='{"command": {"command": "status"}}'
```

## Stop, and what stops for you

```sh {class="command-line" data-prompt="$"}
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.StopAll
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.GetOperations
viam machines part run --part=<part-id> --method=viam.robot.v1.RobotService.CancelOperation --data='{"id": "<op-id>"}'
```

`StopAll` stops every operation and every actuator in one call.

Each client connection to the machine carries a heartbeat.
When it lapses because the client exits or crashes, `viam-server` stops the actuators that client commanded, within about two seconds.
For CLI users that means:

- Every `part run` is its own connection, so a command that starts a motion and exits has that motion stopped when the connection ends.
  Long moves belong in the motion service, whose `Move` returns when the motion finishes.
- On some gripper models the same stop releases the drive, dropping what the gripper holds.
  A sequence that must hold an object across steps belongs in one process with one connection, which means an SDK script rather than separate CLI commands.
  Check `IsHoldingSomething` after a lift; do not trust `Grab`'s return value alone.

Motion-service moves are not covered by the heartbeat: a `Move` in progress continues after the client that started it disappears.
Use `StopAll` if it must end.

## Change the machine

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource --part=<part-id> --name=my-cam --resource-subtype=camera --model-name=viam:camera:realsense
viam machines part remove-resource --part=<part-id> --name=my-cam
viam machines api-key create --machine-id=<machine-id> --name=agent-key
viam machines create --name=my-robot --location=<location-id>
viam machines part logs --part=<part-id> --count=50
viam machines part logs --part=<part-id> --tail
```

After a configuration change the machine converges within about ten seconds.
Confirm with `GetMachineStatus`, which reports the config revision and each resource's state, rather than by waiting.

## Reading errors

| Error                                                                            | Meaning                                                                                             |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `resource rdk:component:arm/my-arm not found`                                    | Wrong name or not configured; check `ResourceNames`.                                                |
| `Unimplemented`                                                                  | This model does not implement that method. No further detail is given.                              |
| `all IK solutions failed constraints. Failures: { obstacle constraint: 62.00% }` | The planner could not reach the goal; the percentages say which constraint blocked most candidates. |
| `arm stalled at waypoint 2/2 (stuck joints: j3: at 110.0 want 118.8)`            | The arm hit something during execution.                                                             |
| `modular resource config validation error: context deadline exceeded`            | The module did not answer in time, usually because it is still starting.                            |

## Method names by API

| API                                                     | Read                                                                                                                       | Act                                                                           |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Machine (full names under `viam.robot.v1.RobotService`) | `ResourceNames`, `GetMachineStatus`, `ResourceRPCSubtypes`, `FrameSystemConfig`, `TransformPose`, `GetOperations`          | `StopAll`, `CancelOperation`, `RestartModule`                                 |
| Arm                                                     | `GetJointPositions`, `GetEndPosition`, `GetKinematics`, `GetGeometries`, `IsMoving`                                        | `MoveToPosition`, `MoveToJointPositions`, `MoveThroughJointPositions`, `Stop` |
| Gripper                                                 | `IsHoldingSomething`, `GetGeometries`, `GetKinematics`, `IsMoving`                                                         | `Open`, `Grab`, `Stop`                                                        |
| Camera                                                  | `GetImages`, `GetPointCloud`, `GetProperties`, `GetGeometries`                                                             |                                                                               |
| Sensor                                                  | `GetReadings`                                                                                                              |                                                                               |
| Base                                                    | `GetProperties`, `IsMoving`                                                                                                | `MoveStraight`, `Spin`, `SetVelocity`, `SetPower`, `Stop`                     |
| Motor                                                   | `GetPosition`, `GetProperties`, `IsPowered`, `IsMoving`                                                                    | `SetPower`, `GoFor`, `GoTo`, `SetRPM`, `Stop`                                 |
| Vision service                                          | `GetDetectionsFromCamera`, `GetClassificationsFromCamera`, `GetObjectPointClouds`, `CaptureAllFromCamera`, `GetProperties` |                                                                               |
| Motion service                                          | `GetPose`, `GetPlan`, `ListPlanStatuses`                                                                                   | `Move`, `StopPlan`                                                            |
| Any resource                                            |                                                                                                                            | `DoCommand`                                                                   |

The full, current list always comes from the machine itself through `ResourceRPCSubtypes`.
When in doubt, ask the machine.
