// :snippet-start: tag-images
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
	classifierName := ""
	binaryDataID := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	classifierName = "classifier-1"
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
	if data1[0].Metadata.CaptureMetadata.Tags != nil {
		for _, tag := range data1[0].Metadata.CaptureMetadata.Tags {
			_, err = dataClient.RemoveTagsFromBinaryDataByIDs(ctx, []string{tag}, []string{binaryDataID})
			if err != nil {
				logger.Fatal(err)
			}
			fmt.Printf("Deleted tag: %s\n", tag)
		}
	}
	// :remove-end:

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

	// :remove-start:
	// Teardown - delete the labels
	data, err = dataClient.BinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}

	// Access the bounding boxes from the annotations
	// TODO: Uncomment this when deleting tags works again
	// if data[0].Metadata.CaptureMetadata.Tags != nil {
	// 	for _, tag := range data[0].Metadata.CaptureMetadata.Tags {
	// 		_, err = dataClient.RemoveTagsFromBinaryDataByIDs(ctx, []string{tag}, []string{binaryDataID})
	// 		if err != nil {
	// 			logger.Fatal(err)
	// 		}
	// 		fmt.Printf("Deleted tag: %s\n", tag)
	// 	}
	// } else {
	// 	logger.Fatal("No tags found on image")
	// }
	// :remove-end:
}
// :snippet-end: