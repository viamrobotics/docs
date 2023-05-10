---
title: "Get Started Programming your Robot with Viam's SDKs"
linkTitle: "Write Code"
weight: 40
type: "docs"
description: "Access and control your robot with the resource and robot APIs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
aliases:
  - "product-overviews/sdk-as-client"
  - "program/sdk-as-client"
---

## Connect to your robot

## Code Sample

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **Setup** tab and follow the instructions there.
4. [Configure](../../manage/configuration) your robot.

{{% /alert %}}

TODO: Should similar alert also be in main index file?

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **Code Sample** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your {{< glossary_tooltip term_id="remote" text="remote">}} or local robot.
These code snippets import all the necessary libraries and sets up a connection with the Viam app in the cloud.

{{< readfile "/static/include/snippet/secret-share.md" >}}

Your boilerplate code sample should look similar to this:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET FROM THE VIAM APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
  "context"

  "github.com/edaniels/golog"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := golog.NewDevelopmentLogger("client")
  robot, err := client.New(
      context.Background(),
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "SECRET FROM THE VIAM APP",
      })),
  )
  if err != nil {
      logger.Fatal(err)
  }
  defer robot.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< alert title="Note" color="note" >}}
The TypeScript SDK currently only support building web browser apps.
{{< /alert >}}

```ts {class="line-numbers linkable-line-numbers"}
import { Client, createRobotClient, RobotClient } from '@viamrobotics/sdk';

async function connect() {
  // You can remove this block entirely if your robot is not authenticated.
  // Otherwise, replace with an actual secret.
  const secret = '<SECRET>';
  const credential = {
    payload: secret,
    type: 'robot-location-secret',
  };

  // Replace with the host of your actual robot running Viam.
  const host = "<HOST>";

  // Replace with the signaling address. If you are running your robot on Viam,
  // it is most likely https://app.viam.com:443.
  const signalingAddress = 'https://app.viam.com:443';

  const iceServers = [{ urls: 'stun:global.stun.twilio.com:3478' }];

  return createRobotClient({
    host,
    credential,
    authEntity: host,
    signalingAddress,
    iceServers
  });
}

async function main() {
  // Connect to client
  let client: Client;
  try {
    client = await connect();
    console.log('connected!');

    let resources = await client.resourceNames();
    console.log('Resources:');
    console.log(resources);
  } catch (error) {
    console.log(error);
    return;
  }
}

main();
```

{{% /tab %}}
{{< /tabs >}}

## Add Control Logic

<!-- You can add control logic for each [component](/components/) of your robot by using the built-in component methods.

Find documentation on how to use these methods here:

- [Arm](/components/arm/#api)
- [Base](/components/base/#api)
- [Camera](/components/camera/#api)
- [Gantry](/components/gantry/#api)
- [Gripper](/components/gripper/#api)
- [Input Controller](/components/input-controller/#api)
- [Motor](/components/motor/#api)
- [Movement Sensor](/components/movement-sensor/#api)
- [Sensor](/components/sensor/#api)
- [Servo](/components/servo/#api)

You can find example code in the [Python SDK example GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1), the [Golang SDK example GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples), or the [TypeScript SDK example GitHub repository](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples). -->
