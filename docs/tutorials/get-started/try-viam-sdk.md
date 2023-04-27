---
title: "Drive the Viam Rover with the Viam SDK"
linkTitle: "Drive with the SDK"
weight: 40
type: "docs"
description: "Use a Viam SDK to program a Viam Rover to move in a square."
webmSrc: "/tutorials/img/try-viam-sdk/image1.webm"
mp4Src: "/tutorials/img/try-viam-sdk/image1.mp4"
videoAlt: "A Viam Rover driving in a square"
tags: ["base", "viam rover", "try viam", "sdk", "python"]
aliases:
    - /tutorials/get-started/try-viam-sdk
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/daU5iNsSO0w">}}

The Viam SDKs allow you to write code in Python, Go, or TypeScript to control a Viam-connected robot like the [Viam Rover](https://app.viam.com/try).
You can follow this tutorial with a [rented Viam Rover](https://app.viam.com/try) or with [your own Viam Rover](/try-viam/rover-resources/).

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="../../img/try-viam-sdk/image1.webm" mp4_src="../../img/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square.">}}
</div>

{{< alert title="Tip" color="tip" >}}
You can also directly see the [complete code for the tutorial](#complete-code).
{{< /alert >}}

## Install a Viam SDK

Install either the [Viam Python SDK](https://python.viam.dev/), the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme), or the [TypeScript SDK](https://ts.viam.dev/) on your local computer.

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), we recommend that you get the Viam SDK set up before your reservation starts.
This way, you can maximize the amount of time you have using the Viam Rover.

If you are running out of time during your rental, you can [extend your rover rental](/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

## Connect to your Viam Rover

{{< tabs >}}
{{% tab name="Python" %}}

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **code sample** tab, and copy the boilerplate code from the section labeled **Python**.

This code snippet imports all the necessary libraries and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>square.py</file> and paste the boilerplate code from the **code sample** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 square.py
```

{{% /tab %}}
{{% tab name="Go" %}}

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **code sample** tab, and copy the boilerplate code from the section labeled **Go**.

This code snippet imports all the necessary libraries and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>square.go</file> and paste the boilerplate code from the **code sample** tab of the Viam app into your file.
Then, save your file.

Initialize your project, and install the necessary libraries, and then run the program to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go mod init square
go mod tidy
go run square.go
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **code sample** tab, and copy the boilerplate code from the section labeled **TypeScript**.

This code snippet imports all the necessary libraries and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>main.ts</file> and paste the boilerplate code from the **code sample** tab of the Viam app into your file.
Then, save your file.

Create another file named <file>package.json</file> with the following contents:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "test-rover",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "watch": "esbuild ./main.ts --bundle --outfile=static/main.js --servedir=static",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Viam Docs Team",
  "license": "ISC",
  "devDependencies": {
    "esbuild": "0.16.12"
  },
  "dependencies": {
    "@viamrobotics/sdk": "^0.0.28"
  }
}
```

Create a folder <file>static</file> and inside it another file named <file>index.html</file>.
Add the following markup:

```html {class="line-numbers linkable-line-numbers"}
<!DOCTYPE html>
<html>
  <head>
    <title>Drive a Viam Rover</title>
    <link rel="icon" href="favicon.ico" />
  </head>
  <body>
    <div id="main">
      <button id="main-button" disabled=true>
        Click me
      </button>
    </div>
    <script type="module" src="main.js">
    </script>
  </body>
</html>
```

Run the following commands to install the necessary libraries, and then run the program to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install
npm run watch
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app, the program prints the names of your rover's resources to the terminal.
These are the components and services that the roobot is configured with in the Viam app.

<img src="../../img/try-viam-sdk/image3.png" alt="The output of the program is an array of resources that have been pulled from the Viam app. Some of these are the Vision Service, Data Manager, and Board." width="100%">

{{% alert title="Tip" color="tip" %}}

If you are [renting your rover](https://app.viam.com/try), and your reservation ends before you have completed this tutorial, change the connection information (the robot address and the payload) to connect to your new rover and continue.

{{% /alert %}}

## Drive your rover in a square

Now that you have connected the rover to Viam with the SDK, you can start writing code to control the Viam Rover.
The following code moves the Viam Rover in a square:

{{< tabs >}}
{{% tab name="Python" %}}

The first thing you need to do is import the [base component](https://python.viam.dev/autoapi/viam/components/base/index.html#module-viam.components.base).
The base is responsible for controlling the motors attached to the base of the rover.
Add the following line of code to your imports:

```python
from viam.components.base import Base
```

Next, you need to initialize your Viam Rover base.

In the main function, after you connect, paste the code from line 5.
By default, the base name is `viam_base`.
If you have changed the base name, update the name in your code.

Your main function should look like this:

```python {class="line-numbers linkable-line-numbers" data-line="5"}
async def main():
    robot = await connect()

    # Get the base component from the Viam Rover
    roverBase = Base.from_robot(robot, 'viam_base')

    await robot.close()
```

Now that your Viam Rover base is initialized, you can write code to drive it in a square.
Paste this snippet above your `main()` function:

```python
async def moveInSquare(base):
    for _ in range(4):
        # moves the Viam Rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the Viam Rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")
```

Invoke the `moveInSquare()` function in your main function after initializing your base.

Your main function should now look like this:

```python {class="line-numbers linkable-line-numbers" data-line="8"}
async def main():
    robot = await connect()

    # Get the base component from the Viam Rover
    roverBase = Base.from_robot(robot, 'viam_base')

    # Move the Viam Rover in a square
    await moveInSquare(roverBase)

    await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

The first thing you need to do is import the [base component](https://pkg.go.dev/go.viam.com/rdk@v0.2.4/components/base#Base).
The base is responsible for controlling the motors attached to the base of the rover.
Add the following line of code to your imports before:

```go {class="line-numbers linkable-line-numbers" data-line="3"}
import (
    // Be sure to keep all of the other imported libraries
    "go.viam.com/rdk/components/base"
)
```

Next, you need to initialize your Viam Rover base.

In the main function, after you connect, paste the code from lines 19-22.
By default, the base name is `viam_base`.
If you have changed the base name, update the name in your code.

Your main function should look like this:

```go {class="line-numbers linkable-line-numbers" data-line="19-22"}
func main() {
    logger := golog.NewDevelopmentLogger("client")
    robot, err := client.New(
        context.Background(),
        "ADDRESS_FROM_VIAM_APP",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type: utils.CredentialsTypeRobotLocationSecret,
            Payload: "SECRET_FROM_VIAM_APP",
        })),
    )
    if err != nil {
        logger.Fatal(err)
    }

    defer robot.Close(context.Background())

    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }
}
```

Now that your Viam Rover base has been initialized, you can write code to drive it in a square.
Paste this snippet above your `main()` function:

```go
func moveInSquare(ctx context.Context, base base.Base, logger golog.Logger) {
    for i := 0; i < 4; i++ {
        // moves the Viam Rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the Viam Rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
  }
}
```

Invoke the `moveInSquare()` function in your main function after initializing your base.

Your main function should now look like this:

```go {class="line-numbers linkable-line-numbers" data-line="10"}
func main() {
    // Connect rover to Viam...
    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    // Move the Viam Rover in a square
    moveInSquare(context.Background(), roverBase, logger)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Your main function should look like this:

```ts {class="line-numbers linkable-line-numbers"}
async function main() {
  // Connect to client
  let client: VIAM.RobotClient;
  try {
    client = await connect();
    console.log('connected!');

    let resources = await client.resourceNames();
    console.log(resources)

  } catch (error) {
    console.log(error);
    return;
  }

}
```

Next, add the following function that initializes your Viam Rover base and drives it in a square.

By default, the base name is `viam_base`.
If you have changed the base name, update the name in your code.

Paste this snippet above your `main()` function:

```ts {class="line-numbers linkable-line-numbers"}
// This function moves a base component in a square.
// Feel free to replace it whatever logic you want to test out!
async function run(client: VIAM.RobotClient) {
  // Replace with the name of a motor on your robot.
  const name = 'viam_base';
  const baseClient = new VIAM.BaseClient(client, name);

  try {
    button().disabled = true;
    for(let i=0; i<4; i++) {
      console.log("move straight");
      await baseClient.moveStraight(500, 500);
      console.log("spin 90 degrees");
      await baseClient.spin(90, 100);
    }
  } finally {
    button().disabled = false;
  }
}
```

Invoke the `run()` function in your main function after initializing your base.

Your main function should now look like this:

```ts {class="line-numbers linkable-line-numbers" data-line="16-19"}
async function main() {
  // Connect to client
  let client: VIAM.RobotClient;
  try {
    client = await connect();
    console.log('connected!');

    let resources = await client.resourceNames();
    console.log(resources)

  } catch (error) {
    console.log(error);
    return;
  }

  button().onclick = async () => {
    await run(client);
  };
  button().disabled = false;
}
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), go to the **control** tab, and make sure you can monitor the camera feed from your rover.
{{< /alert >}}

When you run your code, your robot moves in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="../../img/try-viam-sdk/image2.webm" mp4_src="../../img/try-viam-sdk/image2.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square on the left, and on the right, a terminal window shows the output of running the square function as the rover moves in a square.">}}
</div>

## Complete Code

This is the complete code for the tutorial:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET_FROM_VIAM_APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS_FROM_VIAM_APP', opts)

async def moveInSquare(base):
    for _ in range(4):
        # moves the Viam Rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the Viam Rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    roverBase = Base.from_robot(robot, 'viam_base')

    # Move the Viam Rover in a square
    await moveInSquare(roverBase)

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
    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
    "go.viam.com/utils/rpc"
)

func moveInSquare(ctx context.Context, base base.Base, logger golog.Logger) {
    for i := 0; i < 4; i++ {
        // moves the Viam Rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the Viam Rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
    }
}

func main() {
    logger := golog.NewDevelopmentLogger("client")
    robot, err := client.New(
        context.Background(),
        "ADDRESS_FROM_VIAM_APP",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type:    utils.CredentialsTypeRobotLocationSecret,
            Payload: "SECRET_FROM_VIAM_APP",
        })),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(context.Background())

    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    moveInSquare(context.Background(), roverBase, logger)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

<file>package.json</file>:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "test-rover",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "watch": "esbuild ./main.ts --bundle --outfile=static/main.js --servedir=static",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Viam Docs Team",
  "license": "ISC",
  "devDependencies": {
    "esbuild": "0.16.12"
  },
  "dependencies": {
    "@viamrobotics/sdk": "^0.0.28"
  }
}
```

<file>static/index.html</file>:

```html {class="line-numbers linkable-line-numbers"}
<!DOCTYPE html>
<html>
  <head>
    <title>Drive a Viam Rover</title>
    <link rel="icon" href="favicon.ico" />
  </head>
  <body>
    <div id="main">
      <button id="main-button" disabled=true>
        Click me
      </button>
    </div>
    <script type="module" src="main.js">
    </script>
  </body>
</html>
```

<file>main.ts</file>:

```ts {class="line-numbers linkable-line-numbers"}
import * as VIAM from '@viamrobotics/sdk';

async function connect(): Promise<VIAM.RobotClient> {
  // You can remove this block entirely if your robot is not authenticated.
  // Otherwise, replace with an actual secret.
  const secret = 'SECRET_FROM_VIAM_APP';
  const credential = {
    payload: secret,
    type: 'robot-location-secret',
  };

  // Replace with the host of your actual robot running Viam.
  const host = 'ADDRESS_FROM_VIAM_APP';

  // Replace with the signaling address. If you are running your robot on Viam,
  // it is most likely https://app.viam.com:443.
  const signalingAddress = 'https://app.viam.com:443';

  // You can replace this with a different ICE server, append additional ICE
  // servers, or omit entirely. This option is not strictly required but can
  // make it easier to connect via WebRTC.
  const iceServers = [{ urls: 'stun:global.stun.twilio.com:3478' }];

  return VIAM.createRobotClient({
    host,
    credential,
    authEntity: host,
    signalingAddress,
    iceServers,
  });
}

function button() {
  return <HTMLButtonElement>document.getElementById('main-button');
}

// This function moves a base component in a square.
// Feel free to replace it whatever logic you want to test out!
async function run(client: VIAM.RobotClient) {
  // Replace with the name of a motor on your robot.
  const name = 'viam_base';
  const baseClient = new VIAM.BaseClient(client, name);

  try {
    button().disabled = true;
    for(let i=0; i<4; i++) {
      console.log("move straight");
      await baseClient.moveStraight(500, 500);
      console.log("spin 90 degrees");
      await baseClient.spin(90, 100);
    }
  } finally {
    button().disabled = false;
  }
}

async function main() {
  // Connect to client
  let client: VIAM.RobotClient;
  try {
    client = await connect();
    console.log('connected!');

    let resources = await client.resourceNames();
    console.log(resources)
  } catch (error) {
    console.log(error);
    return;
  }

  button().onclick = async () => {
    await run(client);
  };
  button().disabled = false;
}

main();
```

{{% /tab %}}
{{< /tabs >}}

## Next Steps

If you're ready for more, try making your rover move in different ways.
Can you make it move in a circle?
A figure-eight?
You could also write some code to control the other components on the Viam Rover, like the [camera](/components/camera/), or the rover's [motors](/components/motor/).

You could also control Viam's services, by adding [data management](/manage/data/) to collect data in real time or [Vision Services](/services/vision/) to [add color detection to your Rover](/tutorials/services/try-viam-color-detection/).

{{< snippet "social.md" >}}
