package main

import (
	"context"
	"fmt"
	"image/jpeg"
	"bytes"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	detectorName := ""
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

	dataClient := viamClient.DataClient()


	detector, err := vision.FromRobot(machine, detectorName)
	if err != nil {
		logger.Fatal(err)
	}

	data, err := dataClient.BinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}
	binaryData := data[0]

	// Convert binary data to image.Image
	img, err := jpeg.Decode(bytes.NewReader(binaryData.Binary))
	if err != nil {
		logger.Fatal(err)
	}

	// Get detections using the image
	detections, err := detector.Detections(ctx, img, nil)
	if err != nil {
		logger.Fatal(err)
	}

    if len(detections) == 0 {
        logger.Fatal(err)
    } else {
        for _, detection := range detections {
            // Ensure bounding box is big enough to be useful
			if float64(detection.NormalizedBoundingBox()[2]-detection.NormalizedBoundingBox()[0]) <= 0.01 ||
				float64(detection.NormalizedBoundingBox()[3]-detection.NormalizedBoundingBox()[1]) <= 0.01 {
				continue
			}
			bboxID, err := dataClient.AddBoundingBoxToImageByID(
				ctx,
				binaryDataID,
				detection.Label(),
				float64(detection.NormalizedBoundingBox()[0]),
				float64(detection.NormalizedBoundingBox()[1]),
				float64(detection.NormalizedBoundingBox()[2]),
				float64(detection.NormalizedBoundingBox()[3]),
			)
			if err != nil {
				logger.Fatal(err)
			}
			fmt.Printf("Added bounding box to image: %s\n", bboxID)
		}
	}

}
