// :snippet-start: capture-annotate-dataset
package main

import (
	"context"
	"fmt"
	"time"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/services/vision"
	"go.viam.com/rdk/components/camera"
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

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	datasetName := "test-" + time.Now().Format("20060102150405")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	orgID := os.Getenv("TEST_ORG_ID")
	cameraName = "camera-1"
	classifierName = "classifier-1"
	partID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
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

	dataClient := viamClient.DataClient()

	// :remove-start:
	fmt.Println("Creating dataset...")
	datasetID, err = dataClient.CreateDataset(ctx, datasetName, orgID)
	if err != nil {
		fmt.Println("Error creating dataset. It may already exist.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Created dataset: %s\n", datasetID)
	// :remove-end:

	// Upload image to Viam
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

	fmt.Printf("Uploaded image: %s\n", binaryDataID)

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

	// :remove-start:
	// Teardown - delete the tags
	tags := []string{}
	for _, classification := range classifications {
		tags = append(tags, classification.Label())
	}
	fmt.Printf("Tags: %s\n", tags)

	_, err = dataClient.RemoveTagsFromBinaryDataByIDs(ctx, tags, []string{binaryDataID})
	if err != nil {
		fmt.Println("Error deleting tags.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Deleted tags: %s\n", tags)

	// Teardown - delete the image
	_, err = dataClient.DeleteBinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		fmt.Println("Error deleting image.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Deleted image: %s\n", binaryDataID)

	// Teardown - delete the dataset
	err = dataClient.DeleteDataset(ctx, datasetID)
	if err != nil {
		fmt.Println("Error deleting dataset.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Deleted dataset: %s\n", datasetID)
	// :remove-end:
}
// :snippet-end: