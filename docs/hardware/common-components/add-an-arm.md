---
linkTitle: "Arm"
title: "Add an arm"
weight: 5
layout: "docs"
type: "docs"
description: "Add and configure a robotic arm, verify joint motion, and test end-effector positioning."
date: "2025-03-07"
aliases:
  - /operate/reference/components/arm/
  - /operate/reference/components/arm/eva/
  - /operate/reference/components/arm/yahboom-dofbot/
  - /hardware-components/add-an-arm/
---

Add a robotic arm to your machine's configuration so you can control it from the Viam app and from code.

## Concepts

An arm component controls a multi-jointed robotic arm. The API provides:

- **Joint-level control**: move individual joints to specific angles.
- **End-effector positioning**: move the end effector to a pose in 3D space
  (Viam handles the inverse kinematics).
- **Motion planning integration**: the motion service can plan
  collision-free paths for the arm.

Arm models almost always come from **modules in the registry** because each arm manufacturer has its own communication protocol.
See the Registry modules list below for Viam-maintained arm modules.

The `fake` built-in model is useful for testing code without physical hardware.
It supports kinematics for several arm models (ur5e, ur20, xarm6, xarm7, lite6).

### Built-in models

- [`fake`](/reference/components/arm/fake/) — A model used for testing, with no physical hardware.

### Registry modules

Viam-maintained arm modules:

| Module                                                                       | Arms supported               |
| ---------------------------------------------------------------------------- | ---------------------------- |
| [`viam:ufactory`](https://app.viam.com/module/viam/ufactory)                 | xArm6, xArm7, xArm850, Lite6 |
| [`viam:universal-robots`](https://app.viam.com/module/viam/universal-robots) | UR3e, UR5e, UR7e, UR20       |
| [`viam:yaskawa`](https://app.viam.com/module/viam/yaskawa)                   | GP12, GP180-120              |

For arms not covered above, search for `arm` in the [Viam registry](https://app.viam.com/registry). Each module's configuration is documented on its registry page.

## Steps

### 1. Add an arm component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your arm manufacturer and model:
   - For a UFactory xArm, search for **xArm6** (or xArm5, xArm7, Lite6).
   - For a Universal Robots arm, search for **ur5e** (or ur3e, ur10e, ur16e).
4. Name your arm (for example, `my-arm`) and click **Create**.

### 2. Configure arm attributes

Attributes vary by arm module. Most network-connected arms need a host
address:

**UFactory xArm 6:**

```json
{
  "host": "192.168.1.100",
  "speed_degs_per_sec": 30,
  "acceleration_degs_per_sec_per_sec": 100
}
```

| Attribute                           | Type   | Required | Description                                                                                                                                                                                                                                                                                                      |
| ----------------------------------- | ------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `host`                              | string | Yes      | IP address of the arm's control box. You can find this on a sticker on the control box or in the manufacturer's network settings.                                                                                                                                                                                |
| `speed_degs_per_sec`                | float  | No       | How fast joints rotate, in degrees per second. Range: 3-180. Default: 60. Start low (15-30) when testing a new setup. Increase once you're confident in your configuration and collision boundaries.                                                                                                             |
| `acceleration_degs_per_sec_per_sec` | float  | No       | How quickly joints ramp up to speed, in degrees per second squared. Range: 0-1145. Default: ~382. Lower values produce smoother, more predictable motion, which matters when the arm carries a payload or works near obstacles. Most users don't need to change this unless motion is too jerky or too sluggish. |

These are common attributes for the [UFactory xArm module](https://app.viam.com/module/viam/ufactory-xarm).
Check your module's documentation in the registry for the full list of attributes.
For example, see the [Universal Robots module](https://app.viam.com/module/viam/universal-robots).

### 3. Configure a frame (recommended)

If you plan to use motion planning or coordinate with other components (like a
camera or gripper), add a frame to define the arm's position in your workspace.

This frame places the arm's base at the world origin, which is common for single-arm setups:

```json
{
  "frame": {
    "parent": "world",
    "translation": { "x": 0, "y": 0, "z": 0 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  }
}
```

For two-arm setups, one arm is typically at the world origin and the other is offset by its distance from the first arm in the x and y directions using the `translation` field.

See [Frame System](/motion-planning/frame-system/) for details on configuring frames.

### 4. Save and test

Click **Save**, then expand the **Test** section.

- Use the joint position controls to move individual joints.
- Verify each joint moves in the expected direction.
- Start with slow speeds until you're confident in the configuration.

## Try it with a fake arm

To develop and test code without physical hardware, use the `fake` built-in
model:

```json
{
  "arm-model": "xarm6"
}
```

The fake arm simulates kinematics for the specified model. Set `arm-model` to `ur5e`, `ur20`, `xarm6`, `xarm7`, or `lite6`. It responds to all API calls and reports joint positions, but doesn't move anything physical.

## Control your arm from code

Read the arm's current joint positions, move two joints, and confirm the positions changed.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.

If you're using a real arm, you'll see it physically move when you run the code below.
With a fake arm, the positions update in memory without physical motion, but you can watch the joint values update in real time by expanding the **test** section on the arm's component card in the **CONFIGURE** tab.
The **3D Scene** tab on your machine's page renders the arm's live pose, which also helps visualize simulated motion.

{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `arm_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    arm = Arm.from_robot(robot, "my-arm")

    # Read current joint positions
    joints = await arm.get_joint_positions()
    print(f"Joint positions before move: {joints.values}")

    # Move joints 1 and 2
    new_joints = JointPositions(values=[10, -10, 0, 0, 0, 0])
    await arm.move_to_joint_positions(new_joints)

    # Read joint positions again to confirm the move
    joints = await arm.get_joint_positions()
    print(f"Joint positions after move: {joints.values}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python arm_test.py
```

You should see all zeros before the move, then joints 1 and 2 at 10 and -10 degrees:

```text
Joint positions before move: [0, 0, 0, 0, 0, 0]
Joint positions after move: [10, -10, 0, 0, 0, 0]
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir arm-test && cd arm-test
go mod init arm-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/arm"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("arm-test")

    robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithCredentials(utils.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            Payload: "YOUR-API-KEY",
        }),
        client.WithAPIKeyID("YOUR-API-KEY-ID"),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)

    a, err := arm.FromProvider(robot, "my-arm")
    if err != nil {
        logger.Fatal(err)
    }

    // Read current joint positions
    joints, err := a.JointPositions(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Joint positions before move: %v\n", joints)

    // Move joints 1 and 2
    newJoints := []referenceframe.Input{
        {Value: 10}, {Value: -10}, {Value: 0},
        {Value: 0}, {Value: 0}, {Value: 0},
    }
    err = a.MoveToJointPositions(ctx, newJoints, nil)
    if err != nil {
        logger.Fatal(err)
    }

    // Read joint positions again to confirm the move
    joints, err = a.JointPositions(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Joint positions after move: %v\n", joints)
}
```

Run it:

```bash
go run main.go
```

You should see all zeros before the move, then joints 1 and 2 at 10 and -10 degrees.

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Cannot connect to arm" >}}

- Check the **Error logs** section on the arm's configuration card for initialization failures, and the **LOGS** tab for anything else `viam-server` printed on startup.
- Verify the arm is powered on and connected to the same network as your machine.
- Ping the arm's IP address from the machine to confirm network connectivity.
- Check that no other software (manufacturer's own control software) has an exclusive connection to the arm.

{{< /expand >}}

{{< expand "Arm moves but positions are wrong" >}}

- Verify the frame configuration matches the arm's physical placement.
- If using motion planning, check that the kinematics model matches your
  arm. Using the wrong model causes incorrect inverse kinematics.

{{< /expand >}}

{{< expand "Motion planning fails" >}}

- Ensure the arm has a frame configured with `parent: "world"`.
- Check that the target pose is within the arm's reachable workspace.
- See [Obstacles](/motion-planning/obstacles/) for configuring obstacles and
  [Constraints](/motion-planning/move-an-arm/constraints/) for motion constraints.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/arm.md" >}}

## Related

- [Arm API reference](/reference/apis/components/arm/): full method documentation.
- [Fragments](/hardware/fragments/): save and reuse working
  hardware configurations.
- [Motion Planning](/motion-planning/): configure frames, kinematics, and
  obstacles for motion planning.
- [What is a module?](/build-modules/overview/): write a module that
  coordinates the arm with sensors.
