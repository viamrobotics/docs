### DeleteRobot

{{< tabs >}}
{{% tab name="Python" %}}

Delete the specified robot.

**Parameters:**

- `robot_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot to delete.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot(robot_id="1a123456-x1yz-0ab0-a12xyzabc")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRobot.html).

{{% /tab %}}
{{< /tabs >}}
