---
title: "Get Started Programming your Robot with Viam's SDKs"
linkTitle: "Write Code"
weight: 40
type: "docs"
description: "Access and control your robot with the resource and robot APIs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
no_list: true
aliases:
  - "/product-overviews/sdk-as-client"
  - "/program/sdk-as-client"
---

## Connect to your robot

## Code Sample

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **Setup** tab and follow the instructions there.
4. [Configure](../../manage/configuration) your robot.

{{% /alert %}}

The easiest way to get started is to navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **Code Sample** tab, select your preferred SDK, and copy the code generated for you.

These boilerplate code samples import all of the necessary libraries and set up a client connection to your robot whether your code runs on your robot or on a different machine.
This connection is established through the Viam app in the cloud.

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
        payload='LOCATION SECRET FROM THE VIAM APP')
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
          Payload: "LOCATION SECRET FROM THE VIAM APP",
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
The TypeScript SDK currently only supports building web browser apps.
{{< /alert >}}

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.

import * as VIAM from '@viamrobotics/sdk';

async function main() {
  const host = 'ADDRESS FROM THE VIAM APP';

  const robot = await VIAM.createRobotClient({
    host,
    credential: {
      type: 'robot-location-secret',
      payload: 'LOCATION SECRET FROM THE VIAM APP',
    },
    authEntity: host,
    signalingAddress: 'https://app.viam.com:443',
  });
  

  console.log('Resources:');
  console.log(await robot.resourceNames());
}

main().catch((error) => {
  console.error('encountered an error:', error)
});
```

{{% /tab %}}
{{% tab name="C++" %}}

{{< alert title="Note" color="note" >}}
The C++ SDK is currently in alpha.
{{< /alert >}}

```cpp {class="line-numbers linkable-line-numbers"}
# include <string>
# include <vector>

# include <boost/optional.hpp>

# include <viam/api/common/v1/common.pb.h>
# include <viam/api/robot/v1/robot.grpc.pb.h>

# include <viam/sdk/robot/client.hpp>
# include <viam/sdk/components/camera/client.hpp>

using namespace viam::sdk;

int main() {
  std::string host("ADDRESS FROM THE VIAM APP");
  DialOptions dial_opts;
  Credentials credentials("LOCATION SECRET FROM THE VIAM APP");
  dial_opts.set_credentials(credentials);
  boost::optional<DialOptions> opts(dial_opts);
  Options options(0, opts);

  auto robot = RobotClient::at_address(host, options);

  std::cout << "Resources:\n";
  for (const ResourceName& resource: *robot->resource_names()) {
    std::cout << resource.namespace_() << ":" << resource.type() << ":"
              << resource.subtype() << ":" << resource.name() << "\n";
  }

  return 0;
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

{{< alert title="Note" color="note" >}}
The Flutter SDK is currently in alpha.
{{< /alert >}}

```cpp {class="line-numbers linkable-line-numbers"}
import 'package:viam_sdk/viam_sdk.dart';

// Connect to an existing robot
// *NOTE* Get the <LOCATION> and <SECRET> from app.viam.com
final options = RobotClientOptions.withLocationSecret('<SECRET>');
final robot = await RobotClient.atAddress('<LOCATION>', options);

// Print the available resources
print(robot.resourceNames);

// Access a component
final movementSensor = MovementSensor.fromRobot(robot, 'my_sensor');
print(await movementSensor.readings())
```

{{% /tab %}}
{{< /tabs >}}

## Add Control Logic

<!-- You can add control logic for each [component](/components/) of your robot by using the built-in component methods.

Find documentation on how to use these methods here:

- [Arm](/components/arm/#api)
- [Base](/components/base/#api)
- [Board](/components/board/#api)
- [Camera](/components/camera/#api)
- [Encoder](/components/encoder/#api)
- [Gantry](/components/gantry/#api)
- [Gripper](/components/gripper/#api)
- [Input Controller](/components/input-controller/#api)
- [Motor](/components/motor/#api)
- [Movement Sensor](/components/movement-sensor/#api)
- [Sensor](/components/sensor/#api)
- [Servo](/components/servo/#api)

You can find example code in the [Python SDK example GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1), the [Golang SDK example GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples), or the [TypeScript SDK example GitHub repository](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples). -->
