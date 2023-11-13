---
title: "Manage Robots with Viam's Robot API"
linkTitle: "Robot Management"
weight: 20
type: "docs"
description: "How to use the Robot API to monitor and manage your machines."
tags: ["robot state", "sdk", "apis", "robot api"]
---

The _robot API_ is the application programming interface that manages each of your machines running `viam-server`.
Use the robot API to connect to your machine from within a supported [Viam SDK](/program/apis/), and send commands remotely.

The robot API is supported for use with the [Viam Python SDK](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient), the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient), and the [Viam C++ SDK](https://cpp.viam.dev/classviam_1_1sdk_1_1RobotClient.html).

## Establish a connection

To interact with the robot API with Viam's SDKs, instantiate a `RobotClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

To find the api key, api key id, and robot address, go to [Viam app](https://app.viam.com/), select the robot you wish to connect to, and go to the [**Code sample**](https://docs.viam.com/manage/fleet/robots/#code-sample) tab.
Toggle **Include api key**, and then copy and paste the API key id and the API key into your environment variables or directly into the code:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
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
    # Make a RobotClient
    robot_client = await connect()
    print('Resources:')
    print(robot.resource_names)
    await robot_client.close()

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
  robot, err := client.New(
      timeoutContext,
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
}
```

The example above shows a timeout of 10 seconds configured.

{{% /tab %}}
{{< /tabs >}}

## API

The robot API support the following selected methods.
For the full list of methods, see the [Viam Python SDK documentation](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient) or the [Viam Go SDK documentation](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient).

{{< readfile "/static/include/services/apis/robot.md" >}}

### DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` [(List [viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery): A list of [tuples of API and model](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(List[viam.proto.robot.Discovery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery): The list of discovered component configurations corresponding to `queries`.

```python
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components)

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery): A list of [tuples of API and model](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk/resource#Discovery): The search query `qs` and the corresponding list of discovered component configurations as an interface called `Results`.
  `Results` may be comprised of primitives, a list of primitives, maps with string keys (or at least can be decomposed into one), or lists of the forementioned type of maps.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// Define a new discovery query.
q := resource.NewDiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define a list of discovery queries.
qs := []resource.DiscoverQuery{q}

// Get component configurations with these queries.
component_configs, err := robot.DiscoverComponents(ctx.Background(), qs)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `queries` [(DiscoveryQuery[])](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html): An array of [tuples of API and model](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html#constructor) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(Discovery[])](https://ts.viam.dev/classes/robotApi.Discovery.html): List of discovered component configurations.

```typescript
// Define a new discovery query.
const q = new proto.DiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define an array of discovery queries.
let qs:  proto.DiscoveryQuery[] = [q]

// Get the array of discovered component configurations.
const componentConfigs = await robot.discoverComponents(queries);
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

### FrameSystemConfig

Get the configuration of the frame system of a given robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` [(Optional[List[viam.proto.common.Transform]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): A optional list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- `frame_system` [(List[FrameSystemConfig])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig): The configuration of a given robot’s frame system.

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the robot.
frame_system = await robot.get_frame_system_config()
print(f"frame system configuration: {frame_system}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(framesystem.Config)](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#Config): The configuration of the given robot’s frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Print the frame system configuration
frameSystem, err := robot.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` [(Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): An optional array of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(FrameSystemConfig[])](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): An array of individual parts that make up a robot's frame system.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#frameSystemConfig).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the frame system configuration.
console.log("FrameSytemConfig:", await robot.frameSystemConfig());
```

{{% /tab %}}
{{< /tabs >}}

### Status

Get the status of the resources on the robot.
You can provide a list of ResourceNames for which you want statuses.
If no names are passed in, the status of every resource configured on the robot is returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `resourceNames` [(Optional[List[viam.proto.common.ResourceName]])](https://docs.python.org/library/typing.html#typing.Optional): An optional list of ResourceNames for components you want the status of.
  If no names are passed in, all resource statuses are returned.

**Returns:**

- ([List[str]](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): A list containing the status of each resource.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

```python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the robot.
statuses = await robot.get_status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `resourceNames` [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): An optional list of ResourceNames for components you want the status of.
  If no names are passed in, all resource statuses are returned.

**Returns:**

- [([]Status)](https://pkg.go.dev/go.viam.com/rdk/robot#Status): Status of each resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
status, err = robot.Status(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `resourceNames` [(commonApi.ResourceName[])](https://ts.viam.dev/classes/commonApi.ResourceName.html): An optional array of ResourceNames for components you want the status of.
  If no names are passed in, all resource statuses are returned.

**Returns:**

- [(robotApi.Status[])](https://ts.viam.dev/classes/robotApi.Status.html): An array containing the status of each resource.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
const status = await robot.getStatus();
```

{{% /tab %}}
{{< /tabs >}}

### Close

Close the underlying connections and stop any periodic tasks across all constituent parts of the robot.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.close).

```python {class="line-numbers linkable-line-numbers"}
# Cleanly close the underlying connections and stop any periodic tasks.
await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks,
err := robot.Close(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#disconnect).

```typescript {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks
await robot.disconnect();
```

{{% /tab %}}
{{< /tabs >}}

### StopAll

Cancel all current and outstanding operations for the robot and stop all actuators and movement.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Dict[viam.proto.common.ResourceName, Dict[str, Any]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`ResourceName`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

```python {class="line-numbers linkable-line-numbers"}
# Cancel all current and outstanding operations for the robot and stop all
# actuators and movement.
await robot.stop_all()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[resource.Name]map[string]interface{})](https://pkg.go.dev/go.viam.com/rdk/resource#Name): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`Name`](https://pkg.go.dev/go.viam.com/rdk/resource#Name).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
err := robot.StopAll(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#stopAll).

```typescript {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stopAll();
```

{{% /tab %}}
{{< /tabs >}}

### ResourceNames

Get a list of all known resource names connected to this robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): List of all known resource names. A property of a [RobotClient](https://python.viam.dev/autoapi/viam/robot/client/index.html)

```python
resource_names = robot.resource_names
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): List of all known resource names.

```go
resource_names := robot.ResourceNames()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(ResourceName.AsObject[])](https://ts.viam.dev/modules/commonApi.ResourceName-1.html): List of all known resource names.

```typescript
// Get a list of all resources on the robot.
const resource_names = await robot.resourceNames();
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

### WithAPIKey

Create a client to interact with your robot using an API key as credentials.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `api_key` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): [An API key](/manage/cli/#authenticate) with access to the robot.

- `api_key_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Your API key ID.
  Must be a valid UUID.

**Returns:**

- [(RobotClient.Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient): A gRPC client for interacting with your robot.

- [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): List of all known resource names. A property of a [RobotClient](https://python.viam.dev/autoapi/viam/robot/client/index.html)

```python
api_key = "your_api_key"
api_key_id = "valid_uuid"
robot_client = RobotClient.with_api_key(api_key, api_key_id)
```

{{% /tab %}}
{{< /tabs >}}

For the full list of robot API methods, see the [Viam Python SDK documentation](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient) or the [RDK (the Viam Go SDK) documentation](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient).
