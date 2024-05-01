### CreateRobotPartSecret

{{< tabs >}}
{{% tab name="Python" %}}

Create a robot part secret.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to create a secret for.


**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The robot part the new secret was generated for.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_robot_part_secret).

``` python {class="line-numbers linkable-line-numbers"}
part_with_new_secret = await cloud.create_robot_part_secret(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/createRobotPartSecret.html).

{{% /tab %}}
{{< /tabs >}}
