---
title: "Manage Machines with Viam's Robot API"
linkTitle: "Machine Management"
weight: 20
type: "docs"
description: "How to use the Robot API to monitor and manage your machines."
tags: ["robot state", "sdk", "apis", "robot api"]
aliases:
  - /program/apis/robot/
  - /build/program/apis/robot/
---

The _robot API_ is the application programming interface that manages each of your machines running `viam-server`.
Use the robot API to connect to your machine from within a supported [Viam SDK](/appendix/apis/), and send commands remotely.

The robot API is supported for use with the [Viam Python SDK](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient), the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient), and the [Viam C++ SDK](https://cpp.viam.dev/classviam_1_1sdk_1_1RobotClient.html).

## Establish a connection

To interact with the robot API with Viam's SDKs, instantiate a `RobotClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

To find the API key, API key ID, and machine address, go to [Viam app](https://app.viam.com/), select the machine you wish to connect to, and go to the [**Code sample**](/cloud/machines/#code-sample) tab.
Toggle **Include API key**, and then copy and paste the API key ID and the API key into your environment variables or directly into the code:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.robot.client import RobotClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


async def main():
    # Make a RobotClient
    machine = await connect()
    print('Resources:')
    print(machine.resource_names)
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

You can use this code to connect to your machine and instantiate a `RobotClient` that you can then use with the [robot API](#api).
As an example, this code uses the instantiated `RobotClient` to return the {{< glossary_tooltip term_id="resource" text="resources" >}} currently configured.
Remember to always close the connection (using `close()`) when done.

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
  machine, err := client.New(
      context.Background(),
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your machine's
      // API Key ID
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
  logger.Info("Resources:")
  logger.Info(machine.ResourceNames())
}
```

You can use this code to connect to your machine and instantiate a `robot` client that you can then use with the [Robot API](#api).
As an example, this code uses the instantiated `robot` client to return the configured {{< glossary_tooltip term_id="resource" text="resources" >}}.
Remember to always close the connection (using `Close()`) when done.

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated the robot client, you can run any of the [robot API methods](#api) against the `robot` object to communicate with your machine.

### Configure a timeout

Because the robot API needs to be able to reliably connect to a deployed machine even over a weak or intermittent network, it supports a configurable timeout for connection and command execution.

To configure a timeout when using the robot API:

{{< tabs >}}
{{% tab name="Python" %}}

Add a `timeout` to [`DialOptions`](https://python.viam.dev/autoapi/viam/rpc/dial/index.html#viam.rpc.dial.DialOptions):

```python {class="line-numbers linkable-line-numbers"}
# Add the timeout argument to DialOptions:
dial_options = DialOptions(credentials=creds, timeout=10)
```

The example above shows a timeout of 10 seconds configured.

{{% /tab %}}
{{% tab name="Go" %}}

Import the `time` package, then add a timeout to your context using `WithTimeout`:

```go {class="line-numbers linkable-line-numbers"}
// Import the time package in addition to the other imports:
import (
  ...
  "time"
  ...
)

// Edit your main() to configure a timeoutContext, then pass this context to the dial invocation:
func main() {
  ctx := context.Background()
  timeoutContext, cancel := context.WithTimeout(ctx, 10*time.Second)
  defer cancel()
  machine, err := client.New(
      timeoutContext,
      "ADDRESS FROM THE VIAM APP",
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
}
```

The example above shows a timeout of 10 seconds configured.

{{% /tab %}}
{{< /tabs >}}

## API

The robot API support the following selected methods.
For the full list of methods, see the [Viam Python SDK documentation](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient) or the [Viam Go SDK documentation](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient).

{{< readfile "/static/include/robot/apis/generated/robot-table.md" >}}

{{< readfile "/static/include/robot/apis/generated/robot.md" >}}
