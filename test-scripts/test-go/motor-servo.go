package main

import (
	"context"

	"go.viam.com/rdk/components/movementsensor"
	"go.viam.com/rdk/components/powersensor"

	"go.viam.com/rdk/components/sensor"
	"go.viam.com/rdk/components/servo"

	"go.viam.com/rdk/components/motor"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)

func main() {
	logger := logging.NewDebugLogger("client")
	machine, err := client.New(
		context.Background(),
		"",
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			"",
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: "",
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	defer machine.Close(context.Background())
	logger.Info("Resources:")
	logger.Info(machine.ResourceNames())

	// motor-1
	motor1, err := motor.FromProvider(machine, "motor-1")
	if err != nil {
		logger.Error(err)
		return
	}
	motor1ReturnValue, err := motor1.IsMoving(context.Background())
	if err != nil {
		logger.Error(err)
		return
	}
	logger.Infof("motor-1 IsMoving return value: %+v", motor1ReturnValue)

	// Set the motor power to 40% forwards.
	motor1.SetPower(context.Background(), 0.4, nil)

	// Set the motor's RPM to 50
	motor1.SetRPM(context.Background(), 50, nil)

	motor1.GoFor(context.Background(), 60, 7.2, nil)

	// Turn the motor to 8.3 revolutions from home at 75 RPM.
	motor1.GoTo(context.Background(), 75, 8.3, nil)

	// Set the current position as the new home position with no offset.
	motor1.ResetZeroPosition(context.Background(), 0.0, nil)

	// Get the current position of an encoded motor.
	position, err := motor1.Position(context.Background(), nil)

	// Log the position
	logger.Info("Position:")
	logger.Info(position)

	// Return whether or not the motor supports certain optional features.
	properties, err := motor1.Properties(context.Background(), nil)

	// Log the properties.
	logger.Info("Properties:")
	logger.Info(properties)

	// Check whether the motor is currently running.
	powered, pct, err := motor1.IsPowered(context.Background(), nil)

	logger.Info("Is powered?")
	logger.Info(powered)
	logger.Info("Power percent:")
	logger.Info(pct)

	// Stop all motion of the arm. It is assumed that the arm stops immediately.
	motor1.Stop(context.Background(), nil)

	// Log if the arm is currently moving.
	is_moving, err := motor1.IsMoving(context.Background())
	logger.Info(is_moving)

	// BUG: unimplemented
	command := map[string]interface{}{"cmd": "test", "data1": 500}
	result, err := motor1.DoCommand(context.Background(), command)
	logger.Info(result)

	err = motor1.Close(context.Background())

	// movement_sensor-1
	movementSensor1, err := movementsensor.FromProvider(machine, "movement_sensor-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the current linear velocity of the movement sensor.
	linVel, err := movementSensor1.LinearVelocity(context.Background(), nil)
	logger.Info(linVel)

	// Get the current angular velocity of the movement sensor.
	angVel, err := movementSensor1.AngularVelocity(context.Background(), nil)

	// Get the y component of angular velocity.
	yAngVel := angVel.Y
	logger.Info(yAngVel)

	// Get the current compass heading of the movement sensor.
	heading, err := movementSensor1.CompassHeading(context.Background(), nil)
	logger.Info(heading)

	// Get the current orientation of the movement sensor.
	sensorOrientation, err := movementSensor1.Orientation(context.Background(), nil)

	// Get the orientation vector.
	orientation := sensorOrientation.OrientationVectorDegrees()

	// Print out the orientation vector.
	logger.Info("The x component of the orientation vector: ", orientation.OX)
	logger.Info("The y component of the orientation vector: ", orientation.OY)
	logger.Info("The z component of the orientation vector: ", orientation.OZ)
	logger.Info("The number of degrees that the movement sensor is rotated about the vector: ", orientation.Theta)

	// Get the current position of the movement sensor above sea level in meters.
	position, altitude, err := movementSensor1.Position(context.Background(), nil)
	logger.Info(position)
	logger.Info(altitude)

	// Get the supported properties of the movement sensor.
	properties, err = movementSensor1.Properties(context.Background(), nil)
	logger.Info(properties)

	// Get the accuracy of the movement sensor.
	accuracy, err := movementSensor1.Accuracy(context.Background(), nil)
	logger.Info(accuracy.NmeaFix)

	// Get the current linear acceleration of the movement sensor.
	linAcc, err := movementSensor1.LinearAcceleration(context.Background(), nil)
	logger.Info(linAcc)

	// Get the readings provided by the sensor.
	readings, err := movementSensor1.Readings(context.Background(), nil)
	logger.Info(readings)

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = movementSensor1.DoCommand(context.Background(), command)
	print(result)

	err = movementSensor1.Close(context.Background())

	// power_sensor-1
	myPowerSensor, err := powersensor.FromProvider(machine, "power_sensor-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the voltage from device in volts.
	voltage, isAC, err := myPowerSensor.Voltage(context.Background(), nil)
	logger.Info(voltage)
	logger.Info(isAC)

	// Get the current reading from device in amps.
	current, isAC, err := myPowerSensor.Current(context.Background(), nil)
	logger.Info(current)
	logger.Info(isAC)

	// Get the power measurement from device in watts.
	power, err := myPowerSensor.Power(context.Background(), nil)
	logger.Info(power)

	// Get the readings provided by the sensor.
	readings, err = myPowerSensor.Readings(context.Background(), nil)
	logger.Info(readings)

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = myPowerSensor.DoCommand(context.Background(), command)
	logger.Info(result)

	err = myPowerSensor.Close(context.Background())

	// sensor-1
	mySensor, err := sensor.FromProvider(machine, "sensor-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the readings provided by the sensor.
	readings, err = mySensor.Readings(context.Background(), nil)
	logger.Info(readings)

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = mySensor.DoCommand(context.Background(), command)
	logger.Info(result)

	err = mySensor.Close(context.Background())

	// servo-1
	myServoComponent, err := servo.FromProvider(machine, "servo-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Move the servo from its origin to the desired angle of 30 degrees.
	myServoComponent.Move(context.Background(), 30, nil)

	// Get the current set angle of the servo.
	pos1, err := myServoComponent.Position(context.Background(), nil)

	// Move the servo from its origin to the desired angle of 20 degrees.
	myServoComponent.Move(context.Background(), 20, nil)

	// Get the current set angle of the servo.
	pos2, err := myServoComponent.Position(context.Background(), nil)

	logger.Info("Position 1: ", pos1)
	logger.Info("Position 2: ", pos2)

	// Stop all motion of the arm. It is assumed that the arm stops immediately.
	myServoComponent.Stop(context.Background(), nil)

	// Log if the arm is currently moving.
	is_moving, err = myServoComponent.IsMoving(context.Background())
	logger.Info(is_moving)

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = myServoComponent.DoCommand(context.Background(), command)
	logger.Info(result)

	err = myServoComponent.Close(context.Background())
}
