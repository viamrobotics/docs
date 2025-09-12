// :snippet-start: run-vision-service
package main

import (
	"context"
	"fmt"
	"image/jpeg"
	"bytes"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/utils"
	"go.viam.com/utils/rpc"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	classifierName := ""
	cameraName := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	cameraName = "camera-1"
	classifierName = "classifier-1"
	// :remove-end:

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

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

	imageData, _, err := cam.Image(ctx, utils.MimeTypeJPEG, nil)
	if err != nil {
		logger.Fatal(err)
	}

	// Convert binary data to image.Image
	img, err := jpeg.Decode(bytes.NewReader(imageData))
	if err != nil {
		logger.Fatal(err)
	}

	// Get classifications using the image
	classifier, err := vision.FromRobot(machine, classifierName)
	if err != nil {
		logger.Fatal(err)
	}

	classifications, err := classifier.Classifications(ctx, img, 2, nil)
	if err != nil {
		logger.Fatal(err)
	}

	// :remove-start:
	if len(classifications) == 0 {
		fmt.Println("No tags found")
		return
	} else {
		for _, classification := range classifications {
			fmt.Printf("Found tag: %s\n", classification.Label())
		}
	}
	// :remove-end:
	err = machine.Close(ctx)
	if err != nil {
		logger.Fatal(err)
	}
}
// :snippet-end: