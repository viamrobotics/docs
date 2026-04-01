---
linkTitle: "Overview"
title: "Fleet deployment"
weight: 1
layout: "docs"
type: "docs"
description: "Scale from one machine to a fleet: templatize configuration with fragments, provision devices, deploy software and ML models, and manage updates."
---

You have a single machine working. Now you need 10, or 100, or 1,000 machines running the same software with the same configuration. Fleet deployment is how you get there without configuring each machine by hand.

## Three core mechanisms

Viam's fleet deployment is built on three mechanisms that work together:

### Fragments: configuration templates

A fragment is a reusable block of configuration. You define the components, services, modules, and settings a machine needs in a fragment, then apply that fragment to every machine in your fleet. When you update the fragment, every machine that uses it receives the change.

Fragments support **variables** for per-machine customization (different sensor names, different thresholds), **version tags** for controlled rollouts (test on a few machines before deploying to the full fleet), and **overrides** for device-specific adjustments that differ from the template.

### Provisioning: automated first-boot setup

For machines you ship to customers or deploy in the field, provisioning automates the first-boot experience. You install `viam-agent` on a device during manufacturing with a defaults file that specifies which fragment to use. When someone powers on the device, `viam-agent` creates a WiFi hotspot or Bluetooth connection, the user provides network credentials through a mobile app or captive portal, and the machine configures itself from the fragment automatically.

### The module registry: versioned software delivery

Modules and ML models are stored as versioned packages in the Viam registry. When you configure a module or model on a machine (directly or through a fragment), the machine downloads the correct version for its platform. When you upload a new version, machines configured to track that version update automatically. Maintenance windows let you control when updates happen so machines are not interrupted during operation.

## What you can do

| Task                                                 | Guide                                                             |
| ---------------------------------------------------- | ----------------------------------------------------------------- |
| Create reusable configuration templates              | [Reuse configuration with fragments](/fleet/reuse-configuration/) |
| Set up automated device provisioning                 | [Provision devices](/fleet/provision-devices/)                    |
| Help end users connect new devices to WiFi           | [End-user device setup](/fleet/end-user-setup/)                   |
| Deploy modules to machines over the air              | [Deploy software](/fleet/deploy-software/)                        |
| Deploy ML models across your fleet                   | [Deploy ML models](/fleet/deploy-ml-models/)                      |
| Control when and how software updates reach machines | [Manage versions](/fleet/manage-versions/)                        |
| Schedule automated tasks on machines                 | [Schedule jobs](/fleet/schedule-jobs/)                            |
| Tag machines with custom key-value data              | [Add custom metadata](/fleet/metadata/)                           |
| Configure network, tunneling, and system settings    | [System settings](/fleet/system-settings/)                        |
| Change a deployed machine's WiFi network             | [Change network](/fleet/change-network/)                          |

## How fleet deployment fits with other sections

- **[Get started](/foundation/)** covers setting up a single machine. Start there if you haven't created your first machine yet.
- **[Configure hardware](/hardware/)** covers adding components and services to a machine. Use fragments to templatize those configurations for your fleet.
- **[Build and deploy modules](/build-modules/)** covers writing and uploading modules. This section covers deploying those modules to machines.
- **[Train ML models](/train/)** covers training models. This section covers deploying trained models fleet-wide.
- **[Viam CLI](/cli/manage-your-fleet/)** covers fleet operations from the command line: checking machine status, viewing logs, shell access, and file transfer.
