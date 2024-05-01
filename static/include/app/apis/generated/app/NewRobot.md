### NewRobot

{{< tabs >}}
{{% tab name="Python" %}}

Create a new robot.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the new robot.
- `location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): ID of the location under which to create the robot. Defaults to the current authorized location.


**Returns:**

- [(str)](INSERT RETURN TYPE LINK): The new robot’s ID.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.new_robot).

``` python {class="line-numbers linkable-line-numbers"}
new_machine_id = await cloud.new_robot(name="beepboop")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `location` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/newRobot.html).

{{% /tab %}}
{{< /tabs >}}
