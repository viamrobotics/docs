---
linkTitle: "Update software"
title: "Roll out software updates to machines"
weight: 40
layout: "docs"
type: "docs"
description: "As new versions of software modules or ML models become available, you can update the deployed version on all machines in one go."
date: "2025-02-05"
aliases:
  - /manage/software/update-packages/
---

If you have already [deployed software](/manage/software/deploy-software/), you can inspect the fragment you have created.
The JSON object for the deployed module or package has a `version` field.
Unless the `version` field is set to a specific version, some or all updates for that module or package can happen automatically.

To perform other updates or changes to the configuration of all machines using the fragment:

1. [Test your updates](#test-updates)
2. [Update the software version and roll out the changes](#update-the-software-version)
3. [Check the status of your machines](#check-machine-status)

We strongly recommend that you test updates on a subset of machines before deploying it to all machines.

{{% alert title="Updates for microcontrollers" color="note" %}}
To update the firmware on your microcontroller, see [Over-the-air updates](/operate/get-started/other-hardware/micro-module/#over-the-air-updates).
{{% /alert %}}

## Test updates

You can either create a second fragment that you add to a subset of machines, or manually overwrite the version of the package for a subset of machines.

{{< tabs >}}
{{< tab name="A second fragment (recommended)" >}}

{{< table >}}
{{% tablestep %}}
**1. Create a fragment for development**

Copy the JSON object from your primary fragment and create a second fragment.
We recommend you call your second fragment something easily identifiable as your testing environment, such as `FragmentName-DEV`.

Paste the JSON object from your primary fragment.

{{% /tablestep %}}
{{% tablestep %}}
**2. Edit the fragment**

Change the version of your module or package in the development fragment.
For example:

```json {class="line-numbers linkable-line-numbers" data-line="22"}
{
  "components": [
    {
      "api": "rdk:component:camera",
      "attributes": {},
      "model": "rdk:builtin:fake",
      "name": "camera-1"
    },
    {
      "api": "rdk:component:generic",
      "attributes": {},
      "model": "naomi:my-control-logic:control-logic",
      "name": "generic-1"
    }
  ],
  "debug": true,
  "modules": [
    {
      "module_id": "naomi:my-control-logic",
      "name": "naomi_my-control-logic",
      "type": "registry",
      "version": "0.0.7"
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
When you are satisfied that your package works as expected, continue to update your primary fragment.

{{% /tablestep %}}
{{< /table >}}

{{< /tab >}}
{{< tab name="Manual testing" >}}

{{< table >}}
{{% tablestep %}}
**1. Change the version of the module**

You can overwrite parts of a fragment to use a new version of a package without modifying the upstream fragment.

For each machine that you would like to test the new version of the package on, go to its **CONFIGURE** tab, find the package, and edit its version number.

{{<imgproc src="/how-tos/deploy-packages/version-change.png" resize="800x" class="shadow fill" style="width: 600px" declaredimensions=true alt="Configuration builder UI">}}

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
**2. Test the new version**

Test the new version of your package.
When you are satisfied that your package works as expected, continue to [update your primary fragment](#update-the-software-version).

{{% /tablestep %}}
{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

## Update the software version

Once you have confirmed that the new version of your module or package works, go to your primary fragment and edit it to use the new version.

For example:

```json {class="line-numbers linkable-line-numbers" data-line="22"}
{
  "components": [
    {
      "api": "rdk:component:camera",
      "attributes": {},
      "model": "rdk:builtin:fake",
      "name": "camera-1"
    },
    {
      "api": "rdk:component:generic",
      "attributes": {},
      "model": "naomi:my-control-logic:control-logic",
      "name": "generic-1"
    }
  ],
  "debug": true,
  "modules": [
    {
      "module_id": "naomi:my-control-logic",
      "name": "naomi_my-control-logic",
      "type": "registry",
      "version": "0.0.7"
    }
  ]
}
```

Don't forget to **Save**.

All machines configured with your fragment will update when they next check for configuration updates.

## Check machine status

To check when your machines have last updated their configuration, iterate over your machines using the Fleet Management API, connect to each machine, and use the [`GetMachineStatus` method](/dev/reference/apis/robot/#getmachinestatus).

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
