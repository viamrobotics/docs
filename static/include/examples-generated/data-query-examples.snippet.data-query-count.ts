const tabularDataMQLCount = await client.dataClient.tabularDataByMQL(
    ORG_ID,
    [
        { "$match": { "component_name": "sensor-1" } },
        { "$count": "count" }
    ]
);
console.log(tabularDataMQLCount);

const tabularDataSQLCount = await client.dataClient.tabularDataBySQL(
    ORG_ID,
    "SELECT count(*) FROM readings WHERE component_name = 'sensor-1'"
);
console.log(tabularDataSQLCount);
