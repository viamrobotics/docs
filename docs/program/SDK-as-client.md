---
title: "Program your Robot with Viam's SDKs"
linkTitle: "Program your Robot with Viam's SDKs"
weight: 40
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to write code to access and control your robot."
tags: ["client", "sdk"]
---

Viam offers software development kits (SDKs) that wrap the `viam-server` [gRPC](https://grpc.io/) [APIs](https://github.com/viamrobotics/api) and streamline connection, authentication, and encryption.

<img src="../img/SDK-as-client/image1.png" alt="Example diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.">

Use the SDK of your preferred language to write code to control your robots.

Viam currently offers SDKs for the following three languages:

- [Python SDK](https://python.viam.dev/)
- [Go SDK](https://pkg.go.dev/go.viam.com/rdk)
- [TypeScript SDK](https://ts.viam.dev/)

Click on the links above to read more about installation and usage of each SDK.

## Installation

{{< tabs >}}
{{% tab name="Python" %}}

```shell
pip install viam-sdk
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install --save @viamrobotics/sdk
```

{{% /tab %}}
{{< /tabs >}}

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

### Code Samples

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **CODE SAMPLE** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your remote or local robot.

{{% alert title="Caution" color="caution" %}}

Do not share your robot secret or robot address publicly.
Sharing this information compromises your system security by allowing unauthorized access to your computer.

{{% /alert %}}

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

You can easily add control logic for each [component](/components/) of your robot by using the methods Viam has built into each component's API specification.

Find documentation on how to use these methods here:

- [Arm](/components/arm/#api)
- [Base](/components/base/#api)
- [Camera](/components/camera/#api)
- [Gantry](/components/gantry/#api)
- [Input Controller](/components/input-controller/#api)
- [Motor](/components/motor/#api)
- [Servo](/components/servo/#api)
<!--
Board & Sensor API Docs should be added soon on Viam Documentation, + Movement Sensor, Encoder, Gripper
-->

## Run Your Code

After saving your boilerplate code sample and adding control logic with Viam's API methods, run your program to control your Viam-connected robot.

For example:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go run ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

For an example, see [this execution demo.](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla)

{{% /tab %}}
{{< /tabs >}}

## Next Steps

{{< cards >}}
  {{% card link="/components" size="small" %}}
  {{% card link="/services" size="small" %}}
{{< /cards >}}
