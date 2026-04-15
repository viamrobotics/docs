---
linkTitle: "Move your first arm"
title: "Quickstart: move your first arm"
weight: 10
layout: "docs"
type: "docs"
description: "From zero to an arm moving under motion service control, using a fake arm that runs on any machine."
---

In this quickstart we will configure a fake arm with UR5e kinematics,
connect to it from Python, and call the motion service to drive the
arm's end effector to a target pose. The whole thing runs on any
machine that has `viam-server`; no physical arm required. When you
have a real UR5e (or any other arm with a Viam module) later, the only
change is the component model name in config.

By the end you will have:

- A fake arm running on your machine.
- Code that reads the arm's current pose and calls `motion.Move` to
  drive it to a new pose.
- A verification step confirming the arm ended where you commanded.

Expected total time: about 10 minutes.

## 1. Set up the machine

In the [Viam app](https://app.viam.com), create a new machine or use
an existing one that has `viam-server` running. Go to its
**CONFIGURE** tab.

## 2. Add the fake arm component

1. Click **+** and choose **Component**.
2. Select **arm**.
3. Choose the **fake** model.
4. Name the component **my-arm**.
5. Click **Create**.

In the arm's configuration card, set the `arm-model` attribute to
`"ur5e"` so the fake arm exposes UR5e kinematics:

```json
{
  "arm-model": "ur5e"
}
```

Click **Save**. The fake arm is now running with UR5e geometry and
joint limits.

## 3. Connect and read the current pose

Go to the **CONNECT** tab in the Viam app, select **Python**, and
copy the snippet that includes your machine address and API key.

Create a file named `first_arm.py`:

```python
import asyncio

from viam.robot.client import RobotClient
from viam.components.arm import Arm
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def main():
    async with await connect() as machine:
        my_arm = Arm.from_robot(machine, "my-arm")

        # Read the current end-effector pose in the world frame.
        start = await my_arm.get_end_position()
        print(f"start pose: x={start.x:.1f} y={start.y:.1f} z={start.z:.1f}")


if __name__ == "__main__":
    asyncio.run(main())
```

Replace the three placeholder strings with your machine's address and
API key values from the **CONNECT** tab. Then run:

```sh
pip install viam-sdk
python first_arm.py
```

You should see something like:

```text
start pose: x=-817.2 y=-191.0 z=-5.0
```

The exact values depend on the fake arm's default joint positions.
What matters is that the arm responds and returns a pose.

## 4. Command a motion

Now extend the script to plan and execute a motion through the motion
service. Replace the `main` function with:

```python
async def main():
    async with await connect() as machine:
        my_arm = Arm.from_robot(machine, "my-arm")
        motion_service = MotionClient.from_robot(machine, "builtin")

        # 1. Read the starting pose.
        start = await my_arm.get_end_position()
        print(f"start pose: x={start.x:.1f} y={start.y:.1f} z={start.z:.1f}")

        # 2. Build a target pose 100 mm in front of the start, keeping
        # orientation unchanged.
        destination = PoseInFrame(
            reference_frame="world",
            pose=Pose(
                x=start.x + 100,
                y=start.y,
                z=start.z,
                o_x=start.o_x,
                o_y=start.o_y,
                o_z=start.o_z,
                theta=start.theta,
            ),
        )

        # 3. Plan and execute.
        print("moving...")
        await motion_service.move(
            component_name="my-arm",
            destination=destination,
        )
        print("done.")

        # 4. Verify the final pose.
        end = await my_arm.get_end_position()
        print(f"end pose:   x={end.x:.1f} y={end.y:.1f} z={end.z:.1f}")
```

Run it again:

```sh
python first_arm.py
```

Expected output:

```text
start pose: x=-817.2 y=-191.0 z=-5.0
moving...
done.
end pose:   x=-717.2 y=-191.0 z=-5.0
```

The X coordinate moved by 100 mm. Y and Z remained the same. Because
the fake arm has no real hardware, the motion completes instantly and
exactly at the commanded pose.

## 5. What happened

Under the hood, the motion service:

1. Asked the frame system for the arm's current joint state.
2. Used the UR5e kinematics from the fake module to compute where the
   end effector is right now.
3. Ran the cBiRRT planner to find a joint-space path from the current
   configuration to one that places the end effector at the target
   pose.
4. Smoothed the path and commanded the fake arm to follow it.

Because the fake arm has no obstacles and no real dynamics, every
step is instantaneous and deterministic. With a real arm, the same
call takes longer, may fail on unreachable poses, and needs obstacle
information through `WorldState` for anything beyond an empty
workspace.

## Where to next

- **Add obstacles.** Pass a `WorldState` with a `Geometry` to the
  `move` call and try to drive the arm _through_ it. The planner
  will either route around it or fail, depending on where you place
  it. See [Define obstacles](/motion-planning/obstacles/).
- **Move in joint space instead.**
  [`MoveToJointPositions`](/motion-planning/motion-how-to/move-arm-joint-positions/)
  bypasses the planner and drives the joints directly. Useful when
  you want predictable postures.
- **Configure a multi-component machine.** Add a gripper and a
  camera to your arm and wire up the frame system in
  [Quickstart: configure a frame system](/motion-planning/quickstarts/frame-system/).
- **Replace the fake arm with real hardware.** Change `model` on
  your arm component from `fake` to the module that matches your
  physical arm. The Python code above does not change.
