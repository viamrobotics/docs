To authenticate yourself to your robot, you need

1.  The robot's location secret or the org api key:

    {{< tabs >}}

{{% tab name="Location secret" %}}

On your robot's **Code sample** tab, select **Include Secret** and copy the location secret.
Then paste it into your environment variables or directly into your code.

{{% snippet "secret-share.md" %}}

{{% /tab %}}
{{% tab name="Org api key" %}}

To authenticate using an org api key, [create an api key using the CLI](/manage/cli/#create-an-organization-api-key).
Replace the connection code from your code snippet with the following code and copy and paste the api key id and the api key into your environment variables or directly into the code:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="3,5,9,11"}
async def connect():
    creds = Credentials(
        type='api-key',
        # Replace "<API-KEY>" (including brackets) with your robot's api key
        payload='<API-KEY>')
    opts = RobotClient.Options(
        refresh_interval=0,
        # Replace "<API-KEY-ID>" (including brackets) with your robot's api key id
        dial_options=DialOptions(credentials=creds, auth_entity="<API-KEY-ID>")
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
        // Replace "<API-KEY>" (including brackets) with your robot's api key
        "<API-KEY-ID>",
        rpc.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            // Replace "<API-KEY>" (including brackets) with your robot's api key
            Payload: "<API-KEY>",
        }
    )),
)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="1,6,8,11"}
const host = "ADDRESS FROM THE VIAM APP";

const robot = await VIAM.createRobotClient({
  host,
  credential: {
    type: "api-key",
    // Replace "<API-KEY>" (including brackets) with your api key
    payload: "<API-KEY>",
  },
  // Replace "<API-KEY-ID>" (including brackets) with your api key id
  authEntity: "<API-KEY-ID>",
  signalingAddress: "https://app.viam.com:443",
});
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers" data-line="1,3,5,7"}
std::string host("ADDRESS FROM THE VIAM APP");
DialOptions dial_opts;
dial_opts.set_type("api-key");
// Replace "<API-KEY-ID>"" with your api key ID
dial_opts.set_entity("<API-KEY-ID>");
// Replace "<API-KEY>" with your api key
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
Do not share your org api key id, org api key, or robot address publicly.
Sharing this information could compromise your system security by allowing unauthorized access to your robot, or to the computer running your robot.
{{< /alert >}}

{{% /tab %}}

    {{< /tabs >}}

2. The robot's remote address: Include the address, which resembles `12345.somerobot-main.viam.cloud`. The robot address is as a public address to connect to your robot.
   You can find this address at the top of the robot's **Control** tab or in the **Code sample** tab..
