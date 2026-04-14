---
linkTitle: "Industrial arms"
title: "Using industrial arms with Viam"
weight: 40
layout: "docs"
type: "docs"
description: "How Viam abstracts vendor-specific industrial arm SDKs (UR, KUKA, ABB, and others) behind a single motion service API, and where vendor limits still show through."
---

Industrial arms traditionally ship with vendor-specific programming
environments: KUKA Robot Language (KRL), ABB RAPID, Universal Robots
URScript, FANUC TPP. Each one assumes you will build your application
on top of that specific vendor's controller. Switching vendors means
rewriting.

Viam's value proposition for industrial-arm users is the same `Move`
call drives a UR5e, a UFactory xArm 6, a KUKA arm, an ABB IRB, or any
other arm that has a Viam module. Your application code does not
change when the hardware does.

This page is honest about where that abstraction is clean and where
vendor constraints show through.

## One API across vendors

The arm component API and the motion service work the same way
regardless of the underlying hardware. Writing "move the arm to this
pose while avoiding this obstacle" looks the same whether the module
drives a UR or a KUKA:

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

target = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0),
)

await motion_service.move(component_name="my-arm", destination=target)
```

Swap the arm module; the code stays. That is the abstraction.

## Vendor concept mapping

| Vendor concept                     | Viam equivalent                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------- |
| URScript, URCap                    | Not exposed directly. The UR module translates Viam API calls into the necessary vendor commands. |
| KUKA Robot Language (KRL)          | Not exposed directly. KUKA modules translate through KUKA's programmable interfaces.              |
| ABB RAPID                          | Not exposed directly. ABB modules translate through RAPID / EGM.                                  |
| FANUC Karel / TPP                  | Not exposed directly.                                                                             |
| ABB Externally Guided Motion (EGM) | Module-internal. Exposed to your application as the standard motion service.                      |
| KUKA Robot Sensor Interface (RSI)  | Module-internal.                                                                                  |
| Teach pendant programming          | Not a Viam workflow. Configure frames and geometries through the Viam app.                        |
| Safety I/O, protective stops       | Pass through. Vendor safety behavior is preserved end-to-end.                                     |
| Vendor-specific IO mapping         | Module may expose through board or motor components, or through `DoCommand`.                      |

## What transfers

- **Motion planning.** The motion service computes paths for arms
  through the same code path regardless of vendor. Obstacles,
  constraints, and frame system work identically.
- **Cartesian and joint-space moves.** Both `MoveToPosition` (with
  obstacle avoidance through `motion.Move`) and
  `MoveToJointPositions` are available on every arm module. See
  [Move an arm by setting joint positions](/motion-planning/motion-how-to/move-arm-joint-positions/).
- **URDF-based kinematics.** Many industrial arm modules ship with
  URDFs or Viam SVA JSON files that encode the kinematic chain. See
  [Arm kinematics](/motion-planning/reference/kinematics/).
- **Safety heartbeat.** The motion service's safety heartbeat
  mechanism terminates ongoing motion when connectivity to the
  controlling process is lost. This works across all supported arms.

## Vendor limits that pass through

The abstraction does not change the arm's physical reality. A set of
behaviors are controlled by the vendor's own firmware and safety
system, and the Viam module cannot override them. Be prepared for:

- **Protective stops near singularities or joint limits.** UR arms
  document error codes C150 (position close to joint limits), C151
  (tool orientation limits), C152 (safety plane), C153 (trajectory
  deviation), and C154 (position in singularity). These halt the arm
  at the controller level, and the error surfaces in the module's
  response. The motion service does not have a pre-check that
  prevents these; they happen at execution time.
- **Joint limit enforcement.** Every vendor's controller enforces its
  own joint limits. Viam's kinematics file can narrow the range
  (through `input_range_override` in the motion service config), but
  cannot widen it.
- **Real-time control ceilings.** Vendor interfaces like EGM (ABB)
  and URScript servoing (UR) have hard limits on how fast you can
  stream new targets. Modules that use these interfaces inherit
  those limits. For UR-family arms, the 500 Hz control loop is a
  real ceiling; Viam cannot make the arm accept faster updates than
  the vendor controller will process.
- **Default speed profiles.** If you do not specify velocity or
  acceleration (through `MoveOptions` for Go callers, or by relying
  on defaults for Python callers), the module picks a vendor-
  appropriate default. Different modules pick different defaults.
- **Vendor-specific programming language features.** If you rely on
  KRL's `CIRC` motion instruction or RAPID's `MoveL` with zones, the
  module typically does not expose those directly. Use Viam's
  `LinearConstraint` for straight-line motion as a substitute.

## What you gain over vendor-specific SDKs

- **Portability.** Code written against the Viam API runs unchanged
  across vendors. Swap the arm module in config; redeploy.
- **Obstacle-aware motion out of the box.** Viam's motion service
  ships with collision-free planning. Vendor SDKs vary: some have
  motion planners, some do not. You get a uniform capability through
  Viam.
- **Network-accessible from application code.** Call the arm from
  Python, Go, or any other SDK, from anywhere on the network the
  Viam app reaches. No vendor-specific deployment requirements.
- **Fleet deployment.** Fragments let you roll the same motion logic
  across a fleet with different arm hardware.
- **Vocabulary and workflow alignment.** The same frame system,
  obstacles, constraints, and monitoring work for industrial arms
  and for research-oriented arms like xArm alike.

## What you give up

- **Vendor-specific tooling.** Pendants, vendor simulation
  environments (RobotStudio, KUKA.Sim), teach-by-demonstration
  workflows that assume a specific controller.
- **Direct access to vendor programming languages.** You cannot call
  KRL procedures from Viam; you can call `DoCommand` on the arm
  module if the module author exposed a passthrough, but that is
  module-specific.
- **Fine-grained trajectory blending.** Advanced vendor features like
  ABB's concurrent motion, KUKA's smooth path blending with
  continuous velocity, and similar real-time tooling are not
  uniformly exposed.

## Getting started with an industrial arm on Viam

1. Find the module for your arm in the Viam registry. Common
   industrial arm modules include UR, xArm, KUKA LBR iiwa, ABB
   GoFa, and others. Module availability changes; check the registry
   for current options.
2. Follow the module's configuration instructions to connect Viam
   to your arm controller. The configuration is module-specific
   (IP address, port, sometimes safety configuration).
3. Configure the arm's frame and any geometries. See
   [Arm with gripper and wrist camera](/motion-planning/frame-system-how-to/arm-gripper-camera/)
   or a sibling frame-how-to for your hardware layout.
4. Call `motion.Move` or `arm.MoveToPosition` from your SDK.

## What's next

- [Move an arm to a pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  the Viam workflow for Cartesian arm motion.
- [Move by joint positions](/motion-planning/motion-how-to/move-arm-joint-positions/):
  joint-space control, useful when you need specific postures.
- [Configure motion constraints](/motion-planning/constraints/):
  the closest analog to industrial CIRC and MoveL-with-zones.
- [How motion planning works](/motion-planning/how-planning-works/):
  what the planner does before the vendor controller takes over.
