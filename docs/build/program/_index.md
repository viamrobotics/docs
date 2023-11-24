---
title: "Program a Machine"
linkTitle: "Program Machines"
childTitleEndOverwrite: "Program Machines"
description: "Use the SDK of your preferred language to write code to control your machines."
weight: 45
no_list: true
type: docs
image: "/general/code.png"
imageAlt: "Program a machine"
images: ["/general/code.png"]
aliases:
  - "product-overviews/sdk-as-client"
  - "program/sdk-as-client"
  - "program/sdks"
  - /program/
---

You can write code to control your machines using the following software development kits (SDKs):

- [Python SDK](https://python.viam.dev/)
- [Go SDK](https://pkg.go.dev/go.viam.com/rdk)
- [TypeScript SDK](https://ts.viam.dev/)
- [C++ SDK (beta)](https://cpp.viam.dev/)
- [Flutter SDK (beta)](https://flutter.viam.dev/)

The SDKs provide idiomatic wrappers around Viam's robot [gRPC APIs](https://github.com/viamrobotics/api).

![Diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.](/build/program/sdks/robot-client.png)

## Requirements

Before you get started with your program, ensure that you have [installed `viam-server`](/get-started/installation/) on the computer you want to use to control your robot (likely a [single-board computer](/build/configure/components/board/#supported-models)), and [configured your robot](/build/configure/configuration/).

Next, to install your preferred Viam SDK on your Linux or macOS development machine or [single-board computer](/build/configure/components/board/), run one of the following commands in your terminal:

{{< tabs >}}
{{% tab name="Python" %}}

If you are using the Python SDK, [set up a virtual environment](/build/program/python-venv/) to package the SDK inside before running your code, avoiding conflicts with other projects or your system.

```sh {class="command-line" data-prompt="$"}
pip install viam-sdk
```

If you intend to use the [ML (machine learning) model service](/build/configure/services/ml/), use the following command instead, which installs additional required dependencies along with the Python SDK:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {class="command-line" data-prompt="$"}
npm install --save @viamrobotics/sdk
```

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter pub add viam_sdk
```

{{% /tab %}}
{{< /tabs >}}

## Hello World: The Code Sample Tab

Create a program in the language of your choice to connect to your robot and use methods built into the SDK's client API libraries to [interact with and control](/build/program/apis/) the {{< glossary_tooltip term_id="resource" text="resources" >}} on the robot.

Start by navigating to your robot's page on [the Viam app](https://app.viam.com/robots).
Select the **Code Sample** tab, select your preferred SDK, and copy the code generated for you.
This code snippet imports all the necessary libraries to set up a connection with your robot and interface with its configured components and services.

Your boilerplate code sample should look similar to this:

{{%expand "Click this to see example boilerplate code from the Code Sample tab" %}}
{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient


async def connect():
    opts = RobotClient.Options.with_api_key(
      # Replace "<API-KEY>" (including brackets) with your robot's api key
      api_key='<API-KEY>',
      # Replace "<API-KEY-ID>" (including brackets) with your robot's api key
      # id
      api_key_id='<API-KEY-ID>'
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

  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := logging.NewLogger("client")
  robot, err := client.New(
      context.Background(),
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your robot's api key id
      "<API-KEY-ID>",
      rpc.Credentials{
          Type:    rpc.CredentialsTypeAPIKey,
          // Replace "<API-KEY>" (including brackets) with your robot's api key
          Payload: "<API-KEY>",
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

{{< alert title="Info" color="info" >}}
The TypeScript SDK currently only supports building web browser apps.
{{< /alert >}}

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.

import * as VIAM from "@viamrobotics/sdk";

async function main() {
  // Replace with the host of your actual robot running Viam.
  const host = "ADDRESS FROM THE VIAM APP";

  const robot = await VIAM.createRobotClient({
    host,
    credential: {
      type: "api-key",
      // Replace "<API-KEY>" (including brackets) with your robot's api key
      payload: "<API-KEY>",
    },
    // Replace "<API-KEY-ID>" (including brackets) with your robot's api key id
    authEntity: "<API-KEY-ID>",
    signalingAddress: "https://app.viam.com:443",
  });

  console.log("Resources:");
  console.log(await robot.resourceNames());
}

main().catch((error) => {
  console.error("encountered an error:", error);
});
```

{{% /tab %}}
{{% tab name="C++" %}}

{{< alert title="Stability Notice" color="note" >}}
The C++ SDK is currently in beta.
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
  dial_opts.set_type("api-key");
  // Replace "<API-KEY-ID>" with your robot's api key ID
  dial_opts.set_entity("<API-KEY-ID>");
  // Replace "<API-KEY>" with your robot's api key
  Credentials credentials("<API-KEY>");
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

{{< alert title="Stability Notice" color="note" >}}
The Flutter SDK is currently in beta.
{{< /alert >}}

```cpp {class="line-numbers linkable-line-numbers"}
// This must be run from inside an existing app,
// e.g. the default Flutter app created by `flutter create APP_NAME`

// Step 1: Import the viam_sdk
import 'package:viam_sdk/viam_sdk.dart';

// Step 2: Call this function from within your widget
Future<void> connectToViam() async {
  const host = 'ADDRESS FROM THE VIAM APP';
  // Replace '<API-KEY-ID>' (including brackets) with your api key ID
  const apiKeyID = '<API-KEY-ID>';
  // Replace '<API-KEY>' (including brackets) with your api key
  const apiKey = '<API-KEY>';

  final robot = await RobotClient.atAddress(
    host,
    RobotClientOptions.withApiKey(apiKeyId, apiKey),
  );
  print(robot.resourceNames);
}
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand%}}

Save this file on your development machine with the file type of your preferred SDK.

The sample code contains the required imports as well as the connect logic which establishes a connection for your client application to [communicate with](/reference/internals/robot-to-robot-comms/) the robot's `viam-server` instance.
This section of the boilerplate code contains your robot's address and a placeholder for the API key.

### Authenticate

{{< readfile "/static/include/program/authenticate.md" >}}

### Run the sample code

Once you have saved the sample code, [execute your program](/build/program/run/).

You can run your program on any computer which:

1. has [the appropriate SDK](#requirements) installed
2. can establish a connection to your robot through the cloud, on a local or wide area network (LAN or WAN), or [locally](/build/program/run/#run-code-on-robot)

The program will connect to your robot and print a list of the available {{< glossary_tooltip term_id="resource" text="resources" >}}.

### Edit the sample code

Once you have successfully run the sample code, you can edit the boilerplate code by [adding control logic](/build/program/apis/) to make a client application that connects to your robot and controls it in the way you want.
You can find the right libraries to import for SDK methods, typing, interfaces, and utilities at the start of [each resource's API documentation](/build/program/apis/), as well as in the individual SDK documentation sites and [on GitHub](https://github.com/viamrobotics/rdk).

{{< cards >}}
{{% card link="/build/program/apis/" customTitle="Add Logic to Interface with Resources" %}}
{{% card link="/build/program/run/" %}}
{{% card link="/build/program/debug/" %}}
{{< /cards >}}
