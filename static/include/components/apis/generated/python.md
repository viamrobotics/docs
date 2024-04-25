### GetEndPosition

Get the current position of the end of the arm expressed as a Pose.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.arm.Pose](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_end_position).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the end position of the arm as a Pose.
pos = await my_arm.get_end_position()
```

### MoveToPosition

Move the end of the arm to the Pose specified in pose.


**Parameters:**

- `pose` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_position).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose.
await my_arm.move_to_position(pose=examplePose)
```

### GetJointPositions

Get the JointPositions representing the current position of the arm.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.proto.component.arm.JointPositions](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_joint_positions).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the current position of each joint on the arm as JointPositions.
pos = await my_arm.get_joint_positions()
```

### MoveToJointPositions

Move each joint on the arm to the corresponding angle specified in positions.


**Parameters:**

- `positions` [(float)](https://python.viam.dev/autoapi/viam/../proto/component/arm/index.html#viam.proto.component.arm.JointPositions): Optional.
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/component/arm/index.html#viam.proto.component.arm.JointPositions): Optional.
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/component/arm/index.html#viam.proto.component.arm.JointPositions): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_joint_positions).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Declare a list of values with your desired rotational value for each joint on
# the arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.
jointPos = arm.move_to_joint_positions(
    JointPositions(values=[0.0, 45.0, 0.0, 0.0, 0.0]))

# Move each joint of the arm to the position these values specify.
await my_arm.move_to_joint_positions(positions=jointPos)
```

### Stop

Stop all motion of the arm. It is assumed that the arm stops immediately.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.stop).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()
```

### IsMoving

Get if the arm is currently moving.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.is_moving).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(my_arm.is_moving())
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetKinematics

Get the kinematics information associated with the arm.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[viam.components.arm.KinematicsFileFormat.ValueType, bytes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_kinematics).

```python
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the kinematics information associated with the arm.
kinematics = await my_arm.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.close).

```python
await component.close()
```

### MoveStraight

Move the base in a straight line the given distance, expressed in millimeters, at the given velocity, expressed in millimeters per second. When distance or velocity is 0, the base will stop. This method blocks until completed or cancelled.


**Parameters:**

- `distance` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `velocity` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base 40 mm at a velocity of 90 mm/s, forward.
await my_base.move_straight(distance=40, velocity=90)

# Move the base 40 mm at a velocity of -90 mm/s, backward.
await my_base.move_straight(distance=40, velocity=-90)
```

### Spin

Spin the base in place angle degrees, at the given angular velocity, expressed in degrees per second. When velocity is 0, the base will stop. This method blocks until completed or cancelled.


**Parameters:**

- `angle` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `velocity` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.spin).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Spin the base 10 degrees at an angular velocity of 15 deg/sec.
await my_base.spin(angle=10, velocity=15)
```

### SetPower

Set the linear and angular velocity of the Base When linear is 0, the the base will spin. When angular is 0, the the base will move in a straight line. When both linear and angular are 0, the base will stop. When linear and angular are both nonzero, the base will move in an arc, with a tighter radius if angular power is greater than linear power.


**Parameters:**

- `linear` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `angular` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Make your wheeled base move forward. Set linear power to 75%.
print("move forward")
await my_base.set_power(
    linear=Vector3(x=0, y=-.75, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base move backward. Set linear power to -100%.
print("move backward")
await my_base.set_power(
    linear=Vector3(x=0, y=-1.0, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base spin left. Set angular power to 100%.
print("spin left")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=1))

# Make your wheeled base spin right. Set angular power to -75%.
print("spin right")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=-.75))
```

### SetVelocity

Set the linear and angular velocities of the base.


**Parameters:**

- `linear` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `angular` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Set the linear velocity to 50 mm/sec and the angular velocity to
# 15 degree/sec.
await my_base.set_velocity(
    linear=Vector3(x=0, y=50, z=0), angular=Vector3(x=0, y=0, z=15))
```

### Stop

Stop the base.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.stop).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base forward 10 mm at a velocity of 50 mm/s.
await my_base.move_straight(distance=10, velocity=50)

# Stop the base.
await my_base.stop()
```

### IsMoving

Get if the base is currently moving.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.is_moving).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Check whether the base is currently moving.
moving = await my_base.is_moving()
print('Moving: ', moving)
```

### GetProperties

Get the base width and turning radius


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.base.Base.Properties](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.get_properties).

```python
my_base = Base.from_robot(robot=robot, name="my_base")

# Get the width and turning radius of the base
properties = await my_base.get_properties()

# Get the width
print(f"Width of base: {properties.width_meters}")

# Get the turning radius
print(f"Turning radius of base: {properties.turning_radius_meters}")

# Get the wheel circumference
print(f"Wheel circumference of base: {properties.wheel_circumference_meters}")
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.close).

```python
await component.close()
```

### Read

Read the current value.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.AnalogReaderClient.read).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
duty_cycle = await pin.get_pwm()

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(
    name="my_example_analog_reader")

# Get the value of the digital signal "my_example_analog_reader" has most
# recently measured.
reading = reader.read()
```

### Value

Get the current value of the interrupt, which is based on the type of interrupt.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.DigitalInterruptClient.value).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Get the amount of times this DigitalInterrupt has been interrupted with a
# tick.
count = await interrupt.value()
```

### GetGPIO

Get the high/low state of the pin.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
high = await pin.get()
```

### SetGPIO

Set the pin to either low or high.


**Parameters:**

- `high` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the pin to high.
await pin.set(high="true")
```

### PWM

Get the pin’s given duty cycle.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([float](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
duty_cycle = await pin.get_pwm()
```

### SetPWM

Set the pin to the given duty_cycle.


**Parameters:**

- `duty_cycle` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the duty cycle to .6, meaning that this pin will be in the high state for
# 60% of the duration of the PWM interval period.
await pin.set_pwm(cycle=.6)
```

### PWMFrequency

Get the PWM frequency of the pin.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([int](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get the PWM frequency of this pin.
freq = await pin.get_pwm_frequency()
```

### SetPWMFrequency

Set the pin to the given PWM frequency (in Hz). When frequency is 0, it will use the board’s default PWM frequency.


**Parameters:**

- `frequency` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the PWM frequency of this pin to 1600 Hz.
high = await pin.set_pwm_frequency(frequency=1600)
```

### ReadAnalogReader

Get an AnalogReader by name.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.components.board.board.Board.AnalogReader](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_reader_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(name="my_example_analog_reader")
```

### GetDigitalInterruptValue

Get a DigitalInterrupt by name.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.components.board.board.Board.DigitalInterrupt](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")
```

### GPIOPinByName

Get a GPIO Pin by name.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([viam.components.board.board.Board.GPIOPin](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.gpio_pin_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")
```

### AnalogReaderNames

Get the names of all known analog readers.


**Parameters:**


**Returns:**

([List[str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_reader_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every AnalogReader configured on the board.
names = await my_board.analog_reader_names()
```

### DigitalInterruptNames

Get the names of all known digital interrupts.


**Parameters:**


**Returns:**

([List[str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every DigitalInterrupt configured on the board.
names = await my_board.digital_interrupt_names()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### SetPowerMode

Set the board to the indicated power mode.


**Parameters:**

- `mode` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `duration` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.set_power_mode).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Set the power mode of the board to OFFLINE_DEEP.
status = await my_board.set_power_mode(mode=PowerMode.POWER_MODE_OFFLINE_DEEP)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### WriteAnalog

Write an analog value to a pin on the board.


**Parameters:**

- `pin` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `value` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.write_analog).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Set pin 11 to value 48.
await my_board.write_analog(pin="11", value=48)
```

### <NO PROTO FOUND, USING METHOD NAME> stream_ticks

Stream digital interrupt ticks.


**Parameters:**

- `interrupts` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.board.board.TickStream](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.stream_ticks).

```python
my_board = Board.from_robot(robot=robot, name="my_board")
di8 = await my_board.digital_interrupt_by_name(name="8"))
di11 = await my_board.digital_interrupt_by_name(name="11"))

Stream ticks from pins 8 and 11.
ticks = my_board.stream_ticks([di8, di11])
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.close).

```python
await component.close()
```

### GetImage

Get the next image from the camera as an Image or RawImage. Be sure to close the image when finished.


**Parameters:**

- `mime_type` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([PIL.Image.Image | viam.components.camera.RawImage](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_image).

```python
my_camera = Camera.from_robot(robot=robot, name="my_camera")

# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_camera.get_image(mime_type = CameraMimeType.VIAM_RAW_DEPTH)

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame = frame.bytes_to_depth_array()
```

### GetImages

Get simultaneous images from different imagers, along with associated metadata. This should not be used for getting a time series of images from the same imager.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[List[viam.media.video.NamedImage], viam.proto.common.ResponseMetadata]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_images).

```python
my_camera = Camera.from_robot(robot=robot, name="my_camera")

images, metadata = await my_camera.get_images()
img0 = images[0].image
timestamp = metadata.captured_at
```

### GetPointCloud

Get the next point cloud from the camera. This will be returned as bytes with a mimetype describing the structure of the data. The consumer of this call should encode the bytes into the formatted suggested by the mimetype.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[bytes, str]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_point_cloud).

```python
import numpy as np
import open3d as o3d

data, _ = await camera.get_point_cloud()

# write the point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(data)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

### GetProperties

Get the camera intrinsic parameters and camera distortion parameters


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.camera.Camera.Properties](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_properties).

```python
my_camera = Camera.from_robot(robot=robot, name="my_camera")

properties = await my_camera.get_properties()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.close).

```python
await component.close()
```

### ResetPosition

Set the current position to be the new zero (home) position.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.reset_position).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Reset the zero position of the encoder.
await my_encoder.reset_position()
```

### GetPosition

Report the position of the encoder. The value returned is the current position in terms of it’s position_type. The position will be either in relative units (ticks away from a zero position) for PositionType.TICKS or absolute units (degrees along a circle) for PositionType.DEGREES.


**Parameters:**

- `position_type` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[float, viam.proto.component.encoder.PositionType.ValueType]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_position).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get the position of the encoder in ticks
position = await my_encoder.get_position(encoder.PositionTypeTicks)
print("The encoder position is currently ", position[0], position[1])
```

### GetProperties

Return a dictionary of the types of position reporting this encoder supports


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.encoder.encoder.Encoder.Properties](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_properties).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get whether the encoder returns position in ticks or degrees.
properties = await my_encoder.get_properties()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.close).

```python
await component.close()
```

### GetPosition

Get the position in millimeters.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[float]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Get the current positions of the axes of the gantry in millimeters.
positions = await my_gantry.get_position()
```

### MoveToPosition

Move the gantry to a new position at the requested speeds.


**Parameters:**

- `positions` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `speeds` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.move_to_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Create a list of positions for the axes of the gantry to move to. Assume in
# this example that the gantry is multi-axis, with 3 axes.
examplePositions = [1, 2, 3]

exampleSpeeds = [3, 9, 12]

# Move the axes of the gantry to the positions specified.
await my_gantry.move_to_position(
    positions=examplePositions, speeds=exampleSpeeds)
```

### Home

Home the gantry to find it’s starting and ending positions


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.home).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

await my_gantry.home()
```

### GetLengths

Get the lengths of the axes of the gantry in millimeters.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[float]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_lengths).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await my_gantry.get_lengths()
```

### Stop

Stop all motion of the gantry. It is assumed that the gantry stops immediately.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.stop).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the gantry stops
# immediately.
await my_gantry.stop()
```

### IsMoving

Get if the gantry is currently moving.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.is_moving).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the
# gantry stops immediately.
await my_gantry.stop()

# Print if the gantry is currently moving.
print(my_gantry.is_moving())
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.close).

```python
await component.close()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, Any]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.close).

```python
await component.close()
```

### Open

Open the gripper.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.open).

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Open the gripper.
await my_gripper.open()
```

### Grab

Instruct the gripper to grab.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.grab).

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Grab with the gripper.
grabbed = await my_gripper.grab()
```

### Stop

Stop the gripper. It is assumed the gripper stops immediately.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.stop).

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Stop the gripper.
await my_gripper.stop()
```

### IsMoving

Get if the gripper is currently moving.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.is_moving).

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Check whether the gripper is currently moving.
moving = await my_gripper.is_moving()
print('Moving:', moving)
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.close).

```python
await component.close()
```

### GetControls

Returns a list of Controls provided by the Controller


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.components.input.input.Control]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_controls).

```python
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the list of Controls provided by the controller.
controls = await my_controller.get_controls()

# Print the list of Controls provided by the controller.
print(f"Controls: {controls}")
```

### GetEvents

Returns the most recent Event for each input (which should be the current state)


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Dict[viam.components.input.input.Control, viam.components.input.input.Event]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_events).

```python
# Get the controller from the machine.
my_controller = Controller.from_robot(
    robot=myRobotWithController, name="my_controller")

# Get the most recent Event for each Control.
recent_events = await my_controller.get_events()

# Print out the most recent Event for each Control.
print(f"Recent Events: {recent_events}")
```

### RegisterControlCallback

Register a function that will fire on given EventTypes for a given Control


**Parameters:**

- `control` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `triggers` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `function` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(Dict[str, Any])](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.register_control_callback).

```python
# Define a function to handle pressing the Start Menu Button "BUTTON_START" on
# your controller, printing out the start time.
def print_start_time(event):
    print(f"Start Menu Button was pressed at this time: {event.time}")


# Define a function that handles the controller.
async def handle_controller(controller):
    # Get the list of Controls on the controller.
    controls = await controller.get_controls()

    # If the "BUTTON_START" Control is found, register the function
    # print_start_time to fire when "BUTTON_START" has the event "ButtonPress"
    # occur.
    if Control.BUTTON_START in controls:
        controller.register_control_callback(
            Control.BUTTON_START, [EventType.BUTTON_PRESS], print_start_time)
    else:
        print("Oops! Couldn't find the start button control! Is your "
            "controller connected?")
        exit()

    while True:
        await asyncio.sleep(1.0)


async def main():
    # ... < INSERT CONNECTION CODE FROM MACHINE'S CODE SAMPLE TAB >

    # Get your controller from the machine.
    my_controller = Controller.from_robot(
        robot=myRobotWithController, name="my_controller")

    # Run the handleController function.
    await handleController(my_controller)

    # ... < INSERT ANY OTHER CODE FOR MAIN FUNCTION >
```

### TriggerEvent

Directly send an Event (such as a button press) from external code


**Parameters:**

- `event` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.trigger_event).

```python
# Define a "Button is Pressed" event for the control BUTTON_START.
button_is_pressed_event = Event(
    time(), EventType.BUTTON_PRESS, Control.BUTTON_START, 1.0)

# Trigger the event on your controller. Set this trigger to timeout if it has
# not completed in 7 seconds.
await myController.trigger_event(event=my_event, timeout=7.0)
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.close).

```python
await component.close()
```

### SetPower

Sets the “percentage” of power the motor should employ between -1 and 1. When power is negative, the rotation will be in the backward direction.


**Parameters:**

- `power` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.set_power).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the power to 40% forwards.
await my_motor.set_power(power=0.4)
```

### GoFor

Spin the motor the specified number of revolutions at specified rpm. When rpm or revolutions is a negative value, the rotation will be in the backward direction. Note: if both rpm and revolutions are negative, the motor will spin in the forward direction.


**Parameters:**

- `rpm` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `revolutions` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.go_for).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor 7.2 revolutions at 60 RPM.
await my_motor.go_for(rpm=60, revolutions=7.2)
```

### GoTo

Spin the motor to the specified position (provided in revolutions from home/zero), at the specified speed, in revolutions per minute. Regardless of the directionality of the rpm this function will move the motor towards the specified position.


**Parameters:**

- `rpm` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `position_revolutions` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.go_to).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor to 8.3 revolutions from home at 75 RPM.
await my_motor.go_to(rpm=75, revolutions=8.3)
```

### ResetZeroPosition

Set the current position (modified by offset) to be the new zero (home) position.


**Parameters:**

- `offset` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.reset_zero_position).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the current position as the new home position with no offset.
await my_motor.reset_zero_position(offset=0.0)
```

### GetPosition

Report the position of the motor based on its encoder. The value returned is the number of revolutions relative to its zero position. This method will raise an exception if position reporting is not supported by the motor.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([float](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_position).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Get the current position of the motor.
position = await my_motor.get_position()
```

### GetProperties

Report a dictionary mapping optional properties to whether it is supported by this motor.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.motor.motor.Motor.Properties](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_properties).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Report a dictionary mapping optional properties to whether it is supported by
# this motor.
properties = await my_motor.get_properties()

# Print out the properties.
print(f'Properties: {properties}')
```

### Stop

Stop the motor immediately, without any gradual step down.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.stop).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Stop the motor.
await my_motor.stop()
```

### IsPowered

Returns whether or not the motor is currently running.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[bool, float]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_powered).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently running.
powered = await my_motor.is_powered()

print('Powered: ', powered)
```

### IsMoving

Get if the motor is currently moving.


**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([bool](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_moving).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently moving.
moving = await my_motor.is_moving()
print('Moving: ', moving)
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.close).

```python
await component.close()
```

### GetPosition

Get the current GeoPoint (latitude, longitude) and altitude (m)


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[viam.components.movement_sensor.GeoPoint, float]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_position).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot,
    name="my_movement_sensor")

# Get the current position of the movement sensor.
position = await my_movement_sensor.get_position()
```

### GetLinearVelocity

Get the current linear velocity as a Vector3 with x, y, and z axes represented in m/sec


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.Vector3](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_linear_velocity).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear velocity of the movement sensor.
lin_vel = await my_movement_sensor.get_linear_velocity()
```

### GetAngularVelocity

Get the current angular velocity as a Vector3 with x, y, and z axes represented in degrees/sec


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.Vector3](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_angular_velocity).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current angular velocity of the movement sensor.
ang_vel = await my_movement_sensor.get_angular_velocity()

# Get the y component of angular velocity.
y_ang_vel = ang_vel.y
```

### GetLinearAcceleration

Get the current linear acceleration as a Vector3 with x, y, and z axes represented in m/sec^2


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.Vector3](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_linear_acceleration).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear acceleration of the movement sensor.
lin_accel = await my_movement_sensor.get_linear_acceleration()

# Get the x component of linear acceleration.
x_lin_accel = lin_accel.x
```

### GetCompassHeading

Get the current compass heading in degrees


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([float](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_compass_heading).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current compass heading of the movement sensor.
heading = await my_movement_sensor.get_compass_heading()
```

### GetOrientation

Get the current orientation


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.Orientation](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_orientation).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current orientation vector of the movement sensor.
orientation = await my_movement_sensor.get_orientation()
```

### GetProperties

Get the supported properties of this sensor


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.movement_sensor.MovementSensor.Properties](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_properties).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the supported properties of the movement sensor.
properties = await my_movement_sensor.get_properties()
```

### GetAccuracy

Get the accuracy of the various sensors


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([viam.components.movement_sensor.movement_sensor.MovementSensor.Accuracy](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_accuracy).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the accuracy of the movement sensor.
accuracy = await my_movement_sensor.get_accuracy()
```

### GetReadings

Obtain the measurements/data specific to this sensor. If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.SensorReading]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_readings).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the latest readings from the movement sensor.
readings = await my_movement_sensor.get_readings()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.close).

```python
await component.close()
```

### GetVoltage

Get the voltage reading and bool IsAC


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[float, bool]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_voltage).

```python
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the voltage reading from the power sensor
voltage, is_ac = await my_power_sensor.get_voltage()
print("The voltage is", voltage, "V, Is AC:", is_ac)
```

### GetCurrent

Get the current reading and bool IsAC


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Tuple[float, bool]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_current).

```python
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the current reading from the power sensor
current, is_ac = await my_power_sensor.get_current()
print("The current is ", current, " A, Is AC: ", is_ac)
```

### GetPower

Get the power reading in watts


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([float](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_power).

```python
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the power reading from the power sensor
power = await my_power_sensor.get_power()
print("The power is", power, "Watts")
```

### GetReadings

Obtain the measurements/data specific to this sensor. If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.SensorReading]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_readings).

```python
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_power_sensor.get_readings()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.close).

```python
await component.close()
```

### GetReadings

Obtain the measurements/data specific to this sensor.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.SensorReading]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/client/index.html#viam.components.sensor.client.SensorClient.get_readings).

```python
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

### DoCommand

Send/Receive arbitrary commands to the Resource


**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([Mapping[str, viam.utils.ValueTypes]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/client/index.html#viam.components.sensor.client.SensorClient.do_command).

```python
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

### GetGeometries

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.


**Parameters:**

- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

([List[viam.proto.common.Geometry]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/client/index.html#viam.components.sensor.client.SensorClient.get_geometries).

```python
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

### Close

Safely shut down the resource and prevent further use.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/client/index.html#viam.components.sensor.client.SensorClient.close).

```python
await component.close()
```

