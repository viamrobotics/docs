### UpdateRobot

{{< tabs >}}
{{% tab name="Python" %}}

Change the name of an existing robot.

**Parameters:**

- `robot_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot to update.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): New name to be updated on the robot.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location under which the robot exists. Defaults to the location ID provided at AppClient instantiation


**Returns:**

- [(viam.proto.app.Robot)](INSERT RETURN TYPE LINK): The newly updated robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_robot).

``` python {class="line-numbers linkable-line-numbers"}
updated_robot = await cloud.update_robot(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc",
    name="Orange-Robot")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `location` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateRobot.html).

{{% /tab %}}
{{< /tabs >}}
