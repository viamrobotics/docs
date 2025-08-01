### GetVoltage

Return the voltage reading of a specified device and whether it is AC or DC.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)]): A float representing the voltage reading in V. A bool indicating whether the voltage is AC (true) or DC (false).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=machine, name='my_power_sensor')

# Get the voltage reading from the power sensor
voltage, is_ac = await my_power_sensor.get_voltage()
print("The voltage is", voltage, "V, Is AC:", is_ac)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_voltage).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The measurement of the voltage, represented as a 64-bit float number.
- [(bool)](https://pkg.go.dev/builtin#bool): Indicate whether voltage is AC (`true`) or DC (`false`).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the voltage from device in volts.
voltage, isAC, err := myPowerSensor.Voltage(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<readonly [number, boolean]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const powerSensor = new VIAM.PowerSensorClient(
  machine,
  'my_power_sensor'
);
const [voltage, isAc] = await powerSensor.getVoltage();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/PowerSensorClient.html#getvoltage).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Voltage](https://flutter.viam.dev/viam_sdk/Voltage.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var voltageObject = await myPowerSensor.voltage();
double voltageInVolts = voltageObject.volts;
bool isItAC = voltageObject.isAc;
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/PowerSensor/voltage.html).

{{% /tab %}}
{{< /tabs >}}

### GetCurrent

Return the current of a specified device and whether it is AC or DC.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex), [bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)]): A tuple which includes a float representing the current reading in amps, and a bool indicating whether the current is AC (true) or DC (false).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=machine, name='my_power_sensor')

# Get the current reading from the power sensor
current, is_ac = await my_power_sensor.get_current()
print("The current is ", current, " A, Is AC: ", is_ac)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_current).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The measurement of the current, represented as a 64-bit float number.
- [(bool)](https://pkg.go.dev/builtin#bool): Indicate whether current is AC (`true`) or DC (`false`).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current reading from device in amps.
current, isAC, err := myPowerSensor.Current(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<readonly [number, boolean]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const powerSensor = new VIAM.PowerSensorClient(
  machine,
  'my_power_sensor'
);
const [current, isAc] = await powerSensor.getCurrent();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/PowerSensorClient.html#getcurrent).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Current](https://flutter.viam.dev/viam_sdk/Current.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var currentObject = await myPowerSensor.current();
double amps = currentObject.amperes;
bool isItAC = currentObject.isAc;
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/PowerSensor/current.html).

{{% /tab %}}
{{< /tabs >}}

### GetPower

Return the power reading in watts.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The power reading in watts.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=machine, name='my_power_sensor')

# Get the power reading from the power sensor
power = await my_power_sensor.get_power()
print("The power is", power, "Watts")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_power).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The measurement of the power, represented as a 64-bit float number.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the power measurement from device in watts.
power, err := myPowerSensor.Power(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<number>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const powerSensor = new VIAM.PowerSensorClient(
  machine,
  'my_power_sensor'
);
const power = await powerSensor.getPower();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/PowerSensorClient.html#getpower).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var power = await myPowerSensor.power();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/PowerSensor/power.html).

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Get the measurements or readings that this power sensor provides.
If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.SensorReading]): The readings for the PowerSensor. Can be of any type. Includes voltage in volts (float), current inamperes (float), is_ac (bool), and power in watts (float).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=machine, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_power_sensor.get_readings()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_readings).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): A map containing the measurements from the sensor. Contents depend on sensor model and can be of any type.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the readings provided by the sensor.
readings, err := mySensor.Readings(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Sensor).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<Record<string, [JsonValue](https://ts.viam.dev/types/JsonValue.html)>>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const powerSensor = new VIAM.PowerSensorClient(
  machine,
  'my_power_sensor'
);
const readings = await powerSensor.getReadings();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/PowerSensorClient.html#getreadings).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var readings = await myPowerSensor.readings();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/PowerSensor/readings.html).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own power sensor and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

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
my_power_sensor = PowerSensor.from_robot(robot=machine, name="my_power_sensor")
command = {"cmd": "test", "data1": 500}
result = await my_power_sensor.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.do_command).

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
myPowerSensor, err := power_sensor.FromRobot(machine, "my_power_sensor")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myPowerSensor.DoCommand(context.Background(), command)
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
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(
  Struct.fromJson({
    myCommand: { key: 'value' },
  })
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/PowerSensorClient.html#docommand).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this power sensor with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor_name = PowerSensor.get_resource_name("my_power_sensor")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_resource_name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myPowerSensorResourceName = myPowerSensor.getResourceName("my_power_sensor");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/PowerSensor/getResourceName.html).

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
my_power_sensor = PowerSensor.from_robot(robot=machine, name="my_power_sensor")
await my_power_sensor.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myPowerSensor, err := powersensor.FromRobot(machine, "my_power_sensor")

err = myPowerSensor.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
