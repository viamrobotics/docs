To authenticate yourself to your machine, you need

1. The machine part's API key:

      <!-- we will be releasing the ability to create API keys across all types of resources and combinations soon (i.e an API key can have an authorization on a org, location, machine or any combination of all three). this is correct for now though but it will be changing shortly. -->

   To authenticate, [use a machine part API key](/operate/control/api-keys/) or [an API key](/dev/tools/cli/#authenticate) with access to the machine.
   Copy and paste the API key ID and the API key into your environment variables or directly into the code:

   {{< tabs >}}
   {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="4,7,9"}
async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's API key
        # ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('MACHINE ADDRESS', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers" data-line="3,7,11"}
robot, err := client.New(
    context.Background(),
    "MACHINE ADDRESS",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
    // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
    "<API-KEY-ID>",
    rpc.Credentials{
        Type:    rpc.CredentialsTypeAPIKey,
        // Replace "<API-KEY>" (including brackets) with your machine's API key
        Payload: "<API-KEY>",
    })),
)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="2,9,11"}
// Replace with the host of your actual machine running Viam.
const host = "MACHINE ADDRESS";

const robot = await VIAM.createRobotClient({
  host,
  credentials: {
    // Replace "<API-KEY>" (including brackets) with your machine's api key
    type: "api-key",
    payload: "<API-KEY>",
    // Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
    authEntity: "<API-KEY-ID>",
  },
  signalingAddress: "https://app.viam.com:443",
});
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers" data-line="1,5,7"}
std::string host("MACHINE ADDRESS");
DialOptions dial_opts;
dial_opts.set_type("api-key");
// Replace "<API-KEY-ID>" with your machine's API key ID
dial_opts.set_entity("<API-KEY-ID>");
// Replace "<API-KEY>" with your machine's API key
Credentials credentials("<API-KEY>");
dial_opts.set_credentials(credentials);
boost::optional<DialOptions> opts(dial_opts);
Options options(0, opts);

auto robot = RobotClient::at_address(host, options);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="line-numbers linkable-line-numbers" data-line="2,4,6"}
Future<void> connectToViam() async {
  const host = 'MACHINE ADDRESS';
  // Replace '<API-KEY-ID>' (including brackets) with your API key ID
  const apiKeyID = '<API-KEY-ID>';
  // Replace '<API-KEY>' (including brackets) with your API key
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

{{< alert title="Caution" color="caution" >}}
Do not share your machine part API key publicly.
Sharing this information could compromise your system security by allowing unauthorized access to your machine, or to the computer running your machine.
{{< /alert >}}

{{< alert title="Location secret (deprecated)" color="note" >}}

Prior to API keys, Viam used location secrets for authentication.
Location secrets are now deprecated.
To avoid connection issues, start using API keys.

{{< /alert >}}

2. The machine's remote address:

   Include the address, which resembles `12345.somemachine-main.viam.cloud`.
   The machine address is a public address to connect to your machine.
   You can find this address at the top of the machine's **CONNECT** tab.
