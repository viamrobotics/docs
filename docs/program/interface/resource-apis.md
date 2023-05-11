---
title: "Resource APIs with Viam's SDKs"
linkTitle: "Resource APIs"
weight: 40
type: "docs"
description: "Using built-in resource API methods to control the components and services on your robot with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

INTRODUCTION Similar info to modular resources re. resource definitions and namespacing, "what is a resource," what is an API.
Talk about how these methods work --> providing wrapper for gRPC client request to these endpoints, which are how you access/interface with the components you have configured on your robot/`viam-server`.

## Resource Base API

Description, methods.

### ResourceName

### FromRobot

### GetOperation

### DoCommand (hmmm)

## Component APIs

INTRODUCTION: What do these do?

### Arm

The arm component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [GetEndPosition](/components/arm/#getendposition) | Get the current position of the arm as a Pose. |
| [MoveToPosition](/components/arm/#movetoposition) | Move the end of the arm to the desired Pose. |
| [MoveToJointPositions](/components/arm/#movetojointpositions) | Move each joint on the arm to the desired position. |
| [JointPositions](/components/arm/#jointpositions) | Get the current position of each joint on the arm. |
| [Stop](/components/arm/#stop) | Stop the arm from moving. |
| [IsMoving](/components/arm/#is_moving) | Get if the arm is currently moving. |
| [DoCommand](/components/arm/#docommand) | Send or receive model-specific commands. |

### Base

The base component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [MoveStraight](/components/base/#movestraight)  | Move the base in a straight line across the given distance at the given velocity. |
| [Spin](/components/base/#spin) | Move the base to the given angle at the given angular velocity. |
| [SetPower](/components/base/#setpower) | Set the relative power (out of max power) for linear and angular propulsion of the base. |
| [SetVelocity](/components/base/#setvelocity) | Set the linear velocity and angular velocity of the base. |
| [Stop](#stop) | Stop the base. |
| [DoCommand](/components/base/#docommand) | Send or receive model-specific commands. |

### Board

The board component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [AnalogReaderByName](/components/board/#analogreaderbyname) | Get an [`AnalogReader`](#analogs) by `name`. |
| [DigitalInterruptByName](/components/board/#digitalinterruptbyname) | Get a [`DigitalInterrupt`](/components/board/#digital_interrupts) by `name`. |
| [GPIOPinByName](/components/board/#gpiopinbyname) | Get a `GPIOPin` by its [pin number](/appendix/glossary/#term-pin-number). |
| [AnalogReaderNames](/components/board/#analogreadernames) | Get the `name` of every [`AnalogReader`](/components/board/#analogs). |
| [DigitalInterruptNames](/components/board/#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](/components/board/#digital_interrupts). |
| [Status](/components/board/#status) | Get the current status of this board. |
| [ModelAttributes](/components/board/#modelattributes) | Get the attributes related to the model of this board. |
| [SetPowerMode](/components/board/#setpowermode) | Set the board to the indicated power mode. |

### Camera

### Encoder

### Gantry 

### Gripper

### Input Controller

### Motor

### Movement Sensor

### Sensor

### Servo

Table with methods? 
- [Arm](/components/arm/#api)
- [Base](/components/base/#api)
- [Camera](/components/camera/#api)
- [Gantry](/components/gantry/#api)
- [Gripper](/components/gripper/#api)
- [Input Controller](/components/input-controller/#api)
- [Motor](/components/motor/#api)
- [Movement Sensor](/components/movement-sensor/#api)
- [Sensor](/components/sensor/#api)
- [Servo](/components/servo/#api)

## Service APIs

INTRODUCTION: What do these do?

Table with methods?

### Motion

- [Motion](/services/motion/#api)

### SLAM

- [SLAM](/services/slam)

### MLModel

- [MlModel](/services/ml

### Vision
)
- [Vision](/services/vision)

Might be long WIP fully building out here as SLAM, MlModel, Vision client methods are most extensively documented in SDKs, and Sensors service is a bit murky.
Could have tables linking to Go and Python SDK docs for now.

- [Frame System](/services/frame-system/#api)
^^ Tricky, might need explanation.

## Additional Interfaces

### GPIO Pins

In addition to the [Board API](#board), the [board component](/components/board) supports the following methods for interfacing with GPIO Pins on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Set](/components/board/#set) | Set the output of this pin to high/low. |
| [Get](/components/board/#get) | Get if this pin is active (high). |
| [PWM](/components/board/#pwm) | Get the pin’s pulse-width modulation duty cycle. |
| [SetPWM](/components/board/#pwmfreq) | Set the pin’s pulse-width modulation duty cycle. |
| [PWMFreq](/components/board/#pwmfreq) | Get the pulse-width modulation frequency of this pin. |
| [SetPWMFreq](/components/board/#setpwmfreq) | Set the pulse-width modulation frequency of this pin. |

### Analog-to-Digital Converters (ADCs)

In addition to the [Board API](#board), the [board component](/components/board) supports the following methods for interfacing with [ADCs](/components/board/#analogs) on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Read](/components/board/#read) | Read the current integer value of the digital signal output by the ADC. |

###  Digital Interrupts

In addition to the [Board API](#board), the [board component](/components/board) supports the following methods for interfacing with [digital interrupts](/components/board/#digital_interrupts)  on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Value](#value) | Get the current value of this interrupt. |
| [Tick](#tick) | Record an interrupt. |
| [AddCallback](#addcallback) | Add a channel as a callback for [Tick()](#tick). |
| [AddPostProcessor](#addpostprocessor) | Add a PostProcessor function for [Value()](#value). |
