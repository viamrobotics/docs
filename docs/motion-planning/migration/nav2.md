---
linkTitle: "From Nav2"
title: "Navigation for Nav2 users"
weight: 20
layout: "docs"
type: "docs"
description: "Concept mappings from Nav2 (ROS 2) to Viam's navigation service and motion service for mobile base navigation."
---

Nav2's value is breadth: dozens of tunable parameters across multiple
costmap layers, behavior-tree recovery, and a library of controllers
and planners you can swap in. Viam's navigation service makes a
different tradeoff: far fewer knobs, and the ones that remain have
straightforward meaning. If you are building outdoor GPS-based
waypoint navigation, the migration is short. If you have deep
investment in costmap tuning, behavior trees, or non-GPS navigation,
this page is honest about what does not transfer.

## Concept mapping

| Nav2 concept                                               | Viam equivalent                                                                                           |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Navigation stack (Nav2, or move_base in ROS1)              | [Navigation service](/navigation/) plus the motion service                                                |
| BT navigator, behavior trees                               | Not directly exposed. Recovery happens through plan-deviation replanning and application orchestration.   |
| Planner server (NavFn, Theta\*, Smac)                      | cBiRRT inside the motion service. One algorithm, not user-selectable.                                     |
| Controller server (DWB, MPPI, Regulated Pure Pursuit, TEB) | One path-following controller inside the motion service. Not selectable.                                  |
| Costmap layers (static, obstacle, voxel, inflation, STVL)  | Per-request geometric obstacles plus the base's own geometry on the frame system. No layered costmap.     |
| AMCL                                                       | Movement sensor abstraction. For map-relative localization, the SLAM service (out of scope for new docs). |
| `move_base_simple/goal`                                    | `AddWaypoint` + `SetMode(MODE_WAYPOINT)`                                                                  |
| `xy_goal_tolerance`                                        | `plan_deviation_m` (applied during execution, not just at arrival)                                        |
| Recovery behaviors (spin, backup, clear costmap)           | Automatic replan on deviation. No explicit recovery sequence.                                             |
| `nav2_params.yaml` (hundreds of parameters)                | ~15 navigation-service attributes plus the base's hardware config                                         |
| Behavior tree editor (Groot)                               | Application-level control flow in SDK code                                                                |
| `/cmd_vel` velocity commands                               | Base component's `SetVelocity` and `SetPower`                                                             |
| Geofencing through costmap masks                           | `bounding_regions` in the navigation service config                                                       |
| `nav2_costmap_2d` plugins                                  | Not applicable. Obstacles are geometric per-request.                                                      |

## Writing the same "drive to here" task

In Nav2 (Python, simplified):

```python
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

navigator = BasicNavigator()
goal = PoseStamped()
goal.header.frame_id = 'map'
goal.pose.position.x = 1.0
goal.pose.position.y = 2.0
goal.pose.orientation.w = 1.0
navigator.goToPose(goal)
```

In Viam (Python, navigating to a GPS waypoint):

```python
from viam.services.navigation import NavigationClient
from viam.proto.common import GeoPoint
from viam.proto.service.navigation import Mode

nav = NavigationClient.from_robot(machine, "my-nav")

await nav.add_waypoint(GeoPoint(latitude=40.6640, longitude=-73.9387))
await nav.set_mode(Mode.MODE_WAYPOINT)
```

Both invocations hand the robot a target and let the stack handle
replanning, obstacle avoidance, and arrival detection. The Viam
equivalent targets GPS coordinates; use a movement sensor module
for non-GPS localization, or the (out-of-scope) SLAM service for
map-relative navigation.

## What transfers

- **Waypoint-following semantics.** Add waypoints, switch to waypoint
  mode, robot drives the sequence.
- **Vision-based obstacle detection.** Nav2's obstacle layer receives
  data from sensor drivers; Viam's `obstacle_detectors` receive data
  from vision services. The mechanism is similar: detected obstacles
  feed the planner during execution.
- **Geofencing.** `bounding_regions` is the equivalent of staying
  inside a masked region.
- **Replanning on deviation.** Viam replans when the robot drifts
  beyond `plan_deviation_m` from the current plan, much as Nav2
  replans on deviation under the appropriate BT.

## What is different

- **One controller, not a library.** Viam's navigation does not let
  you swap DWB for MPPI for Regulated Pure Pursuit. There is one
  path-following behavior, tuned through a small number of global
  parameters.
- **No persistent costmap.** The planner does not maintain a 2D or
  voxel grid that accumulates over time. See
  [How Viam's world model differs from ROS](/motion-planning/obstacles/#how-viams-world-model-differs-from-ros).
- **No behavior tree.** Recovery happens in two ways: automatic
  replanning by the navigation service when deviation exceeds
  `plan_deviation_m`, or explicit orchestration in your SDK code
  when you need more control.
- **Mode selector instead of goal topic.** Setting `MODE_WAYPOINT`
  starts navigation; setting `MODE_MANUAL` hands control back. The
  UI exposes Manual and Waypoint only; `MODE_EXPLORE` is in the SDK
  but not in the UI.

## What you lose

- **Controller flexibility.** If your deployment depends on TEB for
  trailer-aware navigation, a custom controller plugin, or any of
  Nav2's specialized path-followers, Viam does not expose equivalents.
- **Deep costmap tuning.** Inflation radius, voxel heights, decay
  rates, and layer combinations are Nav2 controls that do not map.
  Viam approximates collision margin through component geometry and
  per-call `collision_buffer_mm`.
- **Behavior-tree recovery design.** No Groot, no BT XML, no custom
  recovery sequences.
- **Map-based localization (AMCL) out of the box.** Viam's SLAM
  service handles this but is not recommended in current docs; most
  users deploy with GPS.

## What you gain

- **Dramatically fewer knobs.** The navigation service has about 15
  configuration attributes. Most deployments change 5 of them.
- **Hot reconfiguration.** Change the config in the Viam app and the
  navigation service picks up the new values on the next cycle; no
  relaunch required.
- **Cloud connectivity and fleet rollout.** The same config can deploy
  to a fleet of bases through Viam's fragments.
- **A simpler surface to reason about.** `plan_deviation_m`,
  `replan_cost_factor`, `obstacle_polling_frequency_hz`, and the
  speed caps are the main tuning controls. You will not spend weeks
  in YAML.

## What's next

- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  the minimal GPS waypoint setup.
- [Tune navigation](/navigation/how-to/tune-navigation/): the ~5
  parameters most users tune.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  the full reference for the ~15 attributes.
- [Replanning behavior](/motion-planning/replanning-behavior/):
  when and how the navigation service replans.
- [Frame system for TF users](/motion-planning/migration/tf/):
  if you also want to understand Viam's coordinate frames.
