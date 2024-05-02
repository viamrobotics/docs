### Log

{{< tabs >}}
{{% tab name="Python" %}}

Send log from Python module over gRPC.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The logger’s name.
- `level` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The level of the log.
- `time` [(datetime.datetime)](https://docs.python.org/3/library/datetime.html) (required): The log creation time.
- `log` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The log message.
- `stack` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The stack information of the log.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.log).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `logs` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[LogEntry](https://flutter.viam.dev/viam_protos.common.common/LogEntry-class.html)> (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.robot.robot/RobotServiceClient/log.html).

{{% /tab %}}
{{< /tabs >}}
