---
title: "Query Data with SQL or MQL"
linkTitle: "Query Data"
weight: 35
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Query tabular data that you have synced to the Viam app using the data management service with SQL or MQL."
icon: true
images: ["/services/icons/data-query.svg"]
aliases:
  - /manage/data/query/
  - /data/query/
# SME: Devin Hilly
---

Once you have [added the data management service](/data/capture/#add-the-data-management-service) and [synced tabular data to the Viam app](/data/cloud-sync/), you can perform queries against that data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You can:

- [Query tabular data in the Viam app](#query-tabular-data-in-the-viam-app): Run SQL or MQL queries against your synced tabular data from the **Query** subtab under the **Data** tab in the Viam app.
- [Query tabular data directly from a compatible client](#query-tabular-data-directly-from-a-compatible-client): Directly query tabular data from an MQL-compatible client, such as `mongosh`.

You can run queries against both the captured tabular data itself as well as its metadata, including machine ID, organization ID, and [tags](/data/dataset/#image-tags).

Only tabular data, such as [sensor](/components/sensor/) readings, can be queried using SQL or MQL.
To search non-tabular data, such as images, see [Filter Data](/services/data/view/#filter-data).
To perform searches against tabular data from within the Python SDK, use the [`TabularDataByFilter`](/appendix/apis/data-client/#tabulardatabyfilter) method.

## Requirements

Before you can configure data query, you must:

1. [Add the data management service](/data/capture/#add-the-data-management-service) to your machine.
1. [Configure data capture](/data/capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data query.
   To search non-tabular data, see [Filter Data](/services/data/view/#filter-data).
1. [Configure cloud sync](/data/cloud-sync/), and sync data to the Viam app.
   When you are able to [view your data in the Viam app](/services/data/view/), you are ready to proceed.

## Query tabular data in the Viam app

Once you have synced tabular data to the Viam app, you can run SQL or MQL queries against your synced data from the [**Query** subtab](https://app.viam.com/data/query) under the **Data** tab in the Viam app.
You must have the [owner](/fleet/rbac/) role in order to query data in the Viam app.

1. Navigate to the [**Query** subtab](https://app.viam.com/data/query).

1. Select either `SQL` or `MQL` from the **Query mode** dropdown menu on the right-hand side, then enter your query using the respective syntax for the language you have selected in the text area at the top of your screen.
   For example:

   - The following shows a SQL query that filters by the component name `my-ultrasonic-sensor` and limits the returned results to 5:

     {{< imgproc src="/services/data/query-ui-sql.png" alt="Viam App Data Query tab with a SQL query shown" resize="800x" >}}

   - The following shows the same search using MQL syntax:

     {{< imgproc src="/services/data/query-ui-mql.png" alt="Viam App Data Query tab with an MQL query shown" resize="800x" >}}

1. Click **Run query** when ready to perform your query and get matching results.
   Query results are displayed as a [JSON array](https://json-schema.org/understanding-json-schema/reference/array) below your query.
   For example:

   - The following shows a SQL query that filters by component name and specific column names, and its returned results:

     {{< imgproc src="/services/data/query-ui-results.png" alt="Viam App Data Query tab with a SQL query shown and results shown below including two matching records" resize="800x" >}}

   - The following shows a SQL query that returns a count of records matching the search criteria:

     {{< imgproc src="/services/data/query-ui-numreadings.png" alt="Viam App Data Query tab with a SQL query shown with the resulting count of matching records displayed below" resize="800x" >}}

For more information on MQL syntax, see the [MQL (MongoDB Query Language)](https://www.mongodb.com/docs/manual/tutorial/query-documents/) documentation.

## Query tabular data directly from a compatible client

Configure direct data query to be able to query captured tabular data in the Viam cloud using {{< glossary_tooltip term_id="mql" text="MQL" >}} or {{< glossary_tooltip term_id="sql" text="SQL" >}} from a MQL-compatible client, such as `mongosh` or MongoDB Compass.
Synced data is stored in a MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance.

You can query against both the captured tabular data itself as well as its metadata, including machine ID, organization ID, and [tags](/data/dataset/#image-tags).

Only tabular data, such as [sensor](/components/sensor/) readings, can be queried in this fashion.

Before being able to query data, you must configure data query.

### Configure data query

{{< alert title="Important" color="note" >}}
These steps are only required when querying tabular data directly from an MQL-compatible client, such as `mongosh`.
You do not need to perform any additional configuration when [querying data in the Viam app](/services/data/query/#query-tabular-data-in-the-viam-app).
{{< /alert >}}

1. If you haven't already, [install the Viam CLI](/cli/#install) and [authenticate](/cli/#authenticate) to Viam.

1. Find your organization ID by running the following command, or from your organization's **Settings** page in [the Viam App](https://app.viam.com/):

   ```sh {class="line-numbers linkable-line-numbers"}
   viam organizations list
   ```

1. Configure a new database user for the Viam organization's MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance, which is where your machine's synced data is stored.

   {{< alert title="Warning" color="warning" >}}
   The command will create a user with your organization ID as the username.
   If you or someone else in your organization have already created this user, the following steps update the password for that user instead.
   Dashboards or other integrations relying on this password will then need to be updated.
   {{< /alert >}}

   Provide your organization's `org-id` from step 2, and a desired new password for your database user.
   Your password must be at least 8 characters long, and include at least one uppercase, one number, and one special character (such as `$` or `%`):

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database configure --org-id=<YOUR-ORGANIZATION-ID> --password=<NEW-DBUSER-PASSWORD>
   ```

   This command configures a new database user for your organization for use with data query, and sets the password.
   If you have already run this command before, this command instead updates the password to the new value you set.

1. Determine the connection URI (also known as a connection string) for your organization's MongoDB Atlas Data Federation instance by running the following command with the organization's `org-id` from step 2:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database hostname --org-id=<YOUR-ORGANIZATION-ID>
   ```

   This command returns both the _connection URI_ to your organization's MongoDB Atlas Data Federation instance, as well as its _hostname_ and _database name_:

   - Most MQL-compatible database clients require the _connection URI_, along with your user credentials, to connect to this server.
   - Some MQL-compatible database client instead require a _hostname_ and _database name_, along with your user credentials, to connect to this server.

   You will need this information to query your data in the next section.

For more information, see the documentation for the [Viam CLI `database` command](/cli/#data).

### Query

Once you have synced tabular data to the Viam app and [configured a database user](#configure-data-query), you can directly query that data from an MQL-compatible database client, such as the [`mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/), [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), or one of many third-party tools.

For example, to use the `mongosh` shell to connect to your Viam organization's MongoDB Atlas instance and query data:

1. If you haven't already, [download the `mongosh` shell](https://www.mongodb.com/try/download/shell).
   See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

1. Run the following command to connect to the Viam organization's MongoDB Atlas instance from `mongosh`:

   ```sh {class="command-line" data-prompt=">"}
   mongosh "<YOUR-DB-CONNECTION-URI>"
   ```

   Where:

   - `<YOUR-DB-CONNECTION-URI>` is your organization's assigned MongoDB Atlas connection URI, determined from the [`viam data database hostname` CLI command](/services/data/query/#configure-data-query).
   - `YOUR-PASSWORD-HERE` (included in the connection URI) is your configured database password, as set by the [`viam data database configure` CLI command](/services/data/query/#configure-data-query).

   If you are connecting from a database client that requires a server hostname and database name, provide those values from the [`viam data database hostname` CLI command](/services/data/query/#configure-data-query) instead.

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

{{< alert title="Tip" color="tip" >}}
If you use a data field that is named the same as a [reserved SQL keyword](https://en.wikipedia.org/wiki/List_of_SQL_reserved_words), such as `value` or `position`, you must escape that field name in your query using backticks ( <file>\`</file> ).
For example, to query against a field named `value` which is a subfield of the `data` field in the `readings` collection, you would use:

```mongodb {class="command-line" data-prompt=">"}
select data.`value` from readings
```

See the [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatability-and-limitations) for more information.

{{< /alert >}}

For information on connecting to your Atlas instance from other MQL clients, see the MongoDB Atlas [Connect to your Cluster Tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

#### Query by date

When using MQL to query your data by date or time range, you can optimize query performance by avoiding the MongoDB `$toDate` expression, using the [BSON `date` type](https://www.mongodb.com/docs/manual/reference/bson-types/#date) instead.

For example, you could use the following query to search by a date range in the `mongosh` shell, using the JavaScript `Date()` constructor to specify an explicit start timestamp, and use the current time as the end timestamp:

```mongodb {class="command-line" data-prompt=">"}
// Switch to sensorData database:
use sensorData

// Set desired start and end times:
const startTime = new Date('2024-02-10T19:45:07.000Z')
const endTime = new Date()

// Run query using $match:
db.readings.aggregate(
    [
        { $match: {
            time_received: {
                $gte: startTime,
                $lte: endTime }
        } }
    ] )
```

## Next steps

With data query enabled, you can now visualize your machine's uploaded tabular data using many popular data visualization services, such as Grafana.
See [Visualize Data](/services/data/visualize/) for instructions on setting up and using these data visualization services with Viam, or the [Visualize data with Grafana](/tutorials/services/visualize-data-grafana/) tutorial for a detailed walkthrough specific to Grafana.

For a tutorial that walks through querying data and displaying it on a TypeScript dashboard, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).

To export your captured data from the cloud, see [Export Data](../export/).

To adjust the rate at which your machine captures data, see [Configure Data Capture](/data/capture/#configure-data-capture-for-individual-components).

To adjust the sync frequency, see [Configure Cloud Sync](/data/cloud-sync/).
