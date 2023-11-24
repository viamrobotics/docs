---
title: "Configure Direct Data Query"
linkTitle: "Configure Direct Data Query"
description: "Configure direct data query to query tabular data with MQL or SQL"
weight: 35
type: "docs"
tags: ["data management", "cloud", "query", "sensor"]
aliases:
  - "/services/data/configure-data-query/"
# SME: Devin Hilly
---

Configure direct data query to be able to query captured tabular data in the Viam cloud using {{< glossary_tooltip term_id="mql" text="MQL" >}} or {{< glossary_tooltip term_id="sql" text="SQL" >}} from a MQL-compatible client, such as `mongosh` or MongoDB Compass.
Synced data is stored in a MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance.

You can query against both the captured tabular data itself as well as its metadata, including robot ID, organization ID, and [tags](/data/dataset/#image-tags).

Only tabular data, such as [sensor](/build/configure/components/sensor/) readings, can be queried in this fashion.

{{< alert title="Important" color="note" >}}
These steps are only required when querying tabular data directly from an MQL-compatible client, such as `mongosh`.
You do not need to perform any additional configuration when [querying data in the Viam app](/data/query/#query-tabular-data-in-the-viam-app).
{{< /alert >}}

## Requirements

Before you can configure data query, you must:

1. [Add the data management service](/build/configure/services/data/configure-data-capture/#add-the-data-management-service) to your machine.
1. [Configure data capture](/build/configure/services/data/configure-data-capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data query.
1. [Configure cloud sync](/build/configure/services/data/configure-cloud-sync/), and sync data to the Viam app.
   When you are able to [view your data in the Viam app](/data/view/), you are ready to proceed.

## Configure data query

Once your machine has synced captured data to the Viam app, you can configure data query using the Viam CLI:

1. If you haven't already, [install the Viam CLI](/fleet/cli/#install) and [authenticate](/fleet/cli/#authenticate) to Viam.

1. Find your organization ID by running the following command, or from your organization's **Settings** page in [the Viam App](https://app.viam.com/):

   ```sh {class="line-numbers linkable-line-numbers"}
   viam organizations list
   ```

1. Configure a new database user for the Viam organization's MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance, which is where your machine's synced data is stored.
   Provide your organization's `org-id` from step 2, and a desired new password for your database user.

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database configure --org-id=<YOUR-ORGANIZATION-ID> --password=<NEW-DBUSER-PASSWORD>
   ```

   This command configures a new database user for your org for use with data query.
   If you have already created this user, this command updates the password for that user instead.

1. Determine the hostname for your organization's MongoDB Atlas Data Federation instance by running the following command with the organization's `org-id` from step 2:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam data database hostname --org-id=<YOUR-ORGANIZATION-ID>
   ```

   This command returns the `hostname` (including database name) to use to connect to your data store on the Viam organization's MongoDB Atlas instance.
   You will need this to query your data in the next section.

For more information, see the documentation for the [Viam CLI `database` command](/fleet/cli/#data).

## Next Steps

Once configured, you can [query your data directly](/data/query/#query-tabular-data-directly-from-a-compatible-client) from your chosen client using either SQL or MQL.

To view your captured data in the cloud, see [View Data](/data/view/).
To export your synced data, see [Export Data](/data/export/).

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
