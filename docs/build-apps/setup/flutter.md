---
linkTitle: "Flutter setup"
title: "Flutter setup"
weight: 30
layout: "docs"
type: "docs"
description: "Set up a project for building a Viam app that runs across iOS, Android, and desktop platforms from a single codebase."
date: "2026-04-10"
---

Set up a project for building a Viam app that runs across iOS, Android, and desktop platforms from a single codebase: a tablet operator interface, a warehouse kiosk, a phone app for technicians in the field. This page covers the project scaffolding with [Flutter](https://flutter.dev/), the Viam Flutter SDK install, and the iOS/macOS and Android platform configuration. For the connection patterns your app will actually use, see [Connect to a machine](/build-apps/tasks/connect-to-machine/).

## Prerequisites

- Flutter SDK 3.0.0 or later ([install Flutter](https://docs.flutter.dev/get-started/install))
- Platform tooling for at least one of your targets:
  - **iOS:** Xcode and an Apple Developer account (or the iOS Simulator)
  - **Android:** Android Studio with Android SDK 23 or later and Kotlin `1.8.20` or later
  - **Linux, macOS, Windows:** the desktop tooling for your target ([Flutter desktop setup](https://docs.flutter.dev/platform-integration/desktop))
  - **Web:** a Chromium-based browser for development ([Flutter web setup](https://docs.flutter.dev/platform-integration/web))
- A configured Viam machine
- The machine's address, an API key, and an API key ID

Get the credentials from the machine's **CONNECT** tab in the Viam app: click **CONNECT**, select **Flutter**, and copy the address, API key ID, and API key from the generated code sample.

## Create a project

```sh {class="command-line" data-prompt="$"}
flutter create my_viam_app
cd my_viam_app
```

`flutter create` generates a project that targets all six Flutter platforms. To narrow the targets, pass `--platforms=ios,android` (or any subset) to the command.

## Add the Viam SDK

```sh {class="command-line" data-prompt="$"}
flutter pub add viam_sdk flutter_dotenv
```

`flutter_dotenv` loads environment variables from a `.env` file at runtime, which keeps credentials out of source code.

## Configure iOS and macOS (if targeting Apple platforms)

The Viam SDK uses WebRTC and mDNS, both of which require explicit permissions on iOS and macOS.

Add the following to `ios/Runner/Info.plist` and `macos/Runner/Info.plist`, inside the top-level `<dict>`:

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>This app needs access to the local network to connect to your Viam machine.</string>
<key>NSBonjourServices</key>
<array>
  <string>_rpc._tcp</string>
</array>
```

Set the minimum iOS deployment target to 13.0 in `ios/Podfile`:

```ruby
platform :ios, '13.0'
```

## Configure Android (if targeting Android)

In `android/app/build.gradle`, confirm that the minimum SDK version is 23 or higher:

```groovy
defaultConfig {
    minSdkVersion 23
    // ...
}
```

If your Kotlin version is lower than `1.8.20`, bump it in `android/build.gradle`:

```groovy
ext.kotlin_version = '1.8.20'
```

## Configure environment variables

Create a `.env` file in your project root:

```text
MACHINE_ADDRESS=my-robot-main.xxxx.viam.cloud
API_KEY_ID=your-api-key-id
API_KEY=your-api-key-secret
```

Replace the three values with what you copied from the **CONNECT** tab.

Add `.env` to your `.gitignore`:

```sh {class="command-line" data-prompt="$"}
echo ".env" >> .gitignore
```

Register `.env` as an asset in `pubspec.yaml` so Flutter bundles it with the app:

```yaml
flutter:
  assets:
    - .env
```

## Verify the connection

Replace the contents of `lib/main.dart` with:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:viam_sdk/viam_sdk.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(body: Center(child: StatusText())),
    );
  }
}

class StatusText extends StatefulWidget {
  const StatusText({super.key});

  @override
  State<StatusText> createState() => _StatusTextState();
}

class _StatusTextState extends State<StatusText> {
  String _status = 'Connecting...';

  @override
  void initState() {
    super.initState();
    _connect();
  }

  Future<void> _connect() async {
    try {
      final address = dotenv.env['MACHINE_ADDRESS']!;
      final apiKeyId = dotenv.env['API_KEY_ID']!;
      final apiKey = dotenv.env['API_KEY']!;

      final robot = await RobotClient.atAddress(
        address,
        RobotClientOptions.withApiKey(apiKeyId, apiKey),
      );

      setState(() {
        _status = 'Connected. Found ${robot.resourceNames.length} resources.';
      });
    } catch (e) {
      setState(() {
        _status = 'Connection failed: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Text(_status);
  }
}
```

## Run the app

Run the app on a connected device or simulator:

```sh {class="command-line" data-prompt="$"}
flutter run
```

If multiple targets are available, Flutter prompts you to choose. Select your device. The app builds, launches, and shows:

```text
Connected. Found N resources.
```

where `N` is the number of components and services on your machine.

If you see `Connection failed:`, the most common causes are:

- **iOS or macOS permissions not granted.** The app prompts the user for local network access on first run; declining blocks WebRTC. Verify the `Info.plist` entries are present on both `ios/Runner/Info.plist` and `macos/Runner/Info.plist` if you target macOS.
- **Android minimum SDK too low.** The Viam Flutter SDK requires Android SDK 23 or later. Raise `minSdkVersion` in `android/app/build.gradle`.
- **`.env` not bundled.** Confirm `.env` is listed under `flutter.assets` in `pubspec.yaml` and that the file exists at the project root.
- **Credentials wrong.** Compare the three values in `.env` to the **CONNECT** tab output.

## Next

- [Connect to a machine](/build-apps/tasks/connect-to-machine/) for the connection patterns your app will actually use, including the `Viam` class for multi-machine access
- [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for reconnection and UI indicators
- [The Flutter SDK reference](https://flutter.viam.dev/) for per-component API details and widget documentation
