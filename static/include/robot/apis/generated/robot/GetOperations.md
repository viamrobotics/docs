### GetOperations

{{< tabs >}}
{{% tab name="Python" %}}

Get the list of operations currently running on the robot.


**Returns:**

- [(List[viam.proto.robot.Operation])](INSERT RETURN TYPE LINK): The list of operations currently running on a given robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_operations).

``` python {class="line-numbers linkable-line-numbers"}
operations = await robot.get_operations()

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**



For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/getOperations.html).

{{% /tab %}}
{{< /tabs >}}
