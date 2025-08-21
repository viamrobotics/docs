---
linkTitle: "Update software"
title: "Roll out software updates to machines"
weight: 40
layout: "docs"
type: "docs"
description: "As new versions of software modules or ML models become available, you can update the deployed version on all machines in one go."
date: "2025-02-14"
aliases:
  - /manage/software/update-packages/
---

If you have already [deployed software](/manage/software/deploy-software/), you can inspect the fragment you have created.
Each deployed {{< glossary_tooltip term_id="module" text="module" >}} or {{< glossary_tooltip term_id="package" text="package" >}} has a `version` field.
Unless the `version` field is set to a specific version, updates for that module or package happen automatically.

{{% alert title="Updates for microcontrollers" color="note" %}}
To update the firmware on your microcontroller, see [Over-the-air updates](/operate/get-started/setup-micro/#configure-over-the-air-updates).
{{% /alert %}}

## Test and update software

You can either use fragment tags for testing or manually overwrite the version of the module or package or the configuration for a subset of machines.
We strongly recommend that you test changes on a subset of machines before deploying it to all machines.

{{< tabs >}}
{{< tab name="Version tags (recommended)" >}}

{{< table >}}
{{% tablestep number=1 %}}
**Navigate to your fragment's page** on On your fragment's page, from the [FRAGMENTS tab](https://app.viam.com/fragments).
{{% /tablestep %}}
{{% tablestep number=2 %}}
**Create a `stable` fragment tag**.
On your fragment's page, click on **Versions** in the menu bar and add a tag called `stable`.
{{% /tablestep %}}
{{% tablestep number=3 %}}
**Pin all machine configurations** to the `stable` fragment tag.
For each machine that uses the fragment, update its configuration.
{{% /tablestep %}}
{{% tablestep number=4 %}}
**Edit the fragment** and change the version of your module or package or the configuration in the development fragment.
This will create a new version of the fragment.

For example:

```json {class="line-numbers linkable-line-numbers"}
{
  "version": "0.0.7"
}
```

{{% /tablestep %}}
{{% tablestep number=5 %}}
**Create a development tag**.
On your fragment's page, click on **Versions** in the menu bar and add a tag called `development`.
Select the most recent version that you just created for the tag.
{{% /tablestep %}}
{{% tablestep number=6 %}}
**Add the development fragment to a subset of machines** by pinning the fragment configuration to the `development` fragment tag.
For each machine that you want to test the changes on, update the configuration.
{{% /tablestep %}}
{{% tablestep number=7 %}}
**Test the new version of your module or package**.
{{% /tablestep %}}
{{% tablestep number=8 %}}
**Update the `stable` fragment tag**.
When you are satisfied that your module or package works as expected, set the **Version** for the `stable` fragment tag to the new version.
This will update all machines that use the `stable` fragment tag.
{{% /tablestep %}}
{{< /table >}}

{{< /tab >}}
{{< tab name="Manual testing" >}}

{{< table >}}
{{% tablestep number=1 %}}
**For one or more machines, change the version of the module.**

You can overwrite parts of a fragment to use a new version of a module or package without modifying the upstream fragment.

For each machine that you would like to test the new version of the module or package on, go to its **CONFIGURE** tab, find the module or package, and edit its version number.

{{<imgproc src="/how-tos/deploy-packages/version-change.png" resize="800x" class="shadow fill" style="width: 600px" declaredimensions=true alt="Configuration builder UI">}}

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Test your changes.**
{{% /tablestep %}}
{{% tablestep number=3 %}}
**Update the fragment.**

When you are satisfied that your changes work as expected, click the **...** menu on the resource you updated and click **Merge changes**.
This will create a new version of your fragment.

Fragment tags remain unchanged.

All machines configured with your fragment will update when they next check for configuration updates.

{{% /tablestep %}}
{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Manage when machines update their config" color="tip" >}}
By default, when a fragment is updated, machines using it will automatically update when the configuration is synced next.
To ensure that updates only occur when your machines are ready, configure a [maintenance window](/operate/reference/viam-server/#maintenance-window).
With a configured maintenance window, configuration updates will only be applied when maintenance is allowed.
{{< /alert >}}

## Check machine status

To check when your machines have last updated their configuration, iterate over your machines using the Fleet Management API, connect to each machine, and use the [`GetMachineStatus` method](/dev/reference/apis/robot/#getmachinestatus).

The following example script iterates over all machines in a given location and if it can connect to the machines, it prints their status information.
If it cannot connect to a machine, it prints the most recent log entries.

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient
from viam.robot.client import RobotClient


# TODO: Replace "<API-KEY>" (including brackets) with your API key and "<API-KEY-ID>"
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

        # Get machine address
        machine_address = main_part.fqdn

        print("Attempting to connect to {}...".format(machine_address))

        try:
            machine = await machine_connect(machine_address)
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
