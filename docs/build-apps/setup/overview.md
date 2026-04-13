---
linkTitle: "Overview"
title: "App scaffolding"
weight: 1
layout: "docs"
type: "docs"
description: "The pattern every Viam app project follows: create a project, install the SDK, configure credentials, and verify the connection."
date: "2026-04-13"
---

Every Viam app follows the same scaffolding pattern regardless of language. The per-language pages in this section walk through each step for a specific SDK, but the shape is always the same:

1. **Create a project.** Set up a directory with the build tooling for your language: `npm init` for TypeScript, `flutter create` for Flutter, `go mod init` for Go, a virtual environment for Python, a CMake project for C++.
2. **Add the Viam SDK as a dependency.** Each language has its own package manager and package name: `npm install @viamrobotics/sdk` for TypeScript, `flutter pub add viam_sdk` for Flutter, `pip install viam-sdk` for Python, `go get go.viam.com/rdk/robot/client` for Go, and a CMake `find_package` for C++. Some platforms need additional dependencies (WebRTC polyfills for Node.js, platform permissions for iOS and Android).
3. **Configure credentials.** Store your machine's address, API key, and API key ID in environment variables or a `.env` file. Never commit credentials to source control.
4. **Write a connection verification.** A short program that connects to your machine and prints the resource count. This confirms the SDK is installed correctly, credentials are valid, and the connection works.
5. **Run it.** Execute the program and confirm you see `Connected. Found N resources.` If you do, the scaffold is complete and you can start writing your app.

After scaffolding, the next step is [Connect to a machine](/build-apps/tasks/connect-to-machine/) for the connection patterns your app will actually use, or one of the [tutorials](/build-apps/app-tutorials/tutorial-dashboard/) for a guided project.

## Pick your language

| Language             | Page                                  | Notes                                                                                                                                                   |
| -------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TypeScript (browser) | [TypeScript setup](./typescript/)     | Web app: dashboards, operator interfaces, any browser-based app. The setup page uses Vite; any bundler that handles TypeScript and ESM works.           |
| TypeScript (Node.js) | [Node.js setup](./node/)              | Node process for backend services and CLI tools. Requires WebRTC polyfills and a custom gRPC transport.                                                 |
| Flutter              | [Flutter setup](./flutter/)           | Cross-platform project for iOS, Android, and desktop. Includes iOS/Android platform configuration.                                                      |
| React Native         | [React Native setup](./react-native/) | Mobile project for teams with existing React Native codebases. Requires six polyfill packages and a custom transport. For new projects, prefer Flutter. |
| Python               | [Python setup](./python/)             | Virtual environment for scripts, services, and backend integrations                                                                                     |
| Go                   | [Go setup](./go/)                     | Go module for backend services, fleet orchestrators, and CLI tools                                                                                      |
| C++                  | [C++ setup](./cpp/)                   | CMake project for embedded and high-performance apps. Requires system-level dependencies (Boost, gRPC, protobuf).                                       |

## Where credentials come from

Every scaffolding page asks for three values: the machine's address, an API key, and an API key ID. Get all three from the same place:

1. Go to the machine's page in the Viam app.
2. Click the **CONNECT** tab.
3. Select the language tab that matches the page you are following.
4. Toggle **Include API key** on.
5. Copy the address, API key ID, and API key from the generated code sample.

For apps that access multiple machines or the Viam cloud APIs, use an organization-scoped or location-scoped API key instead of a machine-scoped one. Create these in [Admin and access](/organization/access/).
