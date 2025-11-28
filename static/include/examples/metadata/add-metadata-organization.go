// :snippet-start: add-metadata-organization
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
	locationID = os.Getenv("TEST_ORG_ID")
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
	appClient.UpdateOrganizationMetadata(ctx, orgID, map[string]interface{}{
		"TEST_API_KEY": "ABC123",
	})

	// :remove-start:
	metadata1, err := appClient.GetOrganizationMetadata(ctx, orgID)
	if err != nil {
		logger.Fatal(err)
	}

	// Print the current metadata
	if metadata1["TEST_API_KEY"] != "ABC123" {
		logger.Fatal("Metadata mismatch")
	}
	appClient.UpdateOrganizationMetadata(ctx, orgID, map[string]interface{}{})
	metadata2, err := appClient.GetOrganizationMetadata(ctx, orgID)
	if err != nil {
		logger.Fatal(err)
	}
	if len(metadata2) != 0 {
		logger.Fatal("Metadata mismatch")
	}
	// :remove-end:
}
// :snippet-end: