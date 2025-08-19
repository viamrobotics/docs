const tabularDataMQLFilter = await client.dataClient.tabularDataByMQL(
    ORG_ID,
    [
        { "$match": { "component_name": "sensor-1" } },
        { "$limit": 2 },
        { "$project": {
            "time_received": 1,
            "data": 1,
            "tags": 1
        }}
    ],
);
console.log(tabularDataMQLFilter);

const tabularDataSQLFilter = await client.dataClient.tabularDataBySQL(
    ORG_ID,
    "SELECT time_received, data, tags FROM readings " +
    "WHERE component_name = 'sensor-1' LIMIT 2"
);
console.log(tabularDataSQLFilter);
