---
title: "Configure an AM5-AS5048 encoder"
linkTitle: "AM5-AS5048"
type: "docs"
description: "Configure an AM5-AS5048 encoder."
tags: ["encoder", "components"]
# SMEs: Rand
---

The [`AM5-AS5048`](https://ams.com/en/as5048a) encoder is an absolute encoder that uses an I2C or SPI interface to connect.

## Requirements

1. To configure an AM5-AS5048 encoder, you must add an I2C bus needs to your board:

    ```json-viam
    {
          "name": "<board_name>",
          "type": "board",
          "model": "<model_name>"
          "attributes": {
            "i2cs": [
              {
                "bus": "<bus>",
                "name": "<bus_name>"
              }
            ]
          },
          "depends_on": [],
    }
    ```

2. Any motors using the `AM5-AS5048` encoder must set `ticks_per_rotation` to `1`.
   This is because the AM5 encoder is an absolute encoder which provides angular measurements directly.

## Configuration

{{< tabs name="Configure an AM5-AS5048 Encoder" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your encoder, select the type <code>encoder</code>, and select the <code>AM5-AS5048</code> model.
<br>
<img src="../img/create-am5.png" alt="Creation of an AM5 encoder in the Viam app config builder." style="max-width:600px" />
<br>
Fill in the attributes for your encoder:
<br>
<img src="../img/configure-am5.png" alt="Configuration of an AM5 encoder in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<encoder_name>",
    "type": "encoder",
    "model" : "AM5-AS5048",
    "attributes": {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": <string>,
        "i2c_addr": <integer>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for AM5-AS5048 encoders:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `board` | *Required* | The name of the board to which the encoder is connected. |
| `connection_type` | *Required* | Use `"i2c"`. |
| `i2c_attributes` | *Optional* | The attributes to configure i2c connection: <ul> <li> <code>i2c_bus</code>: The name of the bus that was added to the board. Example: `"main"`. </li> <li> <code>i2c_addr</code>: The address of the bus. Example: `64`. </li> </ul> |

### Configure a SCUTTLE bot

If you are configuring a SCUTTLE bot, you must:

- Specify the bus number on the board as `"1"`.

  ```json-viam
  {
        "name": "<board_name>",
        "type": "board",
        "model": "<model_name>"
        "attributes": {
          "i2cs": [
            {
              "bus": "1",
              "name": "<main>"
            }
          ]
        },
        "depends_on": [],
  }
  ```

- Configure the left and right encoders as follows:

  - left:

    ```json
    {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "main",
        "i2c_addr": 64
      }
    }
    ```

  - right:

    ```json
    {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "main",
        "i2c_addr": 65
      }
    }
    ```

## Example Code

### Scuttle Encoder

```python {class="line-numbers linkable-line-numbers"}
import Adafruit_GPIO.I2C as Adafruit_I2C        # for i2c communication functions

# import Viam-related libraries
from typing import Any, Dict, Optional
from viam.components.motor import Motor

"""
encL = Adafruit_I2C.Device(0x40, 1)             # encoder i2c address
encR = Adafruit_I2C.Device(0x41, 1)             # encoder i2c address
"""

class ScuttleEncoder(Motor):
    def __init__(self, name: str, is_left: bool):
        self.encoder = Adafruit_I2C.Device(0x40 if is_left else 0x41, 1)
        super().__init__(name)

    def read(self) -> float:
        try:
            # The AS5048B encoder gives a 14 bit angular reading
            msB = self.encoder.readU8(0xFE)    # capture the 8 msb's from encoder
            lsB = self.encoder.readU8(0xFF)    # capture the 6 lsb's from encoder

            # lsB can contribute  at most 1.4 degrees to the reading
            # for msB, perform bitwise operation to get true scaling of these bits
            angle_raw = (msB << 6) | lsB

        except:
            print('Warning (I2C): Could not read encoder')
            angle_raw = 0                           # set to zero, avoid sending wrong value
        return angle_raw                            # the returned value must be scaled by ( 359deg / 2^14 )

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> float:
        return self.read()
```

### Print encoder readings

```python {class="line-numbers linkable-line-numbers"}

import Adafruit_GPIO.I2C as Adafruit_I2C        # for i2c communication functions
import time
import numpy as np                              # for handling arrays

encL = Adafruit_I2C.Device(0x40, 1)             # encoder i2c address
encR = Adafruit_I2C.Device(0x41, 1)             # encoder i2c address

# the readEncs function communicates to one device in one function call
def readEnc(channel):
    try:
        # The AS5048B encoder gives a 14 bit angular reading
        if channel == 'L':
            msB = encL.readU8(0xFE)    # capture the 8 msb's from encoder
            lsB = encL.readU8(0xFF)    # capture the 6 lsb's from encoder
        elif channel == "R":
            msB = encR.readU8(0xFE)    # capture the 8 msb's from encoder
            lsB = encR.readU8(0xFF)    # capture the 6 lsb's from encoder

        # lsB can contribute  at most 1.4 degrees to the reading
        # for msB, perform bitwise operation to get true scaling of these bits
        angle_raw = (msB << 6) | lsB

    except:
        print('Warning (I2C): Could not read encoder ' + channel)
        angle_raw = 0                           # set to zero, avoid sending wrong value
    return angle_raw                            # the returned value must be scaled by ( 359deg / 2^14 )

def read():
    encLeft = readEnc('L')                      # call for left enc value
    encRight = readEnc('R')                     # call for right enc value
    encoders = np.array([encLeft, encRight])    # form array from left and right
    return encoders


if __name__ == "__main__":
    while True:
        encoders = read()
        encoders = np.round((encoders * (360 / 2**14)), 2)      # scale values to get degrees
        print("encoders: ", encoders)                           # print the values

        time.sleep(0.10)
```
