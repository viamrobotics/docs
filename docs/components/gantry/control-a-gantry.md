---
title: "Control a Gantry"
linkTitle: "Control a Gantry"
draft: true
weight: 50
type: "docs"
description: "How to control a gantry component with Viam's Client SDK libraries."
tags: ["gantry", "components"]
icon: "img/components/gantry.png"
# SME: Rand
---

## API

The gantry component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
[Position](#position) | [Position][go_gantry]  |  [get_position][python_get_position] | Get the current positions of the axes of the gantry in mm. |
[MoveToPosition](#movetoposition) |  [MoveToPosition][go_gantry] | [move_to_position][python_move_to_position] | Move the axes of the gantry to the desired positions. |
[Lengths](#lengths) | [Lengths][go_gantry] | [get_lengths][python_get_lengths] | Get the lengths of the axes of the gantry in mm. |
[Stop](#stop) | [Stop][go_gantry] | [stop][python_stop] | Stop the gantry from moving. |
[IsMoving](#ismoving) | [IsMoving][go_gantry] | [is_moving][python_is_moving] | Get if the gantry is currently moving. |

[go_gantry]: https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry
[python_get_position]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.get_position
[python_move_to_position]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.move_to_position
[python_get_lengths]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.get_lengths
[python_stop]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.stop
[python_is_moving]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.is_moving

### Control your gantry with Viam's Client SDK Libraries

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/[COMPONENT_TYPE]/index.html)
- [Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/gantry])

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app.
Check out the [Client SDK Libraries Quick Start](/product-overviews/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/program/app-usage/) for app-specific guidance.

{{% /alert %}}

The following example assumes you have a gantry  called "my_gantry" configured as a component of your robot.
If your gantry has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import GantryClient
from viam.proto.common import WorldState

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot. 
    print('Resources:')
    print(robot.resource_names)

    # Connect to your gantry.
    myGantry = GantryClient.from_robot(robot=robot, name='my_gantry')

    # Disconnect from your robot. 
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
 "go.viam.com/rdk/components/gantry"
 "go.viam.com/rdk/referenceframe"
)

func main() { 

  // Create an instance of a logger. 
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot. 
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      })),
  )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits. 
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot. 
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Connect to your gantry.
  myGantry, err := gantry.FromRobot(robot, "my_gantry")
  if err != nil {
    logger.Fatalf("cannot get gantry: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

### Position

Get the current position

### MoveToPosition

### Lengths

### Stop

### IsMoving

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
