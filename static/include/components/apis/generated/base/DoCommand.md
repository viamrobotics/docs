### DoCommand

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: do_command

Send/Receive arbitrary commands to the Resource

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](<INSERT PARAM TYPE LINK>) (required) The command to execute:
- `command`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.do_command).

``` python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)

```

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: doCommand

**Parameters:**

- `command` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `command`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/doCommand.html).

\{\{% /tab %}}

\{\{< /tabs >}}

