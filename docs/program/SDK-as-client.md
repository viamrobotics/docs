---
title: "Program your Robot with Viam's SDKs"
linkTitle: "Program your Robot with Viam's SDKs"
weight: 40
type: "docs"
description: "Use Viam's SDKs to write code to access and control your robot."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

Viam offers software development kits (SDKs) in popular languages which

- Streamline connection, authentication, and encryption using against a server with {{< glossary_tooltip term_id="webrtc" >}}
- Enable you to interface with robots without calling the `viam-server` [gRPC APIs for robot controls](https://github.com/viamrobotics/api) directly

<img src="../img/SDK-as-client/image1.png" alt="Diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.">

Use the SDK of your preferred language to write code to control your robots.

Viam currently offers SDKs for the following three languages:

- [Python SDK](https://python.viam.dev/)
- [Go SDK](https://pkg.go.dev/go.viam.com/rdk)
- [TypeScript SDK](https://ts.viam.dev/)

Click on the links above to read more about installation and usage of each SDK.

## Install an SDK

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

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **setup** tab and follow the instructions there.
4. [Configure](../../manage/configuration) your robot.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

You can find more examples of Viam's SDKs in the <file>examples</file> folder of the [Python SDK GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1), the [Go SDK GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples), or the [TypeScript SDK GitHub repository](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples).

{{% /alert %}}

### Connect to your robot

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **code sample** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your {{< glossary_tooltip term_id="remote" text="remote">}} or local robot.
These code snippets import all the necessary libraries and sets up a connection with the Viam app in the cloud.

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

You can add control logic for each [component](/components/) of your robot by using the built-in component methods.

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

You can find example code in the [Python SDK example GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1), the [Golang SDK example GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples), or the [TypeScript SDK example GitHub repository](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples).

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

### Run Code Locally

If you need to run [PID control loops](https://en.wikipedia.org/wiki/PID_controller) or other on-robot code, you can run control code on the same board that is running `viam-server`.

To ensure intermittent internet connectivity does not interfere with the code's execution, there are some special steps you need to follow:

{{< alert title="Note" color="note" >}}
Currently, this only works with Python code which is running on the same board that `viam-server` is running on.
{{< /alert >}}

1. Change the `connect()` method to disable Webrtc and add the auth_entity in the DialOptions and use `localhost:8080`:

    ```python {class="line-numbers linkable-line-numbers" data-line="5"}
    async def connect():
      creds = Credentials(type='robot-location-secret', payload=PAYLOAD_SECRET)
      opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(
            credentials=creds,
            disable_webrtc=True,
            auth_entity=ROBOT_NAME
        )
      )
      return await RobotClient.at_address('localhost:8080', opts)
    ```

2. Replace the `ROBOT_NAME` with your robot's Viam cloud address and the `PAYLOAD_SECRET` with your robot secret.
   Your locahost can now make a secure connection to `viam-server` locally.
   SSL will now check the server hostname against `auth_entity` required by {{< glossary_tooltip term_id="grpc" >}} from the `auth_entity` dial options.

   This ensures that you can send commands to the robot through localhost without internet connectivity.
   Note that all commands will be sent using {{< glossary_tooltip term_id="grpc" >}} only without {{< glossary_tooltip term_id="webrtc" >}}.

## Next Steps

{{< cards >}}
  {{% card link="/components" size="small" %}}
  {{% card link="/services" size="small" %}}
  {{% card link="/program/extend/" size="small" %}}
{{< /cards >}}
