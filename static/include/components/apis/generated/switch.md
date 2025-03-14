### SetPosition

Set the position of the switch.
Position must be within the valid range for the switch type.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `position` [(uint32)](https://pkg.go.dev/builtin#uint32)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/switch#Switch).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `position` (number) (required)
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#setPosition).

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Return the current position of the switch.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint32)](https://pkg.go.dev/builtin#uint32)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/switch#Switch).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<number>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#getPosition).

{{% /tab %}}
{{< /tabs >}}

### GetNumberOfPositions

Return the number of valid positions for this switch.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint32)](https://pkg.go.dev/builtin#uint32)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/switch#Switch).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<number>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#getNumberOfPositions).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own switch and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromRobot(machine, "my_switch")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := mySwitch.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#doCommand).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromRobot(machine, "my_switch")

err = mySwitch.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
