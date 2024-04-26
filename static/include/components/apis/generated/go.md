### GetEndPosition

EndPosition returns the current position of the arm.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `spatialmath`[(Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

### MoveToPosition

MoveToPosition moves the arm to the given absolute position.This will block until done or a new operation cancels this one

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `pose`[(Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#pose):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

### MoveToJointPositions

MoveToJointPositions moves the arm's joints to the given positions.This will block until done or a new operation cancels this one

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `pb`[(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#pb):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

### GetJointPositions

JointPositions returns the current joint positions of the arm.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `pb`[(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#pb):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

### MoveStraight

MoveStraight moves the robot straight a given distance at a given speed.If a distance or speed of zero is given, the base will stop.This method blocks until completed or cancelled

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `distanceMm`[(int)](<INSERT PARAM TYPE LINK>)
- `mmPerSec`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

### Spin

Spin spins the robot by a given angle in degrees at a given speed.If a speed of 0 the base will stop.Given a positive speed and a positive angle, the base turns to the left (for built-in RDK drivers)This method blocks until completed or cancelled

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(angleDeg)](<INSERT PARAM TYPE LINK>)
- `degsPerSec`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

### SetPower

For linear power, positive Y moves forwards for built-in RDK driversFor angular power, positive Z turns to the left for built-in RDK drivers

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(linear)](<INSERT PARAM TYPE LINK>)
- `angular`[(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#angular):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

### SetVelocity

linear is in mmPerSec (positive Y moves forwards for built-in RDK drivers)angular is in degsPerSec (positive Z turns to the left for built-in RDK drivers)

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(linear)](<INSERT PARAM TYPE LINK>)
- `angular`[(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#angular):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

### GetProperties



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

### Read



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#AnalogReader).

### Close



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

### ReadAnalogReader

AnalogReaderByName returns an analog reader by name.

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(AnalogReader)](<INSERT PARAM TYPE LINK>)
- [(bool)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### GetDigitalInterruptValue

DigitalInterruptByName returns a digital interrupt by name.

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(DigitalInterrupt)](<INSERT PARAM TYPE LINK>)
- [(bool)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### GPIOPinByName

GPIOPinByName returns a GPIOPin by name.

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(GPIOPin)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### AnalogReaderNames

AnalogReaderNames returns the names of all known analog readers.

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(string)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### DigitalInterruptNames

DigitalInterruptNames returns the names of all known digital interrupts.

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(string)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### Status

Status returns the current status of the board. Usually youshould use the CreateStatus helper instead of directly callingthis.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `commonpb`[(BoardStatus)](https://pkg.go.dev/go.viam.com/api/common/v1#commonpb):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### SetPowerMode

SetPowerMode sets the board to the given power mode. Ifprovided, the board will exit the given power mode afterthe specified duration.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `mode`[(PowerMode)](https://pkg.go.dev/go.viam.com/api/component/board/v1#mode):
- `time`[(Duration)](https://pkg.go.dev/time#time):

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### WriteAnalog

WriteAnalog writes an analog value to a pin on the board.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `pin`[(string)](<INSERT PARAM TYPE LINK>)
- `value`[(int32)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### StreamTicks

StreamTicks starts a stream of digital interrupt ticks.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(string)](<INSERT PARAM TYPE LINK>)
- `chan`[(Tick)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

### Value

Value returns the current value of the interrupt which isbased on the type of interrupt.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

### Tick

Tick is to be called either manually if the interrupt is a proxy to some realhardware interrupt or for tests.nanoseconds is from an arbitrary point in time, but always increasing and always needsto be accurate.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `high`[(bool)](<INSERT PARAM TYPE LINK>)
- `nanoseconds`[(uint64)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

### AddCallback

AddCallback adds a callback to be sent a low/high value to when a tickhappens.

**Parameters:**

- `chan`[(Tick)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

### RemoveCallback

RemoveCallback removes a listener for interrupts.

**Parameters:**

- `chan`[(Tick)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

### SetGPIO

Set sets the pin to either low or high.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `high`[(bool)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### GetGPIO

Get gets the high/low state of the pin.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### PWM

PWM gets the pin's given duty cycle.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### SetPWM

SetPWM sets the pin to the given duty cycle.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `dutyCyclePct`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### PWMFrequency

PWMFreq gets the PWM frequency of the pin.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### SetPWMFrequency

SetPWMFreq sets the given pin to the given PWM frequency. For Raspberry Pis,0 will use a default PWM frequency of 800.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `freqHz`[(uint)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

### Reconfigure



**Parameters:**

- `cfg`[(DigitalInterruptConfig)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#ReconfigurableDigitalInterrupt).

### GetImages

Images is used for getting simultaneous images from different imagers,along with associated metadata (just timestamp for now). It's not for getting a time series of images from the same imager.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- [(NamedImage)](<INSERT PARAM TYPE LINK>)
- `resource`[(ResponseMetadata)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/resource#resource):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

### GetPointCloud

NextPointCloud returns the next immediately available point cloud, not necessarily onea part of a sequence. In the future, there could be streaming of point clouds.Properties returns properties that are intrinsic to the particularimplementation of a camera

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- `pointcloud`[(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/pointcloud#pointcloud):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

### GetImage

{{% alert title="Info" color="info" %}}

Unlike most Viam [component APIs](/build/program/apis/#component-apis), the methods of the Go camera client do not map exactly to the names of the other SDK's camera methods.
To get an image in the Go SDK, you first need to construct a `Stream` and then you can get the next image from that stream.

{{% /alert %}}
Stream returns a stream that makes a best effort to return consecutive imagesthat may have a MIME type hint dictated in the context via gostream.WithMIMETypeHint.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `gostream`[(ErrorHandler)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/gostream#gostream):

**Returns:**

- `gostream`[(VideoStream)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/gostream#gostream):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

### GetProperties



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- [(Properties)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

### Close



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

### GetPosition

Position returns the current position in terms of ticks or degrees, and whether it is a relative or absolute position.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `positionType`[(PositionType)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(PositionType)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

### ResetPosition

ResetPosition sets the current position of the motor to be its new zero position.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

### GetProperties

Properties returns a list of all the position types that are supported by a given encoder

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

### GetPosition

Position returns the position in meters

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

### MoveToPosition

MoveToPosition is in metersThis will block until done or a new operation cancels this one

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(positionsMm)](<INSERT PARAM TYPE LINK>)
- [(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

### GetLengths

Lengths is the length of gantries in meters

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

### Home

Home runs the homing sequence of the gantry and returns true once completed

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

### Open

Open opens the gripper.This will block until done or a new operation cancels this one

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

### Grab

Grab makes the gripper grab.returns true if we grabbed something.This will block until done or a new operation cancels this one

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

### GetControls

Controls returns a list of Controls provided by the Controller

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Control)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

### GetEvents

Events returns most recent Event for each input (which should be the current state)

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `Control`[(Event)](https://pkg.go.dev#Control#Control):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

### RegisterControlCallback

RegisterCallback registers a callback that will fire on given EventTypes for a given Control.The callback is called on the same goroutine as the firer and if any long operation is to occur,the callback should start a goroutine.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `control`[(Control)](<INSERT PARAM TYPE LINK>)
- [(EventType)](<INSERT PARAM TYPE LINK>)
- `ctrlFunc`[(ControlFunction)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Controller).

### TriggerEvent

TriggerEvent allows directly sending an Event (such as a button press) from external code

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `event`[(Event)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Triggerable).

### SetPower

SetPower sets the percentage of power the motor should employ between -1 and 1.Negative power implies a backward directional rotational

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `powerPct`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### GoFor

GoFor instructs the motor to go in a specific direction for a specific amount ofrevolutions at a given speed in revolutions per minute. Both the RPM and the revolutionscan be assigned negative values to move in a backwards direction. Note: if both arenegative the motor will spin in the forward direction.If revolutions is 0, this will run the motor at rpm indefinitelyIf revolutions != 0, this will block until the number of revolutions has been completed or another operation comes in.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(rpm)](<INSERT PARAM TYPE LINK>)
- `revolutions`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### GoTo

GoTo instructs the motor to go to a specific position (provided in revolutions from home/zero),at a specific speed. Regardless of the directionality of the RPM this function will move the motortowards the specified target/positionThis will block until the position has been reached

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(rpm)](<INSERT PARAM TYPE LINK>)
- `positionRevolutions`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### ResetZeroPosition

Set the current position (+/- offset) to be the new zero (home) position.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `offset`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### GetPosition

Position reports the position of the motor based on its encoder. If it's not supported, the returneddata is undefined. The unit returned is the number of revolutions which is intended to be fedback into calls of GoFor.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### GetProperties

Properties returns whether or not the motor supports certain optional properties.

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### IsPowered

IsPowered returns whether or not the motor is currently on, and the percent power (between 0and 1, if the motor is off then the percent power will be 0).

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](<INSERT PARAM TYPE LINK>)
- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

### GetPosition

(lat, long), altitude (m)

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `geo`[(Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#geo):
- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetLinearVelocity

m / sec

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `r3`[(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#r3):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetAngularVelocity

deg / sec

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `spatialmath`[(AngularVelocity)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetLinearAcceleration



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `r3`[(Vector)](https://pkg.go.dev/github.com/golang/geo/r3#r3):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetCompassHeading

[0-&gt;360)

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetOrientation



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `spatialmath`[(Orientation)](https://pkg.go.dev/go.viam.com/rdk@v0.25.0/spatialmath#spatialmath):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetProperties



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetAccuracy



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Accuracy)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

### GetVoltage



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

### GetCurrent



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(bool)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

### GetPower



**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

