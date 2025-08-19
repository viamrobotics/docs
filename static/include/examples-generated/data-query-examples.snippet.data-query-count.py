tabular_data_mql_count = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {
            "$match": {
                "component_name": "sensor-1"
            },
        }, {
            "$count": "count"
        }
    ]
)
print(f"Tabular Data: {tabular_data_mql_count}")

tabular_data_sql_count = await data_client.tabular_data_by_sql(
    organization_id=ORG_ID,
    query="SELECT count(*) FROM readings "
    "WHERE component_name = 'sensor-1'"
)
print(f"Tabular Data: {tabular_data_sql_count}")
