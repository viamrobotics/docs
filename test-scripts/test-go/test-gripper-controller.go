package main

import (
	"context"
	"fmt"
	"slices"

	"go.viam.com/rdk/components/gantry"
	"go.viam.com/rdk/components/generic"
	"go.viam.com/rdk/components/gripper"
	"go.viam.com/rdk/components/input"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)

func main() {
	logger := logging.NewDebugLogger("client")
	machine, err := client.New(
		context.Background(),
		"<REMOTE-ADDRESS>",
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			"<API-KEY-ID>",
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: "<API-KEY>",
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	defer machine.Close(context.Background())
	logger.Info("Resources:")
	logger.Info(machine.ResourceNames())

	// gantry-1
	myGantry, err := gantry.FromProvider(machine, "gantry-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the current positions of the axes of the gantry in millimeters.
	position, err := myGantry.Position(context.Background(), nil)
	logger.Info("position")
	logger.Info(position)

	// Create a list of positions for the axes of the gantry to move to.
	// Assume in this example that the gantry is multi-axis, with 3 axes.
	examplePositions := []float64{1, 2, 3}

	exampleSpeeds := []float64{3, 9, 12}

	// Move the axes of the gantry to the positions specified.
	myGantry.MoveToPosition(context.Background(), examplePositions, exampleSpeeds, nil)

	// Get the lengths of the axes of the gantry in millimeters.
	lengths_mm, err := myGantry.Lengths(context.Background(), nil)
	logger.Info(lengths_mm)

	myGantry.Home(context.Background(), nil)

	// Stop all motion of the gantry. It is assumed that the gantry stops immediately.
	myGantry.Stop(context.Background(), nil)

	// Log if the gantry is currently moving.
	is_moving, err := myGantry.IsMoving(context.Background())
	logger.Info(is_moving)

	command := map[string]interface{}{"cmd": "test", "data1": 500}
	result, err := myGantry.DoCommand(context.Background(), command)
	logger.Info(result)

	// generic-1
	myGeneric, err := generic.FromProvider(machine, "generic-1")
	if err != nil {
		logger.Error(err)
		return
	}

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = myGeneric.DoCommand(context.Background(), command)
	logger.Info(result)

	// gripper-1
	myGripper, err := gripper.FromProvider(machine, "gripper-1")
	if err != nil {
		logger.Error(err)
		return
	}

	// Open the gripper.
	err = myGripper.Open(context.Background(), nil)

	// Grab with the gripper.
	grabbed, err := myGripper.Grab(context.Background(), nil)
	logger.Info(grabbed)

	// Stop all motion of the gripper. It is assumed that the gripper stops immediately.
	myGripper.Stop(context.Background(), nil)

	// Log if the arm is currently moving.
	is_moving, err = myGripper.IsMoving(context.Background())
	logger.Info(is_moving)

	geometries, err := myGripper.Geometries(context.Background(), nil)

	if len(geometries) > 0 {
		// Get the center of the first geometry
		elem := geometries[0]
		fmt.Println("Pose of the first geometry's center point:", elem.Pose())
	}

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = myGripper.DoCommand(context.Background(), command)
	logger.Info(result)

	err = myGripper.Close(context.Background())

	// input_controller-1
	myController, err := input.FromProvider(machine, "input_controller-2")
	if err != nil {
		logger.Error(err)
		return
	}
	inputController1ReturnValue, err := myController.Controls(context.Background(), map[string]interface{}{})
	logger.Infof("input_controller-1 Controls return value: %+v", inputController1ReturnValue)

	// Get the most recent Event for each Control.
	recent_events, err := myController.Events(context.Background(), nil)
	logger.Info(recent_events)

	// Define a function to handle pressing the Start Menu button, "ButtonStart", on your controller and logging the start time
	printStartTime := func(ctx context.Context, event input.Event) {
		logger.Info("Start Menu Button was pressed at this time: %v", event.Time)
	}

	// Define the EventType "ButtonPress" to serve as the trigger for printStartTime.
	triggers := []input.EventType{input.ButtonPress}

	// Get the controller's Controls.
	controls, err := myController.Controls(context.Background(), nil)

	// If the "ButtonStart" Control is found, trigger printStartTime when on "ButtonStart" the event "ButtonPress" occurs.
	if !slices.Contains(controls, input.ButtonStart) {
		logger.Error("button 'ButtonStart' not found; controller may be disconnected")
		return
	}
	myController.RegisterControlCallback(context.Background(), input.ButtonStart, triggers, printStartTime, nil)

	command = map[string]interface{}{"cmd": "test", "data1": 500}
	result, err = myController.DoCommand(context.Background(), command)
	logger.Info(result)

	err = myController.Close(context.Background())
}
