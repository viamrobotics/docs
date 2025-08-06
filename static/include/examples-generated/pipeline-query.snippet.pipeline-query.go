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

	// Create MQL stages as map slices
	mqlStages := []map[string]interface{}{
		{"$match": map[string]interface{}{"component_name": "sensor-1"}},
		{
			"$group": map[string]interface{}{
				"_id": "$location_id",
				"avg_val": map[string]interface{}{"$avg": "$data.readings.a"},
				"count": map[string]interface{}{"$sum": 1},
			},
		},
		{
			"$project": map[string]interface{}{
				"location": "$_id",
				"avg_val": 1,
				"count": 1,
			},
		},
	}

	tabularData, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, &app.TabularDataByMQLOptions{
		TabularDataSourceType: 3,
		PipelineID: pipelineId,
	})
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularData)
}
