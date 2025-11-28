// :snippet-start: add-metadata-location
package main

import (
	"context"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	locationID := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	locationID = "pg5q3j3h95"
	// :remove-end:

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	appClient := viamClient.AppClient()
	appClient.UpdateLocationMetadata(ctx, locationID, map[string]interface{}{
		"TEST_API_KEY": "ABC123",
	})

	// :remove-start:
	metadata1, err := appClient.GetLocationMetadata(ctx, locationID)
	if err != nil {
		logger.Fatal(err)
	}

	// Print the current metadata
	if metadata1["TEST_API_KEY"] != "ABC123" {
		logger.Fatal("Metadata mismatch")
	}
	appClient.UpdateLocationMetadata(ctx, locationID, map[string]interface{}{})
	metadata2, err := appClient.GetLocationMetadata(ctx, locationID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(metadata2) != 0 {
		logger.Fatal("Metadata mismatch")
	}
	// :remove-end:
}
// :snippet-end: