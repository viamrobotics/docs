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
	orgID := ""

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()
	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	dataClient := viamClient.DataClient()


	pipelines, err := dataClient.ListDataPipelines(ctx, orgID)
	if err != nil {
		logger.Fatal(err)
	}
	for _, pipeline := range pipelines {
		fmt.Printf("Pipeline: %s, ID: %s, schedule: %s, data_source_type: %s, enable_backfill: %t\n", pipeline.Name, pipeline.ID, pipeline.Schedule, pipeline.DataSourceType)
	}

}
