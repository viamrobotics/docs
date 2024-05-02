### GetRobotPartHistory

{{< tabs >}}
{{% tab name="Python" %}}

Get a list containing the history of a robot part.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to retrieve history from.

**Returns:**

- [(List[RobotPartHistoryEntry])](INSERT RETURN TYPE LINK): The list of the robot part’s history.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_history).

``` python {class="line-numbers linkable-line-numbers"}
part_history = await cloud.get_robot_part_history(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPartHistory.html).

{{% /tab %}}
{{< /tabs >}}
