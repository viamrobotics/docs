package main

import (
  "context"
  "fmt"
  // :remove-start:
  "os"
  // :remove-end:

  "github.com/golang/geo/r3"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/robot/client"
  // :snippet-start: plan-motion-include
  "go.viam.com/rdk/services/motion"
  // :snippet-end:
  "go.viam.com/rdk/spatialmath"
  "go.viam.com/utils/rpc"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	armName := ""
	gripperName := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	armName = "arm-1"
	gripperName = "gripper-1"
	// :remove-end:

	logger := logging.NewLogger("client")
	machine, err := client.New(
		context.Background(),
		machineAddress,
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			apiKeyID,
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: apiKey,
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	// Access myArm
	myArmComponent, err := arm.FromRobot(machine, armName)
	if err != nil {
		fmt.Println(err)
	}

	// End Position of myArm
	myArmEndPosition, err := myArmComponent.EndPosition(context.Background(), nil)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("myArm EndPosition position value:", myArmEndPosition.Point())
	fmt.Println("myArm EndPosition orientation value:", myArmEndPosition.Orientation())

	// Joint Positions of myArm
	myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("myArm JointPositions return value:", myArmJointPositions)

	// :remove-start:
	cmdJointPositionsZero := []referenceframe.Input{
		{Value: 0.0},
		{Value: 0.0},
		{Value: 0.0},
		{Value: 0.0},
		{Value: 0.0},
		{Value: 0.0},
	}
	err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositionsZero, nil)
	if err != nil {
		fmt.Println(err)
	}
	// :remove-end:
	// Command a joint position move: move the forearm of the arm slightly up
	cmdJointPositions := []referenceframe.Input{
		{Value: 0.0},
		{Value: 0.0},
		{Value: -3.0},
		{Value: 0.0},
		{Value: 0.0},
		{Value: 0.0},
	}
	err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositions, nil)
	if err != nil {
		fmt.Println(err)
	}

	// Generate a simple pose move +100mm in the +Z direction of the arm
	currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
	if err != nil {
		fmt.Println("Error getting end position of myArm:", err)
		fmt.Println(err)
	}
	fmt.Println("Moving to end position +100mm")
	adjustedArmPoint := currentArmPose.Point()
	adjustedArmPoint.Z += 100.0
	cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

	err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, nil)
	if err != nil {
		fmt.Println(err)
	}

	// Access the motion service
	// :snippet-start: motion-service-from-robot
	motionService, err := motion.FromRobot(machine, "builtin")
	if err != nil {
		logger.Fatal(err)
	}
	// :snippet-end:

	// :snippet-start: get-pose
	// Get the pose of myArm from the motion service
	myArmMotionPose, err := motionService.GetPose(context.Background(), armName, referenceframe.World, nil, nil)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Position of myArm from the motion service:", myArmMotionPose.Pose().Point())
	fmt.Println("Orientation of myArm from the motion service:", myArmMotionPose.Pose().Orientation())
	// :snippet-end:

	// :snippet-start: world-state-from-robot
	// Add a table obstacle to a WorldState
	obstacles := make([]spatialmath.Geometry, 0)

	tableOrigin := spatialmath.NewPose(
		r3.Vector{X: -202.5, Y: -546.5, Z: -19.0},
		&spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
	)
	tableDims := r3.Vector{X: 635.0, Y: 1271.0, Z: 38.0}
	tableObj, err := spatialmath.NewBox(tableOrigin, tableDims, "table")
	obstacles = append(obstacles, tableObj)

	// Create a WorldState that has the GeometriesInFrame included
	obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
	worldState, err := referenceframe.NewWorldState([]*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)
	if err != nil {
		logger.Fatal(err)
	}
	// :snippet-end:

	// :snippet-start: move-to-pose
	// Generate a sample "start" pose to demonstrate motion
	testStartPose := spatialmath.NewPose(
		r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
		&spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
	)
	testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)

	moveReq := motion.MoveReq{
		ComponentName: armName,
		Destination:   testStartPoseInFrame,
		WorldState:    worldState,
	}
	_, err = motionService.Move(context.Background(), moveReq)
	if err != nil {
		logger.Fatal(err)
	}
	// :snippet-end:

	// :snippet-start: move-gripper-to-pose
	// This will move the gripper in the -Z direction with respect to its own reference frame
	gripperPoseRev := spatialmath.NewPose(
		r3.Vector{X: 0.0, Y: 0.0, Z: -50.0},
		&spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
	)
	gripperPoseRevInFrame := referenceframe.NewPoseInFrame(gripperName, gripperPoseRev) // Note the change in frame name

	gripperMoveReq := motion.MoveReq{
		ComponentName: gripperName,
		Destination:   gripperPoseRevInFrame,
		WorldState:    worldState,
	}
	_, err = motionService.Move(context.Background(), gripperMoveReq)
	if err != nil {
		logger.Fatal(err)
	}
	// :snippet-end:
}
