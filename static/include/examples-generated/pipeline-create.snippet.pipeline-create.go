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


	// Create MQL stages as map slices
	mqlStages := []map[string]interface{}{
		{"$match": map[string]interface{}{"component_name": "temperature-sensor"}},
		{
			"$group": map[string]interface{}{
				"_id": "$location_id",
				"avg_temp": map[string]interface{}{"$avg": "$data.readings.temperature"},
				"count": map[string]interface{}{"$sum": 1},
			},
		},
		{
			"$project": map[string]interface{}{
				"location": "$_id",
				"avg_temp": 1,
				"count": 1,
				"_id": 0,
			},
		},
	}

	pipelineId, err := dataClient.CreateDataPipeline(
		ctx,
		orgID,
		"test-pipeline",
		mqlStages,
		"0 * * * *",
		false,
		&app.CreateDataPipelineOptions{
			TabularDataSourceType: 0,
		},
	)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Pipeline created with ID: %s\n", pipelineId)
}
