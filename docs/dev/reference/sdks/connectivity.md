---
title: "Client sessions and machine network connectivity"
linkTitle: "Network connectivity"
weight: 80
type: "docs"
description: "When you connect to a machine, the machine automatically chooses the best connection over local LAN, WAN or the internet."
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
aliases:
  - /program/connectivity/
  - /sdks/connectivity/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

When connecting to a machine using the connection code from the [**CONNECT** tab](/dev/reference/sdks/), a [client session](/dev/reference/apis/sessions/) automatically uses the most efficient route to connect to your machine either through local LAN or WAN or the internet.

## Connect over local network or offline

To connect directly to your local machine, you can use the connection code from the **CONNECT** tab if you are using the Python SDK, Go SDK, Flutter SDK, or C++ SDK.

For the TypeScript SDK, you must disable TLS verification for your `viam-server` and change the sinaling address for the connection code:

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

Update the signaling address in your connection code:

```ts {class="line-numbers linkable-line-numbers" data-line="1,12"}
const host = "mymachine-main.0a1bcdefgi.viam.cloud";

const machine = await VIAM.createRobotClient({
  host,
  credentials: {
    type: "api-key",
    /* Replace "<API-KEY>" (including brackets) with your machine's API key */ payload:
      "<API-KEY>",
    authEntity: "<API-KEY-ID>",
    /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
  },
  signalingAddress: `http://${host}.local:8080`,
});
```

## Connectivity Issues

When a machine loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- Cloud sync for the [data management service](/data-ai/capture-data/capture-sync/) will pause until the internet connection is re-established since the machine will be unable to connect to Viam.

When a machine loses its connection to LAN or WAN, all client sessions will timeout and end by default.

### Client session timeout and end

When your client cannot connect to your machine's `viam-server` instance, `viam-server` will end any current client [_sessions_](/dev/reference/apis/sessions/) on this machine and all client operations will [time out automatically](/dev/reference/apis/sessions/) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the machine until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/dev/reference/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/dev/reference/sdks/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

{{% alert title="Note" color="note" %}}

There are a couple of exceptions to the general timeout behavior:

- If a [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) or [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) command has completed a motion plan and returned an execution ID before the connection is lost, the resource that receives the motion plan will complete the motion without a connection.
- If a navigation service and motion service are running on the same machine, the navigation service will continue sending requests to the motion service even after losing internet connectivity.

{{% /alert %}}

### Configure a connection timeout

When connecting to a machine using the [robot API](/dev/reference/apis/robot/) from a supported [Viam SDK](/dev/reference/apis/), you can configure an [optional timeout](/dev/reference/apis/sessions/#change-the-session-timeout) to account for intermittent or delayed network connectivity.
