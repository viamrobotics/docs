tabular_data_mql_filter = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {
            "$match": {
                "component_name": "sensor-1"
            },
        }, {
            "$limit": 2
        }, {
            "$project": {
                "time_received": 1,
                "data": 1,
                "tags": 1
            }
        }
    ]
)
print(f"Tabular Data: {tabular_data_mql_filter}")

tabular_data_sql_filter = await data_client.tabular_data_by_sql(
    organization_id=ORG_ID,
    sql_query="SELECT time_received, data, tags FROM readings "
    "WHERE component_name = 'sensor-1' LIMIT 2"
)
print(f"Tabular Data: {tabular_data_sql_filter}")
