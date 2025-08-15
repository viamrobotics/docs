// :snippet-start: create-dataset
package main

import (
	"context"
	"fmt"
	"os"
	// :remove-start:
	"time"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	orgID := ""
	datasetName := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	orgID = os.Getenv("TEST_ORG_ID")
	datasetName = "test-" + time.Now().Format("20060102150405")
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

	fmt.Println("Creating dataset...")
	datasetID, err := dataClient.CreateDataset(ctx, datasetName, orgID)
	if err != nil {
		fmt.Println("Error creating dataset. It may already exist.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Created dataset: %s\n", datasetID)

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