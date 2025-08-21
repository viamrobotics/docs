---
linkTitle: "Create a headless app"
title: "Create a headless app"
weight: 30
layout: "docs"
type: "docs"
description: "Run control logic on a machine."
images: ["/general/code.png"]
aliases:
  - /product-overviews/sdk-as-client/
  - /program/sdk-as-client/
  - /program/sdks/
  - /program/
  - /program/run/
  - /program/debug/
  - /how-tos/develop-app/
  - /use-cases/develop-app/
  - /product-overviews/sdk-as-client/
---

To write control logic for your machine that will run without a user interface, you can use the Python, Go, or C++ SDK.
The SDKs each include similar methods to hit Viam's [gRPC API](https://github.com/viamrobotics/api) endpoints.

## Decide where to run your code

You can run your code directly on the [machine's](/operate/get-started/setup/) single-board computer (SBC), or you can run it from a separate computer connected to the internet or to the same local network as your machine's SBC or microcontroller.

### On a separate computer

We recommend running your code on a laptop, desktop, or server if:

- You are using computationally-intensive programs involving, for example, computer vision or motion planning, and
- You have a stable internet connection

The client code will establish a connection to the instance of `viam-server` on your machine's SBC over [LAN or WAN](/dev/reference/sdks/connectivity/).

### On the machine itself

We recommend running your code on the SBC that directly controls your hardware if:

- Your machines have intermittent or no network connectivity, or
- You want to reduce latency, for example for running [PID control loops](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller), or
- Your machine runs continuously (for example, an air quality sensor) and it is impractical to constantly run a client from your development computer

## Install an SDK

Install your preferred Viam SDK on the computer or SBC where you plan to run the control script.

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

If you intend to use the [ML (machine learning) model service](/data-ai/ai/deploy/), use the following command instead, which installs additional required dependencies along with the Python SDK:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{% /tab %}}
{{% tab name="Go" %}}

Run the following command to install the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk):

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{< /tabs >}}

## Authenticate

You can find sample connection code on each [machine's](/operate/get-started/setup/) **CONNECT** tab.
Select your preferred **Language** to display a code snippet, with connection code as well as some calls to the APIs of the resources you've configured on your machine.

You can use the toggle to include the machine API key and API key ID, though we strongly recommend storing your API keys in environment variables to reduce the risk of accidentally sharing your API key and granting access to your machines.

If your code will connect to multiple machines or use [Platform APIs](/dev/reference/apis/#platform-apis) you can create an API key with broader access.

## Write your control code

For API reference including code snippets for each method, see [Viam's Client APIs](/dev/reference/apis/).

{{< expand "Example code for moving a rover in a square" >}}

The following code moves a mobile robot base in a square using the [base API](/dev/reference/apis/components/base/).

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with your
        # machine's API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address('<MACHINE-ADDRESS>', opts)


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

{{< /expand >}}

{{< expand "Example Python code for turning on a fan based on sensor readings" >}}

The following example from [Automate air filtration with air quality sensors](https://codelabs.viam.com/guide/air-quality/index.html?index=..%2F..index#0) uses both the sensor API's [GetReadings](/dev/reference/apis/components/sensor/#getreadings) command as well as custom functionality with the generic [DoCommand](/dev/reference/apis/components/generic/#docommand).

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import os
from dotenv import load_dotenv
from viam.logging import getLogger
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor
from viam.components.generic import Generic

load_dotenv()
LOGGER = getLogger(__name__)

robot_api_key = os.getenv('MACHINE_API_KEY') or ''
robot_api_key_id = os.getenv('MACHINE_API_KEY_ID') or ''
robot_address = os.getenv('MACHINE_ADDRESS') or ''

# Define the sensor and plug names on the CONFIGURE tab
sensor_name = os.getenv("SENSOR_NAME", "")
plug_name = os.getenv("PLUG_NAME", "")


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key=robot_api_key,
        api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)


async def main():
    machine = await connect()

    pms_7003 = Sensor.from_robot(machine, sensor_name)
    kasa_plug = Generic.from_robot(machine, plug_name)

    # Define unhealthy thresholds
    unhealthy_thresholds = {
        'pm2_5_atm': 35.4,
        'pm10_atm': 150
    }

    while True:
        readings = await pms_7003.get_readings()
        # Check if any of the PM values exceed the unhealthy thresholds
        if any(readings.get(pm_type, 0) > threshold for pm_type,
                threshold in unhealthy_thresholds.items()):
            LOGGER.info('UNHEALTHY.')
            await kasa_plug.do_command({"toggle_on": []})
        else:
            LOGGER.info('HEALTHY!')
            await kasa_plug.do_command({"toggle_off": []})

        # wait before checking again
        await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
```

{{< /expand >}}

## Run your code

You can run your code manually from your terminal, or you can automatically run it each time your machine starts.

### Run your code manually

To run your code on a laptop or desktop, or to run it on your machine's SBC manually for testing purposes, execute the following command in a terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 /home/myName/project/my_cool_script.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go run /home/myName/project/my_cool_script.go
```

{{% /tab %}}
{{% tab name="C++" %}}

For information on running C++ code see [the instructions on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{< /tabs >}}

### Run your control code in a module

To run your control code on your machine, create a {{< glossary_tooltip term_id="module" text="module" >}} and deploy it to your machine.
You can add functionality to the `DoCommand()` method to, for example, start and stop the control code.

For more information, see [Create a module with machine control logic](/manage/software/control-logic/#add-control-logic-to-your-module).

## Debug

Read and filter a machine's logs to view updates from your machine's `viam-server` instance and troubleshoot issues with your program.

{{< tabs >}}
{{% tab name="App UI" %}}

Navigate to the **LOGS** tab of your machine's page.

Select from the **Levels** dropdown menu to filter the logs by severity level:

![Filtering by log level of info in the logs tab.](/build/program/sdks/log-level-info.png)

{{% /tab %}}
{{% tab name="Command line" %}}

```sh {class="command-line" data-prompt="$"}
viam machines part logs --part=<part-id> --tail=true
```

{{% /tab %}}
{{< /tabs >}}
