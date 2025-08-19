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
	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	orgID = os.Getenv("TEST_ORG_ID")
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

	// :snippet-start: data-query-filter
	// Create MQL stages as map slices
	mqlStages := []map[string]interface{}{
		{"$match": map[string]interface{}{"component_name": "sensor-1"}},
		{"$limit": 2},
		{"$project": map[string]interface{}{
			"time_received": 1,
			"data": 1,
			"tags": 1,
		}},
	}

	tabularDataMQL, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataMQL)

	tabularDataSQL, err := dataClient.TabularDataBySQL(ctx, orgID,
		"SELECT time_received, data, tags FROM readings " +
		"WHERE component_name = 'sensor-1' LIMIT 2")
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataSQL)
	// :snippet-end:

	// :snippet-start: data-query-count
	mqlStages = []map[string]interface{}{
		{"$match": map[string]interface{}{"component_name": "sensor-1"}},
		{"$count": "count"},
	}

	tabularDataMQLCount, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataMQLCount)

	tabularDataSQLCount, err := dataClient.TabularDataBySQL(ctx, orgID,
		"SELECT count(*) FROM readings WHERE component_name = 'sensor-1'")
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataSQLCount)
	// :snippet-end:
}

