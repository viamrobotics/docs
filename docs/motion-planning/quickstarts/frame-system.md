---
linkTitle: "Configure a frame system"
title: "Quickstart: configure a frame system"
weight: 20
layout: "docs"
type: "docs"
description: "Set up a table-mounted arm with a gripper and a wrist camera, and verify the frame configuration with TransformPose."
---

Every multi-component machine eventually hits the same question: when the
camera sees an object, where is it in the arm's world? Frames answer that.

This quickstart configures three components in a parent-child frame
hierarchy (see the tree below) and shows how a point detected in the
camera's frame becomes coordinates the arm can reach. You verify the
hierarchy two ways: by printing each component's world-frame pose, and
by transforming a detected point from the camera frame into the world
frame.

Everything runs on fake components. When you later replace any of them
with real hardware, the frame configuration and the verification code
stay the same.

Expected time: about 15 minutes.

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

1. Click **+** and select **Blocks**.
2. Search for **arm** and choose the **arm/fake** component.
3. Name it **my-arm** and click **Add to machine**.
4. In the arm's attributes, set `arm-model` to `"ur5e"`.
5. Click **Frame** on the arm's card. The Frame section is a JSON
   editor: edit the frame's fields directly as JSON.
   Edit the JSON so the frame sits at the world origin:

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

Click **Save** in the top-right of the page (or press ⌘/Ctrl+S).

## 2. Add the gripper

1. Click **+** and select **Blocks**.
2. Search for **gripper** and choose the **gripper/fake** component.
3. Name it **my-gripper** and click **Add to machine**.
4. Click **Frame** on the gripper's card. Edit the JSON so the
   parent is the arm and the origin is offset 110 mm along the arm's
   end effector's z axis (a typical gripper body length). A frame
   parented to an arm attaches to the arm's end effector:

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

1. Click **+** and select **Blocks**.
2. Search for **camera** and choose the **camera/fake** component.
3. Name it **my-camera** and click **Add to machine**.
4. Click **Frame** on the camera's card. Edit the JSON so the camera
   sits 30 mm to the side of the arm's end effector and 60 mm above it,
   tilted 30 degrees away from the arm's tool axis:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 30, "z": 60 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": -0.5, "z": 0.87, "th": 0 }
  }
}
```

In `ov_degrees`, `(x, y, z)` is the direction the frame's z axis points
in the parent frame, and `th` spins the frame about that direction. A
camera's z axis is its lens, so `(0, -0.5, 0.87)` tips the lens
30 degrees away from the arm's tool axis. Viam normalizes the vector
for you. For the full format, see
[orientation vectors](/motion-planning/reference/orientation-vectors/).

Click **Save**. You now have three components in a frame tree: the arm
based at the world origin, the gripper 110 mm out from its end
effector, and the camera offset to the side and tilted.

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
              my-arm : X: -817.20 Y: -232.90 Z:   62.80 OX:   0.00 OY:  -1.00 OZ:   0.00 Theta:  90.00
          my-gripper : X: -817.20 Y: -342.90 Z:   62.80 OX:   0.00 OY:  -1.00 OZ:   0.00 Theta:  90.00
           my-camera : X: ...
```

Each line is that component's frame origin expressed in the world
frame. An arm's printed pose is its end effector, the end of the
kinematic chain, so `my-arm` prints where the UR5e's end effector sits
at its zero joint configuration rather than the world origin where you
placed the arm's base. The gripper prints 110 mm from the end effector
along the end effector's z axis (which points along world -y at this
configuration), and the camera prints at its own offset from the same
end effector.

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
You will see all three poses change together: `my-arm` prints the end
effector's new pose, and the gripper and camera stay at their fixed
offsets from it wherever it moves. That is the parent-child
propagation in action: the camera and gripper frames are fixed
relative to the arm's end effector, so they move wherever it moves.

## What you learned

- Frames form a tree rooted at `world`.
- Each component's frame config specifies a parent, a translation in
  mm, and an orientation.
- Child frames move with their parents automatically.
- `TransformPose` converts between any two frames using the current
  configured tree and live component state.

## Where to next

- [Allow specific frames to collide](/motion-planning/obstacles/allow-frame-collisions/):
  required when the wrist camera sees the arm it is mounted on.
- [Move your first arm](/motion-planning/quickstarts/first-arm/):
  if you have not already; now you can give the motion service a
  pose in the camera frame and have it reach that point.
- [Frame system](/motion-planning/frame-system/): the concept page
  with more detail on hierarchy, orientation formats, and geometry.
- [Frame system API](/motion-planning/reference/frame-system-api/):
  the full method list for pose queries and transforms.
