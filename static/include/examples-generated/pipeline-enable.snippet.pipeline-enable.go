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
	pipelineId := ""

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()
	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	dataClient := viamClient.DataClient()

	err = dataClient.EnableDataPipeline(ctx, pipelineId)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Pipeline enabled with ID: %s\n", pipelineId)
}
