You also need to configure attributes to specify how the GPS connects to your computer.
You can use either serial communication (over USB) or I<sup>2</sup>C communication (through pins to a [board](../../../board/)).

Use `connection_type` to specify `"serial"` or `"I2C"` connection in the main `attributes` config.
Then create a struct within `attributes` for either `serial_attributes` or `i2c_attributes`, respectively.

{{< tabs >}}
{{% tab name="Serial" %}}

### Serial Config Attributes

For a movement sensor communicating over serial, you'll need to include a `serial_attributes` field containing:

Name | Type | Default Value | Description
---- | ---- | ------------- | -----
`serial_path` | string | - | The name of the port through which the sensor communicates with the computer.
`serial_baud_rate` | int | 115200 | The rate at which data is sent from the sensor. Optional.
---

Serial communication uses a filepath instead of relying on any specific piece of board hardware, so no "board" attribute is needed when configuring a movement sensor with this communication method.

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<my-movement-sensor-name>",
    "type": "<TYPE>",
    "model": "<MODEL>",
    "attributes": {
        "<whatever other attributes>": "<example>",
        "connection_type": "serial",
        "serial_attributes": {
            "serial_baud_rate": 115200,
            "serial_path": "<PATH>"
        }
    }
}
```

{{% /tab %}}
{{% tab name="I2C" %}}

### I<sup>2</sup>C Config Attributes

For a movement sensor communicating over I<sup>2</sup>C, you'll need a `i2c_attributes` field containing:

Name | Type | Default Value | Description
---- | ---- | ------------- | -----
`i2c_bus` | string | - | The name of I<sup>2</sup>C bus wired to the sensor.
`i2c_addr` | int | - | The device's I<sup>2</sup>C address.
`i2c_baud_rate` | int | 115200 | The rate at which data is sent from the sensor. Optional.
---

You'll also need to configure the `board` attribute with the name of the board to which the I<sup>2</sup>C connection is being made.

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<my-movement-sensor-name>",
    "type": "<TYPE>",
    "model": "<MODEL>",
    "attributes": {
        "board": "<name of board, e.g. local>",
        "<whatever other attributes>": "<example>",
        "connection_type": "I2C",
        "i2c_attributes": {
            "i2c_addr": 111,
            "i2c_bus": "1"
        }
    }
}
```

{{% /tab %}}
{{< /tabs >}}
