---
title: "Query sensor data with Python SDK"
linkTitle: "Query sensor data with SDK"
weight: 31
type: "docs"
images: ["/services/icons/data-query.svg"]
description: "Query sensor data that you have synced to the Viam app using the data management service with SQL or MQL."
modulescript: true
# SME: Devin Hilly
---

You can use the data management service to capture sensor or time-series data from any machine and sync that data to the cloud.
Then, you can query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} to obtain actionable insights or connect it to third-party visualization tools.

For example, you can configure data capture for several sensors on one machine, or for serveral sensors across multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

{{< alert title="In this page" color="tip" >}}

1. [Gathering data on any machine and syncing it to the cloud](#gather-and-sync-data).
1. [Querying data with the Python SDK](#search-data-with-the-python-sdk).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "At least one configured sensor. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a sensor model](/components/sensor/) that supports your sensor.

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

## Gather and sync data

{{< readfile "/static/include/how-to/gather-sync-sensor.md" >}}

## Search data with the Python SDK

{{< table >}}
{{< tablestep link="/build/program/#requirements">}}
**1. Install the Python SDK**

For macOS (both Intel x86_64 and Apple Silicon) or Linux (x86, aarch64, armv6l), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

{{< /tablestep >}}
{{< tablestep link="/cli/#organizations">}}
**2. Create an API key**

To access your machines using the Python SDK, you must use an API key:

```sh {class="command-line" data-prompt="$"}
viam organizations api-key create --org-id <org-id> --name my-api-key
```

{{< /tablestep >}}
{{< tablestep link="/appendix/apis/data-client/">}}
**3. Use the API key with the `data_client`**

Use the API key and the [`TabularDataByFilter()`](/appendix/apis/data-client/#tabulardatabyfilter) method to query data:

```python {class="line-numbers linkable-line-numbers" data-line="28-30"}
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
    tabular_data, count, id = await data_client.tabular_data_by_filter(
        filter=my_filter, limit=5)

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

You can also use:

- [`TabularDataBySQL()`](/appendix/apis/data-client/#tabulardatabysql)
- [`TabularDataByMQL()`](/appendix/apis/data-client/#tabulardatabymql)
- [`DeleteTabularData()`](/appendix/apis/data-client/#deletetabulardata)

{{< /tablestep >}}
{{< /table >}}

## Next steps

On top of querying sensor data with the Python SDK, you can also [query](/use-cases/sensor-data-query/) or [visualize](/use-cases/sensor-data-visualize/) it with third-party tools.

{{< cards >}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{% card link="/use-cases/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
