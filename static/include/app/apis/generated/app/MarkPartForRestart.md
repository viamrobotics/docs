### MarkPartForRestart

{{< tabs >}}
{{% tab name="Python" %}}

Mark the specified robot part for restart.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to mark for restart.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.mark_part_for_restart).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.mark_part_for_restart(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/markPartForRestart.html).

{{% /tab %}}
{{< /tabs >}}
