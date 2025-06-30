### SetPosition

Set the position of the switch.
Position must be within the valid range for the switch type.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `position` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The position of the switch within the range of available positions.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch = Switch.from_robot(robot=machine, name="my_switch")

# Update the switch from its current position to the desired position of 1.
await my_switch.set_position(1)

# Update the switch from its current position to the desired position of 0.
await my_switch.set_position(0)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.set_position).

{{% /tab %}}
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

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const mySwitch = new VIAM.SwitchClient(machine, "my_switch");

// Update the switch from its current position to position 1
await mySwitch.setPosition(1);

// Update the switch from its current position to position 0
await mySwitch.setPosition(0);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#setposition).

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Return the current position of the switch.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The current position of the switch within the range of available positions.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch = Switch.from_robot(robot=machine, name="my_switch")

# Update the switch from its current position to the desired position of 1.
await my_switch.set_position(1)

# Get the current set position of the switch.
pos1 = await my_switch.get_position()

# Update the switch from its current position to the desired position.
await my_switch.set_position(0)

# Get the current set position of the switch.
pos2 = await my_switch.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.get_position).

{{% /tab %}}
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

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const mySwitch = new VIAM.SwitchClient(machine, "my_switch");

// Update the switch to position 1
await mySwitch.setPosition(1);

// Get the current set position
const pos1 = await mySwitch.getPosition();

// Update the switch to position 0
await mySwitch.setPosition(0);

// Get the current set position
const pos2 = await mySwitch.getPosition();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#getposition).

{{% /tab %}}
{{< /tabs >}}

### GetNumberOfPositions

Return the number of valid positions for this switch and their labels.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The number of available positions.
- (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): Human-readable labels for each switch position.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch = Switch.from_robot(robot=machine, name="my_switch")

num_positions, labels = await my_switch.get_number_of_positions()
print(f"Switch has {num_positions} positions:")
for i, label in enumerate(labels):
    print(f"  Position {i}: {label}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.get_number_of_positions).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

<<<<<<< HEAD

- [(uint32)](https://pkg.go.dev/builtin#uint32)
- # [([]string)](https://pkg.go.dev/builtin#string)
- [(uint32)](https://pkg.go.dev/builtin#uint32): The number of available positions.
- [([]string)](https://pkg.go.dev/builtin#string): Human-readable labels for each switch position.
  > > > > > > > f08e17e6a (Documentation updates from Promptless)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromRobot(machine, "my_switch")

numPositions, labels, err := mySwitch.GetNumberOfPositions(context.Background(), nil)
if err != nil {
    logger.Fatalf("Failed to get switch positions: %v", err)
}

logger.Infof("Switch has %d positions:", numPositions)
for i, label := range labels {
    logger.Infof("  Position %d: %s", i, label)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/switch#Switch).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[number, string[]]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const mySwitch = new VIAM.SwitchClient(machine, "my_switch");

// Get the number of available positions and their labels
const { numPositions, labels } = await mySwitch.getNumberOfPositions();
console.log(`Switch has ${numPositions} positions:`);
labels.forEach((label, index) => {
  console.log(`  Position ${index}: ${label}`);
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#getnumberofpositions).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own switch and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch = Switch.from_robot(robot=machine, name="my_switch")
command = {"cmd": "test", "data1": 500}
result = await my_switch.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromProvider(machine, "my_switch")

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

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
import { Struct } from "@viamrobotics/sdk";

const result = await resource.doCommand(
  Struct.fromJson({
    myCommand: { key: "value" },
  }),
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this servo.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch_name = Switch.get_resource_name("my_switch")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromProvider(machine, "my_switch")

err = mySwitch.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (string): The name of the resource.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
switch.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SwitchClient.html#name).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_switch = Switch.from_robot(robot=machine, name="my_switch")
await my_switch.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/switch/client/index.html#viam.components.switch.client.SwitchClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySwitch, err := switch.FromProvider(machine, "my_switch")

err = mySwitch.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
