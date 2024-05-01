### AtAddress

{{< tabs >}}
{{% tab name="Python" %}}

Create a robot client that is connected to the robot at the provided address.

**Parameters:**

- `address` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Address of the robot (IP address, URL, etc.)
- `options` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options) (required): Options for connecting and refreshing


**Returns:**

- [(typing_extensions.Self)](INSERT RETURN TYPE LINK): the RobotClient

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.at_address).

``` python {class="line-numbers linkable-line-numbers"}
async def connect():

    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


async def main():
    # Make a RobotClient
    robot = await connect()

```

{{% /tab %}}
