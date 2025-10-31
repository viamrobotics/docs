// :snippet-start: run-vision-service
package main

import (
	"context"
	"fmt"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
	"go.viam.com/rdk/components/camera"
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
	cam, err := camera.FromProvider(machine, cameraName)
	if err != nil {
		logger.Fatal(err)
	}

	images, _, err := cam.Images(ctx, nil, nil)
	if err != nil {
		logger.Fatal(err)
	}
	image := images[0]
	img, err := image.Image(ctx)
	if err != nil {
		logger.Fatal(err)
	}

	// Get classifications using the image
	classifier, err := vision.FromProvider(machine, classifierName)
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