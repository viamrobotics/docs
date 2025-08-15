// :snippet-start: pipeline-execution
package main

import (
	"context"
	"fmt"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	pipelineId := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	pipelineId = "16b8a3e5-7944-4e1c-8ccd-935c1ba3be59"
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

	pipelineRuns, err := dataClient.ListDataPipelineRuns(ctx, pipelineId, 10)
	if err != nil {
		logger.Fatal(err)
	}
	for _, run := range pipelineRuns.Runs {
		fmt.Printf("Run: ID: %s, status: %s, start_time: %s, end_time: %s, data_start_time: %s, data_end_time: %s\n", run.ID, run.Status, run.StartTime, run.EndTime, run.DataStartTime, run.DataEndTime)
	}

	// :remove-start:
	if len(pipelineRuns.Runs) != 10 {
		logger.Fatal("Expected 10 runs, got " + strconv.Itoa(len(pipelineRuns.Runs)))
	}
	// :remove-end:
}
// :snippet-end: