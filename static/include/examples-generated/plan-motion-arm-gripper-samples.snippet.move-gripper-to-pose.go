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
