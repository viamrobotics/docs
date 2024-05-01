### WithChannel

{{< tabs >}}
{{% tab name="Python" %}}

Create a robot that is connected to a robot over the given channel.

**Parameters:**

- `channel` [(grpclib.client.Channel | viam.rpc.dial.ViamChannel)](https://python.viam.dev/autoapi/viam/rpc/dial/index.html#viam.rpc.dial.ViamChannel) (required): The channel that is connected to a robot, obtained by viam.rpc.dial
- `options` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options) (required): Options for refreshing. Any connection options will be ignored.


**Returns:**

- [(typing_extensions.Self)](INSERT RETURN TYPE LINK): the RobotClient

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.with_channel).

``` python {class="line-numbers linkable-line-numbers"}
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial


async def connect_with_channel() -> RobotClient:
    async with await dial('ADDRESS', DialOptions()) as channel:
        return await RobotClient.with_channel(channel, RobotClient.Options())

robot = await connect_with_channel()

```

{{% /tab %}}
