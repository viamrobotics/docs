---
title: "Query sensor data with the Python SDK"
linkTitle: "Query sensor data with an SDK"
type: "docs"
images: ["/services/icons/data-query.svg"]
icon: true
description: "Retrieve and query sensor data that you have synced to the Viam app using Python SDK."
aliases:
  - /use-cases/sensor-data-query-sdk/
languages: ["python"]
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "core"]
level: "Beginner"
date: "2024-08-16"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
# SME: Devin Hilly
---

You can use the data management service to [capture sensor data](/how-tos/collect-sensor-data/) from any machine and sync that data to the cloud.
Then, you can use the Python SDK to retrieve and query that data.
For example, you can configure data capture for several sensors on one machine, or for several sensors across multiple machines, to report the ambient operating temperature.
You can then write a script to run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation or to take action if the machines are overheating.

{{< alert title="In this page" color="tip" >}}

1. [Setting up the Python SDK](#set-up-the-python-sdk).
1. [Querying data with the Python SDK](#query-data-with-the-python-sdk).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/how-tos/collect-sensor-data/).

{{% /expand%}}

## Set up the Python SDK

{{< table >}}
{{% tablestep link="/sdks/#installation"%}}
**1. Install the Python SDK**

For macOS (both Intel x86_64 and Apple Silicon) or Linux (x86, aarch64, armv6l), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

{{% /tablestep %}}
{{% tablestep%}}
**2. Install requirements**

To query data with the Python SDK, you will the `bson` package or the `pymongo` package.
To install `bson`, run the following command:

```sh {class="command-line" data-prompt="$"}
pip install bson
```

{{% /tablestep %}}
{{< /table >}}

## Query data with the Python SDK

{{< table >}}
{{% tablestep link="/cloud/organizations/" %}}
**1. Get an API key**

To access your machines using the Python SDK, you must use an API key.
You can get an organization API key from the organization's **Settings** accessible in the top right of the navigation bar in the [Viam app](https://app.viam.com).

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/"%}}
**2. Use the API key with the `data_client`**

Use the API key and [`TabularDataByFilter()`](/appendix/apis/data-client/#tabulardatabyfilter), [`TabularDataBySQL()`](/appendix/apis/data-client/#tabulardatabysql), [`TabularDataByMQL()`](/appendix/apis/data-client/#tabulardatabymql), and[`DeleteTabularData()`](/appendix/apis/data-client/#deletetabulardata) to query data by creating and running the following Python script:

{{% alert title="Note" color="note" %}}
Make sure to replace the value in line 30 with your correct sensor name, line 35 with your organization ID which you can get by running `viam organizations list`, and line 37 with your location ID which you can get by running `viam locations list`.
{{% /alert %}}

```python {class="line-numbers linkable-line-numbers" data-line="29-54, 30, 37, 40"}
import asyncio
import bson

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app.data import Filter


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client

    # TODO: replace "my-sensor" with your correct sensor name
    my_filter = Filter(component_name="my-sensor")
    data, count, id = await data_client.tabular_data_by_filter(
        filter=my_filter, limit=5)
    # This query requests all stored data grouped by hour and calculates the
    # average, minimum, and maximum of the memory usage
    data = await data_client.tabular_data_by_mql(
      # TODO: Replace  <ORGANIZATION-ID> with your organization ID
      organization_id='<ORGANIZATION-ID>',
      mql_binary=[
        # TODO: Replace  <LOCATION-ID> with your location ID
        bson.dumps({'$match': {'location_id': '<LOCATION-ID>'}}),
        bson.dumps({
          "$group": {
            "_id": {
              "year": {"$year": "$time_requested"},
              "dayOfYear": {"$dayOfYear": "$time_requested"},
              "hour": {"$hour": "$time_requested"}
            },
            "count": {"$sum": 1},
            "max_mem": {"$max": "$data.readings.mem.used_percent"},
            "min_mem": {"$min": "$data.readings.mem.used_percent"},
            "average_mem": {"$avg": "$data.readings.mem.used_percent"}
          }
        })
      ])
    print(data)

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tablestep %}}
{{< /table >}}

Adjust the Python script to query your data further with the [`data_client` API](/appendix/apis/data-client/#api).

## Next steps

On top of querying sensor data with the Python SDK, you can also [query](/how-tos/sensor-data-query-with-third-party-tools/) or [visualize](/how-tos/sensor-data-visualize/) it with third-party tools.

{{< cards >}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{% card link="/how-tos/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
