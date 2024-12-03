---
linkTitle: "Update packages"
title: "Update packages"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "TODO"
---

## Testing Strategies

If you inspect the fragment you have created, you will notice it contains a `version` field.

As you develop new versions of your software, your machines will continue to use the version of the software that you have configured in the fragment.

We generally recommend that you test updates on a subset of machines before deploying it to all machines.

You can either create a second fragment that you add to a subset of machines, or manually overwrite the version of the package for a subset of machines:

{{< tabs >}}
{{< tab name="A second fragment" >}}

{{< table >}}
{{% tablestep %}}
**1. Create a fragment for development**

Copy the JSON object from your primary fragment and create a second fragment.
We recommend you call your second fragment something easily identifiable as your testing environment, such as `FragmentName-DEV`.

Paste the JSON object from your primary fragment.

{{% /tablestep %}}
{{% tablestep %}}
**2. Edit the fragment**

Change the version of your package in the development fragment.
For example:

```json {class="line-numbers linkable-line-numbers" data-line="16"}
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      "version": "0.5.3"
    }
  ]
}
```

{{% /tablestep %}}
{{% tablestep %}}
**3. Add the development fragment to a subset of machines**

Configure a subset of your machines with the development fragment.
If you had configured them already with the primary fragment, remove that fragment first.

{{% /tablestep %}}
{{% tablestep %}}
**4. Test the new version**

Test the new version of your package.
When you are satisfied that your package works as expected, continue to [update your primary fragment](#update-a-package-version).

{{% /tablestep %}}
{{< /table >}}

{{< /tab >}}
{{< tab name="Manual testing" >}}

{{< table >}}
{{% tablestep %}}
**1. Change the version of the module**

You can overwrite parts of a fragment to use a new version of a package without modifying the upstream fragment.

For each machine that you would like to test the new version of the package on, go to its **CONFIGURE** tab, find the package, and edit its version number.

{{<imgproc src="/how-tos/deploy-packages/version-change.png" resize="800x" class="fill aligncenter" style="width: 600px" declaredimensions=true alt="Configuration builder UI">}}

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
**2. Test the new version**

Test the new version of your package.
When you are satisfied that your package works as expected, continue to [update your primary fragment](#update-a-package-version).

{{% /tablestep %}}
{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

## Update a package version

Once you have confirmed that the new version of your package works, go to your primary fragment and edit it to use the new version of your package.

For example:

```json {class="line-numbers linkable-line-numbers" data-line="16"}
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      "version": "0.5.3"
    }
  ]
}
```

Don't forget to **Save**.

All machines configured with your fragment will update when they next check for configuration updates.

To check when your machines have last updated their configuration, iterate over your machines using the Fleet Management API, connect to each machine, and use the [`GetMachineStatus` method](/appendix/apis/robot/#getmachinestatus).

The following example script iterates over all machines in a given location and if it can connect to the machines, it prints their status information.
If it cannot connect to a machine, it prints the most recent log entries.

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient
from viam.robot.client import RobotClient


# Replace "<API-KEY>" (including brackets) with your API key and "<API-KEY-ID>"
# with your API key ID
API_KEY = "<API-KEY>"
API_KEY_ID = "<API-KEY-ID>"
LOCATION_ID = "<LOCATION-ID>"


async def connect() -> ViamClient:
    dial_options = DialOptions.with_api_key(API_KEY, API_KEY_ID)
    return await ViamClient.create_from_dial_options(dial_options)


async def machine_connect(address):
    opts = RobotClient.Options.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID
    )
    return await RobotClient.at_address(address, opts)


async def main():
    viam_client = await connect()
    cloud = viam_client.app_client

    machines = await cloud.list_robots(location_id=LOCATION_ID)
    print("Found {} machines.".format(len(machines)))

    for m in machines:
        machine_parts = await cloud.get_robot_parts(m.id)
        main_part = None
        for p in machine_parts:
            if p.main_part:
                main_part = p

        print("Attempting to connect to {}...".format(main_part.fqdn))

        try:
            machine = await machine_connect(main_part.fqdn)
            status = await machine.get_machine_status()
            print(status.config)

        except ConnectionError:
            print("Unable to establish a connection to the machine.")
            logs = await cloud.get_robot_part_logs(
                robot_part_id=main_part.id,
                num_log_entries=5
            )
            if not logs:
                print("No logs available.")
            else:
                print("Most recent 5 log entries:")
            for log in logs:
                print("{}-{} {}: {}".format(
                    log.logger_name, log.level, log.time, log.message))
                if log.stack:
                    print(log.stack)

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```
