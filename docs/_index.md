---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam adapts software engineering paradigms to building machines for the physical world."
weight: 1
type: "docs"
sitemap:
  priority: 1.0
outputs:
  - html
  - REDIR
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
noedit: true
date: "2024-09-17"
updated: "2025-10-08"
aliases:
  - "/getting-started/"
  - "/getting-started/high-level-overview"
  - "/product-overviews/"
  - "/viam/"
  - "/viam/app.viam.com/"
  - "/get-started/"
  - "/platform/"
next: /operate/hello-world/quickstart/
---

# Viam Documentation

Viam adapts software engineering paradigms to building machines for the physical world.

## Get started with Viam

You can build many types of robotics project on Viam, from single-component projects to human-in-the-loop or AI-powered autonomous intelligent systems.

- [Hardware agnostic](/operate/hello-world/quickstart/#supported-platforms): Viam runs on almost all single-board computers.
- [SDKs](/dev/reference/sdks/): Program machines in your favorite programming language.
- [Module Registry](https://app.viam.com/registry): Find and use a variety of integrations for popular hardware, common logic patterns, machine learning models, and more.
- [CLI](/dev/tools/cli/): Control, manage, and test from the command-line from anywhere.

We recommend starting with the [Quick Start](/operate/hello-world/quickstart/) and following the [Tutorial: Desk Safari](/operate/hello-world/tutorial-desk-safari/) to build your first machine.

## Build your projects

You can use Viam to build entire projects or to add functionality to existing projects.
Before you begin, we recommend reading [How to think about building a machine](/operate/hello-world/building/) to understand the building blocks of a machine and how to go from prototype to production.

- [Modules](/operate/modules/other-hardware/create-module/): The foundational building blocks of machines which keep your machine code maintainable as your project grows in complexity because you can make changes to single modules without changing the rest of the project.
- [Standardized APIs](/dev/reference/apis/): It doesn't matter which robotic arm, motor, or other piece of hardware you are using, the code to operate the hardware is the same. This means you can swap hardware as you iterate.
- [Fragments](/manage/fleet/reuse-configuration/): Reuse configuration chunks across machines. Version control??
- [Parts and sub-parts](/operate/reference/architecture/parts/): Create arbitrarily complex projects by connecting multiple `viam-server` instances.

## Use Viam's platform capabilities

The Viam platform offers many builtin capabilities from which you can pick and choose, such as:

- [Data Management](/data-ai/capture-data/capture-sync/): Capture data from devices to the cloud.
- [Machine learning and Computer Vision](/data-ai/train/create-dataset/): Build and deploy machine learning models.
- [Alerting](/data-ai/ai/alert/): Send alerts in the form of email notifications or webhook requests.
- [Motion Planning](/operate/mobility/motion-concepts/): Smooth and intelligent motion for arms, bases, and gantries.
- [Viam applications](/operate/control/viam-applications/): Deploy custom web interface for your machines while Viam handles hosting and authentication.

## Productionize and scale

When you ship machines, use one or more of the following tools:

- [Provisioning](/manage/fleet/provision/setup/): ship machines with a preconfigured setup so customers can connect them to the internet and get them up and running
- [Role-based access control](/manage/manage/access/): Grant fine-grained permissions as needed.
- [Remote monitoring](/manage/troubleshoot/monitor/): monitor, operate, and troubleshoot machines from anywhere in the world
- [Machine settings](/manage/fleet/system-settings/): manage operating system package updates, network configuration, and system-level logging
- [Billing](/manage/manage/white-labeled-billing/): bill customers for usage through the Viam platform
