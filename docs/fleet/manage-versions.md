---
linkTitle: "Manage versions and rollouts"
title: "Manage software versions and rollouts"
weight: 35
layout: "docs"
type: "docs"
description: "Control which software versions reach your machines, stage rollouts with fragment tags, and verify what each machine is running."
---

Control which software versions your machines run, when updates are applied, and how to confirm a rollout actually reached every machine. By default, machines track the latest version of every module and model. Use version pinning, fragment tags, and maintenance windows to control rollouts more precisely.

## Version pinning options

Each module and ML model package on a machine (configured directly or through a fragment) has a version field with three options:

- **Latest version** (default): the machine downloads the newest version on its next config sync. Updates happen as soon as a new version is available.
- **Pin to version**: the machine stays on a specific version string and never updates automatically.
- **Pin to tag**: the machine uses whichever version the fragment tag currently points to. See [fragment tags](/fleet/reuse-configuration/#version-and-tag-fragments-for-staged-rollouts).

{{% alert title="Caution" color="caution" %}}
When a module updates, it restarts. If the module is performing work that cannot be safely interrupted, pin to a specific version and update manually during planned maintenance.
{{% /alert %}}

To change the version strategy, navigate to the machine's **CONFIGURE** tab, find the module or fragment card, and update the version setting.

## Maintenance windows

A maintenance window tells `viam-server` when it is safe to apply configuration updates. Without a maintenance window, configuration changes (including module version updates) take effect immediately on sync. With a maintenance window, changes are held until the window opens.

Maintenance windows use a sensor-based approach: you configure a sensor that returns a boolean value indicating whether maintenance is allowed. When the sensor returns `true`, `viam-server` applies pending configuration changes. When it returns `false`, changes are deferred.

### Configure a maintenance window

1. Create a sensor (or use an existing one) that returns a boolean reading indicating whether maintenance is allowed. For example, a sensor that returns `true` during off-hours and `false` during production.
1. On the machine's **CONFIGURE** tab, click **+**, open the **Advanced** submenu, and select **Maintenance window**.
1. In the maintenance card, set:
   - `sensor_name`: the name of the sensor to read.
   - `maintenance_allowed_key`: the key in the sensor's readings that contains the boolean value.
1. Click **Save**.

While the maintenance window is closed (sensor returns `false`), `viam-server` continues running with its current configuration. When the window opens, all pending changes are applied at once.

## Staged rollouts with fragment tags

For fleets where you want to test changes before deploying to all machines, use the fragment tag workflow. This is the closest equivalent to a canary deployment in Viam: instead of allocating a percentage of devices automatically, you assign tags to fragment revisions and re-tag to promote.

1. Create `stable` and `development` tags on your fragment. See [fragment tags](/fleet/reuse-configuration/#create-a-tag).
2. Pin production machines to the `stable` tag.
3. Pin test machines to the `development` tag.
4. Make changes to the fragment and save.
5. Move the `development` tag to the new revision.
6. Verify the changes on test machines.
7. Move the `stable` tag to the new revision. All production machines update.

This gives you a manual gate between development and production without maintaining separate fragments.

## Verify a rollout across the fleet

After you push an update, you need to confirm every machine actually received it. The fleet dashboard at [app.viam.com/fleet/machines](https://app.viam.com/fleet/machines) shows whether each machine is online but does not currently display per-machine version or config information. To check what each machine is running, query the machines directly.

### Check that machines picked up a config change

Most rollouts change a fragment that machines depend on, which means the goal is to confirm each machine pulled the new config revision. Use the Python SDK's `get_machine_status` on each machine to read its current revision.

```python
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


async def get_revision(machine_address, api_key, api_key_id):
    creds = Credentials(type="api-key", payload=api_key)
    opts = DialOptions(auth_entity=api_key_id, credentials=creds)
    machine = await RobotClient.at_address(machine_address, opts)
    status = await machine.get_machine_status()
    return status.config.revision
```

Find each machine's address, API key, and API key ID on the machine's **CONNECT** tab in the Viam app. To check the entire fleet, list machines with `AppClient.list_robots`, connect to each, and compare the returned revision to the one you expect.

### Check viam-server or viam-agent version

The per-part `viam_server_version` and `viam_agent_version` fields are populated in the cloud through the `ListMachineSummaries` RPC on `app.proto`, but this RPC is not yet wrapped in the Python SDK or exposed through the CLI. To read it today, make a direct gRPC call to the app service.

If a deployed agent or `viam-server` version fails to start, viam-agent does not automatically roll back to the previous version. It will keep retrying that version until you change the cloud config to pin an older one. See [Limitations](#limitations).

## Limitations

- Maintenance windows require a sensor that produces a boolean reading. There is no built-in time-based scheduling for maintenance windows; you need a sensor module or logic module that returns `true` during your desired maintenance period.
- There is no built-in canary or percentage-based rollout. Use fragment tags as a manual gate.
- Rollback is manual at every layer:
  - Fragment-level rollback: revert the fragment to a previous revision, or pin machines to an older version.
  - Agent and `viam-server` rollback: viam-agent does not automatically revert when a deployed version fails to start. Edit the cloud config to pin a known-good version.
- Per-machine version status is not displayed in the fleet dashboard today. Use the Python SDK or direct gRPC (see [Verify a rollout across the fleet](#verify-a-rollout-across-the-fleet)) to find machines stuck on an old version.

## Related pages

- [Reuse configuration](/fleet/reuse-configuration/) for fragment creation and tag management
- [Deploy software](/fleet/deploy-software/) for deploying modules through fragments
- [Deploy ML models](/fleet/deploy-ml-models/) for deploying models through fragments
