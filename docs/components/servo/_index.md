---
title: "Servo Component"
linkTitle: "Servo"
childTitleEndOverwrite: "Servo Component"
weight: 80
type: "docs"
description: "A hobby servo is a special type of small motor whose position you can precisely control."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
no_list: true
# SME: #team-bucket
---

The servo component supports ["RC" or "hobby" servo motors](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos).
These are small motors with built-in potentiometer position sensors, enabling you to control the angular position of the servo precisely.

As servos can use a lot of power, drawing voltage away from a [board](/components/board/), you should power your servo with its own power supply in most cases.
The following shows an example wiring diagram for a hobby servo wired to a [`pi` board](/components/board/pi/):

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](/components/servo/servo-wiring.png)

The colors of the servo wires in this diagram may not match your servo.
Refer to your servo's data sheet for wiring specifications.

Most robots with a servo need at least the following hardware:

- A [board component](/components/board/) that can run `viam-server`
- A servo
- A power supply for the board
- A power supply for the servo

## Related Services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

{{% alert title="Tip" color="tip" %}}

The Viam servo component supports [hobby servos](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos).

If your motor is coupled with an [encoder](/components/encoder/), not a potentiometer, for position feedback, you should not configure it as a servo.
Check your device's data sheet and configure that type of servo as an [encoded motor](/components/motor/gpio/encoded-motor/).

{{% /alert %}}

## Supported Models

To use your servo with Viam, check whether one of the following [built-in models](#built-in-models) supports your servo.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
| [`gpio`](gpio/) | A hobby servo wired to any model of [board](/components/board/#supported-models) besides `pi`. |
| [`pi`](pi/) | A hobby servo wired to a [Raspberry Pi board](/components/board/pi/). |

<!-- ### Modular Resources

{{<modular-resources api="rdk:component:servo" type="servo">}}
-->

If none of these models fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

## Control your servo with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a servo called `"my_servo"` configured as a component of your robot.
If your servo has a different name, change the `name` in the code.

Be sure to import the servo package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.servo import Servo
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/servo"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The servo component supports the following methods:

{{< readfile "/static/include/components/apis/servo.md" >}}

### Move

Move the servo to the desired angle in degrees.

{{% alert title="Stability Notice" color="note" %}}
Support for continuous servos with the GPIO servo model is experimental.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

If you are using a continuous rotation servo, you can use the `Move` command, but instead of moving to a given position, the servo will start moving at a set speed.

The speed will be related to the "angle" you pass in as a linear approximation.
90 degrees represents stop, 91 to 180 represents counter-clockwise rotation from slowest to fastest, and 89 to 1 represents clockwise from slowest to fastest.
It is recommended that you test your servo to determine the desired speed.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `angle` [(int)](https://docs.python.org/3/library/functions.html#int): The desired angle of the servo in degrees.
- `extra` [(Optional\[Mapping\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.move).

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Move the servo from its origin to the desired angle of 90 degrees.
await my_servo.move(90)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(uint32)](https://pkg.go.dev/builtin#uint32): The desired angle of the servo in degrees.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
myServo, err := servo.FromRobot(robot, "my_servo")

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Move the servo from its origin to the desired angle of 90 degrees.
myServo.Move(context.Background(), 90, nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Get the current set angle of the servo in degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Mapping\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The current set angle of the servo in degrees.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.get_position).

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Get the current set angle of the servo.
pos1 = await my_servo.get_position()

# Move the servo from its origin to the desired angle of 20 degrees.
await my_servo.move(20)

# Get the current set angle of the servo.
pos2 = await my_servo.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint32)](https://pkg.go.dev/builtin#uint32): The current set angle of the servo in degrees.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
myServo, err := servo.FromRobot(robot, "my_servo")

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Get the current set angle of the servo.
pos1, err = myServo.Position(context.Background(), nil)

// Move the servo from its origin to the desired angle of 20 degrees.
myServo.Move(context.Background(), 20, nil)

// Get the current set angle of the servo.
pos2, err = myServo.Position(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop the servo from moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Mapping\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.stop).

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Stop the servo. It is assumed that the servo stops moving immediately.
await my_servo.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
myServo, err := servo.FromRobot(robot, "my_servo")

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Stop the servo. It is assumed that the servo stops moving immediately.
myServo.Stop(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own servo and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot, "my_servo")

command = {"cmd": "test", "data1": 500}
result = my_servo.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myServo, err := servo.FromRobot(robot, "my_servo")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myServo.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
{{% card link="/tutorials/projects/guardian" %}}
{{% card link="/tutorials/control/yahboom-rover" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai" %}}
{{< /cards >}}
