---
title: "Using Our SDKs for a Client Application"
linkTitle: "SDKs"
weight: 30
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to access and control your robot."
tags: ["client", "sdk"]
---

Viam offers SDKs in popular languages which wrap the `viam-server` [gRPC](https://grpc.io/) APIs and streamline connection, authentication, and encryption against a server.
Using the SDK, you will be able to quickly write code to control and automate your robots.

Viam-server exposes gRPC [APIs for robot controls](https://github.com/viamrobotics/api).
It also supports [WebRTC](https://webrtcforthecurious.com/) connectivity and authentication over those APIs.

SDKs make it easier to interface with the robot without calling the gRPC API directly.

<img src="../img/SDK-as-client/image1.png" alt="Example diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client."><br>

## Viam's Client SDK Libraries

Viam's Client SDKs support several ways to connect and control your robots, with many new ways to connect coming soon.

- [Python SDK](https://python.viam.dev/)

- [Go SDK](https://pkg.go.dev/go.viam.com/rdk)

- [TypeScript SDK](https://ts.viam.dev/)

## Quick Start Examples

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

- Go to [app.viam.com](https://app.viam.com/).

- Create a new robot.

- Go to the **SETUP** tab and follow the instructions there.

- Install either the [Go](https://pkg.go.dev/go.viam.com/rdk), [Python](https://python.viam.dev/), or [TypeScript](https://ts.viam.dev/) SDK on your computer.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

You can find more examples of Viam's SDKs in the <file>examples</file> folder of the [Python SDK GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1), the [Go SDK GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples), or the [TypeScript SDK GitHub repository](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples).

{{% /alert %}}

### How to connect to your robot with Viam

The easiest way to get started writing an application with Viam, is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **CODE SAMPLE** tab, and copy the boilerplate code from the section labeled **Python SDK** or **Go SDK**.
These code snippets import all the necessary libraries and set up a connection with the Viam app in the cloud.

{{% alert title="Caution" color="caution" %}}
Do not share your robot secret or robot address publicly.
Sharing this information compromises your system security by allowing unauthorized access to your computer.
{{% /alert %}}

The SDK connect script should look something like this:

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

## Next Steps

{{< cards >}}
  {{< card link="/components" size="small">}}
  {{< card link="/services" size="small">}}
  {{< card link="/components" size="small">}}
{{< /cards >}}
