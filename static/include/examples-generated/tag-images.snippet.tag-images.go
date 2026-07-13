package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/components/camera"
	rdkdata "go.viam.com/rdk/data"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	classifierName := ""
	binaryDataID := ""


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

	dataClient := viamClient.DataClient()


	data, err := dataClient.BinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}
	binaryData := data[0]

	// Convert binary data to a named image
	img, err := camera.NamedImageFromBytes(binaryData.Binary, "camera", "image/jpeg", rdkdata.Annotations{})
	if err != nil {
		logger.Fatal(err)
	}

	// Get classifications using the image
	classifier, err := vision.FromProvider(machine, classifierName)
	if err != nil {
		logger.Fatal(err)
	}

	classifications, err := classifier.Classifications(ctx, &img, 2, nil)
	if err != nil {
		logger.Fatal(err)
	}

    if len(classifications) == 0 {
        logger.Fatal(err)
    } else {
        for _, classification := range classifications {
			err := dataClient.AddTagsToBinaryDataByIDs(ctx, []string{classification.Label()}, []string{binaryDataID})
			if err != nil {
				logger.Fatal(err)
			}
			fmt.Printf("Added tag to image: %s\n", classification.Label())
		}
	}

}
