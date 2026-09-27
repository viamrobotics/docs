---
title: "Client sessions and machine network connectivity"
linkTitle: "Network connectivity"
weight: 80
type: "docs"
description: "When you connect to a machine, the machine automatically chooses the best connection over local LAN, WAN or the internet."
capabilities: ["sdks"]
diataxis: reference
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
aliases:
  - /dev/reference/sdks/connectivity/
  - /program/connectivity/
  - /sdks/connectivity/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

When connecting to a machine using the connection code from the [**CONNECT** tab](/reference/sdks/), a [client session](/reference/apis/sessions/) automatically uses the most efficient route to connect to your machine either through local LAN or WAN or the internet.

## Connect over local network or offline

To connect directly to your local machine, you can use the connection code from the **CONNECT** tab if you are using the Python SDK, Go SDK, Flutter SDK, or C++ SDK.

For the TypeScript SDK, you must disable TLS on your `viam-server` and set `signalingInsecure: true` in the connection code:

{{< tabs >}}
{{% tab name="Command-line" %}}

Restart `viam-server` with the `-no-tls` flag.

{{% /tab %}}
{{% tab name="Configuration" %}}

1. Add `"no_tls": true` to the `"network"` section of your machine's JSON configuration:

   ```json {class="line-numbers linkable-line-numbers" data-line="5"}
   "network": {
   "no_tls": true
   }
   ```

1. Restart your machine.
   You can restart your machine by clicking on the machine status indicator in Viam and clicking **Restart**.

{{% /tab %}}
{{< /tabs >}}

Update your connection code to set `signalingInsecure` to `true` and point the signaling address at your machine's local address:

```ts {class="line-numbers linkable-line-numbers" data-line="1,2,13,14"}
const host = "mymachine-main.0a1bcdefgi.viam.cloud";
const localAddress = `${host.replace(".viam.cloud", ".local.viam.cloud")}:8080`;

const machine = await VIAM.createRobotClient({
  host,
  credentials: {
    type: "api-key",
    /* Replace "<API-KEY>" (including brackets) with your machine's API key */ payload:
      "<API-KEY>",
    authEntity: "<API-KEY-ID>",
    /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
  },
  signalingAddress: localAddress,
  signalingInsecure: true,
});
```

Port `8080` is the `viam-server` default; use a different port if your machine is configured to listen on one.

## Connectivity Issues

When a machine loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- Cloud sync for the [data management service](/data/capture-sync/capture-and-sync-data/) will pause until the internet connection is re-established since the machine will be unable to connect to Viam.

When a machine loses its connection to LAN or WAN, all client sessions will timeout and end by default.

### Client session timeout and end

When your client cannot connect to your machine's `viam-server` instance, `viam-server` will end any current client [_sessions_](/reference/apis/sessions/) on this machine and all client operations will [time out automatically](/reference/apis/sessions/) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the machine until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/reference/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/reference/sdks/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

{{% alert title="Note" color="note" %}}

There are a couple of exceptions to the general timeout behavior:

- If a [`MoveOnMap`](/reference/apis/services/motion/#moveonmap) or [`MoveOnGlobe`](/reference/apis/services/motion/#moveonglobe) command has completed a motion plan and returned an execution ID before the connection is lost, the resource that receives the motion plan will complete the motion without a connection.
- If a navigation service and motion service are running on the same machine, the navigation service will continue sending requests to the motion service even after losing internet connectivity.

{{% /alert %}}

### Configure a connection timeout

When connecting to a machine using the [robot API](/reference/apis/robot/) from a supported [Viam SDK](/reference/apis/), you can configure an [optional timeout](/reference/apis/sessions/#change-the-session-timeout) to account for intermittent or delayed network connectivity.

## Log connection events from the TypeScript SDK

To see what the TypeScript SDK does while it connects to a machine, turn on its debug log before you create the client.
The SDK then emits a structured entry for each connection attempt, each gRPC request and response, and each disconnect.
Debug logging is off by default and requires `@viamrobotics/sdk` v0.72.0 or later.

To print entries to the console, pass the built-in console writer to `setDebugLogWriter`:

```ts {class="line-numbers linkable-line-numbers"}
import * as VIAM from "@viamrobotics/sdk";

VIAM.setDebugLogWriter(VIAM.createConsoleLogWriter());

const machine = await VIAM.createRobotClient({
  // your connection options
});
```

The console writer prints each entry with `console.debug`, as a JSON string prefixed with `[viam-sdk]`.
In most browsers, `console.debug` output only shows when you enable the **Verbose** log level in the developer console.

To send entries somewhere else, pass your own function. It receives each entry as a `DebugLogEntry` object.
For example, to append entries to a file in Node.js:

```ts {class="line-numbers linkable-line-numbers"}
import fs from "node:fs";
import { setDebugLogWriter } from "@viamrobotics/sdk";

const logFile = fs.createWriteStream("viam-debug.log", { flags: "a" });
setDebugLogWriter((entry) => logFile.write(JSON.stringify(entry) + "\n"));
```

To turn debug logging off again, call `setDebugLogWriter(undefined)`.

Every entry has a `timestamp`, an `event`, and a `connectionId` that is the same for all events from one connection:

<!-- prettier-ignore -->
| Event | When it is logged | Other fields |
| ----- | ----------------- | ------------ |
| `dial_started` | A connection attempt begins. | `method` (`webrtc` or `grpc`), `host`, `attempt` |
| `dial_success` | The connection is established. | `method`, `host` |
| `dial_failed` | A connection attempt fails. | `method`, `host`, `error` |
| `grpc_request` | The SDK sends a gRPC request. | `type` (`unary` or `stream`), `method` (the full gRPC method name) |
| `grpc_response` | The SDK receives a gRPC response. | `type`, `method`, and `error` if the call failed |
| `ice_disconnected` | The WebRTC ICE connection enters the disconnected state. | |
| `client_closed` | Your code closes the client. | |
