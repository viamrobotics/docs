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
