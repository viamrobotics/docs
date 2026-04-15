---
linkTitle: "Configure a frame system"
title: "Quickstart: configure a frame system"
weight: 20
layout: "docs"
type: "docs"
description: "Set up a table-mounted arm with a gripper and a wrist camera, and verify the frame configuration with TransformPose."
---

In this quickstart we will configure three components with a
parent-child frame hierarchy: a table-mounted UR5e arm, a gripper
attached to the arm's end effector, and a wrist-mounted camera. We
will verify the configuration by asking Viam where each component is
in the world frame, and by transforming a detected object from the
camera frame to the world frame.

Everything uses fake components. Swap any of them for a real
hardware module later and the frame relationships and verification
code are unchanged.

Expected total time: about 15 minutes.

## What you will end up with

```text
world
├── my-arm          (table-mounted, at world origin)
│   ├── my-gripper  (attached to arm end effector)
│   └── my-camera   (mounted on arm near gripper)
```

## 1. Add the arm

In the [Viam app](https://app.viam.com), go to your machine's
**CONFIGURE** tab.

1. Click **+** and add an **arm** component.
2. Choose the **fake** model.
3. Name it **my-arm**.
4. In the arm's attributes, set `arm-model` to `"ur5e"`.
5. Click **Frame** on the arm's card and edit the JSON so the frame
   sits at the world origin:

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Click **Save**.

## 2. Add the gripper

1. Click **+** and add a **gripper** component.
2. Choose the **fake** model.
3. Name it **my-gripper**.
4. Click **Frame** on the gripper's card. Edit the JSON so the
   parent is the arm and the origin is offset 110 mm along the arm's
   z axis (the end of a typical gripper mount):

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 0, "z": 110 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Click **Save**. Because the gripper's parent is the arm, its world
pose moves with the arm automatically.

## 3. Add the camera

1. Click **+** and add a **camera** component.
2. Choose the **fake** model.
3. Name it **my-camera**.
4. Click **Frame**. Edit the JSON so the camera sits 30 mm to the
   side of the arm's end effector and 60 mm above it, tilted 30 degrees
   downward about the x axis:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 30, "z": 60 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 1, "y": 0, "z": 0, "th": -30 }
  }
}
```

Click **Save**.

## 4. Verify with the CLI

Before writing any code, confirm the configuration parsed correctly:

```sh
viam machines part motion print-config --part "YOUR-PART-NAME"
```

You should see `my-arm`, `my-gripper`, and `my-camera` in the output
with the translations and orientations you just configured.

Now print the live world poses:

```sh
viam machines part motion print-status --part "YOUR-PART-NAME"
```

You should see something like:

```text
              my-arm : X:    0.00 Y:    0.00 Z:    0.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:   0.00
          my-gripper : X:    0.00 Y:    0.00 Z:  110.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:   0.00
           my-camera : X:    0.00 Y:   30.00 Z:   60.00 OX:  ...
```

The gripper sits 110 mm above the arm origin. The camera sits 30 mm
to the side and 60 mm above, with the downward tilt reflected in the
orientation vector.

## 5. Transform a detected object to the world frame

Imagine the camera detects an object 200 mm in front of it. You want
to know where that object is in world coordinates so the arm can
reach for it.

```python
import asyncio

from viam.robot.client import RobotClient
from viam.proto.common import PoseInFrame, Pose


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def main():
    async with await connect() as machine:
        # The camera reports the object at (0, 0, 200) in its own frame:
        # 200 mm straight ahead along the camera's z axis.
        detected = PoseInFrame(
            reference_frame="my-camera",
            pose=Pose(x=0, y=0, z=200),
        )

        # Transform to the world frame.
        in_world = await machine.transform_pose(detected, "world")

        print(
            f"object in world: "
            f"x={in_world.pose.x:.1f} "
            f"y={in_world.pose.y:.1f} "
            f"z={in_world.pose.z:.1f}"
        )


if __name__ == "__main__":
    asyncio.run(main())
```

Run it. The output shows the object's world-frame coordinates,
computed from the camera's frame configuration including its
translation, downward tilt, and the arm's current pose.

## 6. Move the arm and watch the camera frame follow

Change the arm's joint configuration (through the **CONTROL** tab or
by calling `move_to_joint_positions`), then re-run `print-status`.
You will see `my-camera` and `my-gripper` poses change while
`my-arm` stays at the world origin. That is the parent-child
propagation in action: the camera and gripper frames are fixed
relative to the arm, so they move wherever the arm moves.

## What you learned

- Frames form a tree rooted at `world`.
- Each component's frame config specifies a parent, a translation in
  mm, and an orientation.
- Child frames move with their parents automatically.
- `TransformPose` converts between any two frames using the current
  configured tree and live component state.

## Where to next

- [Allow specific frames to collide](/motion-planning/motion-how-to/allow-frame-collisions/):
  required when the wrist camera sees the arm it is mounted on.
- [Move your first arm](/motion-planning/quickstarts/first-arm/):
  if you have not already; now you can give the motion service a
  pose in the camera frame and have it reach that point.
- [Frame system](/motion-planning/frame-system/): the concept page
  with more detail on hierarchy, orientation formats, and geometry.
- [Frame system API](/motion-planning/reference/frame-system-api/):
  the full method list for pose queries and transforms.
