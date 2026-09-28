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

## Choose the WebRTC connection route

By default, a WebRTC connection tries every route it can find and prefers a direct peer-to-peer connection, falling back to relay through a TURN server if no direct route works.
To test a specific route, or to work around a network that blocks one, you can restrict which routes the SDK uses:

- **Force relay:** use only TURN relay candidates. Use this to check that your machine is reachable through a TURN server.
- **Force peer-to-peer:** remove all TURN servers, so the SDK only uses direct routes. Use this to check whether a direct connection works without relay fallback.
  Do not combine it with force relay: the connection fails, because force peer-to-peer removes the TURN servers that force relay needs.
- **TURN URI:** use only the TURN server from the signaling server's list whose URI matches, for example `turn:turn.viam.com:443`.
  It has no effect when you force peer-to-peer.
  The Go and TypeScript SDKs can also override the scheme (`turn` or `turns`), transport (`tcp` or `udp`), and port of the matched TURN server.

{{< tabs >}}
{{% tab name="Python" %}}

Set `force_relay`, `force_p2p`, or `turn_uri` on the connection's `DialOptions`:

```python {class="line-numbers linkable-line-numbers" data-line="5"}
opts = RobotClient.Options.with_api_key(
    api_key='<API-KEY>',
    api_key_id='<API-KEY-ID>'
)
opts.dial_options.force_relay = True
machine = await RobotClient.at_address('<MACHINE-ADDRESS>', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

Pass `client.WithForceRelay()`, `client.WithForceP2P()`, `client.WithTurnURI(uri)`, `client.WithTurnScheme(scheme)`, `client.WithTurnTransport(transport)`, or `client.WithTurnPort(port)` to `client.WithDialOptions`:

```go {class="line-numbers linkable-line-numbers" data-line="11"}
machine, err := client.New(
    context.Background(),
    "<MACHINE-ADDRESS>",
    logger,
    client.WithDialOptions(
        client.WithEntityCredentials("<API-KEY-ID>",
            client.Credentials{
                Type:    client.CredentialsTypeAPIKey,
                Payload: "<API-KEY>",
            }),
        client.WithForceRelay(),
    ),
)
```

If you also pass `client.WithWebRTCOptions`, put it before these options. `WithWebRTCOptions` replaces all WebRTC options set before it.

{{% /tab %}}
{{% tab name="TypeScript" %}}

Set `forceRelay`, `forceP2P`, `turnUri`, `turnScheme`, `turnTransport`, or `turnPort` in the options you pass to `createRobotClient`:

```ts {class="line-numbers linkable-line-numbers" data-line="8"}
const machine = await VIAM.createRobotClient({
  host: "<MACHINE-ADDRESS>",
  credentials: {
    type: "api-key",
    payload: "<API-KEY>",
    authEntity: "<API-KEY-ID>",
  },
  forceRelay: true,
  signalingAddress: "https://app.viam.com:443",
});
```

{{% /tab %}}
{{< /tabs >}}

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

### Log connection details from an SDK client

To see more detail about what your client does while it connects to a machine, turn on the SDK's debug logging before you connect.
Debug logging also records other client activity, such as individual gRPC calls, so expect verbose output.

{{< tabs >}}
{{% tab name="Go" %}}

Use a debug logger and pass `client.WithDialDebug()` in the same `client.WithDialOptions` call as your credentials:

```go {class="line-numbers linkable-line-numbers" data-line="1,7"}
logger := logging.NewDebugLogger("client")

machine, err := client.New(ctx, "<machine address>", logger,
  client.WithDialOptions(
    client.WithEntityCredentials("<API-KEY-ID>",
      client.Credentials{Type: client.CredentialsTypeAPIKey, Payload: "<API-KEY>"}),
    client.WithDialDebug(),
  ),
)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Pass a debug log writer to `setDebugLogWriter` before you create the client.
This requires `@viamrobotics/sdk` v0.72.0 or later:

```ts {class="line-numbers linkable-line-numbers" data-line="1"}
VIAM.setDebugLogWriter(VIAM.createConsoleLogWriter());

const machine = await VIAM.createRobotClient({
  // your connection options
});
```

The console writer logs each entry with `console.debug`, which most browsers only show when you enable the **Verbose** log level in the developer console.
To send entries somewhere else or turn logging off, see [`setDebugLogWriter`](https://ts.viam.dev/functions/setDebugLogWriter.html).

{{% /tab %}}
{{< /tabs >}}
