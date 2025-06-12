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

To connect directly to the local machine, change the end of the machine address URI from `.viam.cloud` to `.local.viam.cloud` in your machine's connection code.
The default machine address (URI) from the **CONNECT** tab is of the form `mymachine-main.0a1bcdefgi.viam.cloud`, so `mymachine-main.0a1bcdefgi.local.viam.cloud`.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="10"}
async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address(
        'mymachine-main.0a1bcdefgi.local.viam.cloud', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers" data-line="3"}
machine, err := client.New(
  context.Background(),
  "mymachine-main.0a1bcdefgi.local.viam.cloud",
  logger,
  client.WithDialOptions(rpc.WithEntityCredentials(
          /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
    "<API-KEY-ID>",
    rpc.Credentials{
      Type:    rpc.CredentialsTypeAPIKey,
              /* Replace "<API-KEY>" (including brackets) with your machine's API key */
      Payload: "<API-KEY>",
    })),
)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}
The TypeScript SDK currently does not support mDNS which means you cannot use it to connect to your machine over a local network.
{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="line-numbers linkable-line-numbers" data-line="2"}
Future<void> connectToViam() async {
  const host = 'mymachine-main.0a1bcdefgi.local.viam.cloud';
  /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
  const apiKeyID = '<API-KEY-ID>';
  /* Replace "<API-KEY>" (including brackets) with your machine's API key */
  const apiKey = '<API-KEY>';

  final machine = await RobotClient.atAddress(
    host,
    RobotClientOptions.withApiKey(apiKeyID, apiKey),
  );
  print(machine.resourceNames);
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers" data-line="1"}
std::string host("mymachine-main.0a1bcdefgi.local.viam.cloud");
DialOptions dial_opts;
dial_opts.set_entity(std::string("<API-KEY-ID>"));
/* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
Credentials credentials("api-key", "<API-KEY>");
/* Replace "<API-KEY>" (including brackets) with your machine's API key */
dial_opts.set_credentials(credentials);
boost::optional<DialOptions> opts(dial_opts);
Options options(0, opts);

auto machine = RobotClient::at_address(host, options);
```

{{% /tab %}}
{{< /tabs >}}

## Connectivity Issues

When a machine loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- Cloud sync for the [data management service](/data-ai/capture-data/capture-sync/) will pause until the internet connection is re-established since the machine will be unable to connect to Viam.

When a machine loses its connection to LAN or WAN, all client sessions will timeout and end by default.

### Client session timeout and end

When your client cannot connect to your machine's `viam-server` instance, `viam-server` will end any current client [_sessions_](/dev/reference/apis/sessions/) on this machine and all client operations will [timeout automatically](/dev/reference/apis/sessions/) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the machine until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/dev/reference/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/dev/reference/sdks/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

{{% alert title="Note" color="note" %}}

There are a couple of exceptions to the general timeout behavior:

- If a [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) or [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) command has completed a motion plan and returned an execution ID before the connection is lost, the resource that receives the motion plan will complete the motion without a connection.
- If a navigation service and motion service are running on the same machine, the navigation service will continue sending requests to the motion service even after losing internet connectivity.

{{% /alert %}}

### Configure a connection timeout

When connecting to a machine using the [robot API](/dev/reference/apis/robot/) from a supported [Viam SDK](/dev/reference/apis/), you can configure an [optional timeout](/dev/reference/apis/robot/#configure-a-timeout) to account for intermittent or delayed network connectivity.
