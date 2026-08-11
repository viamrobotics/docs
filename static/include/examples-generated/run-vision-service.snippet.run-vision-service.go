package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
	"go.viam.com/rdk/components/camera"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	classifierName := ""
	cameraName := ""


	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	machine, err := client.New(
		context.Background(),
		machineAddress,
		logger,
		client.WithDialOptions(client.WithEntityCredentials(
			apiKeyID,
			client.Credentials{
				Type:    client.CredentialsTypeAPIKey,
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

	// Get classifications using the image
	classifier, err := vision.FromProvider(machine, classifierName)
	if err != nil {
		logger.Fatal(err)
	}

	classifications, err := classifier.Classifications(ctx, &image, 2, nil)
	if err != nil {
		logger.Fatal(err)
	}

	err = machine.Close(ctx)
	if err != nil {
		logger.Fatal(err)
	}
}
