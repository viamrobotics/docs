// :snippet-start: add-machine-images-to-dataset
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


func fetchBinaryDataIDs(
	ctx context.Context,
	dataClient *app.DataClient,
	partID string,
	maxMatches int) ([]string, error) {
	filter := &app.Filter{
		PartID: partID,
		Interval: app.CaptureInterval{
			Start: time.Now().Add(-200 * time.Hour),
			End: time.Now(),
		},
	}

	var allMatches []string
	last := ""

	fmt.Println("Getting data for part...")

	for len(allMatches) < maxMatches {
		fmt.Println("Fetching more data...")

		resp, err := dataClient.BinaryDataByFilter(
			ctx, false, &app.DataByFilterOptions{
				Filter:            filter,
				Limit:             5,
				Last:              last,
				IncludeInternalData: false,
			},
		)
		if err != nil {
			return nil, fmt.Errorf("failed to fetch binary data: %w", err)
		}
		if len(resp.BinaryData) == 0 {
			break
		}
		for _, data := range resp.BinaryData {
			allMatches = append(allMatches, data.Metadata.BinaryDataID)
		}
		last = resp.Last
	}

	fmt.Println("All matches:")
	fmt.Println(allMatches)

	return allMatches, nil
}

func main() {
	apiKey := ""
	apiKeyID := ""
	partID := ""
	datasetID := ""
	maxMatches := 50
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	orgID := os.Getenv("TEST_ORG_ID")
	datasetName := "test-" + time.Now().Format("20060102150405")
	partID = "824b6570-7b1d-4622-a19d-37c472dba467"
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

	fmt.Println("Fetching machine images...")
	binaryDataIDs, err := fetchBinaryDataIDs(ctx, dataClient, partID, maxMatches)
	if err != nil {
		fmt.Println("Error fetching machine images.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Printf("Fetched %d machine images.\n", len(binaryDataIDs))

	fmt.Println("Adding machine images to dataset...")
	err = dataClient.AddBinaryDataToDatasetByIDs(
		ctx,
		binaryDataIDs,
		datasetID,
	)
	if err != nil {
		fmt.Println("Error adding machine images to dataset.")
		fmt.Printf("Exception: %v\n", err)
		return
	}
	fmt.Println("Machine images added to dataset successfully")
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