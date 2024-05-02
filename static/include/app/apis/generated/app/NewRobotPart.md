### NewRobotPart

{{< tabs >}}
{{% tab name="Python" %}}

Create a new robot part.

**Parameters:**

- `robot_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the the robot to create a new part for.
- `part_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the new part.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The new robot part’s ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot_part).

``` python {class="line-numbers linkable-line-numbers"}
new_part_id = await cloud.new_robot_part(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc", part_name="myNewSubPart")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `partName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `robotId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/newRobotPart.html).

{{% /tab %}}
{{< /tabs >}}
