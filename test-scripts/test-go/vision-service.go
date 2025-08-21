package main

import (
	"context"

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
	"go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/services/vision"
	"go.viam.com/rdk/vision/viscapture"
)

func main() {
	logger := logging.NewLogger("client")
	machine, err := client.New(
		context.Background(),
		// TODO: Replace with your machine address from the CONNECT tab.
		"MACHINE-ADDRESS",
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			"API-KEY-ID",
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: "API-KEY",
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	defer machine.Close(context.Background())

	myDetectorService, err := vision.FromRobot(machine, "my_detector")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get detections from the camera output
	detections, err := myDetectorService.DetectionsFromCamera(context.Background(), "cam", nil)
	if err != nil {
		logger.Fatalf("Could not get detections: %v", err)
	}
	if len(detections) > 0 {
		logger.Info(detections[0])
	}

	// Get the stream from a camera
	cam, err := camera.FromRobot(machine, "cam")
	if err != nil {
		logger.Error(err)
		return
	}
	camStream, err := cam.Stream(context.Background())

	// Get an image from the camera stream
	img, release, err := camStream.Next(context.Background())
	defer release()

	myDetectorService2, err := vision.FromRobot(machine, "my_detector")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the detections from the image
	detections2, err := myDetectorService2.Detections(context.Background(), img, nil)
	if err != nil {
		logger.Fatalf("Could not get detections: %v", err)
	}
	if len(detections2) > 0 {
		logger.Info(detections2[0])
	}

	myClassifierService, err := vision.FromRobot(machine, "my_classifier")
	if err != nil {
		logger.Error(err)
		return
	}

	// Get the 2 classifications with the highest confidence scores from the camera output
	classifications, err := myClassifierService.ClassificationsFromCamera(context.Background(), "cam", 2, nil)
	if err != nil {
		logger.Fatalf("Could not get classifications: %v", err)
	}
	if len(classifications) > 0 {
		logger.Info(classifications[0])
	}


	// Get the stream from a camera
	cam1, err := camera.FromRobot(machine, "cam")
	if err != nil {
		logger.Error(err)
		return
	}
	camStream1, err := cam1.Stream(context.Background())
	if err!=nil {
		logger.Error(err)
		return
	}

	// Get an image from the camera stream
	img1, release1, err := camStream1.Next(context.Background())
	defer release1()

	myClassifierService1, err := vision.FromRobot(machine, "my_classifier")
	if err != nil {
		logger.Error(err)
		return
	}
	// Get the 2 classifications with the highest confidence scores from the image
	classifications1, err := myClassifierService1.Classifications(context.Background(), img1, 2, nil)
	if err != nil {
		logger.Fatalf("Could not get classifications: %v", err)
	}
	if len(classifications1) > 0 {
		logger.Info(classifications1[0])
	}

    mySegmenterService, err := vision.FromRobot(machine, "my_segmenter")
    if err != nil {
      logger.Error(err)
      return
    }
	// Get the objects from the camera output
	objects, err := mySegmenterService.GetObjectPointClouds(context.Background(), "cam1", nil)
	if err != nil {
		logger.Fatalf("Could not get point clouds: %v", err)
	}
	if len(objects) > 0 {
		logger.Info(objects[0])
	}

	visService, err := vision.FromRobot(machine, "my_detector")
	if err != nil {
		logger.Error(err)
		return
	}

	// The data to capture and return from the camera
	captOpts := viscapture.CaptureOptions{
		ReturnImage: true,
		ReturnDetections: true,
	}
	// Get the captured data for a camera
	capture, err := visService.CaptureAllFromCamera(context.Background(), "cam", captOpts, nil)
	if err != nil {
		logger.Fatalf("Could not get capture data from vision service: %v", err)
	}
	image2 := capture.Image
	detections3 := capture.Detections
	classifications3 := capture.Classifications
	objects2 := capture.Objects

	logger.Info(capture)
	logger.Info(image2)
	logger.Info(detections3)
	logger.Info(classifications3)
	logger.Info(objects2)

}
