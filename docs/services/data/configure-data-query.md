---
title: "Configure Data Query"
linkTitle: "Configure Data Query"
description: "Configure data query to query tabular data with MQL or SQL"
weight: 35
type: "docs"
tags: ["data management", "cloud", "query", "sensor"]
# SME: Aaron Casas
---

Configure data query to be able to directly query captured tabular data in the Viam cloud using [MQL](https://www.mongodb.com/docs/manual/tutorial/query-documents/) or SQL.
Synced data is stored in a MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance.

You can query both the captured tabular data itself as well as its metadata (such as robot ID, organization ID, and [tags](/manage/data/label/#image-tags)).

Only tabular data, such as [sensor](/components/sensor/) readings, can be queried in this fashion.

## Requirements

Before you can configure data query, you must:

- [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service)
- [Configure data capture](/services/data/configure-data-capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data query.
- [Configure cloud sync](/services/data/configure-cloud-sync/), and sync data to the Viam app.

## Configure data query

Once your smart machine has synced captured data to the Viam app, you can configure data query using the Viam CLI:

1. If you haven't already, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam.

1. Find your organization ID by running the following command, or from your organization's **Settings** page in [the Viam App](https://app.viam.com/):

   ```sh {class="line-numbers linkable-line-numbers"}
   viam organizations list
   ```

1. Configure a new database user for the Viam organization's MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance, which is where your smart machine's synced data is stored.
   Provide your organization's `org-id` from step 2, and a desired new password for your database user.

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database configure --org-id=<YOUR-ORGANIZATION-ID> --password=<NEW-DBUSER-PASSWORD>
   ```

1. Determine the hostname for your organization's MongoDB Atlas Data Federation instance.
   Provide your organization's `org-id` from step 2:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database hostname --org-id=<YOUR-ORGANIZATION-ID>
   ```

   This command returns the `hostname` (including database name) you can use to connect to your data store on the Viam organization's MongoDB Atlas instance.

For more information, see the documentation for the [Viam CLI `database` command](/manage/cli/#data).

## Query data

Once you have [configured data query](#configure-data-query), you can directly query synced tabular data using MQL or SQL.

You can use any client that is capable of connecting to MongoDB Atlas instances, including [the `mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/), [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), and many third-party tools.
Use the `hostname` and `user` returned from the setup above to connect from your desired client to the MongoDB Atlas instance.

For example, to connect to your Viam organization's MongoDB Atlas instance and query data using the `mongosh` shell:

1. If you haven't already, [download the `mongosh` shell](https://www.mongodb.com/try/download/shell).
   See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

1. Run the following command to connect to the Viam organization's MongoDB Atlas instance from `mongosh`:

   ```sh {class="line-numbers linkable-line-numbers"}
   mongosh "mongodb+srv://<YOUR-DB-HOSTNAME>" --apiVersion 1 --username <YOUR-DB-USER>
   ```

   Where:

   - `<YOUR-DB-HOSTNAME>` is your organization's assigned MongoDB Atlas instance hostname (including database name), as returned from `viam data database hostname` above.
   - `<YOUR-DB-USER>` is your organization's database user for that Atlas instance, as returned from `viam data database configure` above.

1. Once connected, you can run [MQL](https://www.mongodb.com/docs/manual/tutorial/query-documents/) or SQL to query captured data directly. For example:

   - The following MQL query searches the `sensorData` database and `readings` collection, and returns sensor readings from an ultrasonic sensor on a specific `robot_id` where the recorded `distance` measurement is greater than `.2` meters:

     ```mongodb {class="line-numbers linkable-line-numbers"}
     AtlasDataFederation sensorData> db.readings.aggregate(
         [
             { $match: {
                 'robot_id': 'abcdef12-abcd-abcd-abcd-abcdef123456',
                 'component_name': 'my-ultrasonic-sensor',
                 'data.readings.distance': { $gt: .2 } } },
             { $count: 'numStanding' }
         ] )
     [ { numStanding: 215 } ]
     ```

   - The following SQL query uses the MongoDB [`$sql` aggregation pipeline stage](https://www.mongodb.com/docs/atlas/data-federation/query/sql/shell/connect/#aggregation-pipeline-stage-syntax) to perform the same query as the MQL above, but using SQL syntax:

     ```mongodb {class="line-numbers linkable-line-numbers"}
     AtlasDataFederation sensorData> db.aggregate(
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

For more information on MQL syntax see the [MongoDB query language](https://www.mongodb.com/docs/manual/tutorial/query-documents/) documentation.
For information on connecting to your Atlas instance from other MQL clients, see the MongoDB Atlas [Connect to your cluster tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

## Next Steps

To view your captured data in the cloud, see [View Data](/manage/data/view/).
To export your synced data, see [Export data](/manage/data/export/).

For a comprehensive tutorial on data management, see [Intro to Data Management](/tutorials/services/data-management-tutorial/).
