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
		{"$match": map[string]interface{}{"component_name": "sensor-1"}},
		{"$limit": 5},
	}

	tabularDataMQL, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, &app.TabularDataByMQLOptions{})
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataMQL)

	tabularDataSQL, err := dataClient.TabularDataBySQL(ctx, orgID, "SELECT * FROM readings WHERE component_name = 'sensor-1' LIMIT 5")
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Tabular Data: %v\n", tabularDataSQL)
}
