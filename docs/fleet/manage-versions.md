---
linkTitle: "Manage versions"
title: "Manage software versions"
weight: 35
layout: "docs"
type: "docs"
description: "Control when and how software updates reach your machines with version pinning, fragment tags, and maintenance windows."
---

Control which software versions your machines run and when updates are applied. By default, machines track the latest version of every module and model. Use version pinning, fragment tags, and maintenance windows to control rollouts more precisely.

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

For fleets where you want to test changes before deploying to all machines, use the fragment tag workflow:

1. Create `stable` and `development` tags on your fragment. See [fragment tags](/fleet/reuse-configuration/#create-a-tag).
2. Pin production machines to the `stable` tag.
3. Pin test machines to the `development` tag.
4. Make changes to the fragment and save.
5. Move the `development` tag to the new revision.
6. Verify the changes on test machines.
7. Move the `stable` tag to the new revision. All production machines update.

This gives you a manual gate between development and production without maintaining separate fragments.

## Check what versions your machines are running

The fleet dashboard at [app.viam.com/fleet/machines](https://app.viam.com/fleet/machines) shows the `viam-server` version and `viam-agent` version for each machine part.

To check programmatically, iterate over your machines using the fleet management API, connect to each machine, and use `GetMachineStatus` to retrieve the current configuration and version information.

## Limitations

- Maintenance windows require a sensor that produces a boolean reading. There is no built-in time-based scheduling for maintenance windows; you need a sensor module or logic module that returns `true` during your desired maintenance period.
- There is no built-in canary or percentage-based rollout. Use fragment tags to control which machines receive updates.
- Rollback is manual: revert the fragment to a previous revision or pin machines to an older version.

## Related pages

- [Reuse configuration](/fleet/reuse-configuration/) for fragment creation and tag management
- [Deploy software](/fleet/deploy-software/) for deploying modules through fragments
- [Deploy ML models](/fleet/deploy-ml-models/) for deploying models through fragments
