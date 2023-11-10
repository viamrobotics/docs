To authenticate yourself to your robot, you need

1. The robot part's api key:

   <!-- we will be releasing the ability to create API keys across all types of resources and combinations soon (i.e an api key can have an authorization on a org, location, robot or any combination of all three). this is correct for now though but it will be changing shortly. -->
   To authenticate, [use a robot part API key](/manage/fleet/robots/#security) or [an API key](/manage/cli/#authenticate) with access to the robot.
   Copy and paste the API key id and the API key into your environment variables or directly into the code:

   {{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="3,5,9,11"}
async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your robot's api key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your robot's api key
        # id
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers" data-line="3,8"}
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
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="1,6,8,11"}
  // Replace with the host of your actual robot running Viam.
  const host = "ADDRESS FROM THE VIAM APP";

  const robot = await VIAM.createRobotClient({
    host,
    credential: {
      type: 'api-key',
      // Replace "<API-KEY>" (including brackets) with your robot's api key
      payload: '<API-KEY>',
    },
    // Replace "<API-KEY-ID>" (including brackets) with your robot's api key id
    authEntity: '<API-KEY-ID>',
    signalingAddress: 'https://app.viam.com:443',
  });
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers" data-line="1,3,5,7"}
std::string host("ADDRESS FROM THE VIAM APP");
DialOptions dial_opts;
dial_opts.set_type("api-key");
// Replace "<API-KEY-ID>" with your robot's api key ID
dial_opts.set_entity("<API-KEY-ID>");
// Replace "<API-KEY>" with your robot's api key
Credentials credentials("<API-KEY>");
dial_opts.set_credentials(credentials);
boost::optional<DialOptions> opts(dial_opts);
Options options(0, opts);

auto robot = RobotClient::at_address(host, options);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="line-numbers linkable-line-numbers" data-line="2,4,6,10"}
Future<void> connectToViam() async {
  const host = 'ADDRESS FROM THE VIAM APP';
  // Replace '<API-KEY-ID>' (including brackets) with your api key ID
  const apiKeyID = '<API-KEY-ID>';
  // Replace '<API-KEY>' (including brackets) with your api key
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
Do not share your robot part API key or robot address publicly.
Sharing this information could compromise your system security by allowing unauthorized access to your robot, or to the computer running your robot.
   {{< /alert >}}

   {{< alert title="Location secret (deprecated)" color="note" >}}

Prior to API keys, Viam used location secrets for authentication.
Location secrets are now deprecated.
To avoid connection issues, start using API keys.

   {{< /alert >}}

2. The robot's remote address: Include the address, which resembles `12345.somerobot-main.viam.cloud`.
The robot address is a public address to connect to your robot.
   You can find this address at the top of the robot's **Control** tab or in the **Code sample** tab.
