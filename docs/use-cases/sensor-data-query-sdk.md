---
title: "Query sensor data with the Python SDK"
linkTitle: "Query sensor data with SDK"
weight: 31
type: "docs"
images: ["/services/icons/data-query.svg"]
description: "Retrieve and query sensor data that you have synced to the Viam app using Python SDK."
modulescript: true
# SME: Devin Hilly
---

You can use the data management service to [capture sensor data](/use-cases/collect-sensor-data/) from any machine and sync that data to the cloud.
Then, you can use the Python SDK to retrieve and query that data.
For example, you can configure data capture for several sensors on one machine, or for several sensors across multiple machines, to report the ambient operating temperature.
You can then write a script to run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation or to take action if the machines are overheating.

{{< alert title="In this page" color="tip" >}}

1. [Setting up the Python SDK](#set-up-the-python-sdk).
1. [Querying data with the Python SDK](#query-data-with-the-python-sdk).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/use-cases/collect-sensor-data/).

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

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
{{< /table >}}

## Query data with the Python SDK

{{< table >}}
{{% tablestep link="/cli/#organizations"%}}
**1. Create an API key**

To access your machines using the Python SDK, you must use an API key:

```sh {class="command-line" data-prompt="$"}
viam organizations api-key create --org-id <org-id> --name my-api-key
```

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/"%}}
**2. Use the API key with the `data_client`**

Use the API key and [`TabularDataByFilter()`](/appendix/apis/data-client/#tabulardatabyfilter), [`TabularDataBySQL()`](/appendix/apis/data-client/#tabulardatabysql), [`TabularDataByMQL()`](/appendix/apis/data-client/#tabulardatabymql), and[`DeleteTabularData()`](/appendix/apis/data-client/#deletetabulardata) to query data:

```python {class="line-numbers linkable-line-numbers" data-line="28-50"}
import asyncio

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

    my_filter = Filter(component_name="my-sensor")
    data, count, id = await data_client.tabular_data_by_filter(
        filter=my_filter, limit=5)
    # This query requests all stored data grouped by hour and calculates the
    # average, minimum, and maximum of the memory usage
    data = await data_client.tabular_data_by_mql(
      organization_id=organization_id,
      mql_query=[
        bson.dumps({'$match': {'location_id': '<location-id>'}}),
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

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tablestep %}}
{{< /table >}}

Adjust the Python script to uery your data further.

## Next steps

On top of querying sensor data with the Python SDK, you can also [query](/use-cases/sensor-data-query-with-third-party-tools/) or [visualize](/use-cases/sensor-data-visualize/) it with third-party tools.

{{< cards >}}
{{% card link="/use-cases/sensor-data-query-with-third-party-tools/" %}}
{{% card link="/use-cases/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
