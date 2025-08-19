// Get the pose of myArm from the motion service
myArmMotionPose, err := motionService.GetPose(context.Background(), myArmResourceName, referenceframe.World, nil, nil)
if err != nil {
	fmt.Println(err)
}
fmt.Println("Position of myArm from the motion service:", myArmMotionPose.Pose().Point())
fmt.Println("Orientation of myArm from the motion service:", myArmMotionPose.Pose().Orientation())
