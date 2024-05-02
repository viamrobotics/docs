### SetPowerMode

{{< tabs >}}
{{% tab name="Python" %}}

Set the board to the indicated power mode.

**Parameters:**

- `mode` [(viam.proto.component.board.PowerMode.ValueType)](https://python.viam.dev/autoapi/viam/../gen/component/board/v1/board_pb2/index.html#viam.gen.component.board.v1.board_pb2.PowerMode) (required): The desired power mode.
- `duration` [(datetime.timedelta)](<INSERT PARAM TYPE LINK>) (optional): Requested duration to stay in power mode.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.set_power_mode).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Set the power mode of the board to OFFLINE_DEEP.
status = await my_board.set_power_mode(mode=PowerMode.POWER_MODE_OFFLINE_DEEP)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `mode`[(PowerMode)](https://pkg.go.dev/go.viam.com/api/component/board/v1#PowerMode):
- `time`[(Duration)](https://pkg.go.dev/time#Duration):

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `duration` [(Duration)](<INSERT PARAM TYPE LINK>) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `powerMode` [(PowerMode)](https://flutter.viam.dev/viam_protos.component.board/PowerMode-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/setPowerMode.html).

{{% /tab %}}
{{< /tabs >}}
