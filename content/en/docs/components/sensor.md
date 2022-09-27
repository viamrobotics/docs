---
title: "Sensor Component"
linkTitle: "Sensor"
weight: 70
draft: false
type: "docs"
description: "Explanation of sensor types, configuration, and usage in Viam."
draft: true
---
This page explains how to set up a generic sensor component with Viam.
Viam has a few types of sensor implemented including an ultrasonic sensor, but this doc will go over setting up a custom sensor so you can implement almost any sort of sensor.
Note that Viam has a separate, more specific component type called *movement sensor* specifically for GPS units, IMUs, and other sensors that detect position, velocity and acceleration.
Find that page [here](../movementsensor).
Find more information about encoders, another component type, [here](../encoder).

## Hardware Requirements
 - Some sort of sensor
 - A [board](../board)
 - Depending on the type of sensor output, an analog to digital converter may be necessary to allow the sensor to communicate with the board

## Wiring
This will depend on the sensor. Refer to the sensor’s data sheet.

## Viam Configuration
When you create a custom sensor you’ll create a set of attributes unique to that sensor model. The JSON file you create must include a type (`sensor`), model (whatever you named your custom sensor model), and name (of your choice; used to refer to that specific sensor in your code). You will also need to include whatever required attributes you define in your custom sensor component implementation.

``` json
{
    "name": "mySensorName",
    "type": "sensor",
    "model": "mySensorModel",
    "attributes": {},
    "depends_on": []
}
```

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/sensor/index.html)
