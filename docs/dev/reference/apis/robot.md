---
title: "Manage machines with Viam's machine management API"
linkTitle: "Machine management"
weight: 20
type: "docs"
description: "How to use the machine API to monitor and manage your machines."
tags: ["robot state", "sdk", "apis", "robot api"]
aliases:
  - /program/apis/robot/
  - /build/program/apis/robot/
  - /appendix/apis/robot/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The _machine API_ allows you to connect to your machine from within a supported [Viam SDK](/dev/reference/apis/), retrieve status information, and send commands remotely.

The machine API is supported for use with the [Viam Python SDK](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient), the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient), and the [Viam C++ SDK](https://cpp.viam.dev/classviam_1_1sdk_1_1RobotClient.html).

The machine API supports the following methods:

{{< readfile "/static/include/robot/apis/generated/robot-table.md" >}}

## Establish a connection

To interact with the machine API with Viam's SDKs, instantiate a `RobotClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

To find the API key, API key ID, and machine address, go to [Viam](https://app.viam.com/), select the machine you wish to connect to, and go to the **CONNECT** tab.
Toggle **Include API key**, and then copy and paste the API key ID and the API key into your environment variables or directly into the code:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.robot.client import RobotClient


async def connect() -> RobotClient:
    opts = RobotClient.Options.with_api_key(
            # Replace "<API-KEY>" (including brackets) with your API key
            api_key='<API-KEY>',
            # Replace "<API-KEY-ID>" (including brackets) with your
            # API key ID
            api_key_id='<API-KEY-ID>'
        )
    return await RobotClient.at_address(
      address='MACHINE ADDRESS',
      options=opts
    )


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
)

func main() {
  logger := logging.NewLogger("client")
  machine, err := client.New(
      context.Background(),
      "MACHINE ADDRESS",
      logger,
      client.WithDialOptions(utils.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your machine's
      // API Key ID
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

Add a `timeout` to [`DialOptions`](https://python.viam.dev/autoapi/viam/rpc/dial/index.html#viam.rpc.dial.DialOptions) inside of `Options`:

```python {class="line-numbers linkable-line-numbers"}
# Add the timeout argument to DialOptions:
opts = RobotClient.Options(
    dial_options=DialOptions(timeout=10)).with_api_key(
      ...
    )
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
      "MACHINE ADDRESS",
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

{{< readfile "/static/include/robot/apis/generated/robot.md" >}}
