---
title: GPS Component Documentation
summary: Explanation of GPS types, configuration, and usage in Viam.
authors:
    - Rand Hidayah
date: 2022-08-18 
---
# Global Positioning Satellite (GPS) Component

Viam's GPS component code requires the GoNum package. Refer to 
[https://pkg.go.dev/gonum.org/v1/gonum/mat?utm_source=godoc#](https://pkg.go.dev/gonum.org/v1/gonum/mat?utm_source=godoc#) for more information on GoNum. 

## Overview

Want to know where you are in the world? Go outside and use Viam with our GPS component! The Global Positioning System (GPS) refers to the satellite-based radio navigation system that polls where a receiver is on the globe and returns information on the position (latitude and longitude), and height of that receiver (altitude). There are other optional data that can be transmitted by specific satellite systems and ancillary sensors, such as an IMU. 

Since the world of GPS modules is wide, we at Viam are focusing this documentation on how to set up a GPS chip using our software and the supported message interfaces that we have implemented for two main types of GPS: NMEA  and RTK. The National Marine Electronics Association (NMEA) message refers to the message standard that the onboard hardware can output, which any standard GPS should be able to provide. A GPS equipped with a Real-TIme-Kinematics (RTK) algorithm also uses an NMEA message, but also gets another type of message from Radio Technical Commission for Maritime Services (RTCM) to correct the GPS readings so that the receiver can be positioned with 2cm accuracy.

## Requirements
All GPS modules require a board that can make a serial or I2C connection. There are currently (18 Aug 2022) two protocols implemented to receive and signals in the standard NMEA and RTCM messages:

1. GPS Module RTK or NMEA (NMEA/RTK Connected by serial)

(Diagram forthcoming)

2. NMEA/RTK Connected by I2C
(Diagram with Pi forthcoming)

We have two ways of setting up RTK GPS corrections in RDK. Either by logging into a network that provides these correction messages over the internet, an NTRIP server (see, ["Networked Transport of RTCM via Internet Protocol"](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol)). Alternatively, you could set up your own RTK base station using an RTK capable chip and then send the correction data to the receiver chip on a moving robot via serial, radio, bluetooth, or any other method.


# Attributes and Configuration
All GPS in the NMEA package.

Board Models: serial-nmea, serial-I2C

<style>
    .noscrolltable
    {
        width:"90%";
      }
table.test
{
    table-layout:fixed; 
    word-wrap:break-word;
    text-wrap:normal;
    overflow-wrap: break-word;
    word-wrap:break-word
    
}      

td {
    word-wrap:break-word;
}

.align{
    text-align:center;
}

.fixedcol
    {
        column-width:350px;

    }
    </style>



<table class="test">
<tr>
<th>Item</th>
<th>Description</th>
</tr>
<tr>
<td><strong>Board</strong></td>
<td>The board model that the GPS is connected to.</td>
</tr>
<tr><td class="align" colspan="2"><strong>Serial Specific</strong></td>
</tr>
<tr>
<td><strong>Path</strong></td>
<td>The path to the physical connection of the gps often looks like:<br> <file>/dev/serial/by-id/ccc</file>, will be in the <file>/dev/</file> folder.</td>
</tr>
<tr>
<td><strong>Correction_path</strong></td>
<td>The path to the physical port that the correction messages are being<br> received for RTK, if available, in the <file>/dev/</file> directory.</td>
</tr>
<tr>
<td><strong>Baud_rate</strong></td>
<td>The rate at which data is being received on the serial connection, defaults<br>
to 9600 if not set. Needs to be one of the following baud rates <link></td>
</tr>
<tr>
<td><strong>Correction_baudrate</strong></td>
<td>The baud rate at which serial correction data is being received on the<br>  correction serial port</td>
</tr>
<tr>
<td><strong>Disable_nmea</strong></td>
<td>An option to disable receiving NMEA messages</td>
</tr>
<tr><td class="align" colspan="2"><strong>I2C specific</strong></td></tr>
<tr>
<td><strong>Bus</strong></td>
<td>The board bus that handles I2C communication.</td>
</tr>
<tr>
<td><strong>I2c_address</strong></td>
<td>The GPS module's address on the I2C bus.</td>
</tr>
<tr><td class="align" colspan="2"><strong>NTRIP</strong></td></tr>
<tr>
<td><strong>Ntrip_addr</strong></td>
<td>The URL of the correction network service where you login to obtain<br> correction data. Check for available servers in your area of the world.</td>
</tr>
<tr>
<td><strong>Ntrip_connect_attempts</strong></td>
<td>The maximum number of connection attempts for the NTRIP server.</td>
</tr>
<tr>
<td><strong>Ntrip_mountpoint</strong></td>
<td>The specific mountpoint or mountpoint search algorithm from which to<br> obtain correction data. 
The mountpoint corresponds to what your NTRIP<br> network provided. 
Viam recommends using a mountpoint within 10km of<br> your operations.</td>
</tr>
<tr>
<td><strong>Ntrip_password</strong></td>
<td>Your NTRIP account password.</td>
</tr>
<tr>
<td><strong>Ntrip_username</strong></td>
<td>Your NTRIP account username.</td>
</tr>
<tr>
<td><strong>Ntrip_path</strong></td>
<td>An optional secondary device path to write serial messages. 
Typically used <br>to send corrections to a path other than your receiver.</td>
</tr>
<tr>
<td><strong>Ntrip_baud</strong></td>
<td>(Optional) The baud rate for the optional <strong>ntrip_path</strong>.</td>
</tr>
<tr>
<td><strong>Ntrip_input_protocol</strong></td>
<td>The physical connection with which to send correction data to the <br>receiver chip.</td>
</tr>
</table>

## RTK Station
RTK has the same fields as NMEA GPS, above, as well as one additional field to  set a NMEA GPS with one additional field: 

**Children**: A list of child gps modules that will receive RTK correction data (i.e., the RTCM correction stream) on their correction_path.

#Available Methods

- `ReadLocation` returns the current latitude and longitude.

- `ReadAltitude` returns the current altitude in meters.

- `ReadSpeed` returns the current ground speed in mm per sec.

- `ReadAccuracy` Horizontal and vertical position error in meters.

- `ReadSatellites` number of satellites used for fix, and total in view.

- `ReadValid` whether or not the GPS chip had a valid fix for the most recent dataset being received from the satellites.

- `GetReadings` gets all the readings from the gps as one output.

- (Add an interface for adding additional functionality to the component.)