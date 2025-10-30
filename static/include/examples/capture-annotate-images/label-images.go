// :snippet-start: label-images
package main

import (
	"context"
	"fmt"
	"image/jpeg"
	"bytes"
	// :remove-start:
	"os"
	// :remove-end:

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

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	detectorName = "detector-1"
	binaryDataID = "83da9642-3785-4db3-9d60-a3662a03bb04/cj53ft1jy1/fJFzEoxrv459YUxbH3gC9YNzgm8SfEjyLt70aNJbL1GxOovyU7gf69vQSCcMNNV5"
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

	dataClient := viamClient.DataClient()

	// :remove-start:
	// remove existing bounding boxes if present
	data1, err := dataClient.BinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}

	// Access the bounding boxes from the annotations
	if data1[0].Metadata.Annotations.Bboxes != nil {
		for _, bbox := range data1[0].Metadata.Annotations.Bboxes {
			err = dataClient.RemoveBoundingBoxFromImageByID(ctx, bbox.ID, binaryDataID)
			if err != nil {
				logger.Fatal(err)
			}
			fmt.Printf("Deleted bounding box: %s\n", bbox.ID)
		}
	}
	// :remove-end:

	detector, err := vision.FromProvider(machine, detectorName)
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

	// :remove-start:
	// Teardown - delete the labels
	data, err = dataClient.BinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}

	// Access the bounding boxes from the annotations
	if data[0].Metadata.Annotations.Bboxes != nil {
		for _, bbox := range data[0].Metadata.Annotations.Bboxes {
			err = dataClient.RemoveBoundingBoxFromImageByID(ctx, bbox.ID, binaryDataID)
			if err != nil {
				logger.Fatal(err)
			}
			fmt.Printf("Deleted bounding box: %s\n", bbox.ID)
		}
	}
	// :remove-end:
}
// :snippet-end: