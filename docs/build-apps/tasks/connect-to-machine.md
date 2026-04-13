---
linkTitle: "Connect to a machine"
title: "Connect to a machine"
weight: 30
layout: "docs"
type: "docs"
description: "Open a connection to a single Viam machine from your app, structure the connection code correctly, and close the connection when your app is done with it."
date: "2026-04-10"
---

Open a connection to a single Viam machine from your app, structure the connection code so you do not reconnect unnecessarily, and close the connection when the app is done with it. This page covers the basic connection pattern. For reconnection, UI indicators, and connection-state events, see [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/). For apps that access multiple machines or the fleet APIs, see [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/).

## Prerequisites

- A project set up with the Viam SDK (see [App scaffolding](/build-apps/setup/))
- The machine's address, an API key, and an API key ID, copied from the machine's **CONNECT** tab in the Viam app

## Open a connection

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
import * as VIAM from "@viamrobotics/sdk";

const machine = await VIAM.createRobotClient({
  host: "my-robot-main.xxxx.viam.cloud",
  credentials: {
    type: "api-key",
    authEntity: process.env.API_KEY_ID,
    payload: process.env.API_KEY,
  },
  signalingAddress: "https://app.viam.com:443",
});
```

`createRobotClient` returns a `RobotClient` connected to your machine. The `await` resolves once the WebRTC connection is established and the session has started.

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
import 'package:viam_sdk/viam_sdk.dart';

final robot = await RobotClient.atAddress(
  'my-robot-main.xxxx.viam.cloud',
  RobotClientOptions.withApiKey('your-api-key-id', 'your-api-key-secret'),
);
```

`RobotClient.atAddress` returns a `RobotClient` connected to your machine. The `await` resolves once the WebRTC connection is established and the session has started.

{{% /tab %}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='your-api-key-secret',
        api_key_id='your-api-key-id'
    )
    return await RobotClient.at_address('my-robot-main.xxxx.viam.cloud', opts)


machine = await connect()
```

`RobotClient.at_address` is async. All Viam Python SDK methods use `async`/`await` and run inside `asyncio.run()`.

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "context"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/utils/rpc"
)

logger := logging.NewDebugLogger("client")
machine, err := client.New(
    context.Background(),
    "my-robot-main.xxxx.viam.cloud",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
        "your-api-key-id",
        rpc.Credentials{
            Type:    "api-key",
            Payload: "your-api-key-secret",
        },
    )),
)
if err != nil {
    logger.Fatal(err)
}
```

`client.New` returns a `*RobotClient` and an error. Always check the error before using the client.

{{% /tab %}}
{{< /tabs >}}

For an explanation of what the SDK does during connection (WebRTC signaling, ICE, sessions, reconnection), see [Connection model](/build-apps/concepts/how-apps-connect/). The defaults work for machines deployed on Viam Cloud; you override them only for self-hosted or local-network setups.

## Close the connection

Close the connection when your app is done with it. Closing releases resources, ends the session, and stops background reconnection attempts.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
await machine.disconnect();
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
await robot.close();
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
await machine.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
machine.Close(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

In a browser app, the tab closing eventually tears down the connection on its own, but closing explicitly avoids a race where pending operations continue after the page unloads. In a Node.js script, always close before `process.exit()` or the script may hang on an open WebRTC connection. In a Flutter app, close in `State.dispose()` if the connection was created per-screen, or in a service class's dispose method if the connection is app-wide.

## Handle errors during connect

Network failures, wrong credentials, and unreachable machines all raise errors from the connect call. Wrap the call in a try-catch:

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
let machine: VIAM.RobotClient;
try {
  machine = await VIAM.createRobotClient({
    host: "my-robot-main.xxxx.viam.cloud",
    credentials: {
      type: "api-key",
      authEntity: process.env.API_KEY_ID,
      payload: process.env.API_KEY,
    },
    signalingAddress: "https://app.viam.com:443",
  });
} catch (err) {
  console.error("Failed to connect:", err);
  return;
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
late RobotClient robot;
try {
  robot = await RobotClient.atAddress(
    'my-robot-main.xxxx.viam.cloud',
    RobotClientOptions.withApiKey('your-api-key-id', 'your-api-key-secret'),
  );
} catch (e) {
  print('Failed to connect: $e');
  return;
}
```

{{% /tab %}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line=""}
try:
    opts = RobotClient.Options.with_api_key(
        api_key='your-api-key-secret',
        api_key_id='your-api-key-id'
    )
    machine = await RobotClient.at_address(
        'my-robot-main.xxxx.viam.cloud', opts
    )
except Exception as e:
    print(f"Failed to connect: {e}")
    # In a real app: raise, sys.exit(1), or handle appropriately
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
machine, err := client.New(
    context.Background(),
    "my-robot-main.xxxx.viam.cloud",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
        "your-api-key-id",
        rpc.Credentials{
            Type:    "api-key",
            Payload: "your-api-key-secret",
        },
    )),
)
if err != nil {
    logger.Fatalf("Failed to connect: %v", err)
}
defer machine.Close(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

The error from a failed connect is generic. The SDK does not always distinguish credential errors from network errors. Log the error message verbatim when debugging, and check the **CONNECT** tab in the Viam app to confirm the machine is online before assuming the code is wrong.

Once the connection is established, subsequent network drops trigger automatic reconnection rather than thrown errors. See [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for the reconnection pattern.

## Where to put connection code

Create the `RobotClient` once at the right lifetime boundary and share it across the parts of your app that need it. Do not call `createRobotClient` or `RobotClient.atAddress` inside a render function or a click handler: each call opens a new connection and orphans the previous one.

- **Browser SPA.** Create the client in your app's root component or in a service module imported at startup. Pass it down through props, context, or a state store. Close once on app unmount.
- **Node.js script.** Create the client at the top of `main()` and close it before `process.exit()`. For long-running services, keep the client alive and let automatic reconnection handle network drops.
- **Python script or service.** Create the client at the top of your `main()` coroutine. Use `async with` or call `await machine.close()` in a `finally` block. For long-running services, keep the client alive for the service's lifetime.
- **Go service.** Create the client at the top of `main()` and `defer machine.Close(ctx)`. For long-running services, keep the client alive and let automatic reconnection handle drops.
- **Flutter app.** Create the client in `initState` or a service class (Provider, Riverpod, or similar). Dispose in `dispose()`. For apps with multiple screens, put the client in a service class rather than in each screen's state.

## Next

- [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for reconnection behavior, UI indicators, and connection events
- [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/) for apps that access multiple machines or use the fleet, data, and billing APIs
- [Stream video](/build-apps/tasks/stream-video/) for displaying camera feeds from your connected machine
