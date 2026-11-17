---
title: "Write control code with Viam SDKs"
linkTitle: "SDKs"
weight: 10
type: "docs"
description: "Choose a Viam SDK (Python, Go, TypeScript, Flutter, or C++) for the code you want to write, then follow its setup page."
capabilities: ["sdks", "section-index"]
diataxis: overview
aliases:
  - /operate/control/sdks/
  - /sdks/
---

The Viam SDKs are libraries for writing your own code that controls machines and talks to the Viam cloud.
All of them expose the same resources and methods, so what you learn in one carries over to the others.
Pick the one that fits where your code runs and what you are building.

- To write a module, use Python, Go, or C++.
- To build a backend application or script, use Python, Go, or TypeScript (Node.js).
- To build a web app, use TypeScript or Flutter.
- To build a mobile app, use Flutter.

## Choose an SDK

| SDK        | Runs                     | Setup                                                                                                                   | Reference docs                                   |
| ---------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Python     | Backend, or as a module  | [Python setup](/build-apps/setup/python/)                                                                               | [python.viam.dev](https://python.viam.dev/)      |
| Go         | Backend, or as a module  | [Go setup](/build-apps/setup/go/)                                                                                       | [pkg.go.dev](https://pkg.go.dev/go.viam.com/rdk) |
| TypeScript | Browser and Node.js      | [TypeScript setup](/build-apps/setup/typescript/) for the browser, [Node.js setup](/build-apps/setup/node/) for Node.js | [ts.viam.dev](https://ts.viam.dev/)              |
| Flutter    | Mobile (iOS and Android) | [Flutter setup](/build-apps/setup/flutter/)                                                                             | [flutter.viam.dev](https://flutter.viam.dev/)    |
| C++        | Backend, or as a module  | [C++ setup](/build-apps/setup/cpp/), a source build or Conan with no one-line install                                   | [cpp.viam.dev](https://cpp.viam.dev/)            |

If your team already has a React Native codebase, see [React Native setup](/build-apps/setup/react-native/). For new mobile projects, use Flutter.

## Write a module

Modules add hardware drivers and logic to a machine, and they run on the machine itself.
Start from `viam module generate` and follow [Build and deploy modules](/build-modules/overview/).
The generated project handles setup and passes in the resources your module depends on, so you don't need the app setup pages above.
The SDK's resources and method signatures are the same in modules and in apps, so the reference docs apply to both.

A module that calls the Viam cloud APIs, or controls a different machine, needs credentials and a client the same way an app does.
For that, follow the setup page for your language.

## What you can do with the SDKs

- Control [components](/reference/apis/#component-apis) and [services](/reference/apis/#service-apis) on a machine.
- Manage your [fleet](/reference/apis/fleet/), [data](/reference/apis/data-client/), and [billing information](/reference/apis/billing-client/), or [provision](/fleet/provision-devices/) machines.
- Create custom {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} in Python, Go, or C++.

## Next steps

- [App scaffolding](/build-apps/setup/overview/): the steps every app follows, whatever the language.
- [Connect to a machine](/build-apps/tasks/connect-to-machine/): the connection patterns your code will use.
- [Control components](/build-apps/tasks/control-components/): call methods on a machine's resources.
