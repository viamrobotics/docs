package main

import (
	"context"
	"fmt"
	"time"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	cameraName := ""
	partID := ""


	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

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

	// Capture image from camera
	cam, err := camera.FromProvider(machine, cameraName)
	if err != nil {
		logger.Fatal(err)
	}

	images, _, err := cam.Images(ctx, nil, nil)
	if err != nil {
		logger.Fatal(err)
	}
	image := images[0]
	imageData, err := image.Bytes(ctx)
	if err != nil {
		logger.Fatal(err)
	}

	// Upload image to Viam
	dataClient := viamClient.DataClient()

	binaryDataID, err := dataClient.BinaryDataCaptureUpload(
		ctx,
		imageData,
		partID,
		"camera",
		cameraName,
		"GetImage",
		".jpg",
		&app.BinaryDataCaptureUploadOptions{
			DataRequestTimes: &[2]time.Time{time.Now(), time.Now()},
		},
	)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Uploaded image: %s\n", binaryDataID)

}
