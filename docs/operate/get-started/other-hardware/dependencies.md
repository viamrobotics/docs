---
title: "Module dependencies"
linkTitle: "Module dependencies"
weight: 25
layout: "docs"
type: "docs"
description: "Handle dependencies in your custom modular resource."
---

## What are dependencies?

Dependencies are resources that your module needs to access in order to function.

## Access dependencies

From within a module, you cannot access resources in the same way that you would in a client application.
For example, you cannot call `Camera.from_robot()` to get a camera resource.

Instead, you must access dependencies as follows:

### Access implicit dependencies

### Access explicit dependencies

## Make API calls to dependencies

Within your module, you can make calls to the APIs of your dependencies using the Viam SDK methods in the language of your module.

## Access configuration attributes of dependencies

## Configure your module's dependencies more easily with a discovery service
