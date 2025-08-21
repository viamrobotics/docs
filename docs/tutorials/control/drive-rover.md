---
title: "Drive a rover in a square in 2 minutes"
linkTitle: "Drive a rover (2 min)"
type: "docs"
images: ["/general/code.png"]
description: "Use a Viam SDK to program a rover to move in a square."
videos:
  ["/tutorials/try-viam-sdk/image1.webm", "/tutorials/try-viam-sdk/image1.mp4"]
videoAlt: "A Viam Rover driving in a square"
images: ["/tutorials/try-viam-sdk/image1.gif"]
aliases:
  - /tutorials/appendix/try-viam-sdk
  - /tutorials/viam-rover/try-viam-sdk
  - /tutorials/viam-rover/try-viam-sdk
  - "/try-viam/try-viam-tutorial/"
  - "/get-started/try-viam/try-viam-tutorial/"
  - "/get-started/quickstarts/drive-rover/"
  - "/how-tos/drive-rover/"
  - /get-started/drive-rover/
tags: ["base", "viam rover", "try viam", "sdk", "python", "flutter"]
level: "Beginner"
authors: []
weight: 10
no_list: true
date: "2024-07-31"
cost: "0"
resource: "quickstart"
languages: ["python", "go", "typescript", "flutter", "c++"]
viamresources: ["base"]
platformarea: ["core"]
level: "Beginner"
date: "2022-12-08"
updated: "2024-08-06"
cost: "0"
---

In this guide you'll write code that makes a rover drive in a square.

{{< alert title="You will learn" color="tip" >}}

- How to run control code with Viam SDKs
- How to use the base API to move a rover in a square

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/daU5iNsSO0w">}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
You only need the following:

- A Linux, macOS or Windows computer that can run SDK code.
- A [borrowed Viam Rover](https://app.viam.com/try), [your own Viam Rover](/dev/reference/try-viam/rover-resources/), or [another mobile robot](/tutorials/configure/configure-rover/).
  You can use [Try Viam](https://app.viam.com/try) to borrow a rover online at no cost which is already configured with all the components you need.
  If you have your own rover on hand, whether it's a [Viam rover](https://www.viam.com/resources/rover) or not, these instructions work for any wheeled robot that can be configured as a [base component](/operate/reference/components/base/wheeled/).

## Instructions

Follow these steps to get your rover ready and write code to control it:

{{< tabs >}}
{{% tab name="Borrowed Try Viam Rover" %}}
{{< expand "Step 1: Borrow a Viam Rover" >}}

Go to [Try Viam](https://app.viam.com/try) and borrow a rover.
If a rover is available, the rover will take up to 30 seconds to be configured for you.

{{< alert title="Tip" color="tip" >}}
If you are running out of time during your session, you can [extend your rover session](/dev/reference/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{< /expand >}}

{{% /tab %}}
{{% tab name="Other Rover" %}}

{{% alert title="Important" color="note" %}}
If you are using your own robot for this tutorial instead of [borrowing one](https://app.viam.com/try), be sure to [follow the setup instructions and install `viam-server`](/operate/get-started/setup/) on it, and connect and [configure](/tutorials/configure/configure-rover/) its hardware before proceeding with this tutorial.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

{{< expand "Step 2: Install an SDK" >}}

Navigate to your machine's **CONNECT** tab.
Click on any of the listed languages and follow the instructions to install the SDK.

To install your preferred Viam SDK on your Linux or macOS development machine or [single-board computer](/operate/reference/components/board/), run one of the following commands in your terminal:

{{< tabs >}}
{{% tab name="Python" %}}

If you are using the Python SDK, [set up a virtual environment](/dev/reference/sdks/python/python-venv/) to package the SDK inside before running your code, avoiding conflicts with other projects or your system.

For macOS (both Intel `x86_64` and Apple Silicon) or Linux (`x86`, `aarch64`, `armv6l`), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

Windows is not supported.
If you are using Windows, use the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) and install the Python SDK using the preceding instructions for Linux.
For other unsupported systems, see [Installing from source](https://python.viam.dev/#installing-from-source).

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter pub add viam_sdk
```

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}

{{< /tabs >}}

{{< /expand >}}
{{< expand "Step 3: Copy and run the sample code" >}}

The sample code on the **CONNECT** tab will show you how to authenticate and connect to a machine, as well as some of the methods you can use on your configured components and services.

{{< tabs >}}
{{% tab name="Python" %}}

Go to the **CONNECT** tab and select **Python**.
Save your API key and API key ID as environment variables or include them in the code:

{{% snippet "show-secret.md" %}}

Copy the code into a file called <FILE>square.py</FILE> and run the sample code to connect to your machine:

```sh {class="command-line" data-prompt="$"}
python3 square.py
```

The program prints an array of resources.
These are the components and services that the machine is configured with on Viam.

```sh {class="command-line" data-prompt="$" data-output="2-75"}
python3 square.py
2024-08-09 13:21:52,423    INFO    viam.rpc.dial (dial.py:293)    Connecting to socket: /tmp/proxy-BzFWLZQ2.sock
Resources:
[<viam.proto.common.ResourceName rdk:service:sensors/builtin at 0x105b12700>, <viam.proto.common.ResourceName rdk:component:motor/left at 0x105b122a0>, <viam.proto.common.ResourceName rdk:component:camera/cam at 0x105b12390>, <viam.proto.common.ResourceName rdk:component:board/local at 0x105b129d0>, <viam.proto.common.ResourceName rdk:component:base/viam_base at 0x105b12610>, <viam.proto.common.ResourceName rdk:service:motion/builtin at 0x105b12a20>, <viam.proto.common.ResourceName rdk:component:encoder/Lenc at 0x105b12a70>, <viam.proto.common.ResourceName rdk:component:motor/right at 0x105b12ac0>, <viam.proto.common.ResourceName rdk:component:encoder/Renc at 0x105b12b10>]
```

{{% /tab %}}
{{% tab name="Go" %}}

Go to the **CONNECT** tab and select **Golang**.
Save your API key and API key ID as environment variables or include them in the code:

{{% snippet "show-secret.md" %}}

Copy the code into a file called <FILE>square.go</FILE>.
Initialize your project, and install the necessary libraries, and then run the program to verify that the Viam SDK is properly installed and that the `viam-server` instance on your machine is live:

```sh {class="command-line" data-prompt="$"}
go mod init square
go mod tidy
go run square.go
```

The program prints an array of resources.
These are the components and services that the machine is configured with on Viam.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
go run square.go
2024-08-09T11:27:05.034Z    DEBUG    client.webrtc    rpc/wrtc_client.go:111    connecting to signaling server    {"signaling_server":"app.viam.com:443","host":"muddy-snow-main.7kp7y4p393.viam.cloud"}
2024-08-09T11:27:05.314Z    DEBUG    client.webrtc    rpc/wrtc_client.go:125    connected to signaling server    {"signaling_server":"app.viam.com:443"}
...
2024-08-09T11:27:08.916Z    INFO    client    test-rover/square.go:33    Resources:
2024-08-09T11:27:08.916Z    INFO    client    test-rover/square.go:34    [rdk:component:board/local rdk:component:base/viam_base rdk:service:motion/builtin rdk:component:motor/right rdk:component:encoder/Renc rdk:component:encoder/Lenc rdk:service:sensors/builtin rdk:component:motor/left rdk:component:camera/cam]
```

{{% /tab %}}
{{< tab name="TypeScript" >}}

{{< alert title="Fast track" color="note" >}}

If you want to get the full sample code now, run the following command which will set up the files for you:

```sh {class="command-line" data-prompt="$"}
npm create robot-app
```

Then, copy and paste your API key and API key ID, and machine address into the <FILE>.env</FILE> file.
If you have run this command and added your environment variables, skip ahead to running the program.

{{< /alert >}}

Go to the **CONNECT** tab and select **TypeScript**.
Save your API key and API key ID as environment variables or include them in the code:

{{% snippet "show-secret.md" %}}

Copy the code into a file called <FILE>main.ts</FILE>.

Create another file named <file>package.json</file> with the following contents:

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

Create a folder <file>static</file> and inside it another file named <file>index.html</file>.
Add the following markup:

```html {class="line-numbers linkable-line-numbers"}
<!doctype html>
<html>
  <head>
    <title>Drive a Rover</title>
    <link rel="icon" href="favicon.ico" data-proofer-ignore />
  </head>
  <body>
    <div id="main">
      <h1>Drive a rover in a square</h1>
      <p>
        We recommend you open the developer tools in your browser to see logs.
      </p>
      <p>
        Also open a second window with the your rover's
        <b>CONTROL</b> tab, which allows you to interact with your rover's
        resources. Click on one of the camera panels and toggle the camera
        stream on so you can observe the rover's movements.
      </p>
      <button id="main-button" disabled="true">
        Click me to drive rover in square
      </button>
    </div>
    <script type="module" src="main.js" data-proofer-ignore></script>
  </body>
</html>
```

Run the following commands to install the necessary libraries, and then run the program to verify that the Viam SDK is properly installed and that the `viam-server` instance on your machine is live:

```sh {class="command-line" data-prompt="$"}
npm install
npm start
```

Open a web browser and visit `localhost:8000`.
You should see a disabled button that says `Click me to drive rover in square`.
Open the developer console to see the console output.
If you successfully configured your machine and it is able to connect to Viam, you will see some output including the names of your rover's resources.
These are the components and services that the machine is configured with on Viam.

{{< /tab >}}
{{% tab name="Flutter" %}}

Flutter code must be launched from inside a running Flutter application.
To get started programming your rover with Flutter, follow the instructions to [Build a Flutter App that Integrates with Viam](/tutorials/control/flutter-app/).

{{% /tab %}}
{{% tab name="C++" %}}

Go to the **CONNECT** tab and select **C++**.
Save your API key and API key ID as environment variables or include them in the code:

{{% snippet "show-secret.md" %}}

Copy the code into a file called <FILE>drive_in_square.cpp</FILE>.

Compile your code, and then run the program to verify that the Viam SDK is properly installed and that the `viam-server` instance on your machine is live:

```sh {class="command-line" data-prompt="$"}
cmake . -G Ninja
ninja all
./drive_in_square
```

The program prints an array of resources.
These are the components and services that the machine is configured with on Viam.

```sh {class="command-line" data-prompt="$" data-output="2-20"}
./src/viam/examples/camera/example_camera
Resources:
  rdk:component:motor/right
  rdk:component:encoder/Renc
  rdk:component:encoder/Lenc
  rdk:service:sensors/builtin
  rdk:component:motor/left
  rdk:component:camera/cam
  rdk:component:board/local
  rdk:component:base/viam_base
  rdk:service:motion/builtin
 ...
```

{{% /tab %}}

{{< /tabs >}}

{{< /expand >}}
{{< expand "Step 4: Drive a rover in a square" >}}

Now that you have connected the rover to Viam with the SDK, you can write code to move the rover in a square:

{{< tabs >}}
{{% tab name="Python" %}}

The base is responsible for controlling the motors attached to the base of the rover.
Ensure that the `Base` class is being imported:

```python
from viam.components.base import Base
```

Then paste this snippet above your `main()` function, it will move any base passed to it in a square:

```python
async def moveInSquare(base):
    for _ in range(4):
        # moves the rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")
```

Next, remove all the code in the `main()` function between where the machine connection is established and closed and instead initialize your `base` and invoke the `moveInSquare()` function.

On the Try Viam rovers, the default base name is `viam_base`.
If you have a different base name, update the name in your code.

```python {class="line-numbers linkable-line-numbers" data-line="4-8"}
async def main():
    machine = await connect()

    # Get the base component from the rover
    roverBase = Base.from_robot(machine, 'viam_base')

    # Move the rover in a square
    await moveInSquare(roverBase)

    await machine.close()
```

If you have a borrowed Try Viam rover, navigate to your machine's **CONTROL** tab, which allows you to interact with your machine's {{< glossary_tooltip term_id="resource" text="resources" >}}.

Click on one of the camera panels and toggle the camera stream on so you can observe the rover's movements.

Then run your code and watch your rover move in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="/tutorials/try-viam-sdk/image2.webm" mp4_src="../../try-viam-sdk/image2.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square on the left, and on the right, a terminal window shows the output of running the square function as the rover moves in a square.">}}
</div>

{{% /tab %}}
{{% tab name="Go" %}}

The base is responsible for controlling the motors attached to the base of the rover.
Ensure that the `Base` class is being imported:

```go {class="line-numbers linkable-line-numbers" data-line="3"}
import (
    // Be sure to keep all of the other imported libraries
    "go.viam.com/rdk/components/base"
)
```

Then paste this snippet above your `main()` function, it will move any base passed to it in a square:

```go
func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // moves the rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
  }
}
```

Next, remove all the code in the `main()` function after the machine connection is established and instead initialize your `base` and invoke the `moveInSquare()` function.

Also remove any unused imports.

On the Try Viam rovers, the default base name is `viam_base`.
If you have a different base name, update the name in your code.

```go {class="line-numbers linkable-line-numbers" data-line="22-29"}
func main() {
    logger := logging.NewLogger("client")
    machine, err := client.New(
      context.Background(),
      // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
      "<MACHINE-ADDRESS>",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
        // Replace "<API-KEY-ID>" (including brackets) with your machine's
        // API key ID
        "<API-KEY-ID>",
        rpc.Credentials{
          Type:    rpc.CredentialsTypeAPIKey,
          // Replace "<API-KEY>" (including brackets) with your machine's API key
          Payload: "<API-KEY>",
        })),
    )
    if err != nil {
      logger.Fatal(err)
    }

    defer machine.Close(context.Background())

    // Get the base from the rover
    roverBase, err := base.FromRobot(machine, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    // Move the rover in a square
    moveInSquare(context.Background(), roverBase, logger)
}
```

If you have a borrowed Try Viam rover, navigate to your machine's **CONTROL** tab, which allows you to interact with your machine's {{< glossary_tooltip term_id="resource" text="resources" >}}.

Click on one of the camera panels and toggle the camera stream on so you can observe the rover's movements.

Then run your code and watch your rover move in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square." max-width="400px">}}
</div>

{{% /tab %}}
{{% tab name="TypeScript" %}}

Above the `main` function, add the following function that initializes your rover base client and drives it in a square.

On the Try Viam rovers, the default base name is `viam_base`.
If you have a different base name, update the name in your code.

```ts {class="line-numbers linkable-line-numbers"}
// This function moves a base component in a square.
async function moveInSquare(client: VIAM.RobotClient) {
  // TODO: Replace with the name of the base on your machine.
  const name = "viam_base";
  const baseClient = new VIAM.BaseClient(client, name);

  try {
    button().disabled = true;
    for (let i = 0; i < 4; i++) {
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

Underneath the `moveInSquare` function, add this `button` function which gets the `main-button` button from the page loaded from `index.html`:

```ts {class="line-numbers linkable-line-numbers"}
// This function gets the button element
function button() {
  return <HTMLButtonElement>document.getElementById("main-button");
}
```

Next, register a listener on the button you obtain from the `button` function and make it invoke the `moveInSquare` function.
Place this code after the rover connection code:

```ts {class="line-numbers linkable-line-numbers"}
button().onclick = async () => {
  await moveInSquare(machine);
};
button().disabled = false;
```

Your main function should now look like this:

```ts {class="line-numbers linkable-line-numbers" data-line="16-19"}
async function main() {
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
    await moveInSquare(machine);
  };
  button().disabled = false;
}
```

Save your code and refresh the browser page.
When the connection to the rover is established, the `Click me to drive rover in square` button will become enabled.

If you have a borrowed Try Viam rover, open a tab and navigate to your machine's **CONTROL** tab, which allows you to interact with your rover's {{< glossary_tooltip term_id="resource" text="resources" >}}.

Click on one of the camera panels and toggle the camera stream on so you can observe the rover's movements.

Go back to the `Click me to drive rover in square` button and click the button to run your code and switch back to the **CONTROL** tab to watch your rover move in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square." max-width="400px">}}
</div>

{{% /tab %}}
{{% tab name="Flutter" %}}

Add a new file to your application in <file>/lib</file> called <file>base_screen.dart</file>.
Paste this code into your file:

```dart {class="line-numbers linkable-line-numbers"}
/// This is the BaseScreen, which allows us to control a Base.

import 'package:flutter/material.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

class BaseScreen extends StatelessWidget {
  final Base base;

  const BaseScreen(this.base, {super.key});

  Future<void> moveSquare() async {
    for (var i=0; i<4; i++) {
      await base.moveStraight(500, 500);
      await base.spin(90, 100);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(base.name)),
      body: Center(
        child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
              onPressed: moveSquare,
              child: const Text('Move Base in Square'),
            ),
        ]))
        ,);}}
```

This code creates a screen with a singular centered button that, when pressed, calls on the `moveSquare()` method to drive the base in a square.

Then, replace the contents of <file>robot_screen.dart</file> with the following file, or add the highlighted lines of code to your program in the locations indicated:

```dart {class="line-numbers linkable-line-numbers" data-line="11, 73-85, 101-102"}
/// This is the screen that shows the resources available on a robot (or smart machine).
/// It takes in a Viam app client instance, as well as a robot client.
/// It then uses the Viam client instance to create a connection to that robot client.
/// Once the connection is established, you can view the resources available
/// and send commands to them.

import 'package:flutter/material.dart';
import 'package:viam_sdk/protos/app/app.dart';
import 'package:viam_sdk/viam_sdk.dart';

import 'base_screen.dart';

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
    if (_isLoading == false) {
      client.close();
    }
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
    if (rn.subtype == Base.subtype.resourceSubtype) {
      return true;
    }
    return false;
  }

  void _navigate(ResourceName rn) {
    if (rn.subtype == Base.subtype.resourceSubtype) {
      final base = Base.fromRobot(client, rn.name);
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => BaseScreen(base)));
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

This imports the <file>base_screen.dart</file> file into the program and adds logic to check if a {{< glossary_tooltip term_id="resource" text="resource" >}} is "navigable", or, has a screen made for it.
Base is the only resource that is navigable.

To navigate to the base screen, save your code and launch your simulator.
Navigate to the robot screen of a (live) machine with a base resource configured, and see the resources displayed like the following:

{{<imgproc src="/tutorials/try-viam-sdk/resource-menu.png" resize="300x" declaredimensions=true alt="Machine resources listed in an example Flutter app">}}

Then, click on the base to display the base screen.
You may need to scroll to the bottom of the list of resources.

{{<imgproc src="/tutorials/try-viam-sdk/button.png" resize="300x" declaredimensions=true alt="Button to drive a rover in a square in an example Flutter app">}}

Click on the button to move your rover in a square:

{{<video webm_src="/tutorials/try-viam-sdk/square-test-rover.webm" mp4_src="/tutorials/try-viam-sdk/square-test-rover.mp4" alt="An example flutter app moving a Try Viam rover in a square" poster="/tutorials/try-viam-sdk/square-test-rover.jpg">}}

{{% /tab %}}
{{% tab name="C++" %}}

The base is responsible for controlling the motors attached to the base of the rover.
Ensure that the `Base` class is being imported:

```cpp {class="line-numbers linkable-line-numbers"}
#include <viam/sdk/components/base.hpp>
```

Additionally, add the following namespaces under your imports:

```cpp {class="line-numbers linkable-line-numbers"}
using namespace viam::sdk;
using std::cerr;
using std::cout;
using std::endl;
```

Then paste this snippet above your main() function, it will move any base passed to it in a square:

```cpp {class="line-numbers linkable-line-numbers"}
void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    cout << "Move straight" << endl;
    // Move the base forward 600mm at 500mm/s
    base->move_straight(500, 500);
    cout << "Spin" << endl;
    // Spin the base by 90 degree at 100 degrees per second
    base->spin(90, 100);
  }
}
```

Next, remove all the code in the `main()` function after the machine connection is established, and instead initialize your base and invoke the `moveInSquare()` function.

On the Try Viam rovers, the default base name is `viam_base`.
If you have a different base name, update the name in your code.

```cpp {class="line-numbers linkable-line-numbers" data-line="19-31"}
int main() {
    // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    std::string host("<MACHINE-ADDRESS>");
    DialOptions dial_opts;
    // TODO: Replace "<API-KEY-ID>" with your machine's API key ID
    dial_opts.set_entity(std::string("<API-KEY-ID>"));
    // TODO: Replace "<API-KEY>" with your machine's API key
    Credentials credentials("api-key", "<API-KEY>");
    dial_opts.set_credentials(credentials);
    boost::optional<DialOptions> opts(dial_opts);
    Options options(0, opts);

    auto machine = RobotClient::at_address(host, options);

    std::cout << "Resources:\n";
    for (const Name& resource : machine->resource_names()) {
      std::cout << "\t" << resource << "\n";
    }

    std::string base_name("viam_base");

    cout << "Getting base: " << base_name << endl;
    std::shared_ptr<Base> base;
    try {
        base = machine->resource_by_name<Base>(base_name);

        move_in_square(base);

    } catch (const std::exception& e) {
        cerr << "Failed to find " << base_name << ". Exiting." << endl;
        throw;
    }
    return EXIT_SUCCESS;
}
```

If you have a borrowed Try Viam rover, navigate to your machine's **CONTROL** tab, which allows you to interact with your machine's {{< glossary_tooltip term_id="resource" text="resources" >}}.

Click on one of the camera panels and toggle the camera stream on so you can observe the rover's movements.

Then run your code and watch your rover move in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square." max-width="400px">}}
</div>

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}

If you are interested to learn about what other commands you can give to a base, see the standardized [base API](/dev/reference/apis/components/base/#api) for a full list of available API methods.
{{% /alert %}}

{{< /expand>}}

## Complete code

This is the complete code for the tutorial:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


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


async def moveInSquare(base):
    for _ in range(4):
        # moves the rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")


async def main():
    machine = await connect()

    roverBase = Base.from_robot(machine, 'viam_base')

    # Move the rover in a square
    await moveInSquare(roverBase)

    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
    "context"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils")

func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // moves the rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
    }
}

func main() {
    logger := logging.NewLogger("client")
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

    // Get the base from the rover
    roverBase, err := base.FromRobot(machine, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    // Move the rover in a square
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
      <h1>Drive a rover in a square</h1>
      <p>
        We recommend you open the developer tools in your browser to see logs.
      </p>
      <p>
        Also open a second window and navigate to your rover's
        <b>CONTROL</b> tab, which allows you to interact with your rover's
        resources. Click on one of the camera panels and toggle the camera
        stream on so you can observe the rover's movements.
      </p>
      <button id="main-button" disabled="true">
        Click me to drive rover in square
      </button>
    </div>
    <script type="module" src="main.js"></script>
  </body>
</html>
```

<file>main.ts</file>:

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.

import * as VIAM from "@viamrobotics/sdk";

// This function moves a base component in a square.
async function moveInSquare(client: VIAM.RobotClient) {
  // TODO: Replace with the name of the base on your machine.
  const name = "viam_base";
  const baseClient = new VIAM.BaseClient(client, name);

  try {
    button().disabled = true;
    for (let i = 0; i < 4; i++) {
      console.log("move straight");
      await baseClient.moveStraight(500, 500);
      console.log("spin 90 degrees");
      await baseClient.spin(90, 100);
    }
  } finally {
    button().disabled = false;
  }
}

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
    await moveInSquare(machine);
  };
  button().disabled = false;
};

main().catch((error) => {
  console.error("encountered an error:", error);
});
```

{{% /tab %}}
{{% tab name="Flutter" %}}

<file>robot_screen.dart</file>:

```dart {class="line-numbers linkable-line-numbers"}
/// This is the BaseScreen, which allows us to control a Base.

import 'package:flutter/material.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

class BaseScreen extends StatelessWidget {
  final Base base;

  const BaseScreen(this.base, {super.key});

  Future<void> moveSquare() async {
    for (var i=0; i<4; i++) {
      await base.moveStraight(500, 500);
      await base.spin(90, 100);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(base.name)),
      body: Center(
        child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
              onPressed: moveSquare,
              child: const Text('Move Base in Square'),
            ),
        ]))
        ,);}}
```

<file>base_screen.dart</file>:

```dart {class="line-numbers linkable-line-numbers"}
/// This is the screen that shows the resources available on a robot (or smart machine).
/// It takes in a Viam app client instance, as well as a robot client.
/// It then uses the Viam client instance to create a connection to that robot client.
/// Once the connection is established, you can view the resources available
/// and send commands to them.

import 'package:flutter/material.dart';
import 'base_screen.dart';
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
    if (rn.subtype == Base.subtype.resourceSubtype) {
      return true;
    }
    return false;
  }

  void _navigate(ResourceName rn) {
    if (rn.subtype == Base.subtype.resourceSubtype) {
      final base = Base.fromRobot(client, rn.name);
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => BaseScreen(base)));
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

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers"}
#include <boost/optional.hpp>
#include <string>
#include <vector>
#include <viam/sdk/robot/client.hpp>
#include <viam/sdk/components/motor.hpp>
#include <viam/sdk/components/base.hpp>
#include <viam/sdk/components/camera.hpp>
#include <viam/sdk/components/encoder.hpp>

using namespace viam::sdk;
using namespace viam::sdk;
using std::cerr;
using std::cout;
using std::endl;

void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    cout << "Move straight" << endl;
    // Move the base forward 600mm at 500mm/s
    base->move_straight(500, 500);
    cout << "Spin" << endl;
    // Spin the base by 90 degree at 100 degrees per second
    base->spin(90, 100);
  }
}

int main() {
    // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    std::string host("<MACHINE-ADDRESS>");
    DialOptions dial_opts;
    // TODO: Replace "<API-KEY-ID>" with your machine's API key ID
    dial_opts.set_entity(std::string("<API-KEY-ID>"));
    // TODO: Replace "<API-KEY>" with your machine's API key
    Credentials credentials("api-key", "<API-KEY>");
    dial_opts.set_credentials(credentials);
    boost::optional<DialOptions> opts(dial_opts);
    Options options(0, opts);

    auto machine = RobotClient::at_address(host, options);

    std::cout << "Resources:\n";
    for (const Name& resource : machine->resource_names()) {
      std::cout << "\t" << resource << "\n";
    }

    std::string base_name("viam_base");

    cout << "Getting base: " << base_name << endl;
    std::shared_ptr<Base> base;
    try {
        base = machine->resource_by_name<Base>(base_name);

        move_in_square(base);

    } catch (const std::exception& e) {
        cerr << "Failed to find " << base_name << ". Exiting." << endl;
        throw;
    }
    return EXIT_SUCCESS;
}
```

{{% /tab %}}

{{< /tabs >}}
