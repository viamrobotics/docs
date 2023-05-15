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
Python: class methods all classes that inherit from resource base class should possess.
Go it might work differently.

### ResourceName

PYTHON: get_resource_name(name: str)→ viam.proto.common.ResourceName[source]
GO: 

### FromRobot

PYTHON: from_robot(robot: viam.robot.client.RobotClient, name: str)→ typing_extensions.Self[source]
GO: func ResourceFromRobot[T resource.Resource](robot Robot, name resource.Name) (T, error)

### GetOperation

PYTHON: get_operation(kwargs: Mapping[str, Any])→ viam.operations.Operation[source]
GO:

### DoCommand (hmmm)

PYTHON: do_command(command: Mapping[str, viam.utils.ValueTypes], *, timeout: Optional[float] = None, **kwargs)→ Mapping[str, viam.utils.ValueTypes]
GO:

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

| Method Name | Description |
| ----------- | ----------- |
| [GetImage](/components/camera/#getimage) | Return an image from the camera. |
| [GetPointCloud](/components/camera/#getpointcloud) | Return a point cloud from the camera. |
| [GetProperties](/components/camera/#getproperties) | Return the camera intrinsic and camera distortion parameters, as well as whether the camera supports returning point clouds. |

### Encoder

Method Name | Description
----------- | -----------
[GetPosition](/components/encoder/#getposition) | Get the current position of the encoder.
[ResetPosition](/components/encoder/#resetposition) | Reset the position to zero.
[GetProperties](/components/encoder/#getproperties) | Get the supported properties of this encoder.

### Gantry

| Method Name | Description |
| ----------- | ----------- |
[Position](/components/gantry/#position) | Get the current positions of the axes of the gantry in mm. |
[MoveToPosition](/components/encoder//#movetoposition) | Move the axes of the gantry to the desired positions. |
[Lengths](/components/gantry/#lengths) | Get the lengths of the axes of the gantry in mm. |
[Stop](/components/gantry/#stop) | Stop the gantry from moving. |
[IsMoving](/components/gantry#ismoving) | Get if the gantry is currently moving. |

### Gripper

Method Name | Description
----------- | -----------
[`Open`](/components/gripper/#open) | Open the gripper.
[`Grab`](/components/gripper/#grab) | Close the gripper until it grabs something or closes completely.
[`Stop`](/components/gripper/#stop) | Stop the gripper's movement.
[`IsMoving`](/components/gripper/#ismoving) | Report whether the gripper is currently moving.

### Input Controller

| Method Name | Description |
| ----------- | ----------- |
| [Controls](/components/input-controller/#controls) | Get a list of input `Controls` that this Controller provides. |
| [Events](/components/input-controller/#events) | Get the current state of the Controller as a map of the most recent [Event](/components/input-controller/#event-object) for each [Control](/components/input-controller/#control-field). |
| [RegisterControlCallback](/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/components/input-controller/#eventtype-field) selected occurs on the given [Control](/components/input-controller/#control-field). |

### Motor

Method Name | Description
----------- | -----------
[SetPower](/components/motor/#setpower) | Set the power to send to the motor as a portion of max power.
[GoFor](/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified RPM.
[GoTo](/components/motor/#goto) | Send the motor to a specified position (in terms of revolutions from home) at a specified speed.
[ResetZeroPosition](/components/motor/#resetzeroposition) | Set the current position to be the new zero (home) position.
[GetPosition](/components/motor/#getposition) | Report the position of the motor based on its encoder. Not supported on all motors.
[GetProperties](/components/motor/#getproperties) | Return whether or not the motor supports certain optional features.
[Stop](/components/motor/#stop) | Cut power to the motor off immediately, without any gradual step down.
[IsPowered](/components/motor/#ispowered) | Return whether or not the motor is currently on, and the amount of power to it.
[IsMoving](/components/motor/#ismoving) | Return whether the motor is moving or not.

### Movement Sensor

Method Name | Description |
----------- | ----------- |
[GetPosition](/components/movement-sensor/#getposition) | Get the current latitude, longitude and altitude. |
[GetLinearVelocity](/components/movement-sensor/#getlinearvelocity) | Get the current linear velocity as a 3D vector. |
[GetAngularVelocity](/components/movement-sensor/#getangularvelocity) | Get the current angular velocity as a 3D vector. |
[GetLinearAcceleration](/components/movement-sensor/#getlinearacceleration) | Get the current linear acceleration as a 3D vector. |
[GetCompassHeading](/components/movement-sensor/#getcompassheading) | Get the current compass heading in degrees. |
[GetOrientation](/components/movement-sensor/#getorientation) | Get the current orientation. |
[GetProperties](/components/movement-sensor/#getproperties) | Get the supported properties of this sensor. |
[GetAccuracy](/components/movement-sensor/#getaccuracy) | Get the accuracy of the various sensors. |
[GetReadings](/components/movement-sensor/#getreadings) | Obtain the measurements/data specific to this sensor. |

### Sensor

| Method Name | Description |
| ----------- | ----------- |
| [Readings](/components/sensor/#readings) | Get the measurements or readings that this sensor provides. |

### Servo

| Method Name | Description |
| ----------- | ----------- |
| [Move](/components/servo/#move) | Move the servo to the desired angle. |
| [Position](/components/servo/#position) | Get the current angle of the servo. |
| [Stop](/components/servo/#stop) | Stop the servo. |

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

### Digital Interrupts

In addition to the [Board API](#board), the [board component](/components/board) supports the following methods for interfacing with [digital interrupts](/components/board/#digital_interrupts)  on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Value](/components/board/#value) | Get the current value of this interrupt. |
| [Tick](/components/board/#tick) | Record an interrupt. |
| [AddCallback](/components/board/#addcallback) | Add a channel as a callback for [Tick()](/components/board/#tick). |
| [AddPostProcessor](/components/board/#addpostprocessor) | Add a PostProcessor function for [Value()](/components/board/#value). |
