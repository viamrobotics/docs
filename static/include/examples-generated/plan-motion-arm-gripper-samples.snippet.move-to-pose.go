// Generate a sample "start" pose to demonstrate motion
testStartPose := spatialmath.NewPose(
	r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
	&spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
)
testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)

moveReq := motion.MoveReq{
	ComponentName: myArmResourceName,
	Destination:   testStartPoseInFrame,
	WorldState:    worldState,
}
_, err = motionService.Move(context.Background(), moveReq)
if err != nil {
	logger.Fatal(err)
}
