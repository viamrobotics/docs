// :snippet-start: add-metadata-part
package main

import (
	"context"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	partID := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
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

	appClient := viamClient.AppClient()

	appClient.UpdateRobotPartMetadata(ctx, partID, map[string]interface{}{
		"TEST_API_KEY": "ABC123",
	})

	// :remove-start:
	metadata1, err := appClient.GetRobotPartMetadata(ctx, partID)
	if err != nil {
		logger.Fatal(err)
	}

	// Print the current metadata
	if metadata1["TEST_API_KEY"] != "ABC123" {
		logger.Fatal("Metadata mismatch")
	}
	appClient.UpdateRobotPartMetadata(ctx, partID, map[string]interface{}{})
	metadata2, err := appClient.GetRobotPartMetadata(ctx, partID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(metadata2) != 0 {
		logger.Fatal("Metadata mismatch")
	}
	// :remove-end:
}
// :snippet-end: