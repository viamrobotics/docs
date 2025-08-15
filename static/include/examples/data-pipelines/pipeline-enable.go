// :snippet-start: pipeline-enable
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
	apiKey = os.Getenv("VIAM_API_KEY_DATA_REGIONS")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID_DATA_REGIONS")
	orgID := "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
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

	// :remove-start:
	pipelinesToDelete, err := dataClient.ListDataPipelines(ctx, orgID)
	if err != nil {
		logger.Fatal(err)
	}
	for _, pipeline := range pipelinesToDelete {
		err = dataClient.DeleteDataPipeline(ctx, pipeline.ID)
		if err != nil {
			logger.Fatal(err)
		}
		fmt.Printf("Deleted pipeline: %s\n", pipeline.ID)
	}
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

	pipelineId, err = dataClient.CreateDataPipeline(
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

	err = dataClient.DisableDataPipeline(ctx, pipelineId)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Pipeline disabled with ID: %s\n", pipelineId)

	// :remove-end:
	err = dataClient.EnableDataPipeline(ctx, pipelineId)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Pipeline enabled with ID: %s\n", pipelineId)
	// :remove-start:
	// Teardown - delete the pipeline
	err = dataClient.DeleteDataPipeline(ctx, pipelineId)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Printf("Pipeline deleted with ID: %s\n", pipelineId)
	// :remove-end:
}
// :snippet-end: