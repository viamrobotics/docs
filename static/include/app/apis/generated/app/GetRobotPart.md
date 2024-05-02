### GetRobotPart

{{< tabs >}}
{{% tab name="Python" %}}

Get a robot part.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to get.
- `dest` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional filepath to write the robot part’s config file in JSON format to.
- `indent` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Size (in number of spaces) of indent when writing config to dest. Defaults to 4.

**Returns:**

- [(RobotPart)](INSERT RETURN TYPE LINK): The robot part.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part).

``` python {class="line-numbers linkable-line-numbers"}
my_robot_part = await cloud.get_robot_part(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPart.html).

{{% /tab %}}
{{< /tabs >}}
