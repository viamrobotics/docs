---
linkTitle: "Create a headless app"
title: "Create a headless app"
weight: 30
layout: "docs"
type: "docs"
no_list: true
description: "Run control logic on a machine."
images: ["/general/code.png"]
aliases:
  - "product-overviews/sdk-as-client"
  - "program/sdk-as-client"
  - "program/sdks"
  - /program/
  - /program/run/
  - /program/debug/
---

To write control logic for your machine that will run without a user interface, you can use the Python, Go, or C++ SDK.
The SDKs each include similar methods to hit Viam's [gRPC API](https://github.com/viamrobotics/api) endpoints.

## Decide where to run your code

You can run your code directly on the machine's single-board computer (SBC), or you can run it from a separate computer connected to the internet or to the same local network as your machine's SBC or microcontroller.

### On a separate computer

We recommend running your script on a laptop, desktop, or server if:

- You are using computationally-intensive programs involving, for example, computer vision or motion planning, and
- You have a stable internet connection

The client code will establish a connection to the instance of `viam-server` on your machine's SBC over [LAN or WAN](/dev/reference/sdks/connectivity/).

### On the machine itself

We recommend running your script on the SBC that directly controls your hardware if:

- Your machines have intermittent or no network connectivity, or
- You want to reduce latency, for example for running [PID control loops](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller), or
- Your machine runs continuously (for example, an air quality sensor) and it is impractical to constantly run a client from your development computer

## Install an SDK

Install your preferred Viam SDK on the Linux or macOS computer SBC where you plan to run the control script.

{{< tabs >}}
{{% tab name="Python" %}}

If you are using the Python SDK, [set up a virtual environment](/sdks/python/python-venv/) to package the SDK inside before running your code, avoiding conflicts with other projects or your system.

For macOS (both Intel `x86_64` and Apple Silicon) or Linux (`x86`, `aarch64`, `armv6l`), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

Windows is not supported.
If you are using Windows, use the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) and install the Python SDK using the preceding instructions for Linux.
For other unsupported systems, see [Installing from source](https://python.viam.dev/#installing-from-source).

If you intend to use the [ML (machine learning) model service](/services/ml/), use the following command instead, which installs additional required dependencies along with the Python SDK:

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

To connect your code to your machine, use the API keys Viam automatically generates for you.

1. On your machine's page in the [Viam app](https://app.viam.com), click the **CONNECT** tab.

1. Select your preferred programming **Language**.
   A fully functional code snippet will be displayed, with connection code as well as some calls to the APIs of the resources you've configured on your machine.
   The machine address (which resembles `12345.somemachine-main.viam.cloud`) auto-populates into the connection code.
   It is a public address to connect to your machine.

1. Toggle the **Include API key** to auto-populate the API key and API key ID into the code.
   You can either:

   - Copy the code with the API key in it, **OR**
   - To reduce the risk of accidentally sharing your API key when collaborating on code, create environment variables for the API key and API key ID, and copy the code with **Include API key** toggled off.

   {{< tabs >}}
   {{% tab name="Python" %}}

   The `connect()` function will resemble the following:

   ```python {class="line-numbers linkable-line-numbers" data-line="4,7,9"}
   async def connect():
       opts = RobotClient.Options.with_api_key(
           # Replace "<API-KEY>" (including brackets) with your machine's API key
           api_key='<API-KEY>',
           # Replace "<API-KEY-ID>" (including brackets) with your machine's API key
           # ID
           api_key_id='<API-KEY-ID>'
       )
       return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)
   ```

   Copy not just this function but the entire code snippet on the **CONNECT** tab if you'd like to test your connection with some basic API calls.

   {{% /tab %}}
   {{% tab name="Go" %}}

   The machine connection function will resemble the following:

   ```go {class="line-numbers linkable-line-numbers" data-line="3,7,11"}
   machine, err := client.New(
       context.Background(),
       "ADDRESS FROM THE VIAM APP",
       logger,
       client.WithDialOptions(rpc.WithEntityCredentials(
       // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
       "<API-KEY-ID>",
       rpc.Credentials{
           Type:    rpc.CredentialsTypeAPIKey,
           // Replace "<API-KEY>" (including brackets) with your machine's API key
           Payload: "<API-KEY>",
       })),
   )
   ```

   Copy not just this function but the entire code snippet on the **CONNECT** tab if you'd like to test your connection with some basic API calls.

   {{% /tab %}}
   {{% tab name="C++" %}}

   The machine connection code will resemble the following:

   ```cpp {class="line-numbers linkable-line-numbers" data-line="1,5,7"}
   std::string host("ADDRESS FROM THE VIAM APP");
   DialOptions dial_opts;
   dial_opts.set_type("api-key");
   // Replace "<API-KEY-ID>" with your machine's API key ID
   dial_opts.set_entity("<API-KEY-ID>");
   // Replace "<API-KEY>" with your machine's API key
   Credentials credentials("<API-KEY>");
   dial_opts.set_credentials(credentials);
   boost::optional<DialOptions> opts(dial_opts);
   Options options(0, opts);

   auto robot = RobotClient::at_address(host, options);
   ```

   Copy not just this function but the entire code snippet on the **CONNECT** tab if you'd like to test your connection with some basic API calls.

   {{% /tab %}}
   {{< /tabs >}}

{{< alert title="Caution" color="caution" >}}
Do not share your machine part API key or machine address publicly.
Sharing this information could compromise your system security by allowing unauthorized access to your machine, or to the computer running your machine.
{{< /alert >}}

## Write your control script

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
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


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
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(utils.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
      "<API-KEY-ID>",
      utils.Credentials{
          Type:    utils.CredentialsTypeAPIKey,
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
    std::string host("ADDRESS FROM THE VIAM APP");
    DialOptions dial_opts;
    // Replace "<API-KEY-ID>" with your machine's api key ID
    dial_opts.set_entity(std::string("<API-KEY-ID>"));
    // Replace "<API-KEY>" with your machine's api key
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

The following example from [Automate air filtration with air quality sensors](https://codelabs.viam.com/guide/air-quality/index.html?index=..%2F..index#0) uses both the sensor API's [GetReadings](/dev/reference/apis/components/sensor/#getreadings) command as well as custom functionality with the generic [DoCommand](/appendix/apis/components/generic/#docommand).

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

robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

# Define the sensor and plug names from the Viam app CONFIGURE tab
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
        if any(readings.get(pm_type, 0) > threshold for pm_type, threshold in unhealthy_thresholds.items()):
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

## Run your script

You can run your script manually from your terminal, or you can automatically run it each time your machine starts.

### Run your script manually

To run your script on a laptop or desktop, or to run it on your machine's SBC manually for testing purposes, execute the following command in a terminal:

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

### Run your script as an automatic process

If you want your script to run each time your machine boots, configure the script as a _{{< glossary_tooltip term_id="process" text="process" >}}_ on your machine.
Configured processes are managed by `viam-server` and are a way to run any specified command either once on boot or continuously over the lifecycle of `viam-server`.

{{% alert title="Tip" color="tip" %}}
If you are running your code from a laptop or desktop, we do not recommend configuring your script to run as a process because doing so will cause the process to run whenever you boot your computer, even when you are using your computer for unrelated purposes.
{{% /alert %}}

To configure a process, click the **+** button on your machine's **CONFIGURE** tab and select **Process**.
For detailed configuration information, see [Configure a managed process](/manage/reference/processes/).

#### Example

The following example executes the command `python3 my_cool_script.py` in your <file>/home/myName/project/</file> directory every time your machine boots, and restarts the process if it stops running.

{{< tabs >}}
{{% tab name="Builder mode" %}}

![The CONFIGURE tab with a process called run-my-code configured. The executable is python3, the argument is my_cool_script.py, and the working directory is /home/myName/project. Logging is turned on and execute once is turned off.](/build/configure/process-fancy.png)

{{% /tab %}}
{{% tab name="JSON" %}}

```json
"processes": [
    {
      "id": "run-my-code",
      "log": true,
      "name": "python3",
      "args": [
        "my_cool_script.py"
      ],
      "cwd": "/home/myName/project/"
    }
  ]
```

{{% /tab %}}
{{< /tabs >}}

## Debug

Read and filter a machine's logs to view updates from your machine's `viam-server` instance and troubleshoot issues with your program.

{{< tabs >}}
{{% tab name="App UI" %}}

Navigate to the **LOGS** tab of your machine's page in the [Viam app](https://app.viam.com).

Select from the **Levels** dropdown menu to filter the logs by severity level:

![Filtering by log level of info in the logs tab of the Viam app.](/build/program/sdks/log-level-info.png)

{{% /tab %}}
{{% tab name="CLI" %}}

{{< tabs >}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-server
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {class="command-line" data-prompt="$"}
cat $(brew --prefix)/var/log/viam.log
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}