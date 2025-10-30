package main

import (
	"context"
	"fmt"
	"time"
	"image/jpeg"
	"bytes"

	"go.viam.com/rdk/app"
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
	datasetID := ""
	machineAddress := ""
	classifierName := ""
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

	image, _, err := cam.Image(ctx, utils.MimeTypeJPEG, nil)
	if err != nil {
		logger.Fatal(err)
	}

	dataClient := viamClient.DataClient()


	// Upload image to Viam
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

	fmt.Printf("Uploaded image: %s\n", binaryDataID)

	// Convert binary data to image.Image
	img, err := jpeg.Decode(bytes.NewReader(image))
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

	// Add image to dataset
	err = dataClient.AddBinaryDataToDatasetByIDs(ctx, []string{binaryDataID}, datasetID)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Added image to dataset: %s\n", binaryDataID)

}
