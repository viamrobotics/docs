---
linkTitle: "Handle disconnection and reconnection"
title: "Handle disconnection and reconnection"
weight: 50
layout: "docs"
type: "docs"
description: "Show a connection status indicator, react to reconnection, and rebuild your app's UI state after the SDK reconnects to a machine."
date: "2026-04-10"
---

Show a connection status indicator in your app, react to connection events, and rebuild UI state after the SDK reconnects. The SDK reconnects the transport layer automatically; your app is responsible for rebuilding streams, timers, and anything else that depended on the old connection.

For an explanation of how the SDK reconnects under the hood, see [Connection model](/build-apps/concepts/how-apps-connect/#reconnection).

{{< alert title="Behavior change" color="caution" >}}
In versions of the Viam TypeScript SDK prior to v0.69.0, `DISCONNECTED` fired on any connection drop, including transient network interruptions.
From v0.69.0 onward, `DISCONNECTED` fires only on intentional close or when `noReconnect` is set.
Transient drops emit `RECONNECTING` instead, followed by `CONNECTED` on success or `RECONNECTION_FAILED` when retries are exhausted.

If your app listens for `DISCONNECTED` to detect network drops, listen for `RECONNECTING` instead.
{{< /alert >}}

## Prerequisites

- A project with an active machine connection (see [Connect to a machine](/build-apps/tasks/connect-to-machine/))

## TypeScript: subscribe to connection events

The TypeScript SDK emits events on the `RobotClient` whenever the connection state changes. Subscribe to `connectionstatechange` to get a single handler for all state transitions:

```ts
import * as VIAM from "@viamrobotics/sdk";

const machine = await VIAM.createRobotClient({
  /* ... */
});

machine.on("connectionstatechange", (event) => {
  const { eventType } = event as { eventType: VIAM.MachineConnectionEvent };
  switch (eventType) {
    case VIAM.MachineConnectionEvent.DIALING:
    case VIAM.MachineConnectionEvent.CONNECTING:
      console.log("Connecting...");
      break;
    case VIAM.MachineConnectionEvent.CONNECTED:
      console.log("Connected");
      break;
    case VIAM.MachineConnectionEvent.RECONNECTING:
      console.log("Connection dropped, reconnecting...");
      break;
    case VIAM.MachineConnectionEvent.RECONNECTION_FAILED:
      console.log("Reconnection failed, giving up");
      break;
    case VIAM.MachineConnectionEvent.DISCONNECTING:
    case VIAM.MachineConnectionEvent.DISCONNECTED:
      console.log("Disconnected");
      break;
  }
});
```

`MachineConnectionEvent` has seven values:

| Value                 | When the SDK emits it                                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `DIALING`             | The SDK is dialing the initial connection.                                                                                                   |
| `CONNECTING`          | The SDK is establishing the WebRTC or gRPC channel.                                                                                          |
| `CONNECTED`           | The connection is up and ready for calls.                                                                                                    |
| `RECONNECTING`        | The connection dropped and the SDK is retrying with backoff. Replaces the immediate `DISCONNECTED` event for unintentional drops.            |
| `RECONNECTION_FAILED` | All reconnection attempts were exhausted. The event payload includes `error` and `attempts` fields.                                          |
| `DISCONNECTING`       | The app initiated a disconnect (`disconnect()` or app shutdown).                                                                             |
| `DISCONNECTED`        | The connection is closed and will not retry. Emitted when `noReconnect` is set, when the client was closed, or after intentional disconnect. |

To listen for a specific state only, subscribe to that event type directly:

```ts
machine.on(VIAM.MachineConnectionEvent.DISCONNECTED, () => {
  console.log("Disconnected from machine");
});
```

### Show a status indicator in the browser

A minimal connection indicator in a vanilla browser app:

```ts
const statusEl = document.getElementById("status") as HTMLElement;

function setStatus(text: string, color: string) {
  statusEl.textContent = text;
  statusEl.style.color = color;
}

machine.on("connectionstatechange", (event) => {
  const { eventType } = event as { eventType: VIAM.MachineConnectionEvent };
  switch (eventType) {
    case VIAM.MachineConnectionEvent.CONNECTED:
      setStatus("Connected", "green");
      break;
    case VIAM.MachineConnectionEvent.DIALING:
    case VIAM.MachineConnectionEvent.CONNECTING:
      setStatus("Connecting...", "orange");
      break;
    case VIAM.MachineConnectionEvent.RECONNECTING:
      setStatus("Reconnecting...", "orange");
      break;
    case VIAM.MachineConnectionEvent.RECONNECTION_FAILED:
    case VIAM.MachineConnectionEvent.DISCONNECTING:
    case VIAM.MachineConnectionEvent.DISCONNECTED:
      setStatus("Disconnected", "red");
      break;
  }
});
```

In React, Vue, or Svelte, set a reactive state variable inside the handler instead of mutating the DOM directly.

## Flutter: check `isConnected`

The Flutter SDK does not expose a connection-event API. Check `robot.isConnected` to know the current state:

```dart
if (robot.isConnected) {
  // Connected
} else {
  // Not connected
}
```

`RobotClient` runs a background connection check on a timer (default every 10 seconds) and attempts reconnection on its own if the check fails. You can tune these intervals through `RobotClientOptions`:

```dart
final options = RobotClientOptions.withApiKey(apiKeyId, apiKey);
options.checkConnectionInterval = 5;   // seconds between connection checks
options.attemptReconnectInterval = 2;  // seconds between reconnection attempts

final robot = await RobotClient.atAddress(address, options);
```

Setting either interval to `0` disables the corresponding behavior.

### Show a status indicator in Flutter

Poll `isConnected` on a timer to drive a UI indicator:

```dart
class ConnectionIndicator extends StatefulWidget {
  final RobotClient robot;
  const ConnectionIndicator({super.key, required this.robot});

  @override
  State<ConnectionIndicator> createState() => _ConnectionIndicatorState();
}

class _ConnectionIndicatorState extends State<ConnectionIndicator> {
  Timer? _timer;
  bool _connected = true;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 2), (_) {
      setState(() {
        _connected = widget.robot.isConnected;
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(Icons.circle, color: _connected ? Colors.green : Colors.red, size: 12),
        const SizedBox(width: 8),
        Text(_connected ? 'Connected' : 'Disconnected'),
      ],
    );
  }
}
```

Adjust the `Duration(seconds: 2)` to match how quickly you want the UI to reflect state changes. A shorter interval gives faster feedback but uses more CPU.

## Python and Go

The Python and Go SDKs handle reconnection internally with configurable intervals, similar to Flutter. Both provide a connection check and automatic reconnection.

**Python:**

```python
# Connection check and reconnection are configured through RobotClient.Options
opts = RobotClient.Options.with_api_key(api_key, api_key_id)
opts.check_connection_interval = 10  # seconds between checks (default 10)
opts.attempt_reconnect_interval = 1  # seconds between reconnect attempts (default 1)
```

The Python SDK does not expose a connection-event API. For long-running services, wrap SDK calls in try/except blocks to catch connection errors and log them.

**Go:**

```go
// Connection options are set through RobotClientOption functions
machine, err := client.New(
    ctx, address, logger,
    client.WithDialOptions(rpc.WithEntityCredentials(apiKeyID, creds)),
    client.WithCheckConnectedEvery(10 * time.Second),
)
```

The Go SDK reconnects automatically. For long-running services, check errors returned from individual method calls. A `codes.Unavailable` gRPC status indicates the connection is down; the SDK will attempt to reconnect on the next call.

## Rebuild UI state after reconnection

The SDK reconnects the transport layer automatically, but anything your app built on top of the old connection does not resume automatically. This is the single most important pattern for apps that run through network drops:

- **Camera streams** — the stream is torn down when the connection drops. After reconnection, call `getStream` again and re-attach the stream to your video element.
- **Live sensor polling** — if you were polling `sensor.getReadings()` on a timer, the timer may still be running but the calls will have failed during the outage. Cancel and restart the timer on reconnect, or catch the errors and let the timer naturally resume on reconnection.
- **Operation handles** — any operation IDs, session IDs, or other handles from before the reconnection are no longer valid. Drop them.
- **UI state derived from the connection** — lists of resources, last-known readings, and similar cached data may be stale. Re-fetch after reconnection.

A concrete pattern in TypeScript: when the connection handler reaches `CONNECTED` after having seen `RECONNECTING`, call a `rebuildAfterReconnect()` function that restarts streams and polling:

```ts
let wasReconnecting = false;

machine.on("connectionstatechange", async (event) => {
  const { eventType } = event as { eventType: VIAM.MachineConnectionEvent };
  switch (eventType) {
    case VIAM.MachineConnectionEvent.RECONNECTING:
      wasReconnecting = true;
      break;
    case VIAM.MachineConnectionEvent.CONNECTED:
      if (wasReconnecting) {
        wasReconnecting = false;
        await rebuildAfterReconnect();
      }
      break;
    case VIAM.MachineConnectionEvent.RECONNECTION_FAILED:
    case VIAM.MachineConnectionEvent.DISCONNECTED:
      // Reset the flag so a later fresh connect is not treated as a reconnect.
      wasReconnecting = false;
      break;
  }
});

async function rebuildAfterReconnect() {
  // Recreate camera streams, restart polling, re-fetch resource names, etc.
}
```

Use `RECONNECTING` as the trigger rather than `DISCONNECTED`. The SDK emits `RECONNECTING` as soon as it loses an unintentional connection and starts retrying; `DISCONNECTED` is now only emitted for closed clients or when `noReconnect` is set. Clear `wasReconnecting` on `RECONNECTION_FAILED` and `DISCONNECTED` so that a later reconnect attempt (for example, after the user manually reconnects) does not incorrectly trigger `rebuildAfterReconnect()` on its first `CONNECTED` event. Listen for `RECONNECTION_FAILED` separately if you want to surface the give-up state to the user.

## Next

- [Stream video](/build-apps/tasks/stream-video/) for the camera stream rebuild pattern in detail
- [Query captured data](/build-apps/tasks/query-data/) for polling live data from an app
- [Connection model](/build-apps/concepts/how-apps-connect/#reconnection) for a deeper explanation of the reconnection behavior
