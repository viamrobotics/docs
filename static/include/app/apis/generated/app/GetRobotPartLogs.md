### GetRobotPartLogs

{{< tabs >}}
{{% tab name="Python" %}}

Get the logs associated with a robot part.

**Parameters:**

- `robot_part_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the robot part to get logs from.
- `filter` [(str)](<INSERT PARAM TYPE LINK>) (optional): Only include logs with messages that contain the string filter. Defaults to empty string “” (i.e., no filter).
- `dest` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional filepath to write the log entries to.
- `errors_only` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): Boolean specifying whether or not to only include error logs. Defaults to True.
- `num_log_entries` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): Number of log entries to return. Passing 0 returns all logs. Defaults to 100. All logs or the first num_log_entries logs will be returned, whichever comes first.

**Returns:**

- [(List[LogEntry])](INSERT RETURN TYPE LINK): The list of log entries.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.get_robot_part_logs).

``` python {class="line-numbers linkable-line-numbers"}
part_logs = await cloud.get_robot_part_logs(
    robot_part_id="abc12345-1a23-1234-ab12-a22a22a2aa22", num_log_entries=20)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `errorsOnly` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `filter` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `id` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `levels` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required):
- `pageToken` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/getRobotPartLogs.html).

{{% /tab %}}
{{< /tabs >}}
