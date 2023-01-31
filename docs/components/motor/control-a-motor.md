---
title: "Control a Motor"
linkTitle: "Control a Motor"
weight: 15
type: "docs"
description: "The Viam motor API"
# SMEs: Rand, James
---

## Usage example

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you, go to [app.viam.com](https://app.viam.com/), create a new robot and go to the **SETUP** tab and follow the instructions there.

The following example assumes motors called "motor1" and "motor2" are configured as components of your robot.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

This example sends power commands to motors on the robot.

```python
from viam.components.motor import Motor

robot = await connect() # refer to connect code
motor1 = Motor.from_robot(robot, "motor1")
motor2 = Motor.from_robot(robot, "motor2")

# power motor1 at 100% for 3 seconds
await motor1.set_power(1)
await asyncio.sleep(3)
await motor1.stop()

# run motor2 at 1000 rpm for 200 rotations
await motor2.go_for(1000, 200)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"time"
"go.viam.com/rdk/components/motor"
)

robot, err := client.New() // refer to connect code
// grab the motors from the robot
m1, err := motor.FromRobot(robot, "motor1")
m2, err := motor.FromRobot(robot, "motor2")

// power motor1 at 100% for 3 seconds
m1.SetPower(context.Background(), 1, nil)
time.Sleep(3 * time.Second)
m1.Stop(context.Background(), nil)

// run motor2 at 1000 RPM for 200 rotations
m2.GoFor(context.Background(), 1000, 200, nil)
```

{{% /tab %}}
{{< /tabs >}}
