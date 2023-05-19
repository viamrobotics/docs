---
title: "Get Started Programming your Robot with Viam's SDKs"
linkTitle: "Get Started with Viam's SDKs"
weight: 40
type: "docs"
description: "Get started writing a client application with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
aliases:
  - "product-overviews/sdk-as-client"
  - "program/sdk-as-client"
---

Viam offers software development kits (SDKs) in popular languages which

- Streamline connection, authentication, and encryption against a server using {{< glossary_tooltip term_id="webrtc" >}}
- Enable you to interface with robots without calling the `viam-server` [gRPC APIs for robot controls](https://github.com/viamrobotics/api) directly

![Diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.](../img/sdks/robot-client.png)

Use the SDK of your preferred language to write code to control your robots.

<!-- | Python | Go | TypeScript |
| ------ | -- | ---------- |
| https://python.viam.dev/ | https://pkg.go.dev/go.viam.com/rdk | https://ts.viam.dev/ | -->

## Requirements

Before you get started, ensure that you have [installed and connected to `viam-server`](/installation/) on the computer you want to use to control a robot [(likely a single-board computer)](/components/board/#configuration) and [configured a robot](/configuration/#local-setup).

The easiest way to do this is:

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **Setup** tab and follow the instructions there.
4. [Configure](../../manage/configuration) your robot.

Then, run one of the following commands in your terminal to install a Viam SDK on your development machine:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip install viam-sdk
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go install go.viam.com/rdk/robot/client@latest
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install --save @viamrobotics/sdk
```

{{% /tab %}}
{{< /tabs >}}

## Hello World: The Code Sample Tab

Save a program in the language of your choice that connects to your robot and uses methods built into the SDK's client API libraries to [interact with and control](/program/write/) the {{< glossary_tooltip term_id="resource" text="resources" >}} on the robot.

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **Code Sample** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your {{< glossary_tooltip term_id="remote" text="remote">}} or local robot.
These code snippets import all the necessary libraries and sets up a connection with your robot in the cloud through the Viam app.

Your boilerplate code sample should look similar to this:

{{%expand "Click this to see example boilerplate code from the Code Sample tab" %}}
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
{{% /expand%}}

Save this file on your development machine with the file type of your preferred SDK.

Edit the boilerplate code by [adding control logic](/program/write/) to make a client application that connects to your robot controls it in the way you want when the program [is executed](/program/run/).

Then, execute this program on any computing machine as long as:

1. You have installed the appropriate SDK and language on this machine.
2. The program establishes a connection to your robot through the cloud, on a local or wide area network (LAN or WAN), or locally (should be the same machine as is running `viam-server`).

See [Run SDK Code](/program/run) for more information on executing programs to control your Viam-connect robot.

<!-- TODO: transition between these sections? introduction? -->

### `import`

The Code Sample tab contains the required imports for the SDK code at generation.

If you are building out your program further or aren't using the Code Sample tab, you can find the right libraries to import to utilize SDK methods, typing, interfaces, and utilities at the start of [each resource's API documentation](/program/write/resource-apis/), as well as in the individual SDK documentation sites and [on GitHub](https://github.com/viamrobotics/rdk).

### `connect()`

{{< readfile "/static/include/snippet/secret-share.md" >}}

The `connect()` function established a connection through webRTC (TODO check this)

### `main()`
  
- (THIS LANGUAGE IS PYTHON SPECIFIC, WILL NEED TO ADJUST FOR DIFFERENT TABS) In the main() function of your code, as shown in the above Code Sample, you must ...
- directs to "interface with resources" page
