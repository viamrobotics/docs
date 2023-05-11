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

![Diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.](../img/sdks/image1.png)

Use the SDK of your preferred language to write code to control your robots.

Viam currently offers SDKs for the following three languages:

| Python | Go | TypeScript |
| ------ | -- | ---------- |
| https://python.viam.dev/ | https://pkg.go.dev/go.viam.com/rdk | https://ts.viam.dev/ |

## Requirements

Before you get started, ensure that you:

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **Setup** tab and follow the instructions there.
4. [Configure](../../manage/configuration) your robot.
<!-- TODO: above is really the most important requirement, how to separate out for non-app users? -->

- TODO: Go over why you need to install these SDKs and what computer you need to have them on!
- can help clear up the thing matt was saying about potential candidate being confused about what computer she needed to have viam-server or an SDK installed on? 

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

- instructions as to how to create a file, where to save this file, what's happening in alignment with configuration etc.

TODO: will probably need to put the note below somewhere else but I am not sure where yet? lol

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **Code Sample** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your {{< glossary_tooltip term_id="remote" text="remote">}} or local robot.
These code snippets import all the necessary libraries and sets up a connection with the Viam app in the cloud.

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

### `import`

- talks about how code sample should generally generate all the required resources but if not or if you're not working with that, describes what they'll be?

### `connect()`

{{< readfile "/static/include/snippet/secret-share.md" >}}

- where to find robot secret, location secret, etc

### `main()`
  
- (THIS LANGUAGE IS PYTHON SPECIFIC, WILL NEED TO ADJUST FOR DIFFERENT TABS) In the main() function of your code, as shown in the above Code Sample, you must ...
- directs to "interface with resources" page

<!-- #### The Control Tab: built-in UI for control

- this maybe shouldn't go here but I want users to be more aware of this  -->

## Run Code

-- directs to "run your code page" lol 

## Debug

- logging tab or accessing logs when running viam-server process on whatever computer is doing so 

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
