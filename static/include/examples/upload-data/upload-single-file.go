// :snippet-start: upload-single-file
package main

import (
	"context"
	"os"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

// Configuration constants – replace with your actual values
var (
	API_KEY     = "" // API key, find or create in your organization settings
	API_KEY_ID  = "" // API key ID, find or create in your organization settings
	ORG_ID      = "" // Organization ID, find or create in your organization settings
	PART_ID     = "" // Part ID of machine part that should be associated with the data
	FILE_PATH   = "file.txt" // Path to the file to upload
)

func main() {
	// :remove-start:
	ORG_ID = os.Getenv("TEST_ORG_ID")
	API_KEY = os.Getenv("VIAM_API_KEY")
	API_KEY_ID = os.Getenv("VIAM_API_KEY_ID")
	PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
	FILE_PATH = "empty.txt"
	// :remove-end:
    logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, API_KEY, API_KEY_ID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	dataClient := viamClient.DataClient()

	binaryDataID, err := dataClient.FileUploadFromPath(
		ctx,
		PART_ID,
		FILE_PATH,
		&app.FileUploadOptions{
			Tags: []string{"uploaded"},
		},
	)
	if err != nil {
		logger.Fatal(err)
	}
	// :remove-start:
	if binaryDataID == "" {
		logger.Fatal("Binary data ID is empty")
	}
	numDeleted, err := dataClient.DeleteBinaryDataByIDs(ctx, []string{binaryDataID})
	if err != nil {
		logger.Fatal(err)
	}
	if numDeleted != 1 {
		logger.Fatal("Failed to delete binary data")
	}
	// :remove-end:
}
// :snippet-end: