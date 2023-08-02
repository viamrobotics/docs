You also need to configure attributes to specify how the GPS connects to your computer.
You can use either serial communication (over USB) or I<sup>2</sup>C communication (through pins to a [board](../../../board/)).

Use `connection_type` to specify `"serial"` or `"I2C"` connection in the main `attributes` config.
Then create a struct within `attributes` for either `serial_attributes` or `i2c_attributes`, respectively.

{{< tabs >}}
{{% tab name="Serial" %}}

### Serial Config Attributes

For a movement sensor communicating over serial, you'll need to include a `serial_attributes` field containing:

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path.
`serial_baud_rate` | int | Optional | The rate at which data is sent from the sensor. <br> Default: `38400`
---

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<my-movement-sensor-name>",
    "type": "<type>",
    "model": "<model>",
    "attributes": {
        "<whatever other attributes>": "<example>",
        "connection_type": "serial",
        "serial_attributes": {
            "serial_baud_rate": 38400,
            "serial_path": "<PATH>"
        }
    }
}
```

{{% /tab %}}
{{% tab name="I2C" %}}

### I<sup>2</sup>C Config Attributes

For a movement sensor communicating over I<sup>2</sup>C, you'll need a `i2c_attributes` field containing:

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`board` | string | **Required** | The `name` of the [board](/components/board/) to which the [I<sup>2</sup>C](/components/board/#i2cs) connection is being made. This attribute is only required for the `gps-nmea` model.
`i2c_bus` | string | **Required** | The name of the [I<sup>2</sup>C bus](/components/board/#i2cs) wired to the sensor.
`i2c_addr` | int | **Required** | The device's I<sup>2</sup>C address.
`i2c_baud_rate` | int | Optional | The rate at which data is sent from the sensor. Optional. <br> Default: `38400`
---

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<my-movement-sensor-name>",
    "type": "<TYPE>",
    "model": "<MODEL>",
    "attributes": {
        "<whatever other attributes>": "<example>",
        "connection_type": "I2C",
        // "board": "<name of your board>"  Include if "model": "gps-rtk"
        "i2c_attributes": {
            "i2c_addr": 111,
            "i2c_bus": "1",
            // "board": "<name of your board>"  Include if "model": "gps-nmea"
        }
    }
}
```

{{% /tab %}}
{{< /tabs >}}
