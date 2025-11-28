package main

import (
	"context"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	locationID := ""


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

}
