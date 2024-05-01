### TailRobotPartLogs

{{< tabs >}}
{{% tab name="Python" %}}

Get an asynchronous iterator that receives live robot part logs.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to retrieve logs from.
- `errors_only` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): Boolean specifying whether or not to only include error logs. Defaults to True.
- `filter` [(str)](<INSERT PARAM TYPE LINK>) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (i.e., no filter).


**Returns:**

- [(viam.app._logs._LogsStream[List[LogEntry]])](INSERT RETURN TYPE LINK): The asynchronous iterator receiving live robot part logs.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.tail_robot_part_logs).

``` python {class="line-numbers linkable-line-numbers"}
logs_stream = await cloud.tail_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `errorsOnly` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `filter` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/tailRobotPartLogs.html).

{{% /tab %}}
{{< /tabs >}}
