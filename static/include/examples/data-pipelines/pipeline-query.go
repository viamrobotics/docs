// :snippet-start: pipeline-query
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
	orgID := ""
	pipelineId := ""
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	orgID = os.Getenv("TEST_ORG_ID")
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

	// Create MQL stages as map slices
	mqlStages := []map[string]interface{}{
		{"$match": map[string]interface{}{"location": map[string]interface{}{"$exists": true}}},
		{"$limit": 10},
	}

	tabularData, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, &app.TabularDataByMQLOptions{
		TabularDataSourceType: app.TabularDataSourceTypePipelineSink,
		PipelineID: pipelineId,
	})
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularData)
}
// :snippet-end: