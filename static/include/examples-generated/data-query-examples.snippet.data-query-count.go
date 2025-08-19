mqlStages = []map[string]interface{}{
	{"$match": map[string]interface{}{"component_name": "sensor-1"}},
	{"$count": "count"},
}

tabularDataMQLCount, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, &app.TabularDataByMQLOptions{})
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
