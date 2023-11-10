---
title: "Configure Data Query"
linkTitle: "Configure Data Query"
description: "Configure data query to query synced data directly in the cloud."
weight: 35
type: "docs"
tags: ["data management", "cloud", "query"]
# SME: Aaron Casas
---

Configure data query to be able to directly query captured data in the Viam cloud using the [MongoDB Query Language (MQL)](https://www.mongodb.com/docs/manual/tutorial/query-documents/).

## Requirements

Before you can configure [data query](../#data-query), you must [add the data management service](/services/data/configure-data-capture/#add-the-data-management-service) and [configure cloud sync](/services/data/configure-cloud-sync/).

## Configure data query

Once your smart machine has synced captured data to the Viam app, you can configure data query using the Viam CLI:

1. If you haven't already, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam.

1. Find your organization ID by running the following command, or from your organization's **Settings** page in [the Viam App](https://app.viam.com/):

   ```sh {class="line-numbers linkable-line-numbers"}
   viam organizations list
   ```

1. Run the following command to determine the hostname for your organization's MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance, which is where your smart machine's synced data is stored.
   Provide your organizations `org-id` from step 2:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database hostname --org-id=<YOUR-ORGANIZATION-ID>
   ```

   This command returns the `hostname` of your Viam organization's assigned MongoDB Atlas instance.

1. Then, configure a new database user for that database instance.
   Provide your organization's `org-id` from step 2, and a desired new password for your database user.

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database configure --org-id=<YOUR-ORGANIZATION-ID> --password=<NEW-DBUSER-PASSWORD>
   ```

   This command creates a new database `user` for your organization's MongoDB Atlas instance.

For more information, see the documentation for the [Viam CLI `database` command](/manage/cli/#data).

## Query data using MQL

Once you have [configured data query](#configure-data-query), you can directly query synced data using MQL.

You can use any client that supports MQL that is capable of connecting to MongoDB Atlas instances, including [the `mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/), [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), and many third-party tools.
Use the `hostname` and `user` returned from the setup above to connect from your desired client to the MongoDB Atlas instance.

For example, to connect to your Viam organization's MongoDB Atlas instance and query data using the `mongosh` shell:

1. If you haven't already, [download the `mongosh` shell](https://www.mongodb.com/try/download/shell).
   See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

1. Run the following command to connect to your Viam organization's MongoDB Atlas instance from `mongosh`:

   ```sh {class="line-numbers linkable-line-numbers"}
   mongosh "mongodb+srv://<YOUR-DB-HOSTNAME>" --apiVersion 1 --username <YOUR-DB-USER>
   ```

   Where:

   - `<YOUR-DB-HOSTNAME>` is your organization's assigned MongoDB Atlas instance, as returned from `viam data database hostname` above.
   - `<YOUR-DB-USER>` is your organization's database user for that Atlas instance, as returned from `viam data database configure` above.

1. Once connected, you can run MQL to query captured data directly.
   For example, the following MQL queries all synced data in the `sensors` database:

   ```sql {class="line-numbers linkable-line-numbers"}
   db.sensors.find( {} )
   ```

   The following MQL queries synced data in the `sensors` database and returns `sensor_type: temp_sensor` readings greater than a certain `current_temperature`:

   ```sql {class="line-numbers linkable-line-numbers"}
   db.sensors.find( { sensor_type: "temp_sensor", current_temperature: { $gt: 32 } } )
   ```

Consult the documentation for the specific MQL client you are using for more information.

## Next Steps

To view your captured data in the cloud, see [View Data](/manage/data/view/).
To export your synced data, see [Export data](/manage/data/export/).

For a comprehensive tutorial on data management, see [Intro to Data Management](/tutorials/services/data-management-tutorial/).
