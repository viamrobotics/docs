### Options.with_api_key

{{< tabs >}}
{{% tab name="Python" %}}

Create RobotClient.Options with an [API key](/fleet/cli/#authenticate) for credentials and default values for other arguments.

**Parameters:**

- `api_key` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): your API key
- `api_key_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): your API key ID. Must be a valid UUID

**Returns:**

- [(typing_extensions.Self)](INSERT RETURN TYPE LINK): the RobotClient.Options

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options.with_api_key).

``` python {class="line-numbers linkable-line-numbers"}
# Replace "<API-KEY>" (including brackets) with your machine's API key
api_key = '<API-KEY>'
# Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
api_key_id = '<API-KEY-ID>'

opts = RobotClient.Options.with_api_key(api_key, api_key_id)

robot = await RobotClient.at_address('<ADDRESS-FROM-THE-VIAM-APP>', opts)
```

{{% /tab %}}
{{< /tabs >}}
