package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	datasetID := ""
	binaryDataID := ""

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()
	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	dataClient := viamClient.DataClient()


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
}
