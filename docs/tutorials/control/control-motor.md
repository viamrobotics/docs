---
title: "Control a motor in 2 minutes"
linkTitle: "Control a motor (2 min)"
type: "docs"
images: ["/icons/components/motor.svg"]
description: "Use Viam to control a motor's speed and direction in just a few steps."
authors: []
weight: 30
viamresources: ["motor"]
platformarea: ["core"]
no_list: true
cost: "0"
resource: "quickstart"
aliases:
  - /get-started/quickstarts/control-motor/
  - /get-started/control-motor/
  - /how-tos/control-motor/
languages: ["python", "go", "typescript", "flutter", "c++"]
level: "Beginner"
date: "2024-07-31"
# updated: ""  # When the tutorial was last entirely checked
draft: true
---

In this guide you'll configure and control a motor.

{{< alert title="You will learn" color="tip" >}}

- How to create a machine and install `viam-server` or `viam-micro-server`
- How to configure a board and a motor
- How to control your motor with UI and code

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/rWVh6C96Dic">}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
If you have the following components, you can follow along on your own hardware:

- A single-board computer or an ESP32.
- A motor and compatible motor driver.

Make sure to wire your motor to your board before starting.
Power the board on if you want to test your machine while configuring it.

{{% expand "No motor at hand?" %}}
No problem.
If you do not have both a board and motor, install `viam-server` on your laptop or computer and follow the instructions to use a _fake_ motor, which is a model that serves for testing.
{{% /expand%}}

## Instructions

Follow these steps to control your motor:

{{< expand "Step 1: Create a machine" >}}

Add a new machine.

![The 'My Desk' page with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/get-started/quickstarts/add-machine.png)

{{< /expand >}}
{{< expand "Step 2: Install viam-server or viam-micro-server" >}}

Navigate to the **CONFIGURE** tab of your machine's page.
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page.
If you are using a microcontroller, install `viam-micro-server`.
Otherwise, install `viam-server`.
Wait for your device to connect to Viam.

{{< /expand >}}
{{< expand "Step 3: Configure a board" >}}

On the **CONFIGURE** page you can add components and services to your machine.
Click on the **+** icon to select a suitable board.

If you are using a physical board to follow along, look through the [**Supported Models**](/operate/reference/components/board/#configuration) to determine the model of component to configure.
For example, configure a [`viam:raspberry-pi:rpi` board](https://github.com/viam-modules/raspberry-pi) for a Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero 2 W:

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/get-started/quickstarts/configure-pi.png)

If you do not have a physical board, use the [`fake` board model](/operate/reference/components/board/fake/).

Follow the instructions in the board model's documentation to configure any required attributes.
For the `fake` model, there are no required attributes.

{{< /expand >}}
{{< expand "Step 4: Configure a motor" >}}

Add a `motor` component that supports the type of motor and motor driver you're using.
Look through the [**Supported Models**](/operate/reference/components/motor/#configuration) to determine the model of component to configure.
For example, if you are using a standard DC motor (brushed or brushless) wired to a typical GPIO pin-controlled motor driver, configure a [`gpio` motor](/operate/reference/components/motor/gpio/):

![The CONFIGURE tab populated with a configured gpio motor.](/get-started/quickstarts/configure-motor.png)

Follow the motor driver manufacturer's data sheet to wire your motor driver to your board and to your motor.
Follow the [model's documentation](/operate/reference/components/motor/) to configure the attributes so that the computer can send signals to the motor.

If you do not have a physical motor, use the [`fake` motor model](/operate/reference/components/motor/fake/).
For the `fake` model, there are no required attributes.

**Save your configuration.**
{{< /expand >}}
{{< expand "Step 5: Choose how you will control the motor" >}}

You can control your motor directly using the web UI, the mobile app, or the SDKs.

### Option 1: Control from the app

Navigate to your machine's **CONTROL** tab and click on the motor panel.
Then use the **Power %** slider to set the motor's speed.
Use the **Backwards** and **Forwards** buttons to change the direction.

{{<gif webm_src="/get-started/quickstarts/motor-control.webm" mp4_src="/get-started/quickstarts/motor-control.mp4" alt="Using the slider, Backwards, and Forwards buttons to control the direction and speed of a configured motor" class="aligncenter"  min-height="750px">}}

### Option 2: Control from the mobile app

You can use [the Viam mobile app](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app) to control your motor's speed and direction directly from your smart phone.

Open the Viam mobile app and log in to your account.
Select the location that your machine is in from the **Locations** tab.

Choose your machine from the list and use the mobile interface to adjust the motor settings.

{{<gif webm_src="/get-started/quickstarts/mobile-app-motor-control.webm" mp4_src="/get-started/quickstarts/mobile-app-motor-control.mp4" alt="Using an example machine on the Viam mobile app to set the direction and speed of a configured motor using the slider on the user interface" max-height="50px" max-width="200px" class="aligncenter">}}

### Option 3: Control programmatically

Each component has a standardized API.
The following code shows you how to control the motor's speed and direction using the [Motor API](/operate/reference/components/motor/#api).

If you'd like to try it, find your machine's API key and address on your machine's **CONNECT** tab and run the code sample:

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.motor import Motor


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


async def main():
    async with await connect() as machine:
        print('Resources:')
        print(machine.resource_names)

        # Instantiate the motor client
        motor_1 = Motor.from_robot(machine, "motor-1")
        # Turn the motor at 35% power forwards
        await motor_1.set_power(power=0.35)
        # Let the motor spin for 3 seconds
        time.sleep(3)
        # Stop the motor
        await motor_1.stop()


if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
  "context"
  "time"

  "go.viam.com/rdk/logging"
  "go.viam.com/utils/rpc"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/components/motor")

func main() {
  logger := logging.NewDebugLogger("client")
  machine, err := client.New(
    context.Background(),
    // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    "<MACHINE-ADDRESS>",
    logger,
    client.WithDialOptions(utils.WithEntityCredentials(
      // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
      // API key ID
      "<API-KEY-ID>",
      utils.Credentials{
        Type:    utils.CredentialsTypeAPIKey,
        // TODO: Replace "<API-KEY>" (including brackets) with your machine's
        // API key
        Payload: "<API-KEY>",
      })),
  )
  if err != nil {
    logger.Fatal(err)
  }

  defer machine.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(machine.ResourceNames())


  // Instantiate the motor client
  motor1Component, err:= motor.FromProvider(machine, "motor-1")
  if err != nil {
    logger.Error(err)
    return
  }
  // Turn the motor at 35% power forwards
  err = motor1Component.SetPower(context.Background(), 0.35, nil)
  if err != nil {
    logger.Error(err)
    return
  }
  // Let the motor spin for 3 seconds
  time.Sleep(3 * time.Second)
  // Stop the motor
  err = motor1Component.Stop(context.Background(), nil)
  if err != nil {
    logger.Error(err)
    return
  }
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

Flutter code must be launched from inside a running Flutter application.
To get started programming your machine with Flutter, follow the instructions to [Build a Flutter App that Integrates with Viam](/tutorials/control/flutter-app/).
Then return to this page to add motor control to your app.

Add a new file to your application in <file>/lib</file> called <file>motor_screen.dart</file>.
Paste this code into your file:

```dart {class="line-numbers linkable-line-numbers"}
/// This is the MotorScreen, which allows us to control a [Motor].
/// This particular example uses both the Viam-provided [ViamMotorWidget],
/// while also providing an example of how you could create your own
/// widgets to control a resource.
library;

import 'package:flutter/material.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

class MotorScreen extends StatelessWidget {
  final Motor motor;

  const MotorScreen(this.motor, {super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(motor.name)),
      body: Column(children: [
        // The first widget in our column will be the one provided
        // by the Viam SDK.
        ViamMotorWidget(motor: motor),
        const SizedBox(height: 10), // Padding between widgets

        // Here we have a button that controls the [Motor]:
        // Spin the motor at 35% power forwards for three seconds.
        // The [Motor] resource provides many control functions, but here
        // we are using the [Motor.setPower] method.
        //
        // You can extrapolate this to other Viam resources.
        // For example, you could make the onPressed function call
        // [Gripper.open] on a gripper, or [Sensor.readings] on a Sensor.
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          ElevatedButton(
            onPressed: () async {
              motor.setPower(0.35); // Set motor power to 35%
              await Future.delayed(Duration(seconds: 3)); // Let the motor spin for 3 seconds
              await motor.stop(); // Stop the motor
            },
            style: ElevatedButton.styleFrom(
            minimumSize: Size(80, 20), // Adjusts width and height of the button
            padding: EdgeInsets.symmetric(horizontal: 4, vertical: 6), // Adjusts padding inside the button
          ),
            child: const Text('Set motor power', textAlign: TextAlign.center),
          ),
        ]),
      ]),
    );
  }
}
```

This code creates a screen with a power widget to adjust the power and a button that, when pressed, calls on the `setPower()` method to spin the motor forwards at 35% power, waits three seconds to let it spin, and then stops the motor.

Then, replace the contents of <file>robot_screen.dart</file> with the following file, or add the highlighted lines of code to your program in the locations indicated:

```dart {class="line-numbers linkable-line-numbers" data-line="9, 73-85, 99-102"}
/// This is the screen that shows the resources available on a robot (or smart machine).
/// It takes in a Viam app client instance, as well as a robot client.
/// It then uses the Viam client instance to create a connection to that robot client.
/// Once the connection is established, you can view the resources available
/// and send commands to them.
library;

import 'package:flutter/material.dart';
import 'motor_screen.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

class RobotScreen extends StatefulWidget {
  final Viam _viam;
  final Robot robot;

  const RobotScreen(this._viam, this.robot, {super.key});

  @override
  State<RobotScreen> createState() => _RobotScreenState();
}

class _RobotScreenState extends State<RobotScreen> {
  /// Similar to previous screens, start with [_isLoading] to true.
  bool _isLoading = true;

  /// This is the [RobotClient], which allows you to access
  /// all the resources of a Viam Smart Machine.
  /// This differs from the [Robot] provided to us in the widget constructor
  /// in that the [RobotClient] contains a direct connection to the Smart Machine
  /// and its resources. The [Robot] object simply contains information about
  /// the Smart Machine, but is not actually connected to the machine itself.
  ///
  /// This is initialized late because it requires an asynchronous
  /// network call to establish the connection.
  late RobotClient client;

  @override
  void initState() {
    super.initState();
    // Call our own _initState method to initialize our state.
    _initState();
  }

  @override
  void dispose() {
    // You should always close the [RobotClient] to free up resources.
    // Calling [RobotClient.close] will clean up any tasks and
    // resources created by Viam.
    client.close();
    super.dispose();
  }

  /// This method will get called when the widget initializes its state.
  /// It exists outside the overridden [initState] function since it's async.
  Future<void> _initState() async {
    // Using the authenticated [Viam] the received as a parameter,
    // the app can obtain a connection to the Robot.
    // There is a helpful convenience method on the [Viam] instance for this.
    final robotClient = await widget._viam.getRobotClient(widget.robot);
    setState(() {
      client = robotClient;
      _isLoading = false;
    });
  }

  /// A computed variable that returns the available [ResourceName]s of
  /// this robot in an alphabetically sorted list.
  List<ResourceName> get _sortedResourceNames {
    return client.resourceNames..sort((a, b) => a.name.compareTo(b.name));
  }

  bool _isNavigable(ResourceName rn) {
    if (rn.subtype == Motor.subtype.resourceSubtype) {
      return true;
    }
    return false;
  }

  void _navigate(ResourceName rn) {
    if (rn.subtype == Motor.subtype.resourceSubtype) {
      final motor = Motor.fromRobot(client, rn.name);
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => MotorScreen(motor)));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.robot.name)),
        body: _isLoading
            ? const Center(child: CircularProgressIndicator.adaptive())
            : ListView.builder(
                itemCount: client.resourceNames.length,
                itemBuilder: (_, index) {
                  final resourceName = _sortedResourceNames[index];
                  return ListTile(
                    title: Text(resourceName.name),
                    subtitle: Text(
                        '${resourceName.namespace}:${resourceName.type}:${resourceName.subtype}'),
                    onTap: () => _navigate(resourceName),
                    trailing: _isNavigable(resourceName) ? Icon(Icons.chevron_right) : SizedBox.shrink(),
                  );
                }));
  }
}
```

This imports the <file>motor_screen.dart</file> file into the program and adds logic to check if a {{< glossary_tooltip term_id="resource" text="resource" >}} is "navigable", or, has a screen made for it.
Since you added a screen for motor, motor is a navigable resource.

To navigate to the motor screen, save your code and launch your simulator.
Navigate to the robot screen of your (live) machine with a motor resource configured, and see the resource control interface displayed:

{{<imgproc src="/get-started/quickstarts/motor-screen.png" resize="500x" declaredimensions=true alt="iOS simulator of a motor displayed">}}

You can adjust the toggle to change the power of your motor or press the buttons to make it revolve forwards and backwards.

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
    "start": "esbuild ./main.ts --bundle --outfile=static/main.js --servedir=static",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Viam Docs Team",
  "license": "ISC",
  "devDependencies": {
    "esbuild": "*"
  },
  "dependencies": {
    "@viamrobotics/sdk": "*"
  }
}
```

<file>static/index.html</file>:

```html {class="line-numbers linkable-line-numbers"}
<!doctype html>
<html>
  <head>
    <title>Drive a Rover</title>
    <link rel="icon" href="favicon.ico" />
  </head>
  <body>
    <div id="main">
      <button id="main-button" disabled="true">Click me</button>
    </div>
    <script type="module" src="main.js"></script>
  </body>
</html>
```

<file>main.ts</file>:

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.

import * as VIAM from "@viamrobotics/sdk";

// This function gets the button element
function button() {
  return <HTMLButtonElement>document.getElementById("main-button");
}

const main = async () => {
  // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
  const host = "<MACHINE-ADDRESS>";

  const machine = await VIAM.createRobotClient({
    host,
    credentials: {
      // TODO: Replace "<API-KEY>" (including brackets) with your machine's
      // API key
      type: "api-key",
      payload: "<API-KEY>",
      // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
      // API key ID
      authEntity: "<API-KEY-ID>",
    },
    signalingAddress: "https://app.viam.com:443",
  });

  button().onclick = async () => {
    // Instantiate the motor client
    // TODO: Replace with the name of a motor on your machine.
    const name = "motor-1";
    const motorClient = new VIAM.MotorClient(machine, name);

    // Turn the motor at 35% power forwards
    await motorClient.setPower(0.35);
    // Let the motor spin for 3 seconds, then stop the motor
    const sleep = (ms: number) =>
      new Promise((resolve) => setTimeout(resolve, ms));
    await sleep(3000);
    await motorClient.stop();
  };
  button().disabled = false;
};

main().catch((error) => {
  console.error("encountered an error:", error);
});
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
#include <boost/optional.hpp>
#include <string>
#include <vector>
#include <unistd.h>
#include <viam/sdk/robot/client.hpp>
#include <viam/sdk/components/motor.hpp>

using namespace viam::sdk;

int main() {
    std::string host("muddy-snow-main.7kp7y4p393.viam.cloud");
    DialOptions dial_opts;
    dial_opts.set_entity(std::string("<API-KEY-ID>"));
    // Replace "<API-KEY-ID>" (including brackets) with your machine's
    // API key ID
    Credentials credentials("api-key", "<API-KEY>");
    // Replace "<API-KEY>" (including brackets) with your machine's API key
    dial_opts.set_credentials(credentials);
    boost::optional<DialOptions> opts(dial_opts);
    Options options(0, opts);

    auto machine = RobotClient::at_address(host, options);

    std::cout << "Resources:\n";
    for (const Name& resource : machine->resource_names()) {
        std::cout << "\t" << resource << "\n";
    }

    std::string motor_name("motor-1");

    std::cout << "Getting motor: " << motor_name << std::endl;
    std::shared_ptr<Motor> motor;
    try {
        // Get the motor client
        motor = machine->resource_by_name<Motor>(motor_name);
        // Turn the motor at 35% power forwards
        motor->set_power(0.35);
        // Let the motor spin for 3 seconds
        sleep(3);
        // Stop the motor
        motor->stop();
    } catch (const std::exception& e) {
        std::cerr << "Failed to find " << motor_name << ". Exiting." << std::endl;
        throw;
    }
    return EXIT_SUCCESS;
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}
