### DeleteRobotPartSecret

{{< tabs >}}
{{% tab name="Python" %}}

Delete a robot part secret.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to delete the secret from.
- `secret_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the secret to delete.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.delete_robot_part_secret).

``` python {class="line-numbers linkable-line-numbers"}
await cloud.delete_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22",
    secret_id="123xyz12-abcd-4321-12ab-12xy1xyz12xy")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `secretId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/deleteRobotPartSecret.html).

{{% /tab %}}
{{< /tabs >}}
