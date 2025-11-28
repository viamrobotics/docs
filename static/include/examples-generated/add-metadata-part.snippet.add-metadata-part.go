package main

import (
	"context"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/utils/rpc"
)


func main() {
	apiKey := ""
	apiKeyID := ""
	partID := ""


	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	appClient := viamClient.AppClient()

	appClient := viamClient.AppClient()
	appClient.UpdateRobotPartMetadata(ctx, partID, map[string]interface{}{
		"TEST_API_KEY": "ABC123",
	})

}
