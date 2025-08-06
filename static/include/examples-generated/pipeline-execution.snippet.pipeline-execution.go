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

	pipelineRuns, err := dataClient.ListDataPipelineRuns(ctx, pipelineId, 10)
	if err != nil {
		logger.Fatal(err)
	}
	for _, run := range pipelineRuns.Runs {
		fmt.Printf("Run: ID: %s, status: %s, start_time: %s, end_time: %s, data_start_time: %s, data_end_time: %s\n", run.ID, run.Status, run.StartTime, run.EndTime, run.DataStartTime, run.DataEndTime)
	}

}
