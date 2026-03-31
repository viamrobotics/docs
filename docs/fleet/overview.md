---
linkTitle: "Overview"
title: "Fleet deployment"
weight: 1
layout: "docs"
type: "docs"
description: "Deploy machines at scale: templatize configurations with fragments, provision devices, push software updates, and manage system settings."
---

Once you have a single machine working, fleet deployment is how you scale to tens, hundreds, or thousands of machines. Viam provides tools for every stage of fleet lifecycle management: templatizing configuration, provisioning new devices, deploying software and ML models, managing updates, and automating operations.

## How fleet deployment works

Fleet deployment in Viam is built on three core mechanisms:

**Fragments** are reusable configuration templates. You create a fragment once with all the components, services, modules, and settings a machine needs, then apply that fragment to every machine in your fleet. When you update the fragment, every machine that uses it gets the update. Fragments support variables for per-machine customization, version pinning for controlled rollouts, and overrides for device-specific adjustments.

**Provisioning** automates the first-boot experience. You install `viam-agent` on a device during manufacturing with a defaults file that specifies which fragment to use. When the end user powers on the device, `viam-agent` creates a WiFi hotspot or Bluetooth connection, the user provides network credentials (through a mobile app or captive portal), and the machine automatically configures itself from the fragment.

**The module registry** stores versioned software packages (modules and ML models) that machines download on demand. When you upload a new version of a module or model, machines configured to track that version update automatically. Maintenance windows let you control when updates are applied so machines are not interrupted during operation.

## What you can do

| Task                                              | Guide                                              |
| ------------------------------------------------- | -------------------------------------------------- |
| Create reusable config templates for your fleet   | [Reuse configuration](/fleet/reuse-configuration/) |
| Set up zero-touch device provisioning             | [Provision devices](/fleet/provision-devices/)     |
| Help end users connect new devices                | [End-user device setup](/fleet/end-user-setup/)    |
| Deploy modules to machines through fragments      | [Deploy software](/fleet/deploy-software/)         |
| Deploy ML models across your fleet                | [Deploy ML models](/fleet/deploy-ml-models/)       |
| Control software versions and update timing       | [Update software](/fleet/update-software/)         |
| Schedule automated tasks on machines              | [Schedule automated jobs](/fleet/scheduled-jobs/)  |
| Tag machines with custom metadata                 | [Add custom metadata](/fleet/metadata/)            |
| Configure system-level network and agent settings | [System settings](/fleet/system-settings/)         |
| Change a deployed machine's WiFi network          | [Change network](/fleet/change-network/)           |
