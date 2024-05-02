### DoCommand

{{< tabs >}}
{{% tab name="Python" %}}

Send/Receive arbitrary commands to the Resource

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](<INSERT PARAM TYPE LINK>) (required): The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.do_command).

``` python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.powersensor/PowerSensorServiceClient/doCommand.html).

{{% /tab %}}
{{< /tabs >}}
