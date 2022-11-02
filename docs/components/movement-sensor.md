---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
weight: 70
type: "docs"
description: "Explanation of movement sensor types, configuration, and usage in Viam."
# SME: Rand
---
The movement sensor component is an abstraction of a sensor that gives data on where a robot is and how fast it is moving.

We have chosen to abstract these types of sensors into one common API.
There are many different types of sensors that can provide data for some or all of the following methods: `Position`, `Orientation`, `LinearVelocity`, `AngularVelocity` and `CompassHeadings`.
A global positioning system (GPS) can provide position, linear velocity and compass headings.
An innertial measurement unit (IMU) can provide angular velocity and orientation.
We can further apply algorithms, such as a Kalman filter, to combine data from both a GPS and an IMU to output the full set of information of the movement sensor methods.

Currently (01 November 2022), the [RDK](../../appendix/glossary/#rdk_anchor) implements GPS, IMU, and visual odometry-based movement sensors.
We support two IMU models (manufactured by WitMotion and VectorNav) and two GPS models: NMEA-based GPS modules and <a href="https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol" target="_blank">NTRIP</a>[^ntrip]-based <a href="https://en.wikipedia.org/wiki/Real-time_kinematic_positioning" target="_blank">RTK</a>[^rtk] GPS models.
The `cameramono` RDK model is experimental and uses a camera to output data on its position and orientation.

We specifically cover GPS and IMU units in this documentation.
Find the more [generic sensor component here](../../components/sensor/).
Find more information about encoders, another component type, [here](../../components/encoder/).

[^ntrip]: Network Transport of RTCM via Internet Protocol (NTRIP): <a href="https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol</a>

[^rtk]: Real-time kinematic positioning: <a href="https://en.wikipedia.org/wiki/Real-time_kinematic_positioning" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Real-time_kinematic_positioning</a>

{{% alert title="Note" color="note" %}}
Any movement sensor that uses I<sup>2</sup>C must be connected to a board that supports I<sup>2</sup>C and [has it enabled](../../getting-started/installation/#enabling-specific-communication-protocols-on-the-raspberry-pi).
{{% /alert %}}

## GPS
A global positioning system (GPS) is based on receiving signals from satellites in the earth’s orbit.
A GPS is useful for knowing where you are and how fast you’re going.
`Position`, `CompassHeading` and `LinearVelocity` data are provided by all GPS modules.
Fix and Correction data are available by using the sensor GetReadings method, which is available because GPSes wrap the sensor component.

We have integrated the following  GPS modules into Viam’s RDK:

### GPS-NMEA
This GPS model uses communication standards set by the National Marine Electronics Association (NMEA).
The `gps-nmea` model can be connected via and send data through a serial connection to any device, or employ an I<sup>2</sup>C connection to a board:

#### GPS-NMEA over USB/Serial

```json
{
    "depends_on": ["board"],
    "model": "gps-nmea",
    "name": "UBLOX GPS",
    "type": "movement_sensor",
    "attributes": {
        "connection_type": "serial",
        "serial_attributes": {
            "baud_rate": 115200,
            "path": "/dev/ttyACM0"
        }
    }
}
```

The default baud rate is 115200.

#### GPS-NMEA over I2C

```json
{
    "depends_on": ["board"],
    "model": "gps-nmea",
    "name": "UBLOX GPS",
    "type": "movement_sensor",
    "attributes": {
        "board": "board",
        "connection_type": "I2C",
        "i2c_attributes": {
            "i2c_baud_rate": 115200,
            "i2c_addr": 111,
            "i2c_bus": "name_of_bus_on_board"
        }
    }
}
```

The default baud rate is 115200.

### GPS-RTK

This model uses real time kinematic positioning (RTK)[^rtk].
`gps-rtk`, a module with a chip (<a href="https://www.sparkfun.com/rtk" target="_blank">such as one of these from Sparkfun</a>[^chips]) capable of generating positional accuracy of 2cm.
The chip requires a correction source to get to the required positional accuracy.
Our `gps-rtk` model uses an over-the-internet correction source (NTRIP)[^ntrip] and sends the data over serial or I<sup>2</sup>C.

[^chips]: Sparkfun RTK Chips: <a href="https://www.sparkfun.com/rtk" target="_blank">ht<span></span>tps://www.sparkfun.com/rtk</a>

#### GPS-RTK with NTRIP over USB/Serial

```json
{
    "depends_on": ["board"],
    "model": "gps-rtk",
    "name": "UBLOX GPS",
    "type": "movement_sensor",
    "attributes": {
        "connection_type": "serial",
        "correction_source": "ntrip",
        "serial_attributes": {
            "baud_rate": 115200,
            "path": "/dev/ttyACM0"
        },
        "ntrip_attributes": {
            "ntrip_addr": "http://rtn.dot.ny.gov:8080/near_msm",
            "ntrip_baud": 38400,
            "ntrip_password": "pass",
            "ntrip_path": "",
            "ntrip_send_nmea": true,
            "ntrip_username": "user"
        }
    }
}
```

#### GPS-RTK with NTRIP over I2C

```json
{
    "depends_on": ["board"],
    "model": "gps-nmea",
    "name": "UBLOX GPS",
    "type": "movement_sensor",
    "attributes": {
        "board": "board",
        "connection_type": "I2C",
        "i2c_attributes": {
            "i2c_baud_rate": 115200,
            "i2c_addr": 111,
            "I2c_bus": "name_of_bus_on_board",
        },
        "ntrip_attributes": {
 		    "ntrip_addr": "http://rtn.dot.ny.gov:8080/near_msm",
            "ntrip_baud": 38400,
            "ntrip_password": "mypass",
            "ntrip_send_nmea": true,
            "ntrip_username": "user"
        }
    }
}
```

### RTK-Station

_**(Experimental!)**_

The experimental `rtk-station` allows you to configure your own correction source.
This does not provide any movement sensor data on its own, but can be linked to an RTK-ready GPS module on a moving robot and send that robot correction data over your own network, radio or Bluetooth in areas where internet connectivity is limited, or where an NTRIP server is unavailable.
We have implemented this in a way that does not rely on an internet connection to get correction data for a moving GPS.

More information on RTK error correction can be found at <a href="https://novatel.com/an-introduction-to-gnss/chapter-5-resolving-errors/real-time-kinematic-rtk" target="_blank">ht<span></span>tps://novatel.com/an-introduction-to-gnss/chapter-5-resolving-errors/real-time-kinematic-rtk</a>.

For all of the following RTK-station configurations, `children` is the list of one or more other GPS components that can take RTCM corrections.

#### RTK-Station using NTRIP

```json
{
    "children": [
        "gps1"
    ],
    "attributes": {
        "connection_type": "serial",
        "ntrip_attributes": {
            "ntrip_addr": "http://rtn.dot.ny.gov:8080/near_msm",
            "ntrip_baud": 38400,
            "ntrip_password": "johnviam",
            "ntrip_path": "",
            "ntrip_send_nmea": true,
            "ntrip_username": "john"
        },
        "correction_source": "ntrip"
    }
}
```

#### RTK-Station using I2C

```json
{
    "children": [
        "gps1"
    ],
    "attributes": {
        "board": "board",
        "connection_type": "serial",
        "i2c_attributes": {
            "i2c_baud_rate": 115200,
            "i2c_addr": 111,
            "i2c_bus": "name_of_bus_on_board",
       },
        "correction_source": "I2C",
        "loc_accuracy": 10,
        "svin": "time",
        "time_accuracy": 60
    }
}
```

#### RTK-Station using Serial/USB

```json
{
    "children": [
        "gps1"
    ],
    "attributes": {
        "board": "board",
        "connection_type": "serial",
        "serial_attributes": {
        	"baud_rate": 115200,
 		    "correction_path": "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4:1.0"
        },
        "correction_source": "serial"
    }
}
```

## IMU

An inertial measurement unit (IMU) can provide `AngularVelocity`, `Orientation`, and `CompassHeading` methods out of the box (ordered from most common to least common). Acceleration and Magnetometer data are available by using the Sensor `GetReadings` method, which IMUs wrap.  We have included IMUs from two manufacturers in our RDK.

### IMU Configuration

An IMU will be configured with type `movement sensor`. Viam currently (01 November 2022) supports two IMU models, manufactured by WitMotion and VectorNav. They are configured with model `imu-wit` or `imu-vectornav`, respectively.

#### Required Attributes: IMU-WIT
The `imu-wit` model requires:

Name | Type | Default Value | Description
----- | ----- | ----- | -----
`port` | string | - | The name of the port through which the IMU communicates with the computer.
`baud_rate` | int | 115200 | The rate at which data is sent to the IMU.

#### Required Attributes: IMU-VectorNav

The `imu-vectornav` model requires:

Name | Type | Default Value | Description
----- | ----- | ----- | -----
`board` | string | - | The name of the board to which the IMU is wired
`spi_bus` | string | The name of the SPI bus over which the IMU communicates with the board. On a Raspberry Pi, people often use the bus named “1.”
`chip_select_pin` | string | - | The board pin (other than the SPI bus pins) connected to the IMU chip. Used to tell the chip whether the current SPI message is meant for it or for another device.
`speed` | int |
`polling_frequency_hz` | int |

## Cameramono

_**(Experimental!)**_

We have integrated an experimental package that uses a visual odometry algorithm with dead reckoning to track the Position, Orientation, LinearVelocity and AngularVelocity of the camera’s frame.
The `cameramono` model can use any single camera with this algorithm. 

In a Viam configuration file, a camera used as a movement sensor will require a [`camera` type component](../../components/camera/) and then a `movementsensor` type component that depends on the `camera` component, and a `motion_estimation_config` based on the camera properties.

```json
{
    "components": [
        {
            "attributes": {},
            "depends_on": [],
            "model": "pi",
            "name": "example-board",
            "type": "board"
        },
        {
            "name": "myCamera",
            "type": "camera",
            "model": "webcam",
            "attributes": {},
            "depends_on": []
        },
        {
            "name": "movementCamera",
            "type": "movementsensor",
            "model": "cameramono",
            "attributes": {
                "camera": "myCamera",
                "motion_config": "see_vision_documentation"
                },
            "depends_on": [
            "myCamera"
            ]
        }
    ]
}
```

## Software Implementation
[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html)