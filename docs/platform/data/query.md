---
title: "Query Data with SQL or MQL"
linkTitle: "Query Data with SQL or MQL"
weight: 40
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Query tabular data that you have synced to the Viam app using the data management service with SQL or MQL."
aliases:
  - /manage/data/query/
# SME: Devin Hilly
---

Once you have [added the data management service](/platform/build/configure/services/data/configure-data-capture/#add-the-data-management-service) and [synced tabular data to the Viam app](/platform/build/configure/services/data/#cloud-sync), you can perform queries against that data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You can:

- [Query tabular data in the Viam app](#query-tabular-data-in-the-viam-app): Run SQL or MQL queries against your synced tabular data from the **Query** subtab under the **Data** tab in the Viam app.
- [Query tabular data directly from a compatible client](#query-tabular-data-directly-from-a-compatible-client): Directly query tabular data from an MQL-compatible client, such as `mongosh`.

You can run queries against both the captured tabular data itself as well as its metadata, including robot ID, organization ID, and [tags](/platform/data/dataset/#image-tags).

Only tabular data, such as [sensor](/platform/build/configure/components/sensor/) readings, can be queried using SQL or MQL.
To search non-tabular data, such as images, see [Filter Data](/platform/data/view/#filter-data).
To perform searches against tabular data from within the Python SDK, use the [`TabularDataByFilter`](/platform/build/program/apis/data-client/#tabulardatabyfilter) method.

## Requirements

Before you can query your data, you must:

1. [Add the data management service](/platform/build/configure/services/data/configure-data-capture/#add-the-data-management-service) to your machine.
1. [Configure data capture](/platform/build/configure/services/data/configure-data-capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data query using SQL or MQL.
   To search non-tabular data, see [Filter Data](/platform/data/view/#filter-data).
1. [Configure cloud sync](/platform/build/configure/services/data/configure-cloud-sync/), and sync data to the Viam app.
   When you are able to [view your data in the Viam app](/platform/data/view/), you are ready to proceed.

## Query tabular data in the Viam app

Once you have synced tabular data to the Viam app, you can run SQL or MQL queries against your synced data from the [**Query** subtab](https://app.viam.com/data/query) under the **Data** tab in the Viam app.
You must have the [owner](/platform/fleet/#permissions) role in order to query data in the Viam app.

1. Navigate to the [**Query** subtab](https://app.viam.com/data/query).

1. Select either `SQL` or `MQL` from the **Query mode** dropdown menu on the right-hand side, then enter your query using the respective syntax for the language you have selected in the text area at the top of your screen.
   For example:

   - The following shows a SQL query that filters by the component name `my-ultrasonic-sensor` and limits the returned results to 5:

     {{< imgproc src="/platform/data/query-ui-sql.png" alt="Viam App Data Query tab with a SQL query shown" resize="800x" >}}

   - The following shows the same search using MQL syntax:

     {{< imgproc src="/platform/data/query-ui-mql.png" alt="Viam App Data Query tab with an MQL query shown" resize="800x" >}}

1. Click **Run query** when ready to perform your query and get matching results.
   Query results are displayed as a [JSON array](https://json-schema.org/understanding-json-schema/reference/array) below your query.
   For example:

   - The following shows a SQL query that filters by component name and specific column names, and its returned results:

     {{< imgproc src="/platform/data/query-ui-results.png" alt="Viam App Data Query tab with a SQL query shown and results shown below including two matching records" resize="800x" >}}

   - The following shows a SQL query that returns a count of records matching the search criteria:

     {{< imgproc src="/platform/data/query-ui-numreadings.png" alt="Viam App Data Query tab with a SQL query shown with the resulting count of matching records displayed below" resize="800x" >}}

For more information on MQL syntax, see the [MQL (MongoDB Query Language)](https://www.mongodb.com/docs/manual/tutorial/query-documents/) documentation.

## Query tabular data directly from a compatible client

Once you have synced tabular data to the Viam app, you can directly query that data from an MQL-compatible client, such as [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/) or [Compass](https://www.mongodb.com/docs/compass/current/).

1. If you haven't already, [configure direct data query](/platform/build/configure/services/data/configure-data-query/#configure-data-query) to be able to use this query mode.

1. Open your chosen MQL-compatible client an connect to the Viam organization's MongoDB Atlas instance.
   You can use any client that is capable of connecting to a MongoDB Atlas instance, including the [`mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/), [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), and many third-party tools.
   To connect, use the `hostname` you determined when you [configured direct data query](/platform/build/configure/services/data/configure-data-query/#configure-data-query), and structure your username in the following format:

   ```sh
   db-user-<YOUR-ORG-ID>
   ```

   Where `<YOUR-ORG-ID>` is your organization ID, determined from the `viam organizations list` CLI command.
   The full username you provide to your client should therefore resemble `db-user-abcdef12-abcd-abcd-abcd-abcdef123456`.

For example, to connect to your Viam organization's MongoDB Atlas instance and query data using the `mongosh` shell:

1. If you haven't already, [download the `mongosh` shell](https://www.mongodb.com/try/download/shell).
   See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

1. Run the following command to connect to the Viam organization's MongoDB Atlas instance from `mongosh`:

   ```sh {class="command-line" data-prompt=">"}
   mongosh "mongodb+srv://<YOUR-DB-HOSTNAME>" --apiVersion 1 --username db-user-<YOUR-ORG-ID>
   ```

   Where:

   - `<YOUR-DB-HOSTNAME>` is your organization's assigned MongoDB Atlas instance hostname (including database name), determined from the [`viam data database hostname` CLI command](/platform/build/configure/services/data/configure-data-query/#configure-data-query).
   - `<YOUR-ORG-ID>` is your organization ID, determined from the `viam organizations list` CLI command.
     The full username you provide to the `--username` flag should therefore resemble `db-user-abcdef12-abcd-abcd-abcd-abcdef123456`.

1. Once connected, you can run SQL or MQL to query captured data directly. For example:

   - The following SQL query uses the MongoDB [`$sql` aggregation pipeline stage](https://www.mongodb.com/docs/atlas/data-federation/supported-unsupported/pipeline/sql/) to search the `sensorData` database and `readings` collection, and get sensor readings from an ultrasonic sensor on a specific `robot_id` where the recorded `distance` measurement is greater than `.2` meters:

     ```mongodb {class="command-line" data-prompt=">"}
     // Switch to sensorData database:
     use sensorData

     // Run query using $sql:
     db.aggregate(
         [
             { $sql: {
                 statement: "select count(*) as numStanding from readings \
                     where robot_id = 'abcdef12-abcd-abcd-abcd-abcdef123456' and \
                     component_name = 'my-ultrasonic-sensor' and data.readings.distance > 0.2",
                 format: "jdbc"
             }}
         ] )
     [ { '': { numStanding: 215 } } ]
     ```

   - The following MQL query performs the same search as the SQL query above, but uses the [MongoDB query language](https://www.mongodb.com/docs/manual/tutorial/query-documents/):

     ```mongodb {class="command-line" data-prompt=">"}
     // Switch to sensorData database:
     use sensorData

     // Run query using $match:
     db.readings.aggregate(
         [
             { $match: {
                 'robot_id': 'abcdef12-abcd-abcd-abcd-abcdef123456',
                 'component_name': 'my-ultrasonic-sensor',
                 'data.readings.distance': { $gt: .2 } } },
             { $count: 'numStanding' }
         ] )
     [ { numStanding: 215 } ]
     ```

For information on connecting to your Atlas instance from other MQL clients, see the MongoDB Atlas [Connect to your Cluster Tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

## Next Steps

To export your captured data from the cloud, see [Export Data](../export/).

To adjust the rate at which your machine captures data, see [Configure Data Capture](/platform/build/configure/services/data/configure-data-capture/#configure-data-capture-for-individual-components).

To adjust the sync frequency, see [Configure Cloud Sync](/platform/build/configure/services/data/configure-cloud-sync/).
