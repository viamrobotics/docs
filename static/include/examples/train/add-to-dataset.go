// :snippet-start: add-to-dataset
package main

import (
	"context"
	"fmt"
	// :remove-start:
	"os"
	"time"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	datasetID := ""
	binaryDataID := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	orgID := os.Getenv("TEST_ORG_ID")
	datasetName := "test-" + time.Now().Format("20060102150405")
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

	fmt.Println("Adding image to dataset...")
	err = dataClient.AddBinaryDataToDatasetByIDs(
		ctx,
		[]string{binaryDataID},
		datasetID,
	)
	if err != nil {
		fmt.Println("Error adding image to dataset.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Println("Image added to dataset successfully")
	// :remove-start:
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