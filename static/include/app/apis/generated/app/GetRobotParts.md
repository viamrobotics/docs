### GetRobotParts

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of all the parts under a specific robot.

**Parameters:**

- `robot_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot to get parts from.


**Returns:**

- [(List[RobotPart])](INSERT RETURN TYPE LINK): The list of robot parts.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_parts).

``` python {class="line-numbers linkable-line-numbers"}
list_of_parts = await cloud.get_robot_parts(
    robot_id="1a123456-x1yz-0ab0-a12xyzabc")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `robotId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotParts.html).

{{% /tab %}}
{{< /tabs >}}
