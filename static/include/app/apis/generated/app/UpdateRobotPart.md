### UpdateRobotPart

{{< tabs >}}
{{% tab name="Python" %}}

Change the name and assign an optional new configuration to a robot part.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to update.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): New name to be updated on the robot part.
- `robot_config` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Optional new config represented as a dictionary to be updated on the robot part. The robot part’s config will remain as is (no change) if one isn’t passed.

**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The newly updated robot part.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot_part).

``` python {class="line-numbers linkable-line-numbers"}
my_robot_part = await cloud.update_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `robotConfig` [(Struct)](<INSERT PARAM TYPE LINK>) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateRobotPart.html).

{{% /tab %}}
{{< /tabs >}}
