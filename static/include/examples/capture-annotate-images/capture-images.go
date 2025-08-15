// :snippet-start: capture-images
package main

import (
	"context"
	"fmt"
	"time"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/utils"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	cameraName := ""
	partID := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	cameraName = "camera-1"
	partID = "824b6570-7b1d-4622-a19d-37c472dba467"
	// :remove-end:

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
	cam, err := camera.FromRobot(machine, cameraName)
	if err != nil {
		logger.Fatal(err)
	}

	image, _, err := cam.Image(ctx, utils.MimeTypeJPEG, nil)
	if err != nil {
		logger.Fatal(err)
	}

	// Upload image to Viam
	dataClient := viamClient.DataClient()

	binaryDataID, err := dataClient.BinaryDataCaptureUpload(
		ctx,
		image,
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

	// :remove-start:
	// Teardown - delete the image
	_, err = dataClient.DeleteBinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		fmt.Println("Error deleting image.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Deleted image: %s\n", binaryDataID)
	// :remove-end:
}
// :snippet-end: